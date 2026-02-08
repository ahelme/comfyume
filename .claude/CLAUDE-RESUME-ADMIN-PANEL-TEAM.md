# CLAUDE RESUME - COMFYUME (ADMIN PANEL TEAM)

**PHASE**: ADMIN DASHBOARD V2 - IMPLEMENTATION COMPLETE, NEEDS DEPLOY/TEST
**DATE**: 2026-02-08

---

## CONTEXT

**We are the Admin Panel Team.** Branch: `admin-panel-team`.

**Production:** aiworkshop.art runs on Verda (NOT Mello).

---

## CURRENT STATUS

**Admin Dashboard V2 - IMPLEMENTED (Issues #65, #66, #67):**
All 3 phases implemented, UI verified in browser preview. PR #69 merged to main. Issues closed.

4 tabs:
1. **System** - Status cards (Redis/QM/GPU/Disk), container management (list/restart/stop/start/logs)
2. **GPU** - Serverless deployment switching (H200/B300 spot/on-demand) with confirmation dialogs
3. **Storage** - Disk usage breakdown, R2 bucket sizes, directory browser
4. **Queue** - Job queue monitoring with prioritize/cancel actions

**GitHub Issues:** #65, #66, #67 - CLOSED (completed)

**Next steps:**
1. Deploy on staging: `docker compose build admin && docker compose up -d admin`
2. Verify nginx /admin route is configured
3. Test all 4 tabs with live data

---

## QUICK CONTEXT LOADING

Please read:

1. **`./CLAUDE.md`** - Project instructions
2. **`.claude/progress-admin-panel-team-dev.md`** (top ~250 lines) - Recent progress
3. **`.claude/progress-all-teams.md`** - All-teams commit log
4. **`git status && git log --oneline -10`** - Pending work

---

## KEY FILES

| File | Purpose |
|------|---------|
| `./CLAUDE.md` | Project guide, architecture, gotchas |
| `.claude/progress-admin-panel-team-dev.md` | Tasks + session progress |
| `.claude/progress-all-teams.md` | All-teams commit log |

---

## TEAM COORDINATION

**GitHub Issues:** https://github.com/ahelme/comfyume/issues
**Branch:** `admin-panel-team`

---

## SESSION START CHECKLIST

- [ ] Check today's date
- [ ] `git status` - any uncommitted changes?
- [ ] Read `.claude/progress-admin-panel-team-dev.md` top section
- [ ] Check issues #65, #66, #67 for updates
- [ ] Discuss priorities with user
