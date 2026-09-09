# EC2 Launch & Deploy Guide

## 1. Launch the Instance (AWS Console)

1. Go to **EC2 → Launch Instance**
2. **Name:** `streamlit-apps`
3. **AMI:** Ubuntu 24.04 LTS (free tier eligible)
4. **Instance type:** t2.micro *(free tier — 750 hrs/month)*
5. **Key pair:** Create new → name it `streamlit-key` → download `streamlit-key.pem`
6. **Network / Security Group:** Create new, allow:
   - **SSH (22)** — Source: My IP
   - **HTTP (80)** — Source: Anywhere (0.0.0.0/0)
7. **Storage:** 8 GB gp3
8. **Advanced details → Credit specification:** `Standard` *(NOT Unlimited)*
9. Click **Launch Instance**

## 2. SSH from PowerShell

```powershell
# Move the key somewhere safe
Move-Item ~\Downloads\streamlit-key.pem ~\.ssh\streamlit-key.pem

# Connect (replace YOUR-EC2-IP with the public IP from the console)
ssh -i ~/.ssh/streamlit-key.pem ubuntu@YOUR-EC2-IP
```

> **First connection:** type `yes` when asked about the fingerprint.

If you get a "permissions too open" error:

```powershell
icacls $HOME\.ssh\streamlit-key.pem /inheritance:r /grant:r "$($env:USERNAME):(R)"
```

## 3. Run the Setup Script

Once SSHed in:

```bash
git clone https://github.com/Neogus/property_portfolio_simulator.git
sudo bash property_portfolio_simulator/deploy/setup.sh
```

This takes ~3–5 minutes. When it finishes, it prints the URLs:

```
============================================
  SETUP COMPLETE
============================================
  Mortgage Calculator: http://YOUR-EC2-IP/mortgage/
  Trade Simulator:     http://YOUR-EC2-IP/trade/
============================================
```

Open both in your browser to verify they work.

## 4. Add GitHub Secrets (for auto-deploy)

In **each** repo (property_portfolio_simulator AND vectorized-trade-simulator):

1. GitHub → repo → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
2. Add these two secrets:

| Secret Name | Value |
|-------------|-------|
| `EC2_HOST` | Your EC2 public IP (e.g. `3.87.123.45`) |
| `EC2_SSH_KEY` | The ENTIRE contents of `streamlit-key.pem` (open in notepad, copy all) |

## 5. Allow deploy script to restart services without password

The deploy workflow runs `sudo systemctl restart` via SSH. The `ubuntu` user needs passwordless sudo for that specific command.

While still SSHed into EC2:

```bash
sudo visudo -f /etc/sudoers.d/streamlit-deploy
```

Paste this single line, then save (`Ctrl+X`, `Y`, `Enter`):

```
ubuntu ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart mortgage-app, /usr/bin/systemctl restart trade-sim
```

## 6. Replace the Placeholder URL

Once you have the public IP, do a find-and-replace across both local repos:

```powershell
# From your local machine (PowerShell)
cd C:\Users\grabino\PycharmProjects\pythonProject

# Mortgage repo
(Get-ChildItem -Path "Mortgage\calculator" -Recurse -Include *.md,*.yml) | ForEach-Object {
    (Get-Content $_.FullName) -replace '18.195.171.220', 'YOUR-ACTUAL-IP' | Set-Content $_.FullName
}

# Trade Sim repo
(Get-ChildItem -Path "vectorized-trade-simulator" -Recurse -Include *.md,*.yml) | ForEach-Object {
    (Get-Content $_.FullName) -replace '18.195.171.220', 'YOUR-ACTUAL-IP' | Set-Content $_.FullName
}
```

Then commit and push both repos.

## 7. Test the Deploy Pipeline

Push any small change (or go to **Actions** → **Deploy to EC2** → **Run workflow**) and verify the deploy succeeds.

## Useful Commands (SSH into EC2)

```bash
# Check app status
sudo systemctl status mortgage-app
sudo systemctl status trade-sim

# View logs
sudo journalctl -u mortgage-app -f
sudo journalctl -u trade-sim -f

# Restart an app
sudo systemctl restart mortgage-app
sudo systemctl restart trade-sim

# Check Nginx
sudo nginx -t
sudo systemctl status nginx

# Check resource usage
free -h          # RAM + swap
htop             # CPU + processes
df -h            # Disk space
```
## 8. Set Up CloudFront (HTTPS + CDN)

CloudFront gives you HTTPS and a CDN in front of your EC2. Free tier: 1 TB transfer/month for 12 months.

### 8a. Create the Distribution

1. **CloudFront → Create Distribution**
2. **Origin domain:** your EC2 public IP (e.g. `3.87.123.45`)
3. **Protocol:** HTTP only (EC2 doesn't have SSL — CloudFront handles that)
4. **Origin path:** leave blank
5. **Name:** `streamlit-ec2`

### 8b. Cache Behavior (CRITICAL for Streamlit)

Streamlit is fully dynamic + uses WebSockets. Caching will break it.

1. **Cache policy:** `CachingDisabled`
2. **Origin request policy:** `AllViewerExceptHostHeader`
3. **Response headers policy:** leave default
4. **Viewer protocol policy:** `Redirect HTTP to HTTPS`
5. **Allowed HTTP methods:** `GET, HEAD, OPTIONS, PUT, POST, PATCH, DELETE`

### 8c. Enable WebSockets

CloudFront supports WebSockets automatically when you:
- Use `CachingDisabled` cache policy ✅ (already set above)
- Forward `Upgrade` and `Connection` headers ✅ (`AllViewerExceptHostHeader` does this)
- Use HTTP/1.1 or HTTP/2 to origin ✅ (default)

No extra config needed — it just works with the settings above.

### 8d. Finish Creation

1. **Price class:** Use only North America and Europe (cheapest)
2. **Default root object:** leave blank (Nginx handles the `/` redirect)
3. Click **Create Distribution**
4. Wait ~5 minutes for status: **Enabled / Deployed**
5. Your app is now live at: `https://d1234abcde.cloudfront.net/mortgage/`

### 8e. Add Custom Domain + SSL (after buying a domain)

1. **ACM → Request certificate** (⚠️ MUST be in `us-east-1` region)
   - Domain names: `yourdomain.com` and `*.yourdomain.com`
   - Validation: DNS
   - ACM gives you a CNAME record → add it at your DNS provider
   - Wait for status: **Issued**

2. **CloudFront → Distribution → General → Edit**
   - Alternate domain names: `yourdomain.com`, `www.yourdomain.com`
   - Custom SSL certificate: select the ACM cert
   - Save

3. **DNS provider** (Route 53 / Cloudflare / GoDaddy / Namecheap):
   - `yourdomain.com` → ALIAS or CNAME flattening → `d1234abcde.cloudfront.net`
   - `www.yourdomain.com` → CNAME → `d1234abcde.cloudfront.net`

4. Test: `https://yourdomain.com/mortgage/` and `https://yourdomain.com/trade/`

> **Tip:** Route 53 is the easiest DNS for this (supports ALIAS records natively) but costs $0.50/month per hosted zone. Cloudflare is free and supports CNAME flattening.

---


## Cost Summary

| Resource | Free Tier | After 12 months |
|----------|-----------|-----------------|
| t2.micro (750 hrs/month) | $0 | ~$8/month on-demand |
| 8 GB gp3 EBS | $0 | ~$0.64/month |
| Data transfer (15 GB/month) | $0 | ~$0 at your traffic |
| **Total** | **$0/month** | **~$8.64/month** |

> ⚠️ **Don't stop the instance to "save money"** — it's free tier. A stopped instance with an Elastic IP charges ~$3.65/month for the unused IP.
