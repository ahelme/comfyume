# CLAUDE RESUME - COMFYUME (MELLO TEAM)

**PHASE**: SERVERLESS INFERENCE - COMPLETE ✅
**DATE**: 2026-02-04

---

## CURRENT STATUS

🎉 **Phase 11 COMPLETE** - All 4 serverless GPU deployments operational!

| Deployment | GPU | Price | Status |
|------------|-----|-------|--------|
| comfyume-vca-ftv-h200-spot | H200 141GB | €0.97/hr | ✅ |
| comfyume-vca-ftv-h200-on-demand | H200 141GB | €2.80/hr | ✅ |
| comfyume-vca-ftv-b300-spot | B300 288GB | €1.61/hr | ✅ |
| comfyume-vca-ftv-b300-on-demand | B300 288GB | €4.63/hr | ✅ |

**Switch between GPUs:**
```bash
./scripts/switch-gpu.sh h200-spot  # or h200-on-demand, b300-spot, b300-on-demand
docker compose restart queue-manager
```

---

## NEXT PRIORITIES

1. **Issue #18** - End-to-end job submission test (serverless is ready!)
2. **Issue #20** - Workshop readiness checklist
3. **Issue #19** - Multi-user load test (20 concurrent)

---

## QUICK CONTEXT LOADING

Please read:

1. **`./CLAUDE.md`** - Project instructions and architecture
2. **`.claude/progress-mello-dev.md`** (top ~100 lines) - Recent progress
3. **`./SERVERLESS_UPDATE.md`** - Serverless deployment details
4. **`git status && git log --oneline -10`** - Check for pending work

---

## KEY INFRASTRUCTURE

**Serverless (DataCrunch/Verda):**
- All endpoints: `https://containers.datacrunch.io/comfyume-vca-ftv-{gpu}-{mode}/`
- Auth: `SERVERLESS_API_KEY` in .env (Bearer token)
- Models on SFS volume (volume_id: be539393-4946-42fa-9adf-d72fe62cded7)

**Mello (App Server):**
- Redis, queue-manager, 20 user frontends
- Domain: comfy.ahelme.net

**Credentials:**
- All in `.env` (comfyume + comfymulti-scripts repos)
- DataCrunch API: `DATACRUNCH_CLIENT_ID` + `DATACRUNCH_CLIENT_SECRET`
- Serverless auth: `SERVERLESS_API_KEY`

---

## TEAM COORDINATION

**GitHub Issues:** https://github.com/ahelme/comfyume/issues
**Collaboration:** Issue #7
**Private Scripts:** https://github.com/ahelme/comfymulti-scripts

---

## SESSION START CHECKLIST

- [ ] Check today's date
- [ ] `git status` - any uncommitted changes?
- [ ] Read `.claude/progress-mello-dev.md` top section
- [ ] Discuss priorities with user
