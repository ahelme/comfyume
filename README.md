# ComfyuME - ComfyUI v0.11.0 Multi-User Workshop Platform

Multi-user ComfyUI platform for video generation workshops with professional filmmakers.

**Production:** [aiworkshop.art](https://aiworkshop.art) (Verda CPU instance)
**Inference:** Serverless containers on DataCrunch (H200/B300)

---

## Architecture

```
[Users] → HTTPS → [Verda CPU Instance]
                    ├── nginx (SSL, routing)
                    ├── Redis (job queue)
                    ├── queue-manager (FastAPI)
                    ├── admin dashboard
                    └── 20x user frontends (UI only)
                            │
                            ▼ HTTP (serverless)
                   [DataCrunch GPU Containers]
                    ├── H200 141GB (spot/on-demand)
                    └── B300 288GB (spot/on-demand)
```

- **App server** runs on a Verda CPU instance (no GPU needed)
- **Inference** via `INFERENCE_MODE=serverless` — direct HTTP to DataCrunch containers
- **Storage**: SFS for models, block storage for outputs, Cloudflare R2 for backups

---

## Key Features
- 20 isolated ComfyUI web interfaces with HTTP Basic Auth
- Central job queue (FIFO/round-robin/priority)
- Serverless GPU inference (no always-on GPU cost)
- Admin dashboard for instructor
- Comprehensive test suite and monitoring scripts

---

## Structure

```
comfyume/
├── queue-manager/          ← FastAPI job queue + serverless dispatch
├── admin/                  ← Instructor dashboard
├── nginx/                  ← Reverse proxy (SSL, routing, auth)
├── comfyui-frontend/       ← User UI container (v0.11.0)
├── comfyui-worker/         ← GPU worker (local dev/testing only)
├── scripts/                ← Operations & testing scripts
├── data/
│   ├── workflows/          ← 5 templates (Flux2 Klein, LTX-2)
│   ├── models/shared/      ← Model storage (SFS on Verda)
│   ├── user_data/          ← Per-user settings & custom nodes
│   ├── inputs/             ← User uploads
│   └── outputs/            ← Generated files
├── docs/                   ← Admin & testing guides
├── docker-compose.yml      ← Service orchestration
└── .env.example            ← Configuration template (v0.3.5)
```

---

## Status

- Serverless inference working (DataCrunch H200/B300)
- 20 user frontends deployed on Verda CPU instance
- Admin dashboard v2 with GPU switching
- Integration test suite, serverless E2E test, connectivity test
- Production domain: aiworkshop.art with SSL

---

## Configuration

Uses consolidated `.env` file (v0.3.5). See `.env.example` for all variables.

**Key settings:**

| Variable | Value | Purpose |
|----------|-------|---------|
| `INFERENCE_MODE` | `serverless` | Serverless GPU inference (production) |
| `SERVERLESS_ACTIVE` | `h200-spot` | Active GPU endpoint selector |
| `SERVER_MODE` | `dual` | Split app/inference servers |
| `COMFYUI_MODE` | `frontend-testing` | UI only on app server |
| `DOMAIN` | `aiworkshop.art` | Production domain |

For production `.env`, use the consolidated file from [comfymulti-scripts](https://github.com/ahelme/comfymulti-scripts) (private repo).

See [docs/admin-backup-restore.md](docs/admin-backup-restore.md) for deployment guides

---

## 📚 Documentation

- **Issues:** https://github.com/ahelme/comfyume/issues
- **Coordination:** Issue #7 (Mello + Verda teams)
- **Master Task List:** Issue #1
- **Rebuild Plan:** comfy-multi Issue #31

---

---

**Main Branch:** main
**Created:** 2026-01-31
**Updated:** 2026-02-07
