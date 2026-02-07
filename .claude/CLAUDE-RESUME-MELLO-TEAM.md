# CLAUDE RESUME - COMFYUME (MELLO TEAM)

**PHASE**: RUN RESTORE SCRIPT ON VERDA + PRODUCTION VERIFICATION
**DATE**: 2026-02-07

---

## CRITICAL CONTEXT

**aiworkshop.art is PRODUCTION and it runs on VERDA, not Mello!**

`restore-verda-instance.sh` v0.4.0 was created this session (private scripts repo, `main` branch, ea6549b). It needs to be **RUN on Verda** to bring the production app server online.

---

## WHAT WAS DONE THIS SESSION (Session 35)

1. Created `restore-verda-instance.sh` v0.4.0 (replaces `setup-verda-solo-script.sh` v0.3.3)
   - Full app stack: containerized nginx, 20x frontends, queue-manager, Redis, admin
   - Serverless inference, `--skip-sfs` flag, certbot SSL, git clone fallback
   - R2 endpoint `.eu.` fix, firewall 80/443, endpoint verification
2. Updated all active docs (14 files) - PRs #72 and #73 merged
3. Archived stale .claude files (BACKUP-CHECKLIST, DEPLOYMENT-TO-DO, etc.)
4. Re-assessed issue #22 Phase 3: posted comment with analysis

---

## IMMEDIATE PRIORITIES

1. **Run restore script on Verda:**
   ```bash
   ssh root@95.216.229.236
   # Get script onto instance, then:
   ./restore-verda-instance.sh --skip-sfs   # SFS was blocked last session
   # OR with SFS:
   ./restore-verda-instance.sh "<MOUNT_COMMAND>"
   ```

2. **Verify production endpoints:**
   - https://aiworkshop.art/
   - https://aiworkshop.art/admin/
   - https://aiworkshop.art/user001/

3. **Issue #22 cleanup** (from re-assessment comment):
   - Archive 2 obsolete scripts: `scripts/create-gpu-quick-deploy.sh`, `scripts/verda-startup-script.sh`
   - Update `.env.example` to v0.3.5 structure
   - Update `README.md` and `comfyui-worker/README.md` for current architecture

4. **Then:** Issue #18 (e2e test), Issue #20 (workshop readiness), Issue #71 (Mello downgrade)

---

## VERDA INSTANCE

| Detail | Value |
|--------|-------|
| Hostname | soft-wolf-shines-fin-01 |
| Public IP | 95.216.229.236 |
| Tailscale IP | 100.89.38.43 (MUST restore identity!) |
| Spec | CPU.8V.32G (8 CPU / 32GB RAM / 100GB SSD) |
| Contract | 1 month prepaid (~€34/mth, expires 2026-03-06) |
| Role | Production app server → serverless inference |

---

## KEY FILES

**Private Scripts Repo** (`comfymulti-scripts`):
- `restore-verda-instance.sh` (v0.4.0) - production restore script
- `.env` (v0.3.5) - master secrets
- Branches: `main` (has script), `mello-team-new-restore` (clean)

**Comfyume Repo:**
- Branch `main` is up to date (PRs #72, #73 merged)
- Branch `mello-team-3` - current dev branch (clean)

---

## QUICK CONTEXT LOADING

1. **`./CLAUDE.md`** - Project instructions (Verda = PRODUCTION)
2. **`.claude/progress-mello-dev.md`** (top ~110 lines) - Priority tasks + session 35 report
3. **`.claude/progress-all-teams.md`** - All-teams commit log
4. **`git status && git log --oneline -10`** - Pending work

---

## TEAM COORDINATION

**GitHub Issues:** https://github.com/ahelme/comfyume/issues
**Key Issues:** #64 (Verda setup), #22 (env cleanup), #71 (Mello downgrade), #18 (e2e test)
**Private Scripts:** https://github.com/ahelme/comfymulti-scripts

---

## SESSION START CHECKLIST

- [ ] Check today's date
- [ ] `git status` on both repos
- [ ] Can you SSH to Verda? `ssh root@95.216.229.236`
- [ ] Read `.claude/progress-mello-dev.md` top section
- [ ] Discuss priorities with user
