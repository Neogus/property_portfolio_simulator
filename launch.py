#!/usr/bin/env python3
"""Daemonize streamlit so it survives shell exit."""
import os, sys

PROJ = '/mnt/c/Users/grabino/PycharmProjects/pythonProject/Mortgage/calculator'

if os.fork() > 0:
    sys.exit(0)
os.setsid()
if os.fork() > 0:
    sys.exit(0)

devnull = os.open(os.devnull, os.O_RDWR)
os.dup2(devnull, 0)
logf = os.open(os.path.join(PROJ, 'streamlit.log'), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
os.dup2(logf, 1)
os.dup2(logf, 2)

with open(os.path.join(PROJ, 'streamlit.pid'), 'w') as f:
    f.write(str(os.getpid()))

os.chdir(PROJ)
os.execv('/home/grabino/.local/bin/streamlit',
         ['/home/grabino/.local/bin/streamlit', 'run', 'app.py',
          '--server.headless', 'true', '--server.port', '8501'])
