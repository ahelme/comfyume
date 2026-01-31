# ComfyUme - ComfyUI v0.11.0 Multi-User Workshop Platform

**Clean rebuild of comfy-multi for ComfyUI v0.11.0**

🎯 **Workshop-ready multi-user ComfyUI platform** for video generation workshops with professional filmmakers.

---

## 🚀 What's Different from comfy-multi?

### Clean Architecture
- **ComfyUI as immutable dependency** - No core modifications!
- **v0.11.0 stable** - NOT v0.11.1 (has critical bugs)
- **Extension API pattern** - app.registerExtension() (STABLE)
- **Worker API unchanged** - Proven queue-manager copied exactly

### Key Improvements
- ✅ Custom nodes backup (fixes volume mount trap)
- ✅ Version-aware paths (/comfyui/user/default/workflows/)
- ✅ URL-encoded userdata API (workflows%2Ffile.json)
- ✅ Health checks with /system_stats endpoint
- ✅ requests in requirements.txt (no manual install!)

---

## 📦 What We Kept (70% of code!)

**Unchanged from comfy-multi:**
- queue-manager/ - Worker API stable across v0.8.2 → v0.11.1
- admin/ - Dashboard works perfectly
- nginx/ - Generic service names (no path changes!)
- scripts/ - Utility scripts preserved
- docker-compose.yml - Orchestration patterns proven

---

## 🔨 What We Rebuilt (30% - Frontend only!)

**comfyui-frontend/** - Completely rebuilt for v0.11.0:
- Dockerfile - ComfyUI v0.11.0 as immutable base
- docker-entrypoint.sh - Version-aware initialization
- custom_nodes/default_workflow_loader/ - v0.11.0 extension API
- custom_nodes/queue_redirect/ - v0.11.0 extension API

---

## 📂 Structure

```
comfyume/
├── queue-manager/          ← CPU service (unchanged)
├── admin/                  ← Dashboard (unchanged)
├── nginx/                  ← Reverse proxy (unchanged)
├── scripts/                ← Utilities (preserved)
├── comfyui-frontend/       ← REBUILT for v0.11.0
│   ├── Dockerfile
│   ├── docker-entrypoint.sh
│   └── custom_nodes/
│       ├── default_workflow_loader/
│       └── queue_redirect/
├── data/
│   ├── workflows/          ← 5 templates (Flux2 Klein, LTX-2)
│   ├── models/shared/      ← Model storage
│   ├── user_data/          ← User settings
│   ├── inputs/             ← User uploads
│   └── outputs/            ← Generated files
├── docker-compose.yml      ← Service orchestration
└── .env.example            ← Configuration template
```

---

## 🏗️ Build Status

**Phase:** Phase 1 Frontend COMPLETE ✅
**Docker Image:** `comfyume-frontend:v0.11.0` (1.85GB)
**Commits:** 2 pushed to mello-track
**Issues Closed:** 8/8 (Foundation #9-12 + Frontend #13-16)

---

## 🎯 Next Steps

1. **Workflow Templates** - Update for v0.11.0 validation (Issue #17)
2. **Integration Testing** - Frontend + queue-manager + worker (Issue #18)
3. **Multi-User Testing** - 20 users concurrent (Issue #19)
4. **Workshop Readiness** - Final validation (Issue #20)

---

## 📚 Documentation

- **Issues:** https://github.com/ahelme/comfyume/issues
- **Coordination:** Issue #7 (Mello + Verda teams)
- **Master Task List:** Issue #1
- **Rebuild Plan:** comfy-multi Issue #31

---

## 🤝 Credits

Built with systematic precision, documented with love.

**Research Foundation:** 14 AI agents, 11,320 lines of analysis
**Key Insight:** Worker API stable (focus rebuild on frontend!)
**Timeline:** Ahead of schedule (2 hours vs 6-8 hour estimate)

---

**Branch:** mello-track
**Created:** 2026-01-31
**Status:** 🟢 Building momentum!
