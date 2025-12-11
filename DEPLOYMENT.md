# 🚀 Deployment Guide

This guide covers various deployment options for the AI Context-Aware Image Caption Generator.

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 14+**
- **Git**
- **4GB+ RAM** (for AI models)

## 🏠 Local Development

### Quick Start
```bash
# Clone repository
git clone https://github.com/PIYUSHYUZTA/AI-Context-Aware-Image-Caption-Generator.git
cd AI-Context-Aware-Image-Caption-Generator

# Backend setup
pip install -r requirements.txt
python api.py

# Frontend setup (new terminal)
cd frontend
npm install
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./models:/app/models
    
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    environment:
      - REACT_APP_API_URL=http://localhost:8000

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
```

2. **Create Dockerfile (root directory):**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

3. **Create frontend/Dockerfile:**
```dockerfile
FROM node:16-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html

EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

4. **Deploy:**
```bash
docker-compose up --build
```

## ☁️ Cloud Deployment

### Vercel (Frontend Only)

1. **Install Vercel CLI:**
```bash
npm i -g vercel
```

2. **Deploy frontend:**
```bash
cd frontend
vercel --prod
```

3. **Environment Variables:**
```
REACT_APP_API_URL=https://your-backend-url.com
```

### Heroku (Full Stack)

1. **Create Procfile:**
```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

2. **Deploy:**
```bash
heroku create your-app-name
heroku buildpacks:add heroku/python
heroku buildpacks:add heroku/nodejs
git push heroku main
```

3. **Environment Variables:**
```bash
heroku config:set PYTHONPATH=/app
heroku config:set NODE_ENV=production
```

### Railway

1. **Create railway.json:**
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn api:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health"
  }
}
```

2. **Deploy:**
```bash
railway login
railway init
railway up
```

### AWS EC2

1. **Launch EC2 instance** (Ubuntu 20.04 LTS)

2. **Install dependencies:**
```bash
sudo apt update
sudo apt install python3-pip nodejs npm nginx -y
```

3. **Clone and setup:**
```bash
git clone https://github.com/PIYUSHYUZTA/AI-Context-Aware-Image-Caption-Generator.git
cd AI-Context-Aware-Image-Caption-Generator
pip3 install -r requirements.txt
cd frontend && npm install && npm run build
```

4. **Configure Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Create systemd service:**
```ini
[Unit]
Description=Caption Generator API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/path/to/project
ExecStart=/usr/local/bin/uvicorn api:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

6. **Start services:**
```bash
sudo systemctl enable caption-api
sudo systemctl start caption-api
sudo systemctl restart nginx
```

### Google Cloud Platform

1. **Create app.yaml:**
```yaml
runtime: python39

env_variables:
  PYTHONPATH: /srv

automatic_scaling:
  min_instances: 1
  max_instances: 10

resources:
  cpu: 2
  memory_gb: 4
```

2. **Deploy:**
```bash
gcloud app deploy
```

### Azure App Service

1. **Create Azure Web App**

2. **Configure deployment:**
```bash
az webapp up --name your-app-name --resource-group your-rg --runtime "PYTHON|3.9"
```

3. **Set startup command:**
```
uvicorn api:app --host 0.0.0.0 --port 8000
```

## 🔧 Production Configuration

### Environment Variables

**Backend (.env):**
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Model Configuration
MODEL_PATH=./models/caption_model.h5
TOKENIZER_PATH=./models/tokenizer.pkl
USE_EXTERNAL_MODEL=True

# Security
CORS_ORIGINS=["https://your-frontend-domain.com"]
MAX_FILE_SIZE=10485760  # 10MB

# Performance
WORKERS=4
TIMEOUT=300
```

**Frontend (.env.production):**
```env
REACT_APP_API_URL=https://your-backend-domain.com
REACT_APP_MAX_FILE_SIZE=10485760
GENERATE_SOURCEMAP=false
```

### Performance Optimization

1. **Enable Gzip compression**
2. **Use CDN for static assets**
3. **Implement caching strategies**
4. **Monitor resource usage**
5. **Set up auto-scaling**

### Security Checklist

- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] File upload validation
- [ ] Rate limiting implemented
- [ ] Environment variables secured
- [ ] Regular security updates
- [ ] Monitoring and logging

### Monitoring

**Health Check Endpoint:**
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

**Logging Configuration:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🔍 Troubleshooting

### Common Issues

**1. Model Loading Errors**
```bash
# Check model files exist
ls -la models/

# Verify permissions
chmod 644 models/*
```

**2. CORS Issues**
```python
# Update CORS settings in api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**3. Memory Issues**
```bash
# Check available memory
free -h

# Monitor process memory
top -p $(pgrep -f "uvicorn")
```

**4. Port Conflicts**
```bash
# Check port usage
netstat -tulpn | grep :8000

# Kill process using port
sudo kill -9 $(lsof -t -i:8000)
```

### Performance Tuning

**1. Optimize Model Loading**
```python
# Use model caching
@lru_cache(maxsize=1)
def load_model():
    return load_model_from_disk()
```

**2. Enable Async Processing**
```python
# Use background tasks
from fastapi import BackgroundTasks

@app.post("/api/v1/caption")
async def generate_caption(background_tasks: BackgroundTasks):
    # Implementation
```

**3. Database Connection Pooling**
```python
# If using database
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=0
)
```

## 📊 Scaling Strategies

### Horizontal Scaling
- Load balancer (Nginx, HAProxy)
- Multiple backend instances
- Container orchestration (Kubernetes)
- Microservices architecture

### Vertical Scaling
- Increase CPU/RAM
- GPU acceleration for AI models
- SSD storage for faster I/O
- Optimize model inference

### Caching Strategies
- Redis for session storage
- CDN for static assets
- Model result caching
- Database query caching

## 🔐 SSL/TLS Setup

### Let's Encrypt (Free SSL)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Custom SSL Certificate
```nginx
server {
    listen 443 ssl;
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

## 📈 Monitoring and Analytics

### Application Monitoring
- **Sentry** for error tracking
- **New Relic** for performance monitoring
- **DataDog** for infrastructure monitoring
- **Prometheus + Grafana** for custom metrics

### Log Management
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Fluentd** for log collection
- **CloudWatch** (AWS) or **Stackdriver** (GCP)

## 🚀 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: pip install -r requirements.txt
        
      - name: Run tests
        run: pytest
        
      - name: Deploy to production
        run: |
          # Your deployment script
```

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review logs for error messages
3. Create an issue on GitHub
4. Contact the maintainers

---

**Happy Deploying! 🚀**