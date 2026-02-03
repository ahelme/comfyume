# Serverless Implementation Update

**Project:** ComfyuME
**Date:** 2026-02-03
**Status:** 🟡 In Progress - Code complete, deployment testing

---

## Summary

Implemented serverless inference mode with multi-GPU support (H200/B300, spot/on-demand). Code is complete and committed. Verda serverless container deployment created but returning 404 - needs health check path fix.

---

## Completed Work

### 1. Code Implementation (Issue #62)

**Files Modified:**
- `queue-manager/config.py` - Multi-endpoint support with 4 GPU options
- `queue-manager/main.py` - Serverless routing, CORS for aiworkshop.art
- `queue-manager/models.py` - HealthCheck includes active_gpu field
- `docker-compose.yml` - Serverless env vars added to queue-manager
- `.env` - All 4 endpoint URLs configured

**New Files:**
- `h200-spot.env` - H200 SPOT config (€0.97/hr + VAT)
- `h200-on-demand.env` - H200 On-Demand config (€2.80/hr + VAT)
- `b300-spot.env` - B300 SPOT config (€1.61/hr + VAT)
- `b300-on-demand.env` - B300 On-Demand config (€4.63/hr + VAT)
- `scripts/switch-gpu.sh` - CLI tool to switch between GPU modes

**Git Commits:**
- `55337d8` - feat: complete serverless multi-GPU implementation (#62)
- `65e7744` - feat: add H100/B300 spot and on-demand serverless options
- `044b44c` - feat: switch from H100 to H200 for serverless inference

### 2. Pricing Analysis

| Deployment | GPU | Base | +19% VAT | Use Case |
|------------|-----|------|----------|----------|
| comfyume-vca-ftv-h200-spot | H200 141GB | €0.97/hr | €1.15/hr | Workshop, testing |
| comfyume-vca-ftv-h200-on-demand | H200 141GB | €2.80/hr | €3.33/hr | Important demos |
| comfyume-vca-ftv-b300-spot | B300 288GB | €1.61/hr | €1.92/hr | Cheap 4K |
| comfyume-vca-ftv-b300-on-demand | B300 288GB | €4.63/hr | €5.51/hr | Premium 4K |

### 3. Cost Estimates Calculated

**Scenario #1: Boss Demo + Independent Play (24hr)**
- H200: ~€10-15 total (actual GPU time ~4-5 hrs)

**Scenario #2: Workshop (3hr, 20 people)**
- H200: ~€35-45 total (actual GPU time ~16 hrs across parallel containers)

### 4. Verda Serverless Deployment

**Created:** comfyume-vca-ftv-h200-spot

**Configuration:**
```
Container Image:    ghcr.io/ahelme/comfyume-worker:v0.11.0
Registry:           Public
GPU Type:           H200 SXM5 141GB (SPOT)
Number of GPUs:     1
HTTP Port:          8188
Health Check:       /system_stats (NEEDS FIX - see below)
Min Replicas:       0
Max Replicas:       10
Concurrent Req:     1
Scale-up Delay:     0
Scale-down Delay:   300
Request TTL:        36000
Storage:            SFS mounted at /mnt/sfs
```

**Start Command:**
```bash
python /workspace/ComfyUI/main.py --listen 0.0.0.0 --port 8188 --extra-model-paths-config /mnt/sfs/extra_model_paths.yaml
```

**Environment Variables:**
- `HF_HOME=/mnt/sfs/cache/huggingface`
- `HF_TOKEN=<from .env>`

### 5. SFS Configuration

**Created:** `/mnt/sfs/extra_model_paths.yaml`
```yaml
comfyui:
    base_path: /mnt/sfs/models/shared/
    checkpoints: checkpoints/
    diffusion_models: diffusion_models/
    clip: text_encoders/
    vae: vae/
    loras: loras/
    upscale_models: latent_upscale_models/
    controlnet: controlnet/
```

### 6. Endpoint URL Correction

**Wrong (assumed):** `https://comfyume-vca-ftv-h200-spot.containers.verda.com`
**Correct (actual):** `https://containers.datacrunch.io/comfyume-vca-ftv-h200-spot`

Updated in `.env`.

---

## Current Issue: 404 on Serverless Endpoint

**Problem:** All requests to `https://containers.datacrunch.io/comfyume-vca-ftv-h200-spot/` return 404.

**Likely Cause:** Health check path `/system_stats` is wrong.

**Fix Required:** Change health check path in Verda console to:
- `/api/system_stats` OR
- `/` (root - ComfyUI serves HTML there)

**Alternative:** Container may be scaled to 0 and health check fails on startup.

---

## Next Steps

1. **Fix health check path** in Verda console: `/system_stats` → `/api/system_stats` or `/`
2. **Restart deployment** after health check fix
3. **Test endpoint** with curl or browser
4. **Update mello** queue-manager to use serverless:
   ```bash
   ./scripts/switch-gpu.sh h200-spot
   docker compose restart queue-manager
   ```
5. **Create remaining deployments:**
   - comfyume-vca-ftv-h200-on-demand
   - comfyume-vca-ftv-b300-spot
   - comfyume-vca-ftv-b300-on-demand

---

## How to Switch GPU Modes

```bash
# Check current mode
./scripts/switch-gpu.sh status

# Switch to different modes
./scripts/switch-gpu.sh h200-spot       # Workshop (cheapest)
./scripts/switch-gpu.sh h200-on-demand  # Demos (guaranteed)
./scripts/switch-gpu.sh b300-spot       # 4K cheap
./scripts/switch-gpu.sh b300-on-demand  # 4K premium
./scripts/switch-gpu.sh local           # Local/Redis workers

# Apply change
docker compose restart queue-manager
```

---

## Files to Reference

- **Switch script:** `scripts/switch-gpu.sh`
- **Env configs:** `h200-spot.env`, `h200-on-demand.env`, `b300-spot.env`, `b300-on-demand.env`
- **Main config:** `.env` (SERVERLESS_* variables)
- **SFS config:** `/mnt/sfs/extra_model_paths.yaml`
- **GitHub Issue:** #62 (Implement Serverless Inference Mode Switch)

---

## Important Notes

1. **Serverless containers are separate from Verda instance** - The RTX 6000 Ada instance (verda) runs independently
2. **Models on SFS** - All models at `/mnt/sfs/models/shared/` are accessible to both instance and serverless
3. **Flux workflows need special loaders** - Use UNETLoader + DualCLIPLoader + VAELoader (not CheckpointLoaderSimple)
4. **Cold start ~1-2 min** - First request after scale-to-zero takes time

---

**Last Updated:** 2026-02-03 16:30 UTC
