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
**Branch:** testing-scripts-team
**Phase:** Initial Setup
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

- [ ] P1 #6 PR: Create PR to merge testing-scripts-team → main
  - 2026-02-07
  - 6 commits ready, all test scripts implemented
- [ ] P2 #6 Run test.sh on Verda app server to validate
  - 2026-02-07
  - Requires services running on production

---

# Progress Reports

---
### Implementation Phase
**Repository:** comfyume (https://github.com/ahelme/comfyume)
**Branch:** testing-scripts-team
**Phase:** Initial Setup

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
