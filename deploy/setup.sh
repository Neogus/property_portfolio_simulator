#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# EC2 Setup Script — Deploys both Streamlit apps on a single t3.micro
# Usage: sudo bash setup.sh
# Target: Amazon Linux 2023 on EC2 Free Tier (t3.micro, 1 GB RAM)
# =============================================================================

APP_DIR="/opt/apps"
MORTGAGE_REPO="https://github.com/Neogus/property_portfolio_simulator.git"
TRADE_REPO="https://github.com/Neogus/vectorized-trade-simulator.git"

echo "=== [1/7] Updating system ==="
dnf update -y

echo "=== [2/7] Installing dependencies ==="
dnf install -y python3 python3-pip nginx git
# python3-venv not needed on Amazon Linux — venv is built in

echo "=== [3/7] Creating 1 GB swap file ==="
if [ ! -f /swapfile ]; then
    dd if=/dev/zero of=/swapfile bs=1M count=1024
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "Swap created"
else
    echo "Swap already exists"
fi

echo "=== [4/7] Cloning repositories ==="
mkdir -p "$APP_DIR"
cd "$APP_DIR"

if [ ! -d property_portfolio_simulator ]; then
    git clone "$MORTGAGE_REPO"
else
    cd property_portfolio_simulator && git pull && cd ..
fi

if [ ! -d vectorized-trade-simulator ]; then
    git clone "$TRADE_REPO"
else
    cd vectorized-trade-simulator && git pull && cd ..
fi

echo "=== [5/7] Setting up Python environments ==="
# Mortgage Calculator
cd "$APP_DIR/property_portfolio_simulator"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Trade Simulator
cd "$APP_DIR/vectorized-trade-simulator"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r Requirements.txt
deactivate

echo "=== [6/7] Installing systemd services ==="
cp "$APP_DIR/property_portfolio_simulator/deploy/mortgage-app.service" /etc/systemd/system/
cp "$APP_DIR/property_portfolio_simulator/deploy/trade-sim.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable mortgage-app trade-sim
systemctl start mortgage-app trade-sim

echo "=== [7/7] Configuring Nginx ==="
cp "$APP_DIR/property_portfolio_simulator/deploy/nginx.conf" /etc/nginx/conf.d/streamlit-apps.conf
# Amazon Linux uses conf.d/ instead of sites-available/sites-enabled/
nginx -t && systemctl enable nginx && systemctl restart nginx

echo ""
echo "============================================"
echo "  SETUP COMPLETE"
echo "============================================"
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
PUBLIC_IP=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4)
echo "  Mortgage Calculator: http://${PUBLIC_IP}/mortgage/"
echo "  Trade Simulator:     http://${PUBLIC_IP}/trade/"
echo "============================================"
