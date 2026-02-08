# ComfyUI v0.11.0 Worker

GPU worker container for ComfyUI v0.11.0 with VRAM monitoring.

**Production inference is serverless** (DataCrunch H200/B300 via `INFERENCE_MODE=serverless`).
This worker is for **local development and testing only**.

**Issues:** comfyume #2, #3, #4

---

## Components

| File | Purpose |
|------|---------|
| `Dockerfile` | Worker container build (v0.11.0 base) |
| `docker-compose.yml` | Standalone deployment config |
| `worker.py` | Job processing loop (polls queue, executes workflows) |
| `vram_monitor.py` | GPU memory monitoring (OOM prevention) |
| `start-worker.sh` | Container entrypoint (starts ComfyUI + worker) |
| `requirements.txt` | Python dependencies (Redis, httpx, etc.) |

---

## Quick Start

### Build

```bash
docker build -t comfyume-worker:v0.11.0 .
```

### Run (Standalone)

```bash
# Set environment variables (.env v0.3.5)
export INFERENCE_SERVER_REDIS_HOST=100.99.216.71  # Mello VPS via Tailscale
export REDIS_PASSWORD=your_password
export QUEUE_MANAGER_URL=http://100.99.216.71:3000
export COMFYUI_MODE=worker  # Full inference mode

# Start worker
docker compose up -d

# Check logs
docker compose logs -f
```

### Test GPU Detection

```bash
docker run --gpus all comfyume-worker:v0.11.0 nvidia-smi
```

---

## Environment Variables

### Core Settings (.env v0.3.5)
- `WORKER_ID` - Worker identifier (default: worker-1)
- `INFERENCE_SERVER_REDIS_HOST` - Redis server IP (Mello VPS via Tailscale: 100.99.216.71)
- `REDIS_PORT` - Redis port (default: 6379)
- `REDIS_PASSWORD` - Redis authentication
- `QUEUE_MANAGER_URL` - Queue manager API endpoint
- `COMFYUI_URL` - ComfyUI server URL (default: http://localhost:8188)
- `COMFYUI_MODE` - Deployment mode (worker = full inference, frontend-testing = UI only)

### Timeouts
- `COMFYUI_TIMEOUT` - ComfyUI request timeout (default: 900s / 15 min)
- `JOB_TIMEOUT` - Max job execution time (default: 1800s / 30 min)
- `HTTP_CLIENT_TIMEOUT` - Queue manager timeout (default: 30s)
- `WORKER_POLL_INTERVAL` - Queue polling interval (default: 2s)

### VRAM Monitoring
- `ENABLE_VRAM_MONITORING` - Enable/disable (default: true)
- `VRAM_SAFETY_MARGIN_MB` - Safety buffer (default: 2048 / 2GB)
- `VRAM_CHECK_TIMEOUT_SECONDS` - nvidia-smi timeout (default: 5)
- `VRAM_DEFAULT_ESTIMATE_MB` - Fallback estimate (default: 8192 / 8GB)
- `VRAM_CHECK_DRY_RUN` - Test mode (default: false)

### Logging
- `LOG_FORMAT` - "text" or "json" (default: text)
- `PYTHONUNBUFFERED` - Python output buffering (default: 1)

---

## Volume Mounts

### Models (SFS Network Drive)
```bash
/mnt/sfs/models -> /workspace/ComfyUI/models (read-only)
```

### Outputs (Scratch Disk)
```bash
/mnt/scratch/outputs -> /outputs (read-write)
```

### Inputs (Scratch Disk)
```bash
/mnt/scratch/inputs -> /inputs (read-only)
```

---

## Health Checks

**Endpoint:** `http://localhost:8188/`

**Intervals:**
- Check every 60s
- Timeout after 10s
- Start delay: 30s
- Retries: 3

**Test manually:**
```bash
curl -f http://localhost:8188/
```

---

## Key Changes from v0.9.2

### Base Image
- **v0.9.2:** nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04
- **v0.11.0:** nvidia/cuda:12.4.0-runtime-ubuntu22.04

### Dependencies Added
- `curl` - Health checks
- `libgomp1` - Audio nodes (torchaudio)
- `requests` - HTTP client (missing from ComfyUI requirements.txt)

### Worker Integration
- VRAM monitoring (vram_monitor.py)
- Pre-check GPU memory before accepting jobs
- Fail gracefully if insufficient VRAM
- Updated timeouts for video generation (15/30 min)

### API Endpoints (STABLE - unchanged)
- POST `/prompt` - Submit workflow
- GET `/history/{id}` - Poll job status
- WebSocket `/ws` - Real-time updates

---

## Testing

### 1. Build Test
```bash
docker build -t comfyume-worker:v0.11.0 .
```

### 2. GPU Detection
```bash
docker run --gpus all comfyume-worker:v0.11.0 nvidia-smi
```

### 3. VRAM Monitor CLI
```bash
docker run --gpus all comfyume-worker:v0.11.0 python3 /workspace/vram_monitor.py
```

### 4. Integration Test
```bash
# Start worker
docker compose up -d

# Check logs for errors
docker compose logs -f worker-1

# Verify health check
docker inspect comfyume-worker-1 | grep -A 5 Health
```

---

## Troubleshooting

### Container won't start
```bash
# Check logs
docker compose logs worker-1

# Common issues:
# - Missing REDIS_PASSWORD
# - Wrong INFERENCE_SERVER_REDIS_HOST (should be Tailscale IP: 100.99.216.71)
# - Models not mounted (check /mnt/sfs/models exists)
# - COMFYUI_MODE not set to 'worker'
```

### GPU not detected
```bash
# Test nvidia-docker
docker run --gpus all nvidia/cuda:12.4.0-runtime-ubuntu22.04 nvidia-smi

# Check docker daemon supports GPU
docker info | grep Runtimes
```

### ComfyUI won't start
```bash
# Check ComfyUI logs
docker exec -it comfyume-worker-1 tail -f /workspace/ComfyUI/comfyui.log

# Common issues:
# - Models not found (check volume mounts)
# - OOM on startup (reduce model cache)
# - Port 8188 already in use
```

### VRAM check failing jobs
```bash
# Test VRAM monitoring
docker exec -it comfyume-worker-1 python3 /workspace/vram_monitor.py check 24576

# Adjust safety margin
docker compose down
export VRAM_SAFETY_MARGIN_MB=1024  # Reduce to 1GB
docker compose up -d

# Disable monitoring temporarily
export ENABLE_VRAM_MONITORING=false
docker compose up -d
```

---

## Architecture

```
┌─────────────────────────────────────┐
│  Docker Container                   │
│  ┌──────────────────────────────┐   │
│  │  start-worker.sh             │   │
│  │  1. Start ComfyUI :8188      │   │
│  │  2. Wait for ready           │   │
│  │  3. Start worker.py          │   │
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │
│  │  worker.py                   │   │
│  │  - Poll queue (Redis)        │   │
│  │  - Check VRAM (nvidia-smi)   │   │
│  │  - Submit to ComfyUI         │   │
│  │  - Wait for completion       │   │
│  │  - Report results            │   │
│  └──────────────────────────────┘   │
│                                     │
│  ┌──────────────────────────────┐   │
│  │  ComfyUI v0.11.0             │   │
│  │  - Execute workflows         │   │
│  │  - GPU processing            │   │
│  │  - Output to /outputs        │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
         ↕                   ↕
    [Redis Queue]      [GPU/VRAM]
  (Mello via Tailscale)
```

---

## References

- [ComfyUI v0.11.0 Release](https://github.com/comfyanonymous/ComfyUI/releases/tag/v0.11.0)
- [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker)
- [Issue #2 (Dockerfile)](https://github.com/ahelme/comfyume/issues/2)
- [Issue #3 (worker.py)](https://github.com/ahelme/comfyume/issues/3)
- [Issue #4 (VRAM monitoring)](https://github.com/ahelme/comfyume/issues/4)

---

## Configuration Notes

**Environment Variables v0.3.2:**
- `INFERENCE_SERVER_REDIS_HOST` replaces `REDIS_HOST` for GPU workers
- App server containers use `APP_SERVER_REDIS_HOST=redis` (Docker network)
- This separation clarifies dual-server deployment architecture

**Backward Compatibility:**
- Worker.py checks for both `INFERENCE_SERVER_REDIS_HOST` and legacy `REDIS_HOST`
- Falls back gracefully if old variable names are used

---

**Last Updated:** 2026-02-07
