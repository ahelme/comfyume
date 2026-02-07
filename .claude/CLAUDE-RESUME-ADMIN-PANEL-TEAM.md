# CLAUDE RESUME - COMFYUME (ADMIN PANEL TEAM)

**PHASE**: ADMIN DASHBOARD V2 - IMPLEMENTATION COMPLETE, NEEDS DEPLOY/TEST
**DATE**: 2026-02-06

---

## CRITICAL CONTEXT

**We are the Admin Panel Team.** Our branch is `admin-panel-team`.

**Architecture update:** Frontend containers now run on a Verda CPU instance. Inference is via serverless containers on Verda (DataCrunch). Mello (comfy.ahelme.net) serves as staging.

**Production:** aiworkshop.art runs on Verda (NOT Mello).

---

## CURRENT STATUS

**Admin Dashboard V2 - IMPLEMENTED (Issues #65, #66, #67):**
All 3 phases implemented, UI verified in browser preview. Needs deployment and live testing.

4 tabs:
1. **System** - Status cards (Redis/QM/GPU/Disk), container management (list/restart/stop/start/logs)
2. **GPU** - Serverless deployment switching (H200/B300 spot/on-demand) with confirmation dialogs
3. **Storage** - Disk usage breakdown, R2 bucket sizes, directory browser
4. **Queue** - Job queue monitoring with prioritize/cancel actions

**GitHub Issues:**
- #65 - Phase 1: Core Dashboard MVP
- #66 - Phase 2: GPU Deployment Switching
- #67 - Phase 3: Storage & R2 Management
- #63 - Parent: Admin Dashboard V2

---

## QUICK CONTEXT LOADING

Please read:

1. **`./CLAUDE.md`** - Project instructions
2. **`.claude/progress-admin-panel-team-dev.md`** (top ~250 lines) - Recent progress
3. **`.claude/progress-all-teams.md`** - Ultra-concise all-teams commit log
4. **`admin/app.py`** - Admin dashboard backend
5. **`admin/dashboard.html`** - Admin dashboard frontend
6. **`queue-manager/config.py`** - Serverless configuration
7. **`git status && git log --oneline -10`** - Check for pending work

---

## KEY FILES

| File | Purpose |
|------|---------|
| `admin/app.py` | FastAPI backend with API endpoints |
| `admin/dashboard.html` | Dashboard UI (dark ComfyUI theme) |
| `admin/requirements.txt` | Python dependencies |
| `admin/Dockerfile` | Container build |
| `queue-manager/config.py` | Serverless endpoint config |
| `scripts/switch-gpu.sh` | CLI GPU switching (reference) |
| `docker-compose.yml` | Service orchestration |

---

## TEAM COORDINATION

**GitHub Issues:** https://github.com/ahelme/comfyume/issues
**Our Issues:** #65 (Phase 1), #66 (Phase 2), #67 (Phase 3)
**Branch:** `admin-panel-team`

---

## SESSION START CHECKLIST

- [ ] Check today's date
- [ ] `git status` - any uncommitted changes?
- [ ] Read `.claude/progress-admin-panel-team-dev.md` top section
- [ ] Check issues #65, #66, #67 for updates
- [ ] Discuss priorities with user
