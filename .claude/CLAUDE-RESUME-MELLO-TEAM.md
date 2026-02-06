# CLAUDE RESUME - COMFYUME (MELLO TEAM)

**PHASE**: VERDA CPU INSTANCE SETUP + PRODUCTION BACKUP
**DATE**: 2026-02-06

---

## CRITICAL CONTEXT

**aiworkshop.art is PRODUCTION and it runs on VERDA, not Mello!**

The previous Verda GPU instance (wide-tree-opens-fin-01) was terminated (credits ran out). A new CPU instance has been provisioned but NOT YET SET UP.

---

## CURRENT STATUS

**New Verda CPU Instance (provisioned, not yet configured):**

| Detail | Value |
|--------|-------|
| Hostname | soft-wolf-shines-fin-01 |
| IP | 95.216.229.236 |
| Tailscale IP | 100.89.38.43 (MUST restore identity!) |
| Instance ID | bb48b2c2-0414-407b-8f27-77b8867818a3 |
| Spec | CPU.8V.32G (8 CPU / 32GB RAM / 100GB SSD) |
| Contract | 1 month prepaid (~€34/mth, expires 2026-03-06) |
| Role | Production app server: nginx + 20 frontends + queue-manager + Redis + admin |
| Inference | Serverless via DataCrunch containers (unchanged) |

**Storage (all restored/available):**
- OS volume from previous instance (may contain nginx configs for aiworkshop.art)
- Scratch volume (user inputs/outputs)
- SFS network drive (models, cache, scripts)

**Mello (comfy.ahelme.net) - running but secondary:**
- 20 frontends + queue-manager + admin + Redis all healthy
- Serving comfy.ahelme.net (staging)
- RAM: 14GB/15GB used (near capacity)

---

## IMMEDIATE PRIORITIES

1. **SSH into Verda** (`ssh root@95.216.229.236`) and set up:
   - Restore Tailscale identity (BEFORE starting Tailscale!)
   - Install/configure nginx for aiworkshop.art
   - Deploy app (Docker, 20 frontends, queue-manager, Redis, admin)
   - SSL certs for aiworkshop.art (Let's Encrypt)

2. **Capture production nginx configs** from restored OS volume
   - Mount old OS volume, find `/etc/nginx/` configs
   - Copy aiworkshop.art config to `nginx-production/nginx/` in private scripts repo

3. **Verify git repo completeness** for production deployment
   - All service code IS in git (confirmed)
   - Verda-specific nginx config (aiworkshop.art) NOT yet in git
   - May need branch `verda-instance-frontend` if live code differs

4. **Back up everything** to SFS + R2

5. **Then resume**: Issue #18 (end-to-end test), Issue #20 (workshop readiness)

---

## QUICK CONTEXT LOADING

Please read:

1. **`./CLAUDE.md`** - Project instructions (note CRITICAL section about Verda = PRODUCTION)
2. **`.claude/progress-mello-dev.md`** (top ~100 lines) - Recent progress
3. **`./SERVERLESS_UPDATE.md`** - Serverless deployment details
4. **`git status && git log --oneline -10`** - Check for pending work

---

## KEY INFRASTRUCTURE

**Serverless (DataCrunch):**
- Endpoints: `https://containers.datacrunch.io/comfyume-vca-ftv-{gpu}-{mode}/`
- Auth: `SERVERLESS_API_KEY` in .env (Bearer token)
- Models on SFS volume
- Switch: `./scripts/switch-gpu.sh h200-spot` (or h200-on-demand, b300-spot, b300-on-demand)

**Private Scripts Repo:** https://github.com/ahelme/comfymulti-scripts
- `.env` v0.3.5 - updated with new instance details
- `nginx-staging/nginx/` - Mello configs (comfy.ahelme.net)
- `nginx-production/nginx/` - Verda configs (aiworkshop.art) - TO BE POPULATED
- Setup/backup scripts

**Credentials:** All in `.env` (comfyume + comfymulti-scripts repos)

---

## TEAM COORDINATION

**GitHub Issues:** https://github.com/ahelme/comfyume/issues
**Key Issues:** #64 (Verda setup), #18 (e2e test), #20 (workshop readiness)
**Private Scripts:** https://github.com/ahelme/comfymulti-scripts

---

## SESSION START CHECKLIST

- [ ] Check today's date
- [ ] `git status` - any uncommitted changes?
- [ ] Can you SSH to Verda? `ssh root@95.216.229.236`
- [ ] Read `.claude/progress-mello-dev.md` top section
- [ ] Discuss priorities with user
