# CLAUDE RESUME - COMFYUME (ADMIN PANEL TEAM)

**DATE**: 2026-02-09

---

## CONTEXT

**We are the Admin Panel Team.** Branch: `admin-panel-team`.

**Production:** aiworkshop.art runs on Verda CPU instance (95.216.229.236), NOT Mello.

---

## IMMEDIATE PRIORITY

**Fix serverless inference (#101, #103).** Execute Option 1 from #103.

### THE STORAGE SITUATION (#103)

| Storage | What | Serverless sees? | Instance sees? |
|---------|------|-----------------|----------------|
| **REAL SFS** | Verda NFS share (172GB models) | YES at `/mnt/sfs` | NO (NFS mount fails) |
| **Block storage** | 220GB on CPU instance | NO | YES at `/mnt/models-block-storage` |

Block storage a.k.a. "fake SFS" — created because the REAL SFS won't connect to our Verda CPU instance (Verda bug, they are looking into it). We didn't realise the serverless container CAN still access the REAL SFS. Plan: use REAL SFS for serving models for boss's testing period (next week), even though we can only manage it via Verda API or Serverless console. All our yaml edits were on block storage — irrelevant. Block storage renamed from `/mnt/sfs` to `/mnt/models-block-storage`.

### NEXT STEP

1. Run diagnostic startup command on Verda Serverless console:
   ```
   bash -c "cat /mnt/sfs/extra_model_paths.yaml; ls /mnt/sfs/models/shared/ /mnt/sfs/models/shared/latent_upscale_models/ /mnt/sfs/models/shared/upscale_models/"
   ```
2. Check container logs — will show actual yaml and directories on REAL SFS
3. Fix yaml key via one-time startup command (likely `upscale_models` → `latent_upscale_models`)
4. Revert to normal startup: `python3 /workspace/ComfyUI/main.py --listen 0.0.0.0 --port 8188 --extra-model-paths-config /mnt/sfs/extra_model_paths.yaml`
5. Test inference

### The bug

Container logs: `Adding extra search path upscale_models /mnt/sfs/models/shared/latent_upscale_models` — wrong folder type. `LatentUpscaleModelLoader` looks up `latent_upscale_models`, finds nothing.

---

## GITHUB ISSUES

- **#101** — REAL SFS yaml key mapping issue (full debugging context)
- **#102** — Explore Verda General Storage (future)
- **#103** — Architecture decision: REAL SFS vs block storage

---

## KEY FILES

| File | Purpose |
|------|---------|
| `comfyui-frontend/custom_nodes/queue_redirect/web/redirect.js` | Job redirect extension (modified this session) |
| `nginx/nginx.conf` | Reverse proxy config (modified this session) |
| `queue-manager/main.py` | FastAPI queue service with serverless mode (debug logging added) |

---

## VERDA STATE

- Branch `verda-changes` on Verda (has nginx.conf + favicon changes, not yet committed)
- Block storage at `/mnt/models-block-storage` (renamed, fstab updated)
- Old GPU instance can be shut down
- Verda API credentials available to Claude for serverless management
- Serverless startup command limit: 255 chars per line

---

## SESSION START CHECKLIST

- [ ] Read `.claude/progress-admin-panel-team-dev.md` top section
- [ ] Check GitHub issues #101, #103
- [ ] Run diagnostic startup command (step 1 above)
