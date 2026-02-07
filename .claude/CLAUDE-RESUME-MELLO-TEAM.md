# CLAUDE RESUME - COMFYUME (MELLO TEAM)

**PHASE**: RUN RESTORE SCRIPT ON VERDA + PRODUCTION VERIFICATION
**DATE**: 2026-02-07

---

## CRITICAL CONTEXT

**aiworkshop.art is PRODUCTION and it runs on VERDA, not Mello!**

New `restore-verda-instance.sh` (v0.4.0) was created this session. It needs to be RUN on Verda to bring the production app server online.

---

## WHAT WAS DONE THIS SESSION

1. Created `restore-verda-instance.sh` v0.4.0 (private scripts repo, committed to `main` ea6549b)
   - Full app stack restore: containerized nginx, 20x frontends, queue-manager, Redis, admin
   - Serverless inference (no GPU worker)
   - `--skip-sfs` flag, certbot SSL, git clone fallback, endpoint verification
   - R2 endpoint fixed to `.eu.` domain
2. Updated README-RESTORE.md in private scripts repo
3. Updated all active docs in comfyume repo (PR #72, branch `restore-script-v040`)
4. Old `setup-verda-solo-script.sh` v0.3.3 archived (not deleted)

---

## IMMEDIATE PRIORITIES

1. **Merge PR #72** on comfyume repo (doc updates for new script name)
   - URL: https://github.com/ahelme/comfyume/pull/72
   - Branch: `restore-script-v040`

2. **Run restore script on Verda** - SSH in and run:
   ```bash
   ssh root@95.216.229.236
   # Copy restore-verda-instance.sh to /root/ (or download from GitHub)
   # Option A (with SFS): ./restore-verda-instance.sh "<MOUNT_COMMAND>"
   # Option B (no SFS):   ./restore-verda-instance.sh --skip-sfs
   ```
   - SFS was BLOCKED last session (no private network interface on CPU instance)
   - Contact Verda support, or use `--skip-sfs` to proceed without it

3. **Verify production endpoints** after restore:
   - https://aiworkshop.art/ (main app)
   - https://aiworkshop.art/admin/ (admin dashboard)
   - https://aiworkshop.art/user001/ (user frontend)

4. **Then resume**: Issue #18 (end-to-end test), Issue #20 (workshop readiness)

---

## VERDA INSTANCE DETAILS

| Detail | Value |
|--------|-------|
| Hostname | soft-wolf-shines-fin-01 |
| Public IP | 95.216.229.236 |
| Tailscale IP | 100.89.38.43 (MUST restore identity!) |
| Instance ID | bb48b2c2-0414-407b-8f27-77b8867818a3 |
| Spec | CPU.8V.32G (8 CPU / 32GB RAM / 100GB SSD) |
| Contract | 1 month prepaid (~€34/mth, expires 2026-03-06) |
| Role | Production app server: nginx + 20 frontends + queue-manager + Redis + admin |
| Inference | Serverless via DataCrunch containers |

---

## KEY FILES

**Private Scripts Repo** (`comfymulti-scripts`):
- `restore-verda-instance.sh` (v0.4.0) - CURRENT production restore script
- `setup-verda-solo-script.sh` (v0.3.3) - ARCHIVED GPU worker script
- `.env` (v0.3.5) - master secrets
- Branch: `mello-team-new-restore` (clean, no pending changes)

**Comfyume Repo:**
- Branch `restore-script-v040` has PR #72 (doc updates) - MERGE THIS
- Branch `main` is clean

---

## QUICK CONTEXT LOADING

Please read:

1. **`./CLAUDE.md`** - Project instructions (note CRITICAL section: Verda = PRODUCTION)
2. **`.claude/progress-mello-dev.md`** (top ~100 lines) - Recent progress
3. **`.claude/progress-all-teams.md`** - Ultra-concise all-teams commit log
4. **`git status && git log --oneline -10`** - Check for pending work

---

## TEAM COORDINATION

**GitHub Issues:** https://github.com/ahelme/comfyume/issues
**Key Issues:** #64 (Verda setup), #71 (Mello downgrade), #18 (e2e test), #20 (workshop readiness)
**Open PR:** #72 (doc updates for restore script)
**Private Scripts:** https://github.com/ahelme/comfymulti-scripts

---

## SESSION START CHECKLIST

- [ ] Check today's date
- [ ] `git status` on both repos - any uncommitted changes?
- [ ] Merge PR #72 if not yet merged
- [ ] Can you SSH to Verda? `ssh root@95.216.229.236`
- [ ] Read `.claude/progress-mello-dev.md` top section
- [ ] Discuss priorities with user
