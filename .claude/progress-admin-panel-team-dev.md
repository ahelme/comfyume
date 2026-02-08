**Project:** ComfyUI Multi-User Workshop Platform
**Project Started:** 2026-01-02
**Repository:** github.com/ahelme/comfyume
**Domain:** comfy.ahelme.net (staging) / aiworkshop.art (production)
**Doc Created:** 2026-02-06
**Doc Updated:** 2026-02-08 (AEST)

---
# Project Progress Tracker
**Target:** Admin Dashboard V2 - comprehensive management UI
### Implementation Phase
**MAIN Repo:** comfyume (https://github.com/ahelme/comfyume)
**Branch:** admin-panel-team
**Phase:** Admin Dashboard V2 (Issues #65, #66, #67)
---
## 0. Update Instructions

   RE: PRIORITY TASKS
   **UPDATE:**
     - WHEN NEW TASKS EMERGE
     - AT END OF SESSION - YOU MUST UPDATE/CULL TASKS - carefully!!!

   **ALWAYS reference issues in our TWO  Github Issue Trackers**
      - MAIN COMFYUME REPO:   github.com/ahelme/comfyume/issues/
      - PRIVATE SCRIPTS REPO: github.com/ahelme/comfymulti-scripts/issues/

   **FORMAT:**
          [icon] [PRIORITY] [GH#s] [SHORT DESC.]
             - [DATE-CREATED] [DATE-UPDATED]
               - CONCISE NOTES INC. RELATED [GH#] (IF ANY)
   **BE CONCISE**
     - DETAIL BELONGS IN GH ISSUE! and in PROGRESS REPORT BELOW !!!

   RE: Progress Reports (NEWEST AT TOP!)
     **CRITICAL DETAIL - NO FLUFF**
     **UPDATE OFTEN e.g. after RESEARCH, COMMITS, DECISIONS**
      - concise notes, refer to GH issues
      - new blockers / tasks / completed tasks
      - investigations needed
      - research found
      - solutions formulated
      - decisions made
---
## 1. PRIORITY TASKS

✅ **(COMPLETE) - comfyume #65 - Admin Dashboard Phase 1: Core Dashboard MVP**
    - Created: 2026-02-06 | Updated: 2026-02-06
    - System status cards (Redis, Queue Manager, Serverless GPU, Disk Usage)
    - Container list with restart/stop/start actions + log viewer
    - Dark ComfyUI-themed UI with 4-tab navigation

✅ **(COMPLETE) - comfyume #66 - Admin Dashboard Phase 2: GPU Deployment Switching**
    - Created: 2026-02-06 | Updated: 2026-02-06
    - One-click switching between H200/B300 spot/on-demand
    - Reads/writes .env via mounted volume, restarts queue-manager via Docker SDK
    - Confirmation dialog before switching

✅ **(COMPLETE) - comfyume #67 - Admin Dashboard Phase 3: Storage & R2 Management**
    - Created: 2026-02-06 | Updated: 2026-02-06
    - Disk usage breakdown with per-directory sizes
    - R2 bucket overview (objects count + sizes via boto3)
    - Directory browser with breadcrumb navigation (restricted to /outputs, /inputs, /models, /workflows)

✅ **(COMPLETE - VERIFIED ON VERDA) - comfyume #88 - Templates & Models Management (Phase 4)**
    - Created: 2026-02-08 | Updated: 2026-02-08
    - Templates tab: scan workflow JSONs, extract model deps, show on-disk status
    - Copy wget commands for missing models
    - 2 new endpoints: GET /api/templates/scan, GET /api/templates/models
    - Deployed to Verda, all 22 containers running with correct /mnt/sfs/models mount
    - On-disk detection verified: 21 model files (172GB) across all 5 workflows
    - Downloaded all 7 camera control LoRAs, LTX-2 distilled checkpoint, Flux 4B models
    - Only missing: flux-2-klein-9b-fp8.safetensors (distilled 9B, HF gated)

---

# Progress Reports

---
## Progress Report 6 - 2026-02-08 - Models Connected, All Camera LoRAs Downloaded (#88)

**Date:** 2026-02-08 | **Issue:** #88

**Done:**
- Fixed storage architecture: replaced symlinks with direct .env paths
  - `MODELS_PATH=/mnt/sfs/models`, `OUTPUTS_PATH=/mnt/scratch/outputs`, `INPUTS_PATH=/mnt/scratch/inputs`
  - Updated restore script v0.4.2: Step 15 now verifies paths instead of creating symlinks
  - Updated Step 11 to set storage paths dynamically based on available mounts
  - Fixed embedded Redis IPs in restore script (were still Mello's, now Verda Tailscale)
- Downloaded 3 missing Flux Klein 9B models to Verda /mnt/sfs:
  - `diffusion_models/flux-2-klein-base-9b-fp8.safetensors` (9GB) - HF gated, required license acceptance
  - `text_encoders/qwen_3_8b_fp8mixed.safetensors` (8.1GB)
  - `vae/flux2-vae.safetensors` (321MB)
- Downloaded ALL 7 LTX-2 camera control LoRAs for filmmakers:
  - static (2.1GB), dolly-in/out/left/right (313MB each), jib-up/down (2.1GB each)
- Downloaded remaining models for full workflow coverage:
  - `checkpoints/ltx-2-19b-distilled.safetensors` (41GB) for distilled video workflow
  - `diffusion_models/flux-2-klein-base-4b.safetensors` + `flux-2-klein-4b.safetensors` (7.3GB each)
  - `text_encoders/qwen_3_4b.safetensors` (7.5GB) for 4B workflow
- Recreated all 22 containers with correct /mnt/sfs/models mount
- Templates tab verified: on-disk detection working across all 5 workflows
- Added comprehensive workflow template docs to CLAUDE.md:
  - All 5 workflows documented with subgraph explanations
  - Complete model inventory table (21 files, 172GB) with HF download URLs
  - Camera control LoRA table for filmmakers
- Deployed restore script v0.4.2 to Verda (root + dev) via SCP

**Model inventory: 21 files, 172GB on /mnt/sfs (33GB free, 85% usage)**
- Only missing: `flux-2-klein-9b-fp8.safetensors` (distilled 9B variant, HF gated)
- Potential cleanup: `gemma_3_12B_it.safetensors` (19GB full-precision, have fp4_mixed) and legacy checkpoints

**Private scripts repo:** commit 2a3d444 - restore script v0.4.2 pushed to main

---
## Progress Report 5 - 2026-02-08 - Templates & Models Management Tab (#88)

**Date:** 2026-02-08 | **Issue:** #88

**Done:**
- Implemented Phase 4: Templates & Models Management tab in admin panel
- Backend: 2 new endpoints + 2 helper functions (~182 lines added to app.py)
  - `_extract_models_from_workflow()` - parses workflow JSON, extracts models from `properties.models` + widget value fallbacks for UNETLoader/CheckpointLoaderSimple
  - `_check_model_on_disk()` - checks `/models/{dir}/{file}` existence and size
  - `GET /api/templates/scan` - per-workflow model status + disk info
  - `GET /api/templates/models` - deduplicated cross-workflow model list
- Frontend: 5th "Templates" tab (~253 lines added to dashboard.html)
  - 4 summary cards (Workflows, On Disk, Missing, Disk Free)
  - Per-workflow cards with subgraph names + model rows
  - ON DISK (green) / MISSING (red) badges with file sizes
  - "Copy wget" button generates `wget -c -P /mnt/sfs/models/shared/{dir}/ "{url}"`
  - Disk usage bar
- Tested model extraction against all 5 workflow files - correct results
- No new dependencies, no Docker changes needed
- Deployed to Verda: fetched branch, built admin container, restarted
- Fixed REDIS_BIND_IP and INFERENCE_SERVER_REDIS_HOST: Mello IP (100.99.216.71) → Verda Tailscale IP (100.89.38.43)
  - Updated on Verda live .env + private scripts repo .env (comfymulti-scripts 8259d60)
  - Best practice: bind Redis to Tailscale interface only (serverless containers connect via Tailscale)
- Reloaded nginx to pick up new admin container IP after recreation
- Initial browser testing looks great, need /mnt/sfs models mount to verify on-disk detection

---
## Progress Report 4 - 2026-02-08 - Verda debugging, restore script improvements, CLAUDE.md updates

**Date:** 2026-02-08

**Done:**
- Merged 34 commits from main into `admin-panel-team` (fast-forward after stash)
- Resolved merge conflict in `.claude/CLAUDE-RESUME-ADMIN-PANEL-TEAM.md`
- SSHed into Verda production (95.216.229.236) to debug admin panel auth
  - Root cause: browser URL-encoding `/` as `%2F` in password
  - Auth works fine server-side (curl 200), nginx logs confirmed password mismatch from encoded input
  - Generated corrected magic links for all 20 users (fixed domain + URL encoding)
- Copied fresh `.env` from Mello scripts repo to Verda `~/comfyume/.env`
- Copied SSH authorized_keys from root to dev user on Verda (was missing mac + termius keys)
- **Private scripts repo (comfymulti-scripts):**
  - `restore-verda-instance.sh`: added Termius SSH keys, copy keys root→dev, full .env v0.3.5 sync, added MELLO_PUBLIC_IP (PR #32 merged)
  - Created `claude-settings/all-teams/commands/` with all 12 command files
- CLAUDE.md: moved User Preferences to bottom, added "never push directly to main" rule to git workflow + user prefs

**Notable changes from main:**
- New testing-scripts-team with test suites (connectivity, serverless, integration)
- `/pull-main` and `/update-progress` commands added
- Docs archived and cleaned up
- Resume/handover files slimmed down
- Restore script renamed to `restore-verda-instance.sh` v0.4.0

---
## Progress Report 3 - 2026-02-07 - Close GH issues

**Date:** 2026-02-07

**Done:**
- Commented and closed GitHub issues #65, #66, #67 with implementation details referencing PR #69
- PR #69 already merged to main

---
### Implementation Phase
**Repository:** comfyume (https://github.com/ahelme/comfyume)
**Branch:** admin-panel-team
**Phase:** Admin Dashboard V2

## Progress Report 2 - 2026-02-06 - All 3 Phases Implemented

**Date:** 2026-02-06 | **Issues:** #65, #66, #67

**Done:**
- **Phase 1 (#65):** System status cards (Redis, QM, Serverless GPU, Disk), container management (list/restart/stop/start/logs), Docker socket integration
- **Phase 2 (#66):** GPU deployment switching panel with 4 serverless options (H200/B300 spot/on-demand), .env modification + queue-manager auto-restart, confirmation dialogs
- **Phase 3 (#67):** Disk usage breakdown, R2 bucket querying via boto3, directory browser with path security restrictions
- **Design:** Dark ComfyUI-themed UI with node-connection logo, colored port dots, dot-grid canvas background, 4-tab SPA navigation
- **Security:** All endpoints behind HTTP Basic Auth, container operations restricted to `comfy-` prefix, directory traversal prevention, XSS protection via HTML escaping

**Files created/modified:**
- `admin/app.py` - Complete rewrite: 691 lines, 20 API endpoints
- `admin/dashboard.html` - New: comprehensive dark-themed SPA (~600 lines CSS + JS)
- `admin/requirements.txt` - Added docker, redis, boto3 dependencies
- `admin/Dockerfile` - Added dashboard.html to COPY
- `docker-compose.yml` - Added Docker socket mount, .env mount, storage volume mounts, R2 env vars

**API Endpoints (20 total):**
- System: GET /api/system/status
- Containers: GET /api/containers, POST .../restart, POST .../stop, POST .../start, GET .../logs
- GPU: GET /api/gpu/status, POST /api/gpu/switch
- Storage: GET /api/storage/disk, GET /api/storage/r2, GET /api/storage/browse
- Queue: GET /api/queue/status, GET /api/queue/jobs, DELETE .../jobs/{id}, PATCH .../priority

**Architecture:**
- Optional Docker SDK (degrades gracefully if socket not mounted)
- Optional boto3 for R2 (shows helpful error if not configured)
- Optional Redis direct connection for health checks
- All queue operations proxied through admin backend (works behind nginx)

---

## Progress Report 1 - 2026-02-06 - Admin Panel Team Initialized

**Date:** 2026-02-06 | **Issues:** #65, #66, #67

**Done:**
- Team initialization: progress file, handover command, resume context, onboarding file
- Read and analyzed existing codebase: admin/app.py, queue-manager/*, scripts/switch-gpu.sh
- Read both team progress files (mello top 250 lines, verda top 250 lines)
- Designed ComfyUI-themed dark dashboard UI with 4-tab navigation

---
