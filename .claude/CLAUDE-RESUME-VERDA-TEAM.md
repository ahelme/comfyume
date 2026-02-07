CLAUDE RESUME - COMFY-MULTI (ASSUMES WELCOME HAS BEEN COMPLETED) 

**PHASE**: VERDA GPU INSTANCE DEPLOYMENT

## TODAY'S GOALS
                                                                              
  Today we are working in parallel with another dev team "Mello team" 
  on our web app ComfyMulti - designed to economically run ComfyUI 
  for a workshop of ~20 professional filmmakers in generating video with AI.            
                                                                              
  We are using a split server setup (though app can be run single-server): 
  frontend-app: APP SERVER / inference worker: INFERENCE SERVER

  APP-SERVER= 'mello'
  INFERENCE-SERVER= 'verda'

## CORE KNOWLEDGE: DEPLOYMENT WORKFLOWS

**Mello Server**
We always run `mello` - main dev server (Hetzner VPS) 
This is where "Mello team" does development (Claude Code).

For our workshop - mello runs ComfyMulti frontend user containers & files, REDIS

**Verda Server**
We don't always run a `verda` - instance on Verda GPU cloud
 
NOTE: we can in fact choose between GPU or CPU instances
e.g. CPU instance for dev/testing / GPU for workshop use

But sometimes - like TODAY! - the "Verda team" does dev on this machine.

For our workshop - we try to choose/run instances/storage on Verda economically.

**Verda Rental:** 
Verda charges rental fees even while following are stopped: 
1. Instance (on OS-BlockStorage) + 
2. Models, backups/restore cache, inference worker container (SFS network drive) + 
3. Scratch (Data-BlockStorage)
  
Hence we tend to want to delete these when possible to avoid some charges: 
Instance/OS-BlockStorage + Scratch/Data-BlockStorage

When in regular use we keep SFS network drive (with our models+worker) so we don't
need to D/L models from storage, and to quickly restore instance from cache.
  
**DURING 'TESTING MONTH' - or - 'WORKSHOP MONTH'**
We create fresh Verda disks & restore from R2: 
SFS (models, cache) +  Instance/OS-BlockStorage (fully set up, running worker).

We format a fresh Data-Block-Storage (scratch disk)
  
Then we retain the SFS on Verda - (faster than re-downloading models etc. from R2!)

But we delete the Instance & Scratch to save $$$.

**DURING 'TESTING DAYS' or 'WORKSHOP DAYS'**
Our SFS is still running - no need to restore it.

We restore our fresh instance (setup, worker etc.) from cache on SFS.

AND add a fresh Data-BlockStorage as our ephemeral scratch disk (user inputs/outputs).
  
**BETWEEN TESTING / WORKSHOP PERIODS**
We delete Verda instance AND Verda SFS AND Verda block storage to save $$.
  
**BACKUPS WHILE VERDA INSTANCE IS RUNNING**
Hrly cron job backs up verda instance OS volume files -> SFS volume
 
**END OF WORKSHOP DAY 1 (PRIOR TO WORKSHOP DAY 2)**
We run additional backup scripts:
  - verda disks (models, container, config) -> R2  
  - mello files -> R2
  
THEN: we delete Verda GPU instance END OF DAY to save highest cost GPU instance $$. 
  - but leave BOTH: SFS (models) and block storage (scratch disk) running.

**NOTE: If we decide to switch to Serverless inference** 
  - we may choose to rent/restore to a much cheaper Verda CPU (NOT GPU) Instance
  - and keep it running during Workshop periods (less backup/restore)
  - IN WHICH CASE we could explore slightly different Verda disk configurations

## SESSION PROGRESS

**Detailed session notes, see:** `.claude/progress-verda-dev.md`

## CURRENT PENDING WORK

**READ TASKS DASHBOARD in: `.claude/progress-verda-dev.md`

## **Critical Constraints:**
- Preserve restore-verda-instance.sh compatibility (was setup-verda-solo-script.sh)
- Never rewrite existing code from scratch

## NEXT STEPS

  Please now:

 - CHECK today's date

 - read IN FULL:
    - `./README.md` - open source project (deployment agnostic)
    - `./CLAUDE.md` - OUR custom deployment on Hetzner / Verda GPU Cloud
    - `.claude/ARCHITECTURE-ASCII.md` - CRITICAL CONTEXT

  - read IN FULL:
    - `.claude/progress-all-teams.md` - Ultra-concise all-teams commit log

  - read top ~250 lines:
    - `./progress-verda-dev.md` - CURRENT TASKS & RECENT progress log

  - read top 70 lines:
    - [Admin Guide](.docs/admin-guide.md) - Admin docs index

  - perform git status & check commit history
    - REPORT: any pending commits/pushes ?
    - REPORT: was progress-verda-dev.md up to date?

  - read list of implementation phases (phased dev plan)
    - **READ lines: 21-35 ONLY**: `./implementation-backup-restore.md`
    - CURRENT PHASE: **Phase 11** Test Single GPU Instance (Restore & Verify)
    - NOTE: context within overall plan

   - Check comfyume Issue #7 last 2x comments - for Mello Team updates

   - Read and print out CURRENT PENDING TASKS from Task Management section:
    - [.claude/progress-verda-dev.md](.claude/progress-verda-dev.md) - See "CURRENT TASKS DASHBOARD"

