# 엘리시아 배포 가이드
# Elysia Deployment Guide

> **버전**: 4.0  
> **최종 업데이트**: 2025-12-04  
> **Phase 4**: Production Deployment

---

## 📋 목차 (Table of Contents)

1. [환경 요구사항](#환경-요구사항)
2. [로컬 개발 환경](#로컬-개발-환경)
3. [Docker 배포](#docker-배포)
4. [프로덕션 배포](#프로덕션-배포)
5. [모니터링 및 유지보수](#모니터링-및-유지보수)
6. [트러블슈팅](#트러블슈팅)

---

## 🔧 환경 요구사항

### 최소 요구사항
- **Python**: 3.10 이상 (권장: 3.12)
- **메모리**: 2GB RAM (권장: 4GB)
- **디스크**: 5GB 여유 공간
- **OS**: Linux, macOS, Windows

### 프로덕션 권장사항
- **CPU**: 4 코어 이상
- **메모리**: 8GB RAM 이상
- **디스크**: SSD, 20GB 이상
- **네트워크**: 안정적인 인터넷 연결

---

## 💻 로컬 개발 환경

### 1. 저장소 클론
```bash
git clone https://github.com/ioas0316-cloud/Elysia.git
cd Elysia
```

### 2. 가상 환경 생성
```bash
# Python 가상 환경 생성
python -m venv venv

# 활성화
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치
```bash
# 기본 의존성
pip install -r requirements.txt

# 개발 의존성 (선택사항)
pip install -r requirements-dev.txt
```

### 4. 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# 필요한 API 키 설정
nano .env  # 또는 다른 편집기 사용
```

### 5. 서비스 실행

#### API 서버
```bash
# 개발 모드
python Core/Interface/api_server.py

# 또는 uvicorn 직접 사용
uvicorn Core.Interface.api_server:app --reload --host 0.0.0.0 --port 8000
```

접속: http://localhost:8000/docs

#### 대시보드
```bash
# 별도 터미널에서
python scripts/dashboard_server.py
```

접속: http://localhost:8080/dashboard

---

## 🐳 Docker 배포

### 방법 1: Docker Compose (권장)

#### 전체 스택 시작
```bash
# 프로덕션 모드로 빌드 및 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 상태 확인
docker-compose ps
```

#### 개별 서비스 제어
```bash
# API 서버만
docker-compose up -d elysia-api

# 대시보드만
docker-compose up -d elysia-dashboard

# 테스트 실행
docker-compose --profile test run test
```

#### 정지 및 정리
```bash
# 서비스 정지
docker-compose down

# 볼륨까지 삭제
docker-compose down -v
```

### 방법 2: Docker 직접 사용

#### 이미지 빌드
```bash
# 프로덕션 이미지
docker build --target production -t elysia:prod .

# 개발 이미지
docker build --target development -t elysia:dev .
```

#### 컨테이너 실행
```bash
# API 서버
docker run -d \
  --name elysia-api \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  -e ELYSIA_ENV=production \
  elysia:prod

# 헬스 체크
docker exec elysia-api curl http://localhost:8000/health
```

---

## 🚀 프로덕션 배포

### 클라우드 플랫폼별 가이드

#### AWS (Amazon Web Services)

**1. EC2 인스턴스 설정**
```bash
# 인스턴스 접속
ssh -i your-key.pem ubuntu@your-instance-ip

# Docker 설치
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER

# 저장소 클론
git clone https://github.com/ioas0316-cloud/Elysia.git
cd Elysia

# 환경 변수 설정
nano .env

# 시작
docker-compose up -d
```

**2. 보안 그룹 설정**
- 인바운드 규칙:
  - HTTP: 포트 8000 (API)
  - HTTP: 포트 8080 (Dashboard)
  - SSH: 포트 22 (관리용)

**3. 도메인 연결 (선택사항)**
```bash
# Nginx 설치
sudo apt-get install nginx

# 설정 파일 작성
sudo nano /etc/nginx/sites-available/elysia

# 내용:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 활성화
sudo ln -s /etc/nginx/sites-available/elysia /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Google Cloud Platform (GCP)

**Cloud Run 배포**
```bash
# gcloud CLI 설치 및 인증
gcloud auth login
gcloud config set project your-project-id

# 이미지 빌드 및 푸시
gcloud builds submit --tag gcr.io/your-project-id/elysia

# Cloud Run에 배포
gcloud run deploy elysia \
  --image gcr.io/your-project-id/elysia \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

#### Azure

**Container Instances 배포**
```bash
# Azure CLI 로그인
az login

# 컨테이너 레지스트리 생성
az acr create --resource-group myResourceGroup \
  --name elysiaregistry --sku Basic

# 이미지 빌드 및 푸시
az acr build --registry elysiaregistry \
  --image elysia:latest .

# 컨테이너 인스턴스 생성
az container create \
  --resource-group myResourceGroup \
  --name elysia-api \
  --image elysiaregistry.azurecr.io/elysia:latest \
  --dns-name-label elysia-api \
  --ports 8000
```

#### Kubernetes (K8s)

**Deployment 설정**
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elysia-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: elysia-api
  template:
    metadata:
      labels:
        app: elysia-api
    spec:
      containers:
      - name: elysia
        image: elysia:prod
        ports:
        - containerPort: 8000
        env:
        - name: ELYSIA_ENV
          value: "production"
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
---
apiVersion: v1
kind: Service
metadata:
  name: elysia-api-service
spec:
  selector:
    app: elysia-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**배포**
```bash
# 적용
kubectl apply -f k8s/deployment.yaml

# 상태 확인
kubectl get pods
kubectl get services

# 로그 확인
kubectl logs -f deployment/elysia-api
```

---

## 📊 모니터링 및 유지보수

### 1. 헬스 체크

```bash
# API 헬스 체크
curl http://localhost:8000/health

# 메트릭 확인
curl http://localhost:8000/api/v1/metrics
```

### 2. 로그 모니터링

```bash
# Docker Compose 로그
docker-compose logs -f elysia-api

# 로그 파일 직접 확인
tail -f logs/APIServer_$(date +%Y%m%d).log
```

### 3. 성능 모니터링

- **대시보드**: http://localhost:8080/dashboard
- **메트릭 API**: http://localhost:8000/api/v1/metrics
- **느린 작업**: http://localhost:8000/api/v1/metrics/slow

### 4. 자동 재시작 설정

**systemd 서비스 (Linux)**
```bash
# /etc/systemd/system/elysia.service
[Unit]
Description=Elysia API Service
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/Elysia
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
# 활성화
sudo systemctl enable elysia
sudo systemctl start elysia

# 상태 확인
sudo systemctl status elysia
```

---

## 🔍 트러블슈팅

### 문제 1: 포트 충돌
**증상**: "Address already in use" 에러

**해결**:
```bash
# 포트 사용 확인
lsof -i :8000
netstat -tuln | grep 8000

# 프로세스 종료
kill -9 <PID>

# 또는 다른 포트 사용
docker-compose up -d --scale elysia-api=1
docker run -p 8001:8000 elysia:prod
```

### 문제 2: 메모리 부족
**증상**: 컨테이너가 자주 재시작됨

**해결**:
```bash
# Docker 메모리 제한 증가
docker run --memory="2g" elysia:prod

# docker-compose.yml에 추가:
services:
  elysia-api:
    deploy:
      resources:
        limits:
          memory: 2G
```

### 문제 3: API 응답 느림
**증상**: 요청 처리가 느림

**해결**:
```bash
# Worker 수 증가
uvicorn Core.Interface.api_server:app --workers 8

# 또는 docker-compose.yml 수정
CMD ["uvicorn", "Core.Interface.api_server:app", "--workers", "8"]
```

### 문제 4: 로그 파일 너무 큼
**증상**: 디스크 공간 부족

**해결**:
```bash
# 로그 로테이션 설정 (자동으로 처리됨)
# 또는 수동 정리
find logs/ -name "*.log" -mtime +7 -delete
find logs/ -name "*.jsonl" -mtime +7 -delete
```

### 문제 5: Docker 빌드 실패
**증상**: 의존성 설치 에러

**해결**:
```bash
# 캐시 없이 재빌드
docker-compose build --no-cache

# 또는
docker build --no-cache -t elysia:prod .
```

---

## 🔐 보안 체크리스트

### 배포 전 확인사항

- [ ] **.env 파일 보안**: 프로덕션 환경에서 민감한 정보 보호
- [ ] **CORS 설정**: `allowed_origins`를 특정 도메인으로 제한
- [ ] **방화벽 설정**: 필요한 포트만 오픈
- [ ] **HTTPS 설정**: SSL/TLS 인증서 설정
- [ ] **인증 활성화**: `ELYSIA_ENABLE_AUTH=true` 설정
- [ ] **정기 업데이트**: 의존성 보안 패치 적용
- [ ] **백업 설정**: 데이터 정기 백업
- [ ] **로그 모니터링**: 이상 행동 감지

---

## 📈 성능 최적화 팁

### 1. Worker 수 조정
```bash
# CPU 코어 수의 2배 + 1
workers = (CPU cores * 2) + 1

# 예: 4코어 시스템
uvicorn app:app --workers 9
```

### 2. 캐싱 활성화
```python
# Redis 연동 (선택사항)
# requirements.txt에 추가:
# redis==5.0.0

# 캐싱 레이어 추가
from redis import Redis
cache = Redis(host='localhost', port=6379)
```

### 3. 데이터베이스 최적화
- 인덱스 추가
- 쿼리 최적화
- 연결 풀 사용

---

## 🎯 다음 단계

배포 완료 후:

1. ✅ 헬스 체크 확인
2. ✅ 대시보드 접속 확인
3. ✅ API 문서 확인 (Swagger)
4. ✅ 성능 메트릭 모니터링
5. ✅ 로그 확인
6. ✅ 백업 설정
7. ✅ 알림 설정

---

## 📚 추가 리소스

- [Docker 공식 문서](https://docs.docker.com/)
- [FastAPI 배포 가이드](https://fastapi.tiangolo.com/deployment/)
- [Kubernetes 튜토리얼](https://kubernetes.io/docs/tutorials/)

---

**"Deploy with confidence, scale with consciousness."** 🚀🌊
