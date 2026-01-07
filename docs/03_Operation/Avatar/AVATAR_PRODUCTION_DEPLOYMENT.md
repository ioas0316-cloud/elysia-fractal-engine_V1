# Avatar System Production Deployment Guide
# 아바타 시스템 프로덕션 배포 가이드

Complete guide for deploying the Elysia Avatar System to production environments.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Server Setup](#server-setup)
3. [HTTPS/TLS Configuration](#httpstls-configuration)
4. [Nginx Reverse Proxy](#nginx-reverse-proxy)
5. [Performance Tuning](#performance-tuning)
6. [Security Hardening](#security-hardening)
7. [Monitoring Setup](#monitoring-setup)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 2GB
- Disk: 10GB
- OS: Ubuntu 20.04+ / Debian 11+ / CentOS 8+

**Recommended:**
- CPU: 4+ cores
- RAM: 4GB+
- Disk: 20GB SSD
- OS: Ubuntu 22.04 LTS

### Software Dependencies

```bash
# Python 3.10+
python3 --version

# pip
pip3 --version

# Git
git --version

# Nginx (for reverse proxy)
nginx -v

# Certbot (for HTTPS/Let's Encrypt)
certbot --version
```

---

## Server Setup

### 1. Clone Repository

```bash
# Create application directory
sudo mkdir -p /opt/elysia
sudo chown $USER:$USER /opt/elysia

# Clone repository (replace with your repository URL)
cd /opt/elysia
git clone https://github.com/YOUR-USERNAME/Elysia.git
cd Elysia
```

### 2. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install websockets aiohttp
pip install psutil  # Optional: for system metrics

# Verify installation
python -c "import websockets; print('✅ WebSockets OK')"
python -c "import aiohttp; print('✅ aiohttp OK')"
```

### 3. Configure Environment

```bash
# Create environment file
cat > .env << EOF
# Server Configuration
AVATAR_HTTP_PORT=8080
AVATAR_WS_PORT=8765
AVATAR_HOST=0.0.0.0

# Security
AVATAR_REQUIRE_AUTH=false
AVATAR_RATE_LIMIT_ENABLED=true

# Monitoring
AVATAR_MONITORING_ENABLED=true
AVATAR_METRICS_INTERVAL=1.0

# Logging
AVATAR_LOG_LEVEL=INFO
AVATAR_LOG_FILE=/var/log/elysia/avatar.log
EOF

# Create log directory
sudo mkdir -p /var/log/elysia
sudo chown $USER:$USER /var/log/elysia
```

### 4. Test Local Server

```bash
# Start server
python start_avatar_web_server.py

# In another terminal, test connection
curl http://localhost:8080/health
# Expected: {"status": "ok", "uptime": ...}

# Stop server (Ctrl+C)
```

---

## HTTPS/TLS Configuration

### 1. Install Certbot

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# CentOS/RHEL
sudo yum install certbot python3-certbot-nginx
```

### 2. Obtain SSL Certificate

```bash
# IMPORTANT: Replace with your actual domain
DOMAIN="avatar.yourdomain.com"  # ← REPLACE THIS

# Obtain certificate
sudo certbot certonly --nginx -d $DOMAIN

# Certificate files will be at:
# /etc/letsencrypt/live/$DOMAIN/fullchain.pem
# /etc/letsencrypt/live/$DOMAIN/privkey.pem
```

### 3. Auto-Renewal Setup

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot automatically installs renewal cron job
# Verify with:
sudo systemctl status certbot.timer
```

---

## Nginx Reverse Proxy

### 1. Install Nginx

```bash
# Ubuntu/Debian
sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx

# Start and enable
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 2. Configure Nginx

Create `/etc/nginx/sites-available/elysia-avatar`:

**IMPORTANT:** Replace `avatar.yourdomain.com` with your actual domain in ALL locations below!

```nginx
# HTTP → HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name avatar.yourdomain.com;  # ← REPLACE THIS
    
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name avatar.yourdomain.com;  # ← REPLACE THIS
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/avatar.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/avatar.yourdomain.com/privkey.pem;
    
    # SSL security settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # HTTP server (avatar.html, static files)
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers (if needed)
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
    }
    
    # WebSocket server
    location /ws {
        proxy_pass http://127.0.0.1:8765;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket timeouts
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;
        proxy_connect_timeout 60s;
    }
    
    # Static files (VRM models)
    location /static/ {
        alias /opt/elysia/Elysia/static/;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
    
    # Health check
    location /health {
        proxy_pass http://127.0.0.1:8080/health;
        access_log off;
    }
}
```

### 3. Enable Configuration

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/elysia-avatar /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## Performance Tuning

### 1. System Limits

Edit `/etc/security/limits.conf`:

```bash
# Add these lines
* soft nofile 65536
* hard nofile 65536
* soft nproc 32768
* hard nproc 32768
```

Apply changes:
```bash
# Logout and login, or reboot
ulimit -n  # Should show 65536
```

### 2. Python Server Optimization

```bash
# Use production WSGI server (optional, for HTTP)
pip install gunicorn

# Run with Gunicorn (if using HTTP API)
gunicorn -w 4 -b 127.0.0.1:8080 --worker-class aiohttp.GunicornWebWorker app:app
```

### 3. Nginx Tuning

Edit `/etc/nginx/nginx.conf`:

```nginx
user www-data;
worker_processes auto;
worker_rlimit_nofile 65536;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    keepalive_requests 100;
    
    # Compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    
    # Buffers
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 8k;
    
    # Timeouts
    client_body_timeout 12;
    client_header_timeout 12;
    send_timeout 10;
}
```

---

## Security Hardening

### 1. Enable Authentication

```bash
# Edit .env
AVATAR_REQUIRE_AUTH=true

# Or start with flag
python start_avatar_web_server.py --require-auth
```

### 2. Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable

# FirewallD (CentOS)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 3. Rate Limiting (Nginx)

Add to nginx server block:

```nginx
# Rate limiting zone
limit_req_zone $binary_remote_addr zone=avatar_limit:10m rate=10r/s;

server {
    # Apply rate limit
    location /ws {
        limit_req zone=avatar_limit burst=20 nodelay;
        # ... rest of WebSocket config
    }
}
```

### 4. Fail2Ban (Optional)

```bash
# Install
sudo apt install fail2ban

# Create jail for avatar
sudo cat > /etc/fail2ban/jail.d/elysia-avatar.conf << EOF
[elysia-avatar]
enabled = true
port = 80,443
filter = elysia-avatar
logpath = /var/log/elysia/avatar.log
maxretry = 5
bantime = 3600
EOF

# Create filter
sudo cat > /etc/fail2ban/filter.d/elysia-avatar.conf << EOF
[Definition]
failregex = ^.* Rate limit exceeded for client <HOST>
            ^.* Authentication failed for client <HOST>
            ^.* Malicious input detected from <HOST>
ignoreregex =
EOF

# Restart fail2ban
sudo systemctl restart fail2ban
```

---

## Monitoring Setup

### 1. Systemd Service

First, create the dedicated user:

```bash
# Create user for running the service
sudo useradd -r -s /bin/false elysia
sudo chown -R elysia:elysia /opt/elysia
```

Then create `/etc/systemd/system/elysia-avatar.service`:

```ini
[Unit]
Description=Elysia Avatar Server
After=network.target

[Service]
Type=simple
User=elysia
Group=elysia
WorkingDirectory=/opt/elysia/Elysia
Environment="PATH=/opt/elysia/Elysia/venv/bin"
ExecStart=/opt/elysia/Elysia/venv/bin/python start_avatar_web_server.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/log/elysia

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
# Enable service
sudo systemctl daemon-reload
sudo systemctl enable elysia-avatar
sudo systemctl start elysia-avatar

# Check status
sudo systemctl status elysia-avatar
sudo journalctl -u elysia-avatar -f
```

### 2. Health Check Script

Create `/opt/elysia/health-check.sh`:

```bash
#!/bin/bash
# Health check script

URL="http://localhost:8080/health"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ $RESPONSE -eq 200 ]; then
    echo "✅ Avatar server is healthy"
    exit 0
else
    echo "❌ Avatar server is down (HTTP $RESPONSE)"
    # Restart service
    sudo systemctl restart elysia-avatar
    exit 1
fi
```

Add to crontab:

```bash
# Make executable
chmod +x /opt/elysia/health-check.sh

# Add to crontab (every 5 minutes)
crontab -e
*/5 * * * * /opt/elysia/health-check.sh >> /var/log/elysia/health-check.log 2>&1
```

### 3. Log Rotation

Create `/etc/logrotate.d/elysia-avatar`:

```
/var/log/elysia/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 elysia elysia
    sharedscripts
    postrotate
        systemctl reload elysia-avatar > /dev/null 2>&1 || true
    endscript
}
```

---

## Troubleshooting

### Common Issues

#### 1. WebSocket Connection Failed

**Symptoms:** Client cannot connect to WebSocket

**Solutions:**
```bash
# Check if WebSocket port is open
sudo netstat -tlnp | grep 8765

# Check Nginx WebSocket config
sudo nginx -t
sudo tail -f /var/log/nginx/error.log

# Check firewall
sudo ufw status
```

#### 2. High CPU Usage

**Symptoms:** CPU usage consistently >80%

**Solutions:**
```bash
# Check monitoring metrics
curl http://localhost:8080/metrics

# Disable monitoring if not needed
python start_avatar_web_server.py --no-monitoring

# Increase worker processes (if using Gunicorn)
# Edit gunicorn command: -w 8 instead of -w 4
```

#### 3. Memory Leak

**Symptoms:** Memory usage grows over time

**Solutions:**
```bash
# Monitor memory
watch -n 1 'ps aux | grep python | grep avatar'

# Check for too many connections
curl http://localhost:8080/metrics | grep connections

# Restart service
sudo systemctl restart elysia-avatar
```

#### 4. SSL Certificate Issues

**Symptoms:** HTTPS not working, SSL errors

**Solutions:**
```bash
# Check certificate validity
sudo certbot certificates

# Renew certificate
sudo certbot renew

# Check Nginx SSL config
sudo nginx -t
openssl s_client -connect avatar.yourdomain.com:443
```

#### 5. Rate Limiting Too Aggressive

**Symptoms:** Legitimate users being blocked

**Solutions:**
```bash
# Adjust rate limits in avatar_security.py
# Edit Core/Interface/avatar_security.py
# Change RATE_LIMIT_PER_SECOND and RATE_LIMIT_PER_MINUTE

# Or disable rate limiting
# Edit .env: AVATAR_RATE_LIMIT_ENABLED=false
```

### Debug Mode

```bash
# Start with debug logging
export AVATAR_LOG_LEVEL=DEBUG
python start_avatar_web_server.py

# Or edit .env
echo "AVATAR_LOG_LEVEL=DEBUG" >> .env
```

### Performance Diagnostics

```bash
# Check system resources
top
htop
vmstat 1
iostat -x 1

# Check network
netstat -an | grep ESTABLISHED | wc -l
ss -s

# Check Python process
strace -p $(pgrep -f avatar_server)
```

---

## Production Checklist

Before going live:

- [ ] SSL/TLS certificates installed and tested
- [ ] Nginx reverse proxy configured
- [ ] Firewall rules configured
- [ ] Rate limiting enabled
- [ ] Monitoring enabled
- [ ] Log rotation configured
- [ ] Systemd service configured and enabled
- [ ] Health checks running
- [ ] Backup strategy in place
- [ ] Load testing completed
- [ ] Security audit completed
- [ ] Documentation updated

---

## Maintenance

### Regular Tasks

**Daily:**
- Check service status: `sudo systemctl status elysia-avatar`
- Review logs: `sudo journalctl -u elysia-avatar --since today`
- Check metrics: `curl http://localhost:8080/metrics`

**Weekly:**
- Review performance metrics
- Check disk space: `df -h`
- Review security logs
- Update dependencies: `pip list --outdated`

**Monthly:**
- Update system packages: `sudo apt update && sudo apt upgrade`
- Review and rotate logs
- Performance optimization review
- Security audit

---

## Support

For issues and questions:
- GitHub Issues: https://github.com/ioas0316-cloud/Elysia/issues
- Documentation: `/docs` directory
- Logs: `/var/log/elysia/avatar.log`

---

**Last Updated:** 2025-12-07  
**Version:** 1.0.0
