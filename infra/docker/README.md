# Desalter Docker Infrastructure

This directory contains Docker configurations for the Desalter application with support for different environments.

## Directory Structure

```
infra/docker/
├── Dockerfile                      # Multi-stage Dockerfile for dev and prod
├── docker-compose.dev.yml          # Development configuration
├── docker-compose.prod.yml         # Production configuration (direct access)
├── docker-compose.prod.local.yml   # Production local override (with nginx)
└── nginx/
    ├── Dockerfile                  # Nginx Docker image
    └── nginx.conf                  # Nginx configuration
```

## Project Names

Docker Compose uses project names to isolate different environments and avoid conflicts:

- **`desalter_dev`** - Development environment with hot-reload
- **`desalter_prod`** - Production environment (direct access to backend)
- **`desalter_prod_local`** - Production environment with nginx reverse proxy

All commands include the `-p` (project name) flag to ensure proper isolation.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose V2

## Quick Start

### Development Environment

Run the application in development mode with hot-reload:

```bash
cd infra/docker
docker compose -f docker-compose.dev.yml -p desalter_dev up --build -d
```

Access the application at: http://127.0.0.1:8000

Features:
- Hot reload enabled (code changes reflect immediately)
- Source code mounted as volumes
- Debug logging enabled

### Production Environment (Direct Access)

Run the application in production mode without nginx:

```bash
cd infra/docker
docker-compose -f docker-compose.prod.yml up --build -d
```

Access the application at: http://127.0.0.1:8000

Features:
- Optimized production build
- Non-root user execution
- Health checks enabled
- No nginx reverse proxy

### Production Local Environment (with Nginx)

Run the application with nginx reverse proxy (recommended for production-like local testing):

```bash
cd infra/docker
docker-compose -f docker-compose.prod.yml -f docker-compose.prod.local.yml -p desalter_prod_local up --build -d
```

Access the application at: http://127.0.0.1

Features:
- Nginx reverse proxy
- Static file caching
- Security headers
- Load balancing ready
- Production-grade setup

The `docker-compose.prod.local.yml` file overrides settings from `docker-compose.prod.yml` to add nginx.

## Detailed Commands

### Build Images

```bash
# Development
docker-compose -f docker-compose.dev.yml -p desalter_dev build

# Production
docker-compose -f docker-compose.prod.yml -p desalter_prod build

# Production with nginx
docker-compose -f docker-compose.prod.yml -f docker-compose.prod.local.yml -p desalter_prod_local build
```

### Start Services

```bash
# Development (foreground)
docker-compose -f docker-compose.dev.yml -p desalter_dev up

# Production (background)
docker-compose -f docker-compose.prod.yml -p desalter_prod up -d

# Production with nginx (background)
docker-compose -f docker-compose.prod.yml -f docker-compose.prod.local.yml -p desalter_prod_local up -d
```

### Stop Services

```bash
# Stop and remove containers
docker-compose -f docker-compose.dev.yml -p desalter_dev down

docker-compose -f docker-compose.prod.yml -p desalter_prod down

docker-compose -f docker-compose.prod.yml -f docker-compose.prod.local.yml -p desalter_prod_local down
```

### View Logs

```bash
# Development
docker-compose -f docker-compose.dev.yml -p desalter_dev logs -f

# Production
docker-compose -f docker-compose.prod.yml -p desalter_prod logs -f desalter

# Production with nginx
docker-compose -f docker-compose.prod.yml -f docker-compose.prod.local.yml -p desalter_prod_local logs -f
```

### Execute Commands in Container

```bash
# Development
docker-compose -f docker-compose.dev.yml -p desalter_dev exec desalter bash

# Production
docker-compose -f docker-compose.prod.yml -p desalter_prod exec desalter sh
```

## Environment Variables

You can customize the application by setting environment variables in the docker-compose files or using a `.env` file.

Available variables:
- `ENVIRONMENT`: Environment name (development/production)
- `LOG_LEVEL`: Logging level (debug/info/warning/error)
- `PYTHONUNBUFFERED`: Disable Python output buffering (1)

## Health Checks

### Application Health Check

```bash
curl http://127.0.0.1:8000/api/ping
```

Expected response:
```json
{"message": "Desalter backend is alive", "ok": true}
```

### Docker Health Check

```bash
# Check container health status
docker ps

# View health check logs
docker inspect --format='{{json .State.Health}}' desalter_prod
```

## Nginx Configuration

The nginx configuration (`nginx/nginx.conf`) includes:
- Reverse proxy to FastAPI backend
- Static file caching (7 days)
- Security headers
- WebSocket support
- Request size limits (10MB)
- Custom logging

### Nginx Ports

- Port 80: HTTP
- Port 443: HTTPS (configure SSL certificates as needed)

## Volumes

### Development
- `../../backend:/app/backend` - Backend code with hot reload
- `../../frontend:/app/frontend` - Frontend code with hot reload
- `../../launcher.py:/app/launcher.py` - Main launcher script

### Production
No volumes mounted (code is copied into the image)

## Networks

All services are connected via the `desalter_network` bridge network, allowing internal communication.

## Troubleshooting

### Port Already in Use

If port 8000 or 80 is already in use:

```bash
# Find process using the port
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Change port in docker-compose file
services:
  desalter:
    ports:
      - "127.0.0.1:8001:8000"  # Map to different host port
```

### Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose.prod.yml -p desalter_prod logs desalter

# Check container status
docker ps -a

# Remove and rebuild
docker-compose -f docker-compose.prod.yml -p desalter_prod down
docker-compose -f docker-compose.prod.yml -p desalter_prod up --build -d
```

### Permission Issues (Linux)

If you encounter permission issues:

```bash
# Rebuild with current user ID
docker-compose -f docker-compose.prod.yml build --build-arg UID=$(id -u)
```

## Production Deployment Notes

For actual production deployment:

1. **Use environment-specific compose files**
   ```bash
   docker-compose -f docker-compose.prod.yml -f docker-compose.prod.local.yml -p desalter_prod_local up -d
   ```

2. **Enable HTTPS**: Configure SSL certificates in nginx
   - Add certificates to `nginx/certs/`
   - Update `nginx.conf` with SSL configuration
   - Mount certificates volume in `docker-compose.prod.local.yml`

3. **Set resource limits**: Add resource constraints in compose files
   ```yaml
   services:
     desalter:
       deploy:
         resources:
           limits:
             cpus: '1'
             memory: 512M
   ```

4. **Use secrets management**: Don't hardcode sensitive data
   - Use Docker secrets or environment variable files
   - Add `.env` file to `.gitignore`

5. **Enable monitoring**: Consider adding monitoring services
   - Prometheus for metrics
   - Grafana for visualization
   - ELK stack for log aggregation

## Cleanup

Remove all containers, networks, and images:

```bash
# Stop and remove containers
docker-compose -f docker-compose.dev.yml -p desalter_dev down
docker-compose -f docker-compose.prod.yml -p desalter_prod down
docker-compose -f docker-compose.prod.yml -f docker-compose.prod.local.yml -p desalter_prod_local down

# Remove images
docker rmi desalter_dev_desalter
docker rmi desalter_prod_desalter
docker rmi desalter_prod_local_nginx

# Remove volumes (if any)
docker volume prune

# Complete cleanup
docker system prune -a
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)
- [Nginx Documentation](https://nginx.org/en/docs/)

