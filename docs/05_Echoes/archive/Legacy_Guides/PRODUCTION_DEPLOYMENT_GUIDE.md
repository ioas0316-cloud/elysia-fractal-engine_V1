# 프로덕션 배포 가이드
# Production Deployment Guide

**버전**: 1.0.0  
**날짜**: 2025-12-07  
**대상**: Phase 1 + Phase 2 최적화 완료 시스템

---

## 📋 목차

1. [시스템 요구사항](#시스템-요구사항)
2. [설치 및 설정](#설치-및-설정)
3. [환경 변수 설정](#환경-변수-설정)
4. [서비스 배포](#서비스-배포)
5. [리버스 프록시 설정](#리버스-프록시-설정)
6. [모니터링 및 로깅](#모니터링-및-로깅)
7. [성능 튜닝](#성능-튜닝)
8. [보안 강화](#보안-강화)
9. [백업 및 복구](#백업-및-복구)
10. [트러블슈팅](#트러블슈팅)

---

## 시스템 요구사항

### 최소 사양
```
CPU: 2 cores
RAM: 4 GB
Storage: 10 GB
Network: 100 Mbps
OS: Ubuntu 20.04+ / CentOS 8+ / Debian 11+
```

### 권장 사양 (25+ 동시 사용자)
```
CPU: 4 cores (8 threads)
RAM: 8 GB
Storage: 20 GB SSD
Network: 1 Gbps
OS: Ubuntu 22.04 LTS
```

### 소프트웨어 의존성
```bash
Python: 3.9+
Node.js: 16+ (optional, for frontend build tools)
Nginx: 1.18+ (reverse proxy)
```

---

## 설치 및 설정

### 1. 시스템 준비

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10
sudo apt install python3.10 python3.10-venv python3-pip -y

# Install system dependencies
sudo apt install build-essential libssl-dev libffi-dev python3-dev -y

# Install Nginx
sudo apt install nginx -y
```

### 2. 애플리케이션 설치

```bash
# Clone repository
cd /opt
sudo git clone https://github.com/ioas0316-cloud/Elysia.git
cd Elysia

# Create virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install numpy websockets psutil

# Install optional dependencies
pip install prometheus-client  # For metrics
pip install python-json-logger  # For structured logging
```

### 3. 권한 설정

```bash
# Create system user
sudo useradd -r -s /bin/false elysia

# Set ownership
sudo chown -R elysia:elysia /opt/Elysia

# Set permissions
sudo chmod 755 /opt/Elysia
sudo chmod 644 /opt/Elysia/Core/Creativity/web/*
```

---

## 환경 변수 설정

### `/opt/Elysia/.env` 생성

```bash
# Server Configuration
AVATAR_HOST=0.0.0.0
AVATAR_PORT=8765
HTTP_PORT=8080

# Security
ENABLE_AUTH=true
JWT_SECRET=your-secret-key-change-this-in-production

# Performance
MIN_FPS=15
MAX_FPS=60
DELTA_THRESHOLD=0.01

# Monitoring
ENABLE_MONITORING=true
ENABLE_LOGGING=true
LOG_LEVEL=INFO

# Paths
DATA_DIR=/var/lib/elysia
LOG_DIR=/var/log/elysia
```

### 디렉토리 생성

```bash
sudo mkdir -p /var/lib/elysia
sudo mkdir -p /var/log/elysia
sudo chown elysia:elysia /var/lib/elysia /var/log/elysia
```

---

## 서비스 배포

### systemd 서비스 생성

**`/etc/systemd/system/elysia-avatar.service`**:

```ini
[Unit]
Description=Elysia Avatar WebSocket Server
After=network.target

[Service]
Type=simple
User=elysia
Group=elysia
WorkingDirectory=/opt/Elysia
Environment="PATH=/opt/Elysia/venv/bin"
EnvironmentFile=/opt/Elysia/.env
ExecStart=/opt/Elysia/venv/bin/python start_avatar_web_server.py
Restart=always
RestartSec=10
StandardOutput=append:/var/log/elysia/avatar.log
StandardError=append:/var/log/elysia/avatar-error.log

# Security
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/elysia /var/log/elysia

# Resource Limits
LimitNOFILE=65536
MemoryMax=4G
CPUQuota=200%

[Install]
WantedBy=multi-user.target
```

### 서비스 시작

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable elysia-avatar

# Start service
sudo systemctl start elysia-avatar

# Check status
sudo systemctl status elysia-avatar

# View logs
sudo journalctl -u elysia-avatar -f
```

---

## 리버스 프록시 설정

### Nginx 설정

**`/etc/nginx/sites-available/elysia-avatar`**:

```nginx
# HTTP Server (port 80)
server {
    listen 80;
    server_name your-domain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

# HTTPS Server (port 443)
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Static Files (Frontend)
    location / {
        root /opt/Elysia/Core/Creativity/web;
        index avatar.html;
        try_files $uri $uri/ =404;

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # WebSocket Proxy
    location /ws {
        proxy_pass http://127.0.0.1:8765;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 3600s;  # 1 hour for long-lived connections

        # Buffer settings
        proxy_buffering off;
        proxy_request_buffering off;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:8080/health;
        access_log off;
    }

    # Access/Error logs
    access_log /var/log/nginx/elysia-avatar-access.log;
    error_log /var/log/nginx/elysia-avatar-error.log;
}
```

### Nginx 활성화

```bash
# Create symlink
sudo ln -s /etc/nginx/sites-available/elysia-avatar /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

### SSL 인증서 (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (already enabled by default)
sudo systemctl status certbot.timer
```

---

## 모니터링 및 로깅

### 로그 로테이션

**`/etc/logrotate.d/elysia-avatar`**:

```
/var/log/elysia/*.log {
    daily
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

### Prometheus Metrics (Optional)

**`start_avatar_web_server.py` 수정**:

```python
from prometheus_client import start_http_server, Counter, Gauge, Histogram

# Metrics
REQUESTS = Counter('avatar_requests_total', 'Total requests')
ACTIVE_CLIENTS = Gauge('avatar_active_clients', 'Active WebSocket clients')
RESPONSE_TIME = Histogram('avatar_response_seconds', 'Response time')
FPS = Gauge('avatar_current_fps', 'Current FPS')

# Start metrics server
start_http_server(9090)
```

**Prometheus 설정** (`/etc/prometheus/prometheus.yml`):

```yaml
scrape_configs:
  - job_name: 'elysia-avatar'
    static_configs:
      - targets: ['localhost:9090']
```

### Grafana Dashboard (Optional)

```bash
# Install Grafana
sudo apt install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt update && sudo apt install grafana -y

# Start Grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server

# Access: http://your-domain.com:3000
# Default: admin/admin
```

---

## 성능 튜닝

### 1. 시스템 리소스 최적화

**`/etc/sysctl.conf`**:

```bash
# Network performance
net.core.somaxconn = 1024
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.ip_local_port_range = 10000 65535

# File descriptors
fs.file-max = 65536
```

적용:
```bash
sudo sysctl -p
```

### 2. Nginx 튜닝

**`/etc/nginx/nginx.conf`**:

```nginx
worker_processes auto;
worker_rlimit_nofile 65536;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 10M;
    
    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript 
               application/json application/javascript application/xml+rss;
}
```

### 3. 애플리케이션 튜닝

**`start_avatar_web_server.py` 설정**:

```python
# Optimized settings for production
server = AvatarWebSocketServer(
    host="0.0.0.0",
    port=8765,
    require_auth=True,      # Enable authentication
    enable_monitoring=True  # Enable metrics
)

# Configure adaptive FPS
server.min_fps = 15  # Lower min for idle savings
server.max_fps = 60  # Higher max for smoothness

# Configure delta threshold
server.core.delta_threshold = 0.01  # Optimal balance
```

---

## 보안 강화

### 1. 방화벽 설정

```bash
# UFW firewall
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 80/tcp      # HTTP
sudo ufw allow 443/tcp     # HTTPS
sudo ufw enable

# Verify
sudo ufw status
```

### 2. Rate Limiting (Nginx)

**Nginx 설정 추가**:

```nginx
http {
    # Rate limit zone
    limit_req_zone $binary_remote_addr zone=avatar_limit:10m rate=10r/s;
    
    server {
        location /ws {
            # Apply rate limit
            limit_req zone=avatar_limit burst=20 nodelay;
            # ... other proxy settings
        }
    }
}
```

### 3. Fail2Ban (Optional)

```bash
# Install Fail2Ban
sudo apt install fail2ban -y

# Configure for Nginx
sudo nano /etc/fail2ban/jail.local
```

**`/etc/fail2ban/jail.local`**:

```ini
[nginx-req-limit]
enabled = true
filter = nginx-req-limit
action = iptables-multiport[name=ReqLimit, port="http,https", protocol=tcp]
logpath = /var/log/nginx/elysia-avatar-error.log
findtime = 600
bantime = 3600
maxretry = 10
```

---

## 백업 및 복구

### 자동 백업 스크립트

**`/usr/local/bin/backup-elysia.sh`**:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/elysia"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup data
tar -czf $BACKUP_DIR/elysia-data-$DATE.tar.gz /var/lib/elysia

# Backup logs (last 7 days)
tar -czf $BACKUP_DIR/elysia-logs-$DATE.tar.gz /var/log/elysia

# Backup configuration
tar -czf $BACKUP_DIR/elysia-config-$DATE.tar.gz /opt/Elysia/.env /etc/systemd/system/elysia-avatar.service

# Remove backups older than 30 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Backup completed: $DATE"
```

**Cron 설정**:

```bash
# Edit crontab
sudo crontab -e

# Add daily backup at 2 AM
0 2 * * * /usr/local/bin/backup-elysia.sh >> /var/log/elysia/backup.log 2>&1
```

---

## 트러블슈팅

### 일반적인 문제

#### 1. WebSocket 연결 실패

**증상**: 클라이언트가 연결되지 않음

**확인**:
```bash
# Check service status
sudo systemctl status elysia-avatar

# Check WebSocket port
sudo netstat -tulpn | grep 8765

# Check logs
sudo journalctl -u elysia-avatar -n 100
```

**해결**:
- 방화벽 규칙 확인
- Nginx 프록시 설정 확인
- SSL 인증서 유효성 확인

#### 2. 높은 CPU 사용률

**증상**: CPU 사용률 >80%

**확인**:
```bash
# Monitor process
top -p $(pgrep -f avatar_web_server)

# Check FPS
grep "FPS" /var/log/elysia/avatar.log
```

**해결**:
- MIN_FPS 낮추기 (예: 10)
- DELTA_THRESHOLD 높이기 (예: 0.02)
- 동시 사용자 수 제한

#### 3. 메모리 누수

**증상**: 메모리 사용량 지속 증가

**확인**:
```bash
# Monitor memory
watch -n 1 'ps aux | grep avatar_web_server'
```

**해결**:
- 서비스 재시작 스케줄링
- MemoryMax 설정 적용
- 프로파일링 도구 사용

### 성능 모니터링 명령어

```bash
# Real-time monitoring
watch -n 1 'systemctl status elysia-avatar | grep "Memory\|CPU"'

# WebSocket connections
sudo ss -tan | grep :8765 | wc -l

# Log analysis
tail -f /var/log/elysia/avatar.log | grep "FPS\|clients"

# Performance test
python benchmarks/avatar_performance_benchmark.py
```

---

## 체크리스트

### 배포 전
- [ ] 시스템 요구사항 확인
- [ ] 의존성 설치 완료
- [ ] 환경 변수 설정 완료
- [ ] SSL 인증서 설정 완료
- [ ] 방화벽 규칙 설정 완료

### 배포 후
- [ ] 서비스 정상 시작 확인
- [ ] WebSocket 연결 테스트
- [ ] 델타 업데이트 작동 확인
- [ ] 적응형 FPS 작동 확인
- [ ] 로그 로테이션 작동 확인
- [ ] 백업 스크립트 테스트
- [ ] 모니터링 대시보드 설정

### 정기 유지보수
- [ ] 주간: 로그 분석, 성능 모니터링
- [ ] 월간: 백업 검증, 보안 업데이트
- [ ] 분기: 용량 계획, 최적화 검토

---

## 참고 자료

- **프로젝트 문서**: `docs/AVATAR_SYSTEM_REVIEW.md`
- **성능 벤치마크**: `docs/benchmark_results.json`
- **테스트 스위트**: `tests/test_avatar_optimizations.py`
- **GitHub 이슈**: https://github.com/ioas0316-cloud/Elysia/issues

---

**작성자**: Elysia Development Team  
**최종 업데이트**: 2025-12-07  
**라이선스**: Apache License 2.0
