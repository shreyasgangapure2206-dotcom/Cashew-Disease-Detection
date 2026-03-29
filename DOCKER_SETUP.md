# 🐳 DOCKER DEPLOYMENT GUIDE

## Quick Start

### 1. Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p static/uploads static/gradcam instance models

# Expose port
EXPOSE 5000

# Run application
CMD ["python", "app.py"]
```

### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  cashew-ai:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./models:/app/models
      - ./static/uploads:/app/static/uploads
      - ./instance:/app/instance
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - OLLAMA_URL=http://ollama:11434
    depends_on:
      - ollama
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama_data:
```

### 3. Create .dockerignore
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
.venv/
env/
ENV/
.git/
.gitignore
*.md
.vscode/
.idea/
*.log
dataset/
tf_env/
logs/
```

## 🚀 Build & Run

### Build Image
```bash
docker build -t cashew-ai:latest .
```

### Run Container
```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/static/uploads:/app/static/uploads \
  --name cashew-ai \
  cashew-ai:latest
```

### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 Production Optimization

### Multi-Stage Build (Smaller Image)
```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN mkdir -p static/uploads static/gradcam instance models

EXPOSE 5000

# Use production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Add to requirements.txt
```
gunicorn==21.2.0
```

## 🌐 Kubernetes Deployment

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cashew-ai
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cashew-ai
  template:
    metadata:
      labels:
        app: cashew-ai
    spec:
      containers:
      - name: cashew-ai
        image: cashew-ai:latest
        ports:
        - containerPort: 5000
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: cashew-secrets
              key: secret-key
        volumeMounts:
        - name: models
          mountPath: /app/models
        - name: uploads
          mountPath: /app/static/uploads
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: models-pvc
      - name: uploads
        persistentVolumeClaim:
          claimName: uploads-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: cashew-ai-service
spec:
  selector:
    app: cashew-ai
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

## 📦 Image Size Optimization

### Tips:
1. Use `python:3.11-slim` instead of `python:3.11`
2. Multi-stage builds
3. Remove unnecessary files with `.dockerignore`
4. Use `--no-cache-dir` with pip
5. Clean apt cache after install

### Expected Sizes:
- Basic image: ~1.2GB
- Optimized image: ~800MB
- With model: +100MB

## 🔒 Security Best Practices

1. Don't include `.env` in image
2. Use secrets management
3. Run as non-root user
4. Scan images for vulnerabilities
5. Use specific version tags

## 🧪 Testing Docker Build

```bash
# Build
docker build -t cashew-ai:test .

# Test run
docker run -p 5000:5000 cashew-ai:test

# Check logs
docker logs -f <container_id>

# Test API
curl http://localhost:5000/health
```

## 📊 Monitoring

### Health Check
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Resource Limits
```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 2G
```

## 🚀 Cloud Deployment

### AWS ECS
```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker build -t cashew-ai .
docker tag cashew-ai:latest <account>.dkr.ecr.us-east-1.amazonaws.com/cashew-ai:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/cashew-ai:latest
```

### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/<project-id>/cashew-ai
gcloud run deploy cashew-ai --image gcr.io/<project-id>/cashew-ai --platform managed
```

### Azure Container Instances
```bash
# Build and push to ACR
az acr build --registry <registry-name> --image cashew-ai:latest .
az container create --resource-group <rg> --name cashew-ai --image <registry>.azurecr.io/cashew-ai:latest --ports 5000
```

## 📝 Notes

- Model file must be present in `models/` directory
- Database persists in `instance/` volume
- Uploads stored in `static/uploads/` volume
- Ollama optional (for AI insights)
