**Project:** ComfyUI Multi-User Workshop Platform
**Project Started:** 2026-01-02
**Repository:** github.com/ahelme/comfyume
**Domain:** comfy.ahelme.net (staging) / aiworkshop.art (production)
**Doc Created:** 2026-02-07
**Doc Updated:** 2026-02-07 (AEST) - Testing infrastructure rewrite complete

---
# Project Progress Tracker
**Target:** Testing Scripts
### Implementation Phase
**MAIN Repo:** comfyume (https://github.com/ahelme/comfyume)
**Branch:** testing-scripts-team-2
**Phase:** Issue #22 Phase 3 — Doc updates for serverless architecture
---
## 0. Update Instructions

   RE: PRIORITY TASKS
   **UPDATE:**
     - WHEN NEW TASKS EMERGE
     - AT END OF SESSION - YOU MUST UPDATE/CULL TASKS - carefully!!!

   **ALWAYS reference issues in our TWO  Github Issue Trackers**
      - MAIN COMFYUME REPO:   github.com/ahelme/comfyume/issues/
      - PRIVATE SCRIPTS REPO: github.com/ahelme/comfymulti-scripts/issues/

   **FORMAT:**
          [icon] [PRIORITY] [GH#s] [SHORT DESC.]
             - [DATE-CREATED] [DATE-UPDATED]
               - CONCISE NOTES INC. RELATED [GH#] (IF ANY)
   **BE CONCISE**
     - DETAIL BELONGS IN GH ISSUE! and in PROGRESS REPORT BELOW !!!

   RE: Progress Reports (NEWEST AT TOP!)
     **CRITICAL DETAIL - NO FLUFF**
     **UPDATE OFTEN e.g. after RESEARCH, COMMITS, DECISIONS**
      - concise notes, refer to GH issues
      - new blockers / tasks / completed tasks
      - investigations needed
      - research found
      - solutions formulated
      - decisions made
---
## 1. PRIORITY TASKS

- [x] P1 #6 Testing infrastructure rewrite — MERGED (PR #75)
- [x] P1 #22 Phase 3: archive scripts, update .env.example, update READMEs — MERGED (PR #85)
- [x] P1 #71 Mello cleanup script + CLAUDE.md updates
  - 2026-02-08 DONE
  - cleanup-mello.sh created, CLAUDE.md updated (Quick Links, architecture, tech stack)
- [ ] P2 Run test.sh on Verda app server to validate
  - 2026-02-07
  - Requires services running on production

---

# Progress Reports

---
### Implementation Phase
**Repository:** comfyume (https://github.com/ahelme/comfyume)
**Branch:** testing-scripts-team-2
**Phase:** Restore script updates + maintenance

## Progress Report 6 - 2026-02-08 - Portainer Edge Agent in Restore Script

**Date:** 2026-02-08

**Done:**
- Updated `restore-verda-instance.sh` v0.4.0 → v0.4.1 (private scripts repo)
  - Filled in `VERDA_EDGE_ID` and `VERDA_EDGE_KEY` (were empty)
  - Set `VERDA_PORTAINER_CONNECTION_MODE` to `http2` (was `http`)
  - Added Step 16: Start Portainer edge agent (`docker run` with EDGE_PROTOCOL=http2, EDGE_INSECURE_POLL=1, --restart always)
- Commit: 9b66c7c pushed to comfymulti-scripts main

---

## Progress Report 5 - 2026-02-08 - Issue #71 Mello Cleanup

**Date:** 2026-02-08

**Done:**
- Created `scripts/cleanup-mello.sh` — dry-run by default, --execute to remove containers/images
- Updated CLAUDE.md: Quick Links → aiworkshop.art, architecture diagram → Verda CPU + DataCrunch serverless, tech stack → Mello as staging/backup, server table updated
- Containers already removed from Mello by user

---

## Progress Report 4 - 2026-02-07 - Issue #22 Phase 3 Complete

**Date:** 2026-02-07

**Done:**
- Archived `create-gpu-quick-deploy.sh` and `verda-startup-script.sh` to `scripts/archive/`
- Updated `.env.example` v0.3.2 → v0.3.5: added INFERENCE_MODE, serverless endpoint vars, SERVERLESS_API_KEY
- Updated `comfyui-worker/README.md`: added serverless production note
- Updated `README.md`: added aiworkshop.art, serverless architecture, current status

---

## Progress Report 3 - 2026-02-07 - PR #75 Created, Issue #6 Updated

**Date:** 2026-02-07

**Done:**
- PR #75 created: `testing-scripts-team` → `main` (7 commits)
- Issue #6 body rewritten with current architecture, deliverables table, acceptance criteria
- Issue #6 closed — implementation complete
- Pushed all commits + progress updates to remote

---

## Progress Report 2 - 2026-02-07 - Testing Infrastructure Rewrite (#6)

**Date:** 2026-02-07

**Done:**
- `scripts/test-helpers.sh` — shared library (colors, counters, pass/fail, check_http, container helpers)
- `scripts/test.sh` — rewritten: 10 sections for serverless arch, no worker refs, docker compose v2
- `scripts/test-serverless.sh` — new: serverless E2E test with --dry-run/--all/--timeout flags
- `scripts/test-connectivity.sh` — new: Redis/QM/nginx/domain/SSL/Docker network validation
- `docs/admin-testing-guide.md` — new: comprehensive testing guide (10 sections, troubleshooting, reference)
- `scripts/status.sh` — fixed docker-compose → docker compose (3 occurrences)
- `scripts/load-test.sh` — updated "next steps" (removed worker reference)
- `docs/testing-guide.md` → `docs/archive/testing-guide-load-test.md` (archived)

**Key decisions:**
- test.sh sources test-helpers.sh (DRY, consistent output across all test scripts)
- Section 7 (Serverless) only runs when INFERENCE_MODE=serverless
- Section 10 (SSL) only runs when DOMAIN is set and not example value
- test-serverless.sh --dry-run is safe (no GPU cost) — default for CI
- Endpoints returning 401 treated as "route exists" (auth-protected = valid)

---

## Progress Report 1 - 2026-02-07 - Testing Scripts Team Initialized

**Date:** 2026-02-07

**Done:**
- Team initialization: progress file, handover command, resume context, onboarding file
- Branch created: `testing-scripts-team`

---
