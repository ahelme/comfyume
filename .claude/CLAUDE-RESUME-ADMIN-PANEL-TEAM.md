# CLAUDE RESUME - COMFYUME (ADMIN PANEL TEAM)

**DATE**: 2026-02-09

---

## CONTEXT

**We are the Admin Panel Team.** Branch: `admin-panel-team`.

**Production:** aiworkshop.art runs on Verda CPU instance (95.216.229.236), NOT Mello.

---

## IMMEDIATE PRIORITY

**Fix serverless inference (#101, #103)** — use new monitoring tools (#106) to debug.

### THE STORAGE SITUATION (#103)

| Storage | What | Serverless sees? | Instance sees? |
|---------|------|-----------------|----------------|
| **REAL SFS** | Verda NFS share (172GB models) | YES at `/mnt/sfs` | NO (NFS mount fails) |
| **Block storage** | 220GB on CPU instance | NO | YES at `/mnt/models-block-storage` |

Block storage ("fake SFS") was created because the REAL SFS won't connect to our CPU instance (Verda bug). The serverless container CAN still access the REAL SFS. All our yaml edits were on block storage — irrelevant.

### The bug

Container logs: `Adding extra search path upscale_models /mnt/sfs/models/shared/latent_upscale_models` — wrong folder type. `LatentUpscaleModelLoader` looks up `latent_upscale_models`, finds nothing.

### NEXT STEPS

1. Use `/verda-debug-containers` skill to inspect serverless container state
2. Use Verda SDK or OpenTofu to update serverless startup command to run diagnostic
3. Fix yaml key on REAL SFS (likely `upscale_models` → `latent_upscale_models`)
4. Test inference end-to-end

---

## MONITORING STACK (JUST INSTALLED - #106)

Full monitoring stack now live on Verda. Use `/verda-monitoring-check` to verify.

| Tool | Port | Purpose |
|------|------|---------|
| Prometheus | :9090 | Metrics (7d retention) |
| Grafana | :3001 | Dashboards (admin/admin) |
| Loki | :3100 | Log aggregation (7d retention) |
| cAdvisor | :8081 | Container metrics |
| Promtail | :9080 | Ships Docker logs → Loki |
| Dry | - | Docker TUI (`ssh -t root@95.216.229.236 "dry"`) |
| Verda SDK | - | `pip install verda`, env vars in `/root/.bashrc` |
| OpenTofu | - | `tofu`, config dir `/root/tofu/` |

**12 custom skills:** `/verda-ssh`, `/verda-status`, `/verda-logs`, `/verda-containers`, `/verda-terraform`, `/verda-open-tofu`, `/verda-prometheus`, `/verda-dry`, `/verda-loki`, `/verda-grafana`, `/verda-monitoring-check`, `/verda-debug-containers`

---

## GITHUB ISSUES

- **#101** — REAL SFS yaml key mapping issue (blocked, needs diagnostic)
- **#102** — Explore Verda General Storage (future)
- **#103** — Architecture decision: REAL SFS vs block storage
- **#106** — Monitoring stack (Phase 1 COMPLETE, Phase 2 = debug with tools)

---

## VERDA STATE

- Block storage at `/mnt/models-block-storage` (renamed, fstab updated)
- Monitoring stack running (Prometheus, Grafana, Loki, Promtail, cAdvisor)
- Verda SDK env vars in `/root/.bashrc` (VERDA_CLIENT_ID, VERDA_CLIENT_SECRET, VERDA_INFERENCE_KEY)
- OpenTofu at `/root/tofu/`
- Serverless startup command limit: 255 chars per line

---

## SESSION START CHECKLIST

- [ ] Read `.claude/progress-admin-panel-team-dev.md` top section
- [ ] Run `/verda-monitoring-check` to verify stack is healthy
- [ ] Check GitHub issues #101, #103, #106
- [ ] Use `/verda-debug-containers` to investigate SFS model path issue
