**Project:** ComfyUI Multi-User Workshop Platform
**Project Started:** 2026-01-02
**Repository:** github.com/ahelme/comfyume
**Domain:** comfy.ahelme.net
**Doc Created:** 2026-01-02
**Doc Updated:** 2026-02-01 (v0.11.0 clean rebuild - comfyume repo)

---

## ⚠️  CRITICAL INSTRUCTIONS - YOU MUST:

1. **MUTUAL RESPECT - BELIEVE THE USER**
   - When the user reports something isn't working, **BELIEVE THEM**
   - Do not dismiss user reports with "try cache refresh" or "works for me"
   - Investigate the actual problem they're describing
   - Ask for error messages/details, then act on that information
   - The user takes your suggestions seriously - reciprocate that respect
   - Repeating "it's working" when told it isn't is dismissive and wastes time

2. **USE LATEST STABLE LIBRARIES AS OF JAN 2026**

3. **ALWAYS CHECK IF CODE HAS BEEN CREATED FIRST**
   - **NEVER EVER** REWRITE CODE IF IT HAS ALREADY BEEN WRITTEN
   - **ALWAYS CHECK** FOR PREVIOUS SOLUTIONS
  
   - WHY? We just spent A WHOLE WEEK DEALING WITH OLD COMFYUI 0.8.1 BEING INSTALLED BEFORE THE APP WAS ARCHITECTED !!!
   - (user requested "latest" - got "ancient")
   - **A NIGHTMARE.**
   - WE MAY MISS OUR DEADLINE!!!
   - PLEASE, NO MORE!!!

---

## 🚨 TESTING WITH BOSS TODAY - MUST GET WORKING!

**Timeline:** Boss testing in ~3 hours (2026-02-02)
**Status:** ✅ Models ready on SFS (77GB + 8.8GB gemma), ✅ R2 backup complete (98GB), 🔄 Provisioning RTX 6000 ADA

### Selected Templates for Workshop

**Template 1: Flux Klein 9B - Text to Image**
- File: `flux2_klein_9b_text_to_image.json`
- Use case: High-quality image generation
- VRAM: ~12-16GB

**Template 4: LTX-2 Distilled - Text to Video**
- File: `ltx2_text_to_video_distilled.json`
- Use case: Fast video generation (distilled = faster than standard)
- VRAM: ~20-25GB

### GPU Choice: RTX 6000 ADA (48GB VRAM)

**Why RTX 6000 ADA:**
- Cost: €0.7020/hour = **~$28 AUD for 24 hours**
- VRAM: 48GB (handles both templates with headroom)
- vs A100: Save ~$20 AUD per day
- L40S not available, RTX 6000 ADA similar specs/price

**Verda Provisioning:**
- Instance type: RTX 6000 ADA 48GB (on-demand, no spot available)
- Duration: 24 hours (for boss test + safety margin)
- SFS: Mount existing `/mnt/sfs` (models already there - 77GB models + 8.8GB gemma downloaded)

### Required Models (EXACT MATCHES)

**Flux Klein 9B:**
```
diffusion_models/flux-2-klein-9b-fp8.safetensors
https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/diffusion_models/flux-2-klein-9b-fp8.safetensors

text_encoders/qwen_3_8b_fp8mixed.safetensors (8.07 GB)
https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors

vae/flux2-vae.safetensors (320 MB)
https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors
```

**LTX-2 Distilled:**
```
checkpoints/ltx-2-19b-dev-fp8.safetensors (27 GB) - downloading to SFS
text_encoders/gemma_3_12B_it.safetensors (20 GB)
loras/ltx-2-19b-distilled-lora-384.safetensors
latent_upscale_models/ltx-2-spatial-upscaler-x2-1.0.safetensors
```

### Success Criteria
- ✅ Both templates load in ComfyUI
- ✅ Flux Klein generates image in <30 seconds
- ✅ LTX-2 Distilled generates video in 1-2 minutes
- ✅ Boss sees working demo
- ✅ No model loading errors

---

## 📬 **PARALLEL DEV TEAMS** 

**Two Teams Were Recently Working in Parallel:**
- **Mello Team** - Frontend, extensions, workflows
- **Verda Team** - Worker, GPU, VRAM monitoring

**Collab via Issue on Main Repository:** `comfyume` 
- (https://github.com/ahelme/comfyume) - v0.11.0 clean rebuild
**Main Branch:** `main` (unified codebase)
- **Master task list: Issue #1**
- **Team Coordination: Issue #7** ⚠️ CHECK LIKE EMAIL!
  - Both teams post questions, clarifications, decisions
  - While in parallel dev - don't proceed with conflicting work without coordination
---

## 🎯 Project Quick Reference

### What are we building?
- A multi-user ComfyUI platform for video generation workshops.
- Optimised for cost savings:
  - App hosted separately on Hetzner VPS. 
  - Inference via a Remote GPU Cloud provider (e.g. Verda, RunPod, etc.)
  - Storage of models, user files, config, worker etc. on cheap Cloudflare R2.
- Workshop participants/end-users are professional filmmakers.

### Key Requirements
- split architecture - two servers one for CPU, one for GPU
- 20 isolated ComfyUI web interfaces 
- Central job queue (FIFO/round-robin/priority)
- 1-3 GPU workers on H100 OR serverless containers 
- HTTPS with existing ahelme.net SSL cert
- HTTP Basic Auth password protection 
- Tailscale VPN for secure Redis connection 
- Persistent user storage 
- Admin dashboard for instructor 
- Real-time health monitoring 
- Comprehensive backup routines (scripts on private repo)

### Quick Links
- **Production:** https://comfy.ahelme.net/
- **Health Check:** https://comfy.ahelme.net/health
- **Admin Dashboard:** https://comfy.ahelme.net/admin
- **API:** https://comfy.ahelme.net/api/queue/status

---

## 📁 Project Structure

```
/home/dev/comfyume/
├── implementation-deployment-verda.md  # Implementation plan for deployment phases
├── progress-**.md                      # Recent session logs (UPDATE ON COMMITS)
├── CLAUDE.md                           # This file - project guide
├── README.md                           # Public project documentation
├── .env                                # Local configuration (gitignored - ⚠️ FULL OF SECRETS!!!)
├── .env.example                        # Template configuration
├── docker-compose.yml                  # Main orchestration (includes docker-compose.users.yml)
├── docker-compose.users.yml            # ⚠️ 20 USER CONTAINERS - per-user isolation (auto-generated)
├── nginx/                              # Reverse proxy
├── queue-manager/                      # FastAPI service
├── comfyui-worker/                     # GPU worker
├── comfyui-frontend/                   # User UI container base (builds 20 per-user images)
├── admin/                              # Admin dashboard
├── scripts/
│   ├── generate-user-compose.sh        # ⚠️ Regenerates docker-compose.users.yml
│   ├── start.sh                        # Start all services
│   └── stop.sh                         # Stop all services
├── data/
│   ├── user_data/                      # Per-user persistent data (backed up to R2)
│   │   ├── user001/
│   │   │   ├── comfyui.db              # User settings database
│   │   │   ├── default/                # User preferences
│   │   │   └── comfyui/
│   │   │       └── custom_nodes/       # User-installed custom nodes (mounted per-user)
│   │   │           ├── ComfyUI-Manager/
│   │   │           └── my-custom-node/
│   │   │       └── ⚠️ WHERE ARE USER-SAVED WORKFLOWS???⚠️ - <-info needs adding !!!
│   │   ├── user002/
│   │   │   └── ... (same structure)
│   │   └── ... (user003-user020)
│   ├── workflows/                      # Shared template workflows (read-only to all users)
│   │   ├── flux2_klein_9b_text_to_image.json
│   │   ├── flux2_klein_4b_text_to_image.json
│   │   ├── ltx2_text_to_video.json
│   │   ├── ltx2_text_to_video_distilled.json
│   │   └── example_workflow.json
│   ├── models/
│   │   ├── shared/                     # Shared models (empty on mello, populated on Verda SFS)
│   │   │   ├── checkpoints/
│   │   │   ├── text_encoders/
│   │   │   ├── loras/
│   │   │   ├── vae/
│   │   │   └── latent_upscale_models/
│   │   └── user/                       # User-specific models (future)
│   ├── inputs/                         # User uploads (⚠️ symlinked to Verda block storage - EPHEMERAL)
│   │   ├── user001/
│   │   ├── user002/
│   │   └── ... (user003-user020)
│   └── outputs/                        # User outputs (⚠️ symlinked to Verda block storage - EPHEMERAL)
│       ├── user001/
│       ├── user002/
│       └── ... (user003-user020)
└── docs/                               # User/admin guides

/home/dev/projects/comfymulti-scripts/  # ⚠️ PRIVATE REPO FOR SCRIPTS & SECRETS ⚠️
├── .env                           # ⚠️ <- HOW SECRET/PRIVATE .env IS SHARED BETWEEN DEVS ⚠️
├── README-RESTORE.md              # Basic backup/restore doc (may need updating since comfy-multi > comfyume
├── setup-verda-solo-script.sh     # Single consolidated setup/restore script
├── backup-cron.sh                 # Hourly backups: Verda→SFS + triggers mello→R2
├── backup-mello.sh                # Backs up user files on mello e.g. workflows
├── backup-verda.sh                # Backs up all data to R2 before instance deleted
└── archive/                       # Legacy scripts (quick-start.sh, RESTORE-SFS.sh) 
```

---
## Project Management

### 📋 Progress Tracking
- [MELLO TEAM's Progress Log](.claude/progress-mello-dev.md) - Mello's Session log
- [VERDA TEAM's Progress Log](.claude/progress-verda-dev.md) - Verda's Session log
    - ==MUST UPDATE ON COMMIT OF CODE CHANGES==

### 📋 Issue Tracking
- **ComfyuME Project**: https://github.com/ahelme/comfyume/issues
- **Private Scripts Repo**: https://github.com/ahelme/comfymulti-scripts/issues

### 📋 Task Management
- **ALWAYS reference GitHub issue numbers** (e.g., #15, #22, #13)
- **DO NOT use internal task numbers** (no Task #1, Task #2, etc.)
- **If no GitHub issue exists**, create one first before tracking work
- See top section of [.claude/progress-mello-dev.md](.claude/progress-mello-dev.md) / [.claude/progress-verda-dev.md](.claude/progress-verda-dev.md) for comprehensive task instructions

### 📋 Implementation Plan (Phases)

- [Current Implementation Plan: Deploy/Backup/Restore](./implementation-backup-restore.md)
    - IMPLEMENTATION PLANS MUST BE CONCISE! DETAILS CHANGE!    
    - **NO CODE SNIPPETS !**
    - Replace detail with SIMPLE steps 
    - Provide POINTERS to single source of truth (docs)
    - ==UPDATE AS PLAN CHANGES==

---

## 📚 Document Links

### Core Documents
- [README.md](./README.md) - Public code project overview and dev quickstart
- [Progress Log](./progress-**.md) - Session logs
- [Admin Guide](.docs/admin-guide.md) - Admin docs index / overview
- [Deploy/Backup Guide](.docs/admin-backup-restore.md) - Docs: deploy/restore/backups
- [GPU Deployment](./implementation-backup-restore.md) - Plan: deploy/restore/backup

### User Documentation 
- **docs/archive/user-guide.md** - For workshop participants (MAY need update)
- **docs/admin-guide.md** - For developer/maintainer/instructor
- **docs/archive/troubleshooting.md** - Common issues (will need update)

### Documentation Format

Ensure these details are listed the top of ALL .md documentation files:

[example]

**Project Name:** ComfyuME
**Project Desc:** ComfyUI Multi-User Workshop Platform
**Project Started:** 2026-01-02
**Repository:** github.com/ahelme/comfyume
**Domain:** comfy.ahelme.net
**Doc Created:** 2026-01-02
**Doc Updated:** 2026-02-01

==IMPORTANT: Docs MUST be comprehensive yet NO FLUFF== 

==NO extraneous info / hasty "FINAL!" pronouncements / "SUCCESS!" "PRODUCTION-READY" boasting==

---

## 🔄 Update Progress on Commit: Instructions

### At EVERY GIT COMMIT update `.claude/progress-mello-dev.md` OR `.claude/progress-verda-dev.md`:

   1. **PRIORITY TASKS:**
      - What to do next
   2. **PROGRESS REPORT**
      - What was done
      - NO BOASTING!!

---

## 🏗️ Architecture Overview

```
  Split Server Architecture:
  ┌─────────────────────────────────────────┐
  │ Hetzner VPS (comfy.ahelme.net)          │
  │  - Nginx (HTTPS, SSL)                   │
  │  - Redis (job queue)                    │
  │  - Queue Manager (FastAPI)              │
  │  - Admin Dashboard                      │
  │  - User Frontends x20 (UI only)         │
  └──────────────┬──────────────────────────┘
                 │ Network
                 │ (Redis connection)
  ┌──────────────▼──────────────────────────┐
  │ Remote GPU (Verda) instance/serverless  │
  │  - Worker 1 (ComfyUI + GPU)             │
  │  - Worker 2 (ComfyUI + GPU) [optional]  │
  │  - Worker 3 (ComfyUI + GPU) [optional]  │
  │                                         │
  │  REDIS_HOST=comfy.ahelme.net            │
  └─────────────────────────────────────────┘

Code Architecture:

[User Browser]
    ↓ HTTPS
[Nginx :443] → SSL termination, routing
    ├─→ /user001-020/ → Frontend containers
    ├─→ /api → Queue Manager
    └─→ /admin → Admin Dashboard

[Queue Manager :3000] ← FastAPI + WebSocket
    ↓ Redis
[Job Queue] ← Redis list + pub/sub
    ↓
[ComfyUI Workers :8188-8190] ← GPU processing
    ↓
[Shared Volumes] ← models, outputs, workflows
```

---

## 🚀 Git Workflow

### Repository
- **Platform:** GitHub
- **URL:** https://github.com/ahelme/comfyume
- **Branch Strategy:**
  - `main` - production-ready code
  - Feature branches as needed (mello-track-2, verda-track-2)
- **Scripts Repo** (PRIVATE!) https://github.com/ahelme/comfymulti-scripts

### Commit Guidelines
```bash
# Good commit messages
feat: add queue manager REST API endpoints
fix: resolve nginx routing for user/20
docs: update admin guide with priority override
test: add integration tests for worker

NO (you guessed it) BOASTING!!!
```

### When to Commit
- End of each major feature
- Before trying risky changes
- End of each session
- When tests pass
- ==REMEMBER: UPDATE `.claude/progress-mello-dev.md` OR `.claude/progress-verda-dev.md` after commits!==
---

## 🛠️ Technology Stack

### Development & Production Servers
- **'mello' (dev & app server)**: Hetzner VPS CAX31 - Ubuntu
  - Ampere® 8 vCPU, 16GB RAM, 80GB SSD
  - €12.49/month
  - Runs: app frontends, queue-manager, Redis, nginx
- **'verda' (inference server)**: GPU cloud (renewable energy & EU policy)
  - Rented GPU instance OR serverless containers
  - Runs: ComfyUI workers with GPU
- **Local dev machine**: MBP M4 Pro 48GB RAM

### Backups
- **cloud storage**: Cloudflare R2 ( .eu ) - 3x buckets (v. cheap)
- **local storage**: 'verda' SFS (network drive) & block storage + 'mello'

### Infrastructure
- **Container Runtime:** Docker + Docker Compose
- **Reverse Proxy:** Nginx (SSL termination, routing)
- **Queue:** Redis 7+ (job queue, pub/sub)
- **SSL:** Existing ahelme.net certificate via Namecheap

### Services
- **Queue Manager:** Python 3.11+ with FastAPI + WebSocket
- **Workers:** ComfyUI v0.11.0 with GPU support
- **Frontends:** ComfyUI v0.11.0 web UI (COMFYUI_MODE=frontend-testing)
- **Admin:** HTML/JS dashboard

### Deployment
- **Development:** Docker Compose locally (Hetzner VPS)
- **Production:** Hetzner VPS + Remote GPU (e.g. Verda) instance/serverless

### Workshop Models

**Primary Video Generation Model:**
- **LTX-2** (19B parameters) - State-of-the-art open-source video generation
  - Checkpoint: `ltx-2-19b-dev-fp8.safetensors` (checkpoints/)
  - Text Encoder: `gemma_3_12B_it.safetensors` (text_encoders/)
  - Upscaler: `ltx-2-spatial-upscaler-x2-1.0.safetensors` (latent_upscale_models/)
  - LoRAs:
    - `ltx-2-19b-distilled-lora-384.safetensors`
    - `ltx-2-19b-lora-camera-control-dolly-left.safetensors`

**Required ComfyUI Nodes:**
- **Core v0.7.0+:** `LTXAVTextEncoderLoader`, `LTXVAudioVAEDecode`
- **Core v0.3.68+:** `LTXVAudioVAELoader`, `LTXVEmptyLatentAudio`

**Model Sources:**
- HuggingFace: `Lightricks/LTX-2`
- HuggingFace: `Comfy-Org/ltx-2`

**NEW: ADDED IMAGE MODEL**
- **Flux.2 Klein**

---

## ⚙️ Configuration

### Environment Variables
See .env

---

## 📋 Critical Files and Locations                                          

 mello: File/Directory                              │ Purpose
  ──────────────────────────────────────────────────┼───────────────────────────────────────
  .env                                              │ Configuration (passwords, domain, etc.)
  docker-compose.yml                                │ Container orchestration
  /etc/ssl/certs/fullchain.pem                      │ SSL public certificate
  /etc/ssl/private/privkey.pem                      │ SSL private key
  scripts/status.sh                                 │ System health check script
  scripts/start.sh                                  │ Start all services
  scripts/stop.sh                                   │ Stop all services

  ~/comfymulti-scripts/                       │ Backup/Restore/Deploy scripts for Verda GPU Cloud
  ~/comfymulti-scripts/setup-verda-solo-script.sh │ Single setup/restore script for Verda
  ~/comfymulti-scripts/README-RESTORE.md      │ README for restoring Verda

 *(NOTE: restore scripts have their own private gh repo: https://github.com/ahelme/comfymulti-scripts)*

  docs/admin-backup-restore.md                      │ Full docs for deploy/backup/restore

 verda: Storage                                     │ Purpose
  ──────────────────────────────────────────────────┼────────────────────────────────────────
  BlockStorage (OS)                                 │ Instance operating system & worker
  BlockStorage (scratch)                            │ Ephemeral: user inputs/outputs
  SFS (network drive)                               │ Persistent: models, cache, backups
---

## Portainer - container monitoring & management
- uses Tailscale Tailnet - verda, mello, aeon (Mac)
- can see containers across app
- monitor resource consumption
- restart containers
- if GPU is ticked on Verda's Portainer config - we can manage NVIDIA GPU resources

---

## 🔒 Security & Firewall Configuration

### VPS Firewall (UFW)
Current firewall rules lock down all ports except essential services:

```bash
sudo ufw status
```

**Allowed Ports:**
- **22/tcp** - SSH (rate limited)
- **80/tcp, 443/tcp** - HTTP/HTTPS (Nginx Full)
- **Mello only: 21115-21119/tcp** - RustDesk remote desktop
- **Mello only: 21116/udp** - RustDesk UDP

**Redis Security:**
- **Port 6379** - NOT exposed to public internet
- **Access:** Only via Tailscale VPN (100.99.216.71:6379)
- **Auth:** Password protected (REDIS_PASSWORD)

### User Authentication
- **Method:** HTTP Basic Auth (nginx)
- **Users:** 20 users (user001-user020)
- **Credentials:** Stored in `.env` (USER_CREDENTIALS_USER001-020)
- **htpasswd File:** `/etc/nginx/comfyui-users.htpasswd`
- **Encryption:** bcrypt (cost 10)

### Tailscale VPN
- **VPS Tailscale IP:** 100.99.216.71
- **GPU (Verda) Tailscale IP:** 100.89.38.43
- **Purpose:** Secure encrypted tunnel for Redis access between VPS and GPU workers
- **Protocol:** WireGuard (modern, fast, secure)
- **Authentication:** Run `sudo tailscale up --ssh=false`, visit the URL shown in browser to authenticate
- **Note:** Use `--ssh=false` to disable Tailscale SSH (we use regular SSH)

### SSL/TLS
- **Provider:** Existing ahelme.net certificate
- **Domain:** comfy.ahelme.net
- **Expiry:** 2026-04-10
- **Protocols:** TLSv1.2, TLSv1.3

### Cloudflare R2 Buckets
- **Provider:** Cloudflare R2 (S3-compatible)
- **Endpoint:** `https://f1d627b48ef7a4f687d6ac469c8f1dea.r2.cloudflarestorage.com.eu`
- **Cost:** ~$3/month total (no egress fees)
- **Access:** Via AWS CLI with R2 API credentials

**Current .eu R2 Buckets (comfyume v0.11.0):**
- `comfyume-model-vault-backups` - Models (~45GB, EU)
- `comfyume-cache-backups` - Container + configs (~3GB, EU)
- `comfyume-user-files-backups` - User data from mello (~1GB, EU)
- `comfyume-worker-container-backups` - Worker images (~2.5GB, EU)

**Legacy Archive Buckets (KEEP - comfy-multi v0.9.2):**
- `comfy-multi-model-vault-backup` - Models archive
- `comfy-multi-cache` - Cache archive
- `comfy-multi-user-files` - User files archive

### Restore Scripts (Private GitHub Repo)
- **Repo:** `ahelme/comfymulti-scripts` (private)
- **URL:** https://github.com/ahelme/comfymulti-scripts
- **Local path on mello:** `/home/dev/comfymulti-scripts/`
- **Purpose:** Version-controlled setup/restore scripts for Verda instances
- **Contents:**
  - `setup-verda-solo-script.sh` - Single consolidated setup/restore script
  - `backup-cron.sh`, `backup-mello.sh`, `backup-verda.sh` - Backup scripts
  - `README-RESTORE.md` - Quick reference for restore scenarios
  - `archive/` - Legacy scripts (quick-start.sh, RESTORE-SFS.sh, etc.)
- **Note:** Script downloads binary files (models, container) from R2 or SFS cache

---

## ⚠️  Gotchas

### Issue #54 RESOLVED: Workflow Save/Load Now Working

**Issue #54: Workflow save/load was broken** - POST to userdata API returned 405 through nginx

**Root Cause:** nginx `proxy_pass` with trailing slash (`http://backend/;`) decodes URL-encoded characters. ComfyUI requires encoded slashes (`%2F`) in path parameters like `/userdata/workflows%2Ffile.json`.

**Fix Applied (2026-02-05):**
1. Created `/etc/nginx/conf.d/comfyui-userdata-maps.conf` with maps that extract paths from `$request_uri` (preserves encoding)
2. Updated all user location blocks to use `proxy_pass http://backend$userXXX_raw_path$is_args$args;`

**Reference:** [ComfyUI PR #6376](https://github.com/comfyanonymous/ComfyUI/pull/6376)

**Files:**
- `/etc/nginx/conf.d/comfyui-userdata-maps.conf` - Map definitions (live server)
- `nginx/conf.d/comfyui-userdata-maps.conf` - Map definitions (repo)
- `nginx/docker-entrypoint.sh` - Updated to generate maps for containerized nginx

### CRITICAL: Worker Container Infinite Restart Loop

**Symptom:** Worker container restarts every 30 seconds with "ComfyUI failed to start" error.

**Root Cause:**
- Original startup script uses `curl` for health checks
- `curl` not installed in worker container
- Health check always fails → script exits → container restarts

**Fix:** Remove curl-based health check, use simple sleep:
```bash
# /workspace/start-worker.sh (simplified version)
#!/bin/bash
echo "Starting ComfyUI Worker: $WORKER_ID"
cd /workspace/ComfyUI
python3 main.py --listen 0.0.0.0 --port 8188 &
COMFYUI_PID=$!
sleep 60  # Simple wait instead of curl check
cd /workspace
python3 worker.py
kill $COMFYUI_PID 2>/dev/null || true
```

**To apply fix on running container:**
```bash
# Create fixed script
cat > /tmp/start-simple.sh << 'EOF'
#!/bin/bash
echo "Starting ComfyUI Worker: $WORKER_ID"
cd /workspace/ComfyUI
python3 main.py --listen 0.0.0.0 --port 8188 &
sleep 60
cd /workspace && python3 worker.py
EOF
chmod +x /tmp/start-simple.sh

# Copy to stopped container (preserves permissions)
docker stop comfy-worker-1
docker cp /tmp/start-simple.sh comfy-worker-1:/workspace/start-worker.sh
docker start comfy-worker-1
```

**Success indicators:**
- Worker logs show "Worker worker-1 started"
- Polling queue manager every 2s
- HTTP 200 OK responses from queue manager

### .eu domain for R2 Buckets
- connection / uploads can fail and not know why

### CRITICAL: Server Unresponsive Emergency Fix
**If server stops responding (20x user containers overwhelm resources:**
1. Hard Reset the server via hosting provider dashboard
2. SSH in ASAP after reboot
3. Run: `sudo docker stop $(sudo docker ps -q --filter "name=comfy")`

This stops all ComfyUI containers to prevent resource exhaustion on startup.

### Disk Space Monitoring: disk-check.sh
Run `disk-check.sh` before builds/backups. Use `--block` to abort if >90% full. Auto-runs (blocking) in: start.sh, build.sh, backup scripts, setup-verda-solo-script.sh.

### CRITICAL: Silent Failures on Large File Operations

**Why this matters:** Operations report success while actually failing. Hours wasted redownloading, deploying apps that won't work, discovering missing data at critical moments.

**Root causes:**
- **Disk space issues**: /tmp full → silent failure
- **Silent failures**: AWS CLI returns success even when operations fail
- **Incomplete backups**: Assumed complete, weren't verified
- **Lack of verification**: No immediate check of results after operations

**How to avoid:**
1. **Check disk space FIRST**:
   ```bash
   df -h /tmp /mnt/sfs  # before any large operation
   ```

2. **Use adequate temp space**:
   ```bash
   TMPDIR=/mnt/sfs/tmp  # for large downloads
   ```

3. **Verify immediately after operations**:
   ```bash
   # After sync/download
   find /target -type f | wc -l  # file count
   du -sh /target                # total size
   ```

4. **Compare source vs destination**:
   ```bash
   aws s3 ls --recursive | wc -l  # source count
   find /local -type f | wc -l     # dest count
   ```

5. **Use checksums**: Generate md5sums for all files and verify

6. **Manifest-driven operations**: Create expected file list FIRST, then verify against it

7. **Explicit verification in scripts**: Don't trust exit codes alone - check actual results

### Docker Image Architecture (IMPORTANT!)

**Single Shared Image for All Users:**
- All 20 users use `comfyume-frontend:v0.11.0` (NOT per-user images)
- `docker-compose.users.yml` uses `image:` not `build:` (regenerated by `scripts/generate-user-compose.sh`)
- Old per-user images from v0.9.2 are stale - delete if found
- **If containers use wrong image:** Stop containers, delete old images, recreate

**Custom Nodes Volume Mount Gotcha:**
- Custom nodes volume-mounted per user: `./data/user_data/userXXX/comfyui/custom_nodes:/comfyui/custom_nodes`
- **Volume mount OVERWRITES image contents!** Empty host directory = empty container directory
- **Solution:** Copy default custom nodes from `comfyui-frontend/custom_nodes/` to each user's directory
- Required nodes: `default_workflow_loader` (Flux2 Klein auto-load), `queue_redirect` (job submission)

### Health Checks Require Dependencies

**Dockerfile must include:**
- `curl` - Health check uses `CMD ["curl", "-f", "http://localhost:8188/"]`
- `libgomp1` - Required for torchaudio (audio nodes), prevents libgomp.so.1 errors
- `requests` (Python) - Required by frontend (added to requirements.txt in v0.11.0)

**Symptoms if missing:**
- No curl: Health checks timeout after 60s, containers marked unhealthy
- No libgomp1: Audio nodes import errors (non-fatal but noisy logs)
- No requests: `ModuleNotFoundError: No module named 'requests'` on startup

### Batched Startup Architecture

**Dependency Chain:**
1. Queue Manager must be healthy FIRST
2. Then 4 batch leaders start in parallel: user001, user006, user011, user016 (each depends on queue-manager)
3. Within each batch: sequential with health checks (user002 depends on user001, etc.)
4. Total time: ~1-2 minutes for 5 users, ~2-3 minutes estimated for 20 users

**Commands (Mello - App Server):**
- Start: `docker compose up -d` (includes docker-compose.users.yml automatically)
- Set auto-restart: `docker update --restart=unless-stopped $(docker ps -q --filter "name=comfy")` (survives reboots)
- Regenerate: `./scripts/generate-user-compose.sh` (updates docker-compose.users.yml)

**Commands (Verda - Worker):**
- Start worker: `cd ~/comfyume/comfyui-worker/ && sudo docker compose up -d worker-1`
- Check logs: `sudo docker logs comfy-worker-1 -f` (container name, not image name)
- Set auto-restart: `sudo docker update --restart=unless-stopped $(sudo docker ps -q --filter "name=comfy")` (survives reboots)
- Check Redis: `redis-cli -h 100.99.216.71 -p 6379 -a $REDIS_PASSWORD ping`

### ComfyUI v0.11.0 Workflow Storage (CRITICAL!)

**Workflow Location:**
- Workflows MUST be in: `/comfyui/user/default/workflows/`
- Served via ComfyUI's userdata API: `/api/userdata?dir=workflows`

**How It Works:**
- docker-entrypoint.sh copies workflows from `/workflows` volume to `/comfyui/user/default/workflows/`
- Runs on every container startup
- All 5 template workflows (Flux2 Klein, LTX-2) appear in Load menu automatically

**Symptoms if wrong:**
- Workflows folder empty in ComfyUI Load menu
- Browser console errors: `404 /api/userdata?dir=workflows`

### Cloudflare R2 EU location
- don't forget the '.eu' domain!

### Verda Storage Options

**Recommended: Shared File System (SFS)** - €0.01168/h for 50GB (~$14 AUD/month)
- Network-attached (NFS), mount from any instance
- No provisioning gotchas - just mount and go
- Multiple instances can share same storage
- Mount: `mount -t nfs <sfs-endpoint>:/share /mnt/sfs`
- Structure: `/mnt/sfs/models/` (ComfyUI models), `/mnt/sfs/cache/` (container, config, scripts)

**Alternative: Block Storage** - Cheaper but riskier
- ⚠️ **CRITICAL: Gets WIPED if attached during instance provisioning!**
- Must use shutdown-attach-boot workflow for existing data
- Only one instance can use it at a time
- Good for scratch disk

### Block Storage Safe Workflow (if using)

1. Create instance **WITHOUT** block storage attached
2. Boot the instance
3. **Shut down** the instance (required for attachment)
4. Attach block storage via Verda Dashboard
5. Boot instance again
6. Mount the volume: `mount /dev/vdc /mnt/models`

**Volume naming convention:**
- `OS-*` = OS disks (will have Ubuntu installed)
- `Volume-*` = Data volumes (your actual block storage)

### Other Verda Notes
- Verda images have Docker pre-installed (don't try to install docker.io - conflicts with containerd)
- Ubuntu 24.04 uses `ssh` service name, not `sshd`
- Spot instances can be terminated anytime - always use persistent storage (SFS or Block)

---

## 🔗 External Links

### Research References
- [Visionatrix Discussion](https://github.com/comfyanonymous/ComfyUI/discussions/3569) - Multi-user architecture
- [SaladTechnologies/comfyui-api](https://github.com/SaladTechnologies/comfyui-api) - Queue patterns
- [Modal ComfyUI Scaling](https://modal.com/blog/scaling-comfyui) - Architecture insights
- [9elements ComfyUI API](https://9elements.com/blog/hosting-a-comfyui-workflow-via-api/) - Workflow execution

### Deployment Targets
- [Verda Products](https://verda.com/products) - Instance types
- [Verda Containers](https://verda.com/serverless-containers) - Serverless options - dynamic scaling
- [Verda Instances](https://docs.verda.com/cpu-and-gpu-instances/set-up-a-gpu-instance) - Setup an instance
- [Verda Serverless Containers](https://docs.verda.com/containers/overview) - Setup a container 

### ComfyUI Resources
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [ComfyUI Wiki](https://comfyui-wiki.com/)
- [ComfyUI API Docs](https://github.com/comfyanonymous/ComfyUI/discussions/2073)

---

## 🎓 Context for Claude

1. **Existing SSL cert** via Namecheap mounted (not Let's Encrypt)
2. **Queue modes:** FIFO + round-robin + instructor priority
3. **Test with Single H100 Instance** with 1-3 workers (test then scale)
4. **Then try Serverless Containers** for price/performance
5. **Persistent storage** for all user data
6. **User model uploads** allowed

### User Preferences
- Appreciates thoroughness and detail
- Values comprehensive and accurate documentation
- Wants progress tracking (hence `progress-**.md`)
- Likes structured approaches
- Hates BOASTING in DOCS, COMMITS, GH ISSUES, GH COMMENTS
- Why? MASSIVE waste of context & fills up brain with crap.
==EXPRESS PRIDE TO **USER** in chat NOT DOCS/GITHUB!!==

## Deployment

### SSH Keys for Verda

**During Verda provisioning, add BOTH public keys via Verda console:**

1. **User's Mac key** - for manual SSH access
2. **Mello VPS key** - for mello to SSH into Verda

```
# Mello VPS public key (MUST ADD):
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGiwaT6NQcHe7cYDKB5LrtmyIU0O8iRc7DJUmZJsNkDD dev@vps-for-verda
```

**Why this matters for restore scripts:**
- Mac can SSH into Verda ✓ (Mac has private key)
- Mello can SSH into Verda ✓ (Mello has private key)
- Verda CANNOT pull from mello ✗ (Verda has no private key for mello until setup script finishes)

### Restore scripts are adaptive

**Core Restore Workflow:** Restore scripts first check SFS (fast, for workshop month), then fall back to remote:
- **SFS** - First choice (files cached from previous session)
- **R2** - Binary files (models, container image, config tarball)
- **GitHub** - Scripts (`ahelme/comfymulti-scripts` private repo)

### Critical Principles

**1. Check Before Downloading/Restoring (Scripts Check in This Order)**

| File Type                       | Check Order           | Rationale             |
|---------------------------------|-----------------------|-----------------------|
| **Models** (~45GB)              | SFS → R2              | Large, live on SFS    |
| **Config, identity, container** | /root/ → SFS → R2     | Extracted to instance |
| **Scripts**                     | /root/ → SFS → GitHub | Small, versioned      |

**2. Tailscale Identity Must Be Restored BEFORE Starting Tailscale**

If Tailscale starts without the backed-up identity, it gets a **NEW IP address**.
The restore scripts restore `/var/lib/tailscale/` BEFORE running `tailscale up`.
This preserves the expected IP: **100.89.38.43**

### Deployment Prerequisites Checklist

Before starting, verify:
- [ ] mello VPS is running (comfy.ahelme.net)
- [ ] R2: **Models bucket** (`comfyume-model-vault-backups`) contains:
  - [ ] `checkpoints/*.safetensors` (~25-50 GB)
  - [ ] `text_encoders/*.safetensors` (~20 GB)
- [ ] R2: **Cache bucket** (`comfyume-cache-backups`) contains:
  - [ ] `worker-image.tar.gz` (~2.5 GB)
  - [ ] `verda-config-backup.tar.gz` (~14 MB)
- [ ] R2: **Worker container bucket** (`comfyume-worker-container-backups`)
- [ ] R2: **User files bucket** (`comfyume-user-files-backups`) - available to receive backups
- [ ] GitHub: **Private Scripts Repo** (`ahelme/comfymulti-scripts`) contains:
  - [ ] `setup-verda-solo-script.sh`
- [ ] User's Mac: **SSH Keys and Setup Script** added to Verda console during provisioning
  - [ ] `dev@vps-for-verda` (Mello's key) & `developer@annahelme.com` (User's key) - paste into console
  - [ ] `setup-verda-solo-script.sh` (latest version from GitHub!) - paste into console

### Step-by-Step Deployment Process

See [Admin Backup & Restore Guide](./docs/admin-backup-restore.md) for complete step-by-step instructions including:
- Provisioning SFS and GPU instance and block storage (scratch disk) on Verda
- Running setup-verda-solo-script.sh on Verda (runs automatically on first boot)
- Script downloads models from R2 (unless available on SFS already)
- Backup cron jobs are set up automatically by the script

### Deployment To-Dos for Claude (pre-populated)
- Copy these to TodoWrite when deploying: `.claude/DEPLOYMENT-TO-DO.md`

### Troubleshooting

See [Admin Backup & Restore Guide - Troubleshooting](./docs/admin-backup-restore.md#troubleshooting) for common issues and solutions.

---

## 📝 Session Checklist

Before each session ends:
- [ ] Commit & push code changes to git
- [ ] Update `progress-**.md` with session log
- [ ] Update admin/dev docs with key changes made (IMPORTANT!) - CLAUDE.md, README.md, linked dev / project docs
- [ ] Update current `implementation-*.md` when plan changes (push details to docs - single source of truth)
- [ ] Consider any changes made that are relevant to users - if any: scour `user-*.md` docs for details that need changing
- [ ] Note any blockers or decisions
- [ ] Clear next session goals

---

**Last Updated:** 2026-02-03 (AEST)
