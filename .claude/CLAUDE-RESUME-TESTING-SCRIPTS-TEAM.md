# CLAUDE RESUME - COMFYUME (TESTING SCRIPTS TEAM)

**DATE**: 2026-02-08

---

## CONTEXT

**We are the Testing Scripts Team.** Branch: `testing-scripts-team-2`.

**Production:** aiworkshop.art runs on Verda CPU instance. Inference is serverless (DataCrunch H200/B300). Mello is staging/backup only (containers removed).

---

## RECENT WORK (this session)

### Issue #22 — Phase 3 doc updates (MERGED as PR #85)
- Archived 2 obsolete GPU scripts → `scripts/archive/`
- Updated `.env.example` v0.3.2 → v0.3.5 (serverless config)
- Updated `comfyui-worker/README.md` (serverless production note)
- Updated `README.md` (aiworkshop.art, serverless architecture)

### Issue #71 — Mello cleanup (PR #91 open)
- Created `scripts/cleanup-mello.sh` (dry-run by default, --execute to remove)
- Updated CLAUDE.md: Quick Links → aiworkshop.art, architecture diagram → Verda CPU + DataCrunch, server table → Mello staging/backup, tech stack updated
- Containers already removed from Mello by user

---

## PENDING WORK

- [ ] PR #91 needs merge (#71 work)
- [ ] Close #71 after Hetzner downgrade (user handles manually)
- [ ] Run test.sh on Verda app server to validate test scripts
- [ ] Lower-priority stale Mello refs in: `docs/admin-backup-restore.md`, `implementation-backup-restore.md`, `scripts/README-RESTORE.md`

---

## CONTEXT LOADING

Please read:

1. **`./CLAUDE.md`** - Project instructions
2. **`.claude/progress-testing-scripts-team-dev.md`** (top ~250 lines) - Recent progress
3. **`.claude/progress-all-teams.md`** - All-teams commit log
4. **`git status && git log --oneline -10`** - Pending work

---

## KEY FILES

| File | Purpose |
|------|---------|
| `./CLAUDE.md` | Project guide, architecture, gotchas |
| `.claude/progress-testing-scripts-team-dev.md` | Tasks + session progress |
| `.claude/progress-all-teams.md` | All-teams commit log |
| `scripts/test.sh` | Main integration test suite (10 sections) |
| `scripts/test-helpers.sh` | Shared test library |
| `scripts/test-serverless.sh` | Serverless E2E test |
| `scripts/test-connectivity.sh` | Network connectivity test |
| `scripts/cleanup-mello.sh` | Mello container/image cleanup |

---

## TEAM COORDINATION

**GitHub Issues:** https://github.com/ahelme/comfyume/issues
**Completed:** #6 (test scripts — PR #75 merged), #22 (Phase 3 docs — PR #85 merged)
**In Progress:** #71 (Mello cleanup — PR #91 open)
**Branch:** `testing-scripts-team-2`

---

## SESSION START CHECKLIST

- [ ] Check today's date
- [ ] `git status` - any uncommitted changes?
- [ ] Read `.claude/progress-testing-scripts-team-dev.md` top section
- [ ] Check relevant GitHub issues for updates
- [ ] Discuss priorities with user
