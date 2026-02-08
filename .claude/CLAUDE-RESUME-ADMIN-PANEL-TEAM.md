# CLAUDE RESUME - COMFYUME (ADMIN PANEL TEAM)

**DATE**: 2026-02-08

---

## CONTEXT

**We are the Admin Panel Team.** Branch: `admin-panel-team`.

**Production:** aiworkshop.art runs on Verda (95.216.229.236), NOT Mello.

---

## IMMEDIATE PRIORITY

**Serverless inference is NOT working yet.** The `queue_redirect` custom node
has been installed in all 20 user containers but has not been tested end-to-end.

Steps to verify:
1. Open `https://aiworkshop.art/user002/` in browser
2. Load a workflow (e.g. Flux Klein 4B text-to-image)
3. Check browser console for `[QueueRedirect] Extension loaded`
4. Submit a job - it should POST to `/api/queue/submit`
5. Check queue-manager logs: `sudo docker logs comfy-queue-manager --tail 30`
6. Check if `/api/queue/submit` endpoint exists in queue-manager code
7. Verify job appears in admin panel Queue tab

If `/api/queue/submit` doesn't exist, check `queue-manager/` source for the correct submit endpoint.

---

## CONTEXT LOADING

Please read:

1. **`./CLAUDE.md`** - Project instructions
2. **`.claude/progress-admin-panel-team-dev.md`** (top ~120 lines) - Priority tasks + recent progress
3. **`.claude/progress-all-teams.md`** - All-teams commit log
4. **`git status && git log --oneline -10`** - Pending work

---

## KEY FILES

| File | Purpose |
|------|---------|
| `./CLAUDE.md` | Project guide, architecture, gotchas |
| `.claude/progress-admin-panel-team-dev.md` | Tasks + session progress |
| `.claude/progress-all-teams.md` | All-teams commit log |
| `admin/app.py` | Admin backend (~900 lines, 23 endpoints) |
| `admin/dashboard.html` | Admin frontend SPA (5 tabs, ~2000 lines) |
| `comfyui-frontend/custom_nodes/queue_redirect/` | Job redirect extension |
| `queue-manager/` | FastAPI queue service |

---

## VERDA STATE (as of session end)

- 24 containers running (20 frontends + redis + queue-manager + admin + nginx)
- All 20 frontends mount `/mnt/sfs/models` correctly
- All 20 frontends have `queue_redirect` custom node installed
- 22 model files on disk, 138GB used, 67GB free (68%)
- All 5 workflows at 100% model coverage
- Download engine (#93) deployed and working
- SSL certs at `/etc/letsencrypt/live/comfy.ahelme.net/`
- `.env` has `HF_TOKEN`, `NTFY_TOPIC`, `MODELS_PATH=/mnt/sfs/models`

---

## SESSION START CHECKLIST

- [ ] Check today's date
- [ ] `git status` on both repos
- [ ] Read `.claude/progress-admin-panel-team-dev.md` top section
- [ ] Check GitHub issues relevant to current tasks in progress files
- [ ] Discuss priorities with user
