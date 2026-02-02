# HANDOVER - Session Verda 03
**Date:** 2026-02-01
**Context:** Transition to comfyume repo as primary development focus
**Branch:** verda-track-2 (both comfyume and comfymulti-scripts repos)

---

## 🎯 Current Mission

**Primary Goal:** Deploy and test ComfyUI v0.11.0 worker on Verda H100 instance

**Status:**
- ✅ Worker v0.11.0 implementation complete (Issues #2-6)
- ✅ .env consolidation complete (v0.3.1)
- ⏳ Phase 3 cleanup tasks remaining (Issue #22)
- ⏳ Local container build testing pending
- ⏳ Verda deployment and integration testing pending

---

## 📂 Repository Structure

### Primary Repositories

**1. comfyume** (main development repo)
- **URL:** https://github.com/ahelme/comfyume
- **Purpose:** ComfyUI v0.11.0 GPU worker for Verda
- **Branch:** verda-track-2 (active development)
- **Location:** `/home/dev/comfyume/`

**Branch Structure:**
```
main           → Baseline (all work merged here via PR)
verda-track    → Previous work (Issues #2-6 complete, merged to main)
verda-track-2  → Current active development (Phase 3 + testing)
mello-track-2  → Mello Team's parallel work (frontend/services)
```

**2. comfymulti-scripts** (private - deployment scripts)
- **URL:** https://github.com/ahelme/comfymulti-scripts
- **Purpose:** Backup/restore/deployment scripts for Verda
- **Branch:** verda-track-2 (active development)
- **Location:** `/home/dev/comfymulti-scripts/`

**3. comfy-multi** (legacy - VPS frontend)
- **URL:** https://github.com/ahelme/comfy-multi
- **Purpose:** Mello VPS frontend/queue-manager (ongoing)
- **Branch:** main
- **Location:** `/home/dev/projects/comfyui/`
- **Note:** Still active for VPS services, but Verda work is in comfyume

---

## 🔄 What Changed in Session Verda 02

### 1. Worker v0.11.0 Implementation Complete
**Issues Resolved:** #2, #3, #4, #5, #6

**Components Delivered:**
- `comfyui-worker/Dockerfile` - CUDA 12.4, ComfyUI v0.11.0
- `comfyui-worker/worker.py` - Job processing with VRAM checks
- `comfyui-worker/vram_monitor.py` - GPU memory monitoring
- `comfyui-worker/docker-compose.yml` - Standalone deployment
- `comfyui-worker/test-deployment.sh` - Pre-deployment validation
- `comfyui-worker/README.md` - Complete documentation

**Key Features:**
- Pre-check GPU memory before accepting jobs
- Fail gracefully if insufficient VRAM
- Updated timeouts: 15 min (ComfyUI), 30 min (job)
- Health checks with curl, libgomp1 for audio nodes

### 2. .env Consolidation (v0.3.1)
**Source:** comfymulti-scripts repo main branch

**Key Changes:**
- `REDIS_HOST` → `APP_SERVER_REDIS_HOST` / `INFERENCE_SERVER_REDIS_HOST`
- R2 buckets: `comfy-multi-*` → `comfyume-*`
- Added: `PROJECT_NAME="comfyume"`
- Added: `SERVER_MODE=dual`, `USE_HOST_NGINX=true`
- Added: GitHub repo references, Tailscale IPs, SSH keys

**Impact:**
- Mello Team completed Phase 1 & 2 updates
- Phase 3 cleanup tasks remain (see Issue #22)

### 3. Deployment Scripts Updated
**Repository:** comfymulti-scripts (verda-scripts branch → main)

**Scripts Updated:**
- `setup-verda-solo-script.sh` - PROJECT_NAME="comfyume"
- `backup-cron.sh` - Updated paths
- `backup-verda.sh` - Updated paths and R2 buckets
- `.env` - Consolidated v0.3.1 with all secrets

**Commits:**
- `c2a7cd5` - Added PROJECT_NAME parameterization
- `2d529c1` - Hardcoded PROJECT_NAME to comfyume
- `b8e1aa8` - Updated backup scripts

---

## 📋 Current Tasks (Phase 3 - Issue #22)

### Remaining Work

**Task #1: Update create-gpu-quick-deploy.sh**
- File: `scripts/create-gpu-quick-deploy.sh`
- Change: REDIS_HOST → INFERENCE_SERVER_REDIS_HOST
- Verify: All env vars match consolidated .env v0.3.1

**Task #2: Update verda-startup-script.sh**
- File: `scripts/verda-startup-script.sh`
- Update: Comments and examples for new .env structure
- Update: Variable names in documentation

**Task #3: Documentation Updates**
- Files: README.md, comfyui-worker/README.md, guides
- Update: Environment variable references
- Add: .env v0.3.1 consolidation notes

---

## 🚀 Next Steps

### Immediate Priority: Local Container Build Testing

**Before deploying to Verda, test locally:**
1. Build worker container locally
2. Test with mock Redis connection
3. Verify VRAM monitoring works
4. Test health checks
5. Validate volume mounts

**Once local tests pass:**
6. Complete Phase 3 cleanup tasks
7. Commit and push to verda-track-2
8. Create PR: verda-track-2 → main
9. Deploy to Verda H100 instance
10. Run integration tests with live queue

---

## 🔧 Development Workflow

### Where to Commit

**comfyume repo (verda-track-2):**
- Worker code (Dockerfile, worker.py, vram_monitor.py)
- Test scripts (test-deployment.sh, test_vram_monitor.py)
- Documentation (README.md, guides)
- Issue #22 Phase 3 tasks

**comfymulti-scripts repo (verda-track-2):**
- Deployment scripts (setup-verda-solo-script.sh)
- Backup scripts (backup-*.sh)
- .env file (consolidated secrets)

**comfy-multi repo (avoid unless necessary):**
- Legacy VPS code (queue-manager, admin, nginx)
- Only if Mello Team requests Verda Team changes

### Git Workflow

**Branch Strategy:**
```
verda-track-2 (active) → main (via PR)
```

**Commit Messages:**
```bash
feat: add new feature
fix: resolve bug
docs: update documentation
test: add tests
refactor: code improvement
```

**Creating PRs:**
```bash
# When ready to merge work to main:
gh pr create --base main --head verda-track-2 --title "..." --body "..."
```

---

## 🔐 Environment Configuration

### .env File Location

**Development (mello):** `/home/dev/comfymulti-scripts/.env` (v0.3.1)
**Production (verda):** `/home/dev/comfyume/.env` (copied during deployment)

### Key Variables for Worker

```bash
# Redis Connection (Verda connects to Mello via Tailscale)
INFERENCE_SERVER_REDIS_HOST="100.99.216.71"  # Mello's Tailscale IP
REDIS_PORT=6379
REDIS_PASSWORD="230426c07f0b0b5c0570fa514c3408c60e4e573eac2533b1de482d3c13669090"

# Queue Manager
QUEUE_MANAGER_URL="http://100.99.216.71:3000"  # Mello VPS

# Worker Configuration
WORKER_ID="worker-1"
WORKER_POLL_INTERVAL=2
ENABLE_VRAM_MONITORING=true
VRAM_SAFETY_MARGIN_MB=2048

# Timeouts
COMFYUI_TIMEOUT=900      # 15 minutes
JOB_TIMEOUT=1800         # 30 minutes

# Paths (on Verda)
OUTPUTS_PATH=/outputs    # Mapped to /mnt/scratch/outputs
MODELS_PATH=/workspace/ComfyUI/models  # Mapped to /mnt/sfs/models
```

---

## 📦 Deployment Architecture

### Split Server Setup

**Mello VPS (App Server):**
- Location: Hetzner CAX31 (100.99.216.71 via Tailscale)
- Services: Nginx, Redis, Queue Manager, Admin, User Frontends
- Role: Job queue and user interface

**Verda GPU (Inference Server):**
- Location: Verda H100 instance (100.89.38.43 via Tailscale)
- Services: ComfyUI Worker container(s)
- Role: GPU processing and inference

**Connection:**
- Verda worker → Mello Redis (via Tailscale VPN)
- Verda worker → Mello Queue Manager (status updates)

### Storage on Verda

**SFS (Network Drive) - /mnt/sfs:**
- models/ - ComfyUI models (shared, read-only)
- cache/ - Backups, container images, configs

**Block Storage (Scratch) - /mnt/scratch:**
- outputs/ - User outputs (ephemeral)
- inputs/ - User uploads (ephemeral)

**Project Directory - /home/dev/comfyume:**
- comfyui-worker/ - Worker code
- .env - Environment configuration
- Symlinks: data/models → /mnt/sfs/models, data/outputs → /mnt/scratch/outputs

---

## 🔍 Key Files Reference

### comfyume Repository

**Worker Code:**
```
comfyui-worker/
├── Dockerfile              # CUDA 12.4, ComfyUI v0.11.0, dependencies
├── docker-compose.yml      # Standalone deployment config
├── worker.py               # Job processing with VRAM checks
├── vram_monitor.py         # GPU memory monitoring
├── start-worker.sh         # Container entrypoint
├── requirements.txt        # Python dependencies
├── test-deployment.sh      # Pre-deployment validation script
├── test_vram_monitor.py    # Unit tests for VRAM monitor
└── README.md               # Worker documentation
```

**Scripts:**
```
scripts/
├── create-gpu-quick-deploy.sh   # Quick deployment script (needs Phase 3 update)
└── verda-startup-script.sh      # Startup script (needs Phase 3 update)
```

**Documentation:**
```
docs/
├── implementation-plan-v0.11.0.md  # Original implementation plan
└── backup-restore-flow.md          # Backup/restore flow analysis
```

### comfymulti-scripts Repository

**Deployment Scripts:**
```
setup-verda-solo-script.sh   # Main deployment/restore script (v0.3.0)
backup-cron.sh               # Hourly backups (runs on Verda)
backup-verda.sh              # Full Verda backup to R2
backup-mello.sh              # Mello user data backup to R2
```

**Configuration:**
```
.env                         # Consolidated secrets v0.3.1
archive/older/               # Legacy .env files
```

---

## 🧪 Testing Checklist

### Pre-Deployment (Local)

**Docker Build:**
- [ ] Build worker container locally
- [ ] Container starts successfully
- [ ] Health check passes (curl http://localhost:8188/)
- [ ] ComfyUI web UI accessible

**VRAM Monitor:**
- [ ] nvidia-smi command works in container
- [ ] VRAM check returns current usage
- [ ] Safety margin calculation correct
- [ ] Dry run mode works

**Worker Logic:**
- [ ] Mock Redis connection successful
- [ ] Job poll loop functions
- [ ] Workflow submission to ComfyUI works
- [ ] Output files saved to /outputs

### Deployment (Verda H100)

**Environment:**
- [ ] SFS mounted at /mnt/sfs
- [ ] Block storage mounted at /mnt/scratch
- [ ] Tailscale VPN connected (100.89.38.43)
- [ ] .env file present with correct values

**Pre-Deployment Script:**
- [ ] Run test-deployment.sh
- [ ] GPU detection passes
- [ ] Storage mounts verified
- [ ] Tailscale connection confirmed
- [ ] Docker GPU passthrough works

**Worker Deployment:**
- [ ] Container builds successfully
- [ ] Container starts and stays running
- [ ] Connects to Redis on Mello
- [ ] Polls for jobs from queue
- [ ] Processes test job successfully
- [ ] Outputs saved to scratch disk

---

## 🐛 Known Issues & Gotchas

### 1. VRAM Monitoring in Container
**Issue:** nvidia-smi may not work if GPU not properly passed through
**Solution:** Use `--gpus all` in docker-compose.yml runtime config

### 2. Tailscale IP Preservation
**Issue:** New Tailscale install gets new IP, breaks connectivity
**Solution:** Restore /var/lib/tailscale/ BEFORE starting tailscale service

### 3. First Deployment (No Backups)
**Issue:** setup-verda-solo-script.sh expects backups, but none exist
**Solution:** Manual git clone from GitHub or scp from mello (future: add fallback to script)

### 4. R2 Bucket Names
**Issue:** Old scripts use comfy-multi-* bucket names
**Solution:** Updated to comfyume-* in .env v0.3.1 and backup scripts

---

## 📞 Coordination with Mello Team

### Communication

**GitHub Issues:**
- comfyume repo: Issues for worker development
- Use issue numbers in commits: `feat: add feature (Issue #X)`

**Branch Coordination:**
- verda-track-2 (Verda Team - GPU worker)
- mello-track-2 (Mello Team - VPS services)
- Both merge to main via PR

**Handoff Points:**
- Verda Team: Worker implementation, deployment scripts
- Mello Team: Queue manager, frontend, .env consolidation
- Shared: Integration testing, documentation

### Current Division of Labor

**Verda Team (us):**
- ✅ Worker v0.11.0 implementation (Issues #2-6)
- ✅ Deployment scripts (setup, backup)
- ⏳ Phase 3 cleanup (Issue #22)
- ⏳ Local container testing
- ⏳ Verda deployment and integration testing

**Mello Team:**
- ✅ .env consolidation (v0.3.1)
- ✅ Phase 1 & 2 updates (Issue #22)
- ⏳ Workflows for v0.11.0 (in progress)
- ⏳ Queue manager integration testing
- ⏳ Frontend updates for new workflows

---

## 🎯 Session Goals

### This Session (Verda 03)

**Primary Objectives:**
1. Complete Phase 3 cleanup tasks (Issue #22)
2. Test worker container build locally
3. Fix any issues discovered in testing
4. Prepare for Verda deployment

**Secondary Objectives:**
5. Update documentation (READMEs, guides)
6. Create deployment testing issue
7. Coordinate with Mello Team on workflows

**Success Criteria:**
- Worker container builds and runs locally ✓
- All Phase 3 tasks complete ✓
- Ready for Verda H100 deployment ✓

---

## 📝 Quick Reference

### Common Commands

**Switch to working branches:**
```bash
cd /home/dev/comfyume && git checkout verda-track-2
cd /home/dev/comfymulti-scripts && git checkout verda-track-2
```

**Pull latest changes:**
```bash
cd /home/dev/comfyume && git pull origin verda-track-2
cd /home/dev/comfymulti-scripts && git pull origin verda-track-2
```

**Build worker locally:**
```bash
cd /home/dev/comfyume/comfyui-worker
docker build -t comfyume-worker:latest .
```

**Run worker locally (mock):**
```bash
docker run --gpus all -p 8188:8188 \
  -e REDIS_HOST=100.99.216.71 \
  -e REDIS_PASSWORD=... \
  comfyume-worker:latest
```

**Check issues:**
```bash
gh issue list --repo ahelme/comfyume
gh issue view 22 --repo ahelme/comfyume
```

---

## 🚨 Critical Reminders

1. **Always work on verda-track-2 branch** (not main, not verda-track)
2. **Never commit secrets to comfyume repo** (use .env.example only)
3. **Test locally before deploying to Verda** (save costs and time)
4. **Coordinate with Mello Team** (check Issue #22, mello-track-2)
5. **Update HANDOVER docs** (keep this file current for next session)

---

## 📚 Additional Resources

**Documentation:**
- [comfyume README.md](../README.md)
- [Worker README](../comfyui-worker/README.md)
- [Implementation Plan v0.11.0](./implementation-plan-v0.11.0.md)
- [Backup/Restore Flow](./backup-restore-flow.md)

**GitHub:**
- [comfyume Issues](https://github.com/ahelme/comfyume/issues)
- [Issue #22 - .env Consolidation](https://github.com/ahelme/comfyume/issues/22)

**External:**
- [ComfyUI v0.11.0 Release](https://github.com/comfyanonymous/ComfyUI/releases/tag/v0.11.0)
- [Verda Documentation](https://docs.verda.com/)

---

**Last Updated:** 2026-02-01
**Next Session:** Continue with Phase 3 cleanup and local container testing
**Branch:** verda-track-2 (both repos)
