# CLAUDE RESUME - COMFYUME (TESTING SCRIPTS TEAM)

**PHASE**: TESTING SCRIPTS - IMPLEMENTATION COMPLETE
**DATE**: 2026-02-07

---

## CRITICAL CONTEXT

**We are the Testing Scripts Team.** Our branch is `testing-scripts-team`.

**Architecture update:** Frontend containers now run on a Verda CPU instance. Inference is via serverless containers on DataCrunch (H200/B300). Mello (comfy.ahelme.net) serves as staging.

**Production:** aiworkshop.art runs on Verda (NOT Mello).

---

## CURRENT STATUS

**Testing infrastructure rewrite COMPLETE (#6):**
- 6 commits on `testing-scripts-team` branch
- All 4 test scripts + docs + minor fixes implemented
- Ready for PR to main

**Next:** Create PR, run tests on Verda app server to validate

---

## QUICK CONTEXT LOADING

Please read:

1. **`./CLAUDE.md`** - Project instructions
2. **`.claude/progress-testing-scripts-team-dev.md`** (top ~250 lines) - Recent progress
3. **`.claude/progress-all-teams.md`** - Ultra-concise all-teams commit log
4. **`git status && git log --oneline -10`** - Check for pending work

---

## KEY FILES

| File | Purpose |
|------|---------|
| `scripts/test-helpers.sh` | Shared test library (sourced by all test scripts) |
| `scripts/test.sh` | Main integration test suite (10 sections) |
| `scripts/test-serverless.sh` | Serverless inference E2E test (--dry-run/--all/--timeout) |
| `scripts/test-connectivity.sh` | Network connectivity test (Redis/QM/nginx/SSL/Docker) |
| `docs/admin-testing-guide.md` | Comprehensive admin testing guide |
| `queue-manager/main.py` | API contracts: /health, /api/jobs, /api/queue/status |
| `queue-manager/config.py` | Serverless config: endpoints, active selector, API key |
| `queue-manager/models.py` | HealthCheck, QueueStatus response models |

---

## TEAM COORDINATION

**GitHub Issues:** https://github.com/ahelme/comfyume/issues
**Our Issues:** #6 (test scripts)
**Branch:** `testing-scripts-team`

---

## SESSION START CHECKLIST

- [ ] Check today's date
- [ ] `git status` - any uncommitted changes?
- [ ] Read `.claude/progress-testing-scripts-team-dev.md` top section
- [ ] Check relevant GitHub issues for updates
- [ ] Discuss priorities with user
