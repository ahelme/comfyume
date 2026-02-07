"""
Admin Dashboard V2 - Comprehensive Management UI for ComfyUI Workshop

Phase 1: System Status, Container Management (Issue #65)
Phase 2: GPU Deployment Switching (Issue #66)
Phase 3: Storage & R2 Management (Issue #67)
"""
import logging
import secrets
import shutil
import os
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, JSONResponse
import httpx

# Optional: Docker SDK for container management
try:
    import docker
    docker_client = docker.from_env()
    DOCKER_AVAILABLE = True
except Exception:
    docker_client = None
    DOCKER_AVAILABLE = False

# Optional: Redis for direct status checks
try:
    import redis as redis_lib
    REDIS_LIB_AVAILABLE = True
except ImportError:
    REDIS_LIB_AVAILABLE = False

# Optional: boto3 for R2 storage management
try:
    import boto3
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
QUEUE_MANAGER_URL = os.getenv("QUEUE_MANAGER_URL", "http://queue-manager:3000")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "change_me_secure_password")
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
ENV_FILE_PATH = os.getenv("ENV_FILE_PATH", "/app/project.env")

# R2 Configuration
R2_ENDPOINT = os.getenv("R2_ENDPOINT", "")
R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY_ID", "")
R2_SECRET_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
R2_BUCKETS = [
    "comfyume-model-vault-backups",
    "comfyume-cache-backups",
    "comfyume-worker-container-backups",
    "comfyume-user-files-backups",
]

# GPU Deployment options (serverless via DataCrunch)
GPU_DEPLOYMENTS = {
    "h200-spot": {
        "name": "H200 Spot",
        "gpu": "H200 SXM5",
        "vram": "141GB HBM3e",
        "price_eur": 0.97,
        "price_label": "\u20ac0.97/hr",
        "type": "spot",
        "best_for": "Workshop, testing, cost-sensitive",
        "bandwidth": "4.8 TB/s",
    },
    "h200-on-demand": {
        "name": "H200 On-Demand",
        "gpu": "H200 SXM5",
        "vram": "141GB HBM3e",
        "price_eur": 2.80,
        "price_label": "\u20ac2.80/hr",
        "type": "on-demand",
        "best_for": "Important demos, guaranteed availability",
        "bandwidth": "4.8 TB/s",
    },
    "b300-spot": {
        "name": "B300 Spot",
        "gpu": "B300 SXM6",
        "vram": "288GB HBM3e",
        "price_eur": 1.61,
        "price_label": "\u20ac1.61/hr",
        "type": "spot",
        "best_for": "4K experimentation, cheap 4K",
        "bandwidth": "8.0 TB/s",
    },
    "b300-on-demand": {
        "name": "B300 On-Demand",
        "gpu": "B300 SXM6",
        "vram": "288GB HBM3e",
        "price_eur": 4.63,
        "price_label": "\u20ac4.63/hr",
        "type": "on-demand",
        "best_for": "Boss demo 4K, critical 4K production",
        "bandwidth": "8.0 TB/s",
    },
}

app = FastAPI(title="ComfyUI Admin Dashboard V2", version="2.0.0")

# HTTP Basic Auth
security = HTTPBasic()


def verify_admin(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """Verify admin credentials using constant-time comparison"""
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        logger.warning(f"Failed login attempt: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# HTTP client for queue manager
http_client = httpx.AsyncClient(timeout=10.0)

# Redis client for direct status checks
redis_direct = None
if REDIS_LIB_AVAILABLE and REDIS_PASSWORD:
    try:
        redis_direct = redis_lib.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            decode_responses=True,
            socket_timeout=3,
            socket_connect_timeout=3,
        )
    except Exception as e:
        logger.warning(f"Redis direct connection failed: {e}")


# Load dashboard HTML at startup
DASHBOARD_HTML = ""
dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.html")
if os.path.exists(dashboard_path):
    with open(dashboard_path, "r") as f:
        DASHBOARD_HTML = f.read()
else:
    DASHBOARD_HTML = "<html><body><h1>Dashboard HTML not found</h1></body></html>"
    logger.warning(f"Dashboard HTML not found at {dashboard_path}")


@app.get("/", response_class=HTMLResponse)
async def dashboard(username: str = Depends(verify_admin)):
    """Serve the admin dashboard"""
    return HTMLResponse(content=DASHBOARD_HTML)


# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint (no auth required)"""
    return {"status": "healthy", "service": "admin-dashboard", "version": "2.0.0"}


# ============================================================================
# System Status (Phase 1 - Issue #65)
# ============================================================================

@app.get("/api/system/status")
async def system_status(username: str = Depends(verify_admin)):
    """Overall system health: Redis, Queue Manager, Serverless"""
    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {},
        "docker_available": DOCKER_AVAILABLE,
    }

    # Redis status
    redis_ok = False
    redis_info = {}
    if redis_direct:
        try:
            redis_ok = redis_direct.ping()
            mem_info = redis_direct.info("memory")
            client_info = redis_direct.info("clients")
            redis_info = {
                "used_memory_human": mem_info.get("used_memory_human", "unknown"),
                "connected_clients": client_info.get("connected_clients", 0),
            }
        except Exception as e:
            logger.error(f"Redis check failed: {e}")
    result["services"]["redis"] = {"healthy": redis_ok, "info": redis_info}

    # Queue Manager status
    qm_ok = False
    qm_data = {}
    try:
        resp = await http_client.get(f"{QUEUE_MANAGER_URL}/health")
        if resp.status_code == 200:
            qm_ok = True
            qm_data = resp.json()
    except Exception as e:
        logger.error(f"Queue manager check failed: {e}")
    result["services"]["queue_manager"] = {"healthy": qm_ok, "info": qm_data}

    # Queue stats
    try:
        resp = await http_client.get(f"{QUEUE_MANAGER_URL}/api/queue/status")
        if resp.status_code == 200:
            result["queue"] = resp.json()
    except Exception:
        result["queue"] = None

    # Disk usage
    usage = shutil.disk_usage("/")
    result["disk"] = {
        "total_gb": round(usage.total / (1024**3), 1),
        "used_gb": round(usage.used / (1024**3), 1),
        "free_gb": round(usage.free / (1024**3), 1),
        "percent_used": round(usage.used / usage.total * 100, 1),
    }

    return result


# ============================================================================
# Container Management (Phase 1 - Issue #65)
# ============================================================================

@app.get("/api/containers")
async def list_containers(username: str = Depends(verify_admin)):
    """List Docker containers (filtered to comfy- prefix)"""
    if not DOCKER_AVAILABLE:
        return {"error": "Docker not available. Mount /var/run/docker.sock to enable.", "containers": []}

    try:
        containers = docker_client.containers.list(all=True, filters={"name": "comfy"})
        result = []
        for c in containers:
            result.append({
                "id": c.short_id,
                "name": c.name,
                "status": c.status,
                "state": c.attrs.get("State", {}).get("Status", "unknown"),
                "image": c.image.tags[0] if c.image.tags else str(c.image.id[:12]),
                "created": c.attrs.get("Created", ""),
                "health": c.attrs.get("State", {}).get("Health", {}).get("Status", "none"),
            })
        # Sort: services first (redis, queue-manager, admin), then users
        result.sort(key=lambda x: (
            0 if "redis" in x["name"] else
            1 if "queue" in x["name"] else
            2 if "admin" in x["name"] else
            3 if "nginx" in x["name"] else
            4,
            x["name"]
        ))
        return {"containers": result}
    except Exception as e:
        logger.error(f"Container list failed: {e}")
        return {"error": str(e), "containers": []}


@app.post("/api/containers/{container_name}/restart")
async def restart_container(container_name: str, username: str = Depends(verify_admin)):
    """Restart a container (restricted to comfy- prefix)"""
    if not DOCKER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Docker not available")
    if not container_name.startswith("comfy-"):
        raise HTTPException(status_code=403, detail="Can only manage comfy- containers")

    try:
        container = docker_client.containers.get(container_name)
        container.restart(timeout=30)
        logger.info(f"Container {container_name} restarted by {username}")
        return {"status": "restarted", "container": container_name}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {container_name} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/containers/{container_name}/stop")
async def stop_container(container_name: str, username: str = Depends(verify_admin)):
    """Stop a container (restricted to comfy- prefix)"""
    if not DOCKER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Docker not available")
    if not container_name.startswith("comfy-"):
        raise HTTPException(status_code=403, detail="Can only manage comfy- containers")

    try:
        container = docker_client.containers.get(container_name)
        container.stop(timeout=30)
        logger.info(f"Container {container_name} stopped by {username}")
        return {"status": "stopped", "container": container_name}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {container_name} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/containers/{container_name}/start")
async def start_container(container_name: str, username: str = Depends(verify_admin)):
    """Start a stopped container (restricted to comfy- prefix)"""
    if not DOCKER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Docker not available")
    if not container_name.startswith("comfy-"):
        raise HTTPException(status_code=403, detail="Can only manage comfy- containers")

    try:
        container = docker_client.containers.get(container_name)
        container.start()
        logger.info(f"Container {container_name} started by {username}")
        return {"status": "started", "container": container_name}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {container_name} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/containers/{container_name}/logs")
async def container_logs(container_name: str, lines: int = 100, username: str = Depends(verify_admin)):
    """Get container logs (restricted to comfy- prefix)"""
    if not DOCKER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Docker not available")
    if not container_name.startswith("comfy-"):
        raise HTTPException(status_code=403, detail="Can only manage comfy- containers")

    try:
        container = docker_client.containers.get(container_name)
        logs = container.logs(tail=lines, timestamps=True).decode("utf-8", errors="replace")
        return {"container": container_name, "logs": logs}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {container_name} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# GPU Deployment Switching (Phase 2 - Issue #66)
# ============================================================================

@app.get("/api/gpu/status")
async def gpu_status(username: str = Depends(verify_admin)):
    """Get current GPU deployment status"""
    current = {
        "inference_mode": "unknown",
        "active_gpu": "unknown",
        "serverless_active": "unknown",
    }

    # Get live status from queue manager
    try:
        resp = await http_client.get(f"{QUEUE_MANAGER_URL}/health")
        if resp.status_code == 200:
            data = resp.json()
            current.update({
                "inference_mode": data.get("inference_mode", "unknown"),
                "active_gpu": data.get("active_gpu", "unknown"),
                "serverless_endpoint": data.get("serverless_endpoint"),
                "status": data.get("status", "unknown"),
                "queue_depth": data.get("queue_depth", 0),
            })
    except Exception as e:
        logger.error(f"GPU status check failed: {e}")

    # Also read .env for SERVERLESS_ACTIVE
    try:
        if os.path.exists(ENV_FILE_PATH):
            with open(ENV_FILE_PATH) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("SERVERLESS_ACTIVE="):
                        current["serverless_active"] = line.split("=", 1)[1]
                    elif line.startswith("INFERENCE_MODE="):
                        current["inference_mode_env"] = line.split("=", 1)[1]
    except Exception:
        pass

    return {
        "current": current,
        "deployments": GPU_DEPLOYMENTS,
    }


@app.post("/api/gpu/switch")
async def switch_gpu(body: dict, username: str = Depends(verify_admin)):
    """Switch GPU deployment: update .env and restart queue-manager"""
    mode = body.get("mode", "")

    if mode == "local":
        inference_mode = "local"
        serverless_active = "default"
    elif mode in GPU_DEPLOYMENTS:
        inference_mode = "serverless"
        serverless_active = mode
    else:
        valid = list(GPU_DEPLOYMENTS.keys()) + ["local"]
        raise HTTPException(status_code=400, detail=f"Invalid mode: {mode}. Valid: {valid}")

    # Update .env file
    if os.path.exists(ENV_FILE_PATH):
        try:
            with open(ENV_FILE_PATH, "r") as f:
                lines = f.readlines()

            new_lines = []
            found_inference = False
            found_active = False
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("INFERENCE_MODE="):
                    new_lines.append(f"INFERENCE_MODE={inference_mode}\n")
                    found_inference = True
                elif stripped.startswith("SERVERLESS_ACTIVE="):
                    new_lines.append(f"SERVERLESS_ACTIVE={serverless_active}\n")
                    found_active = True
                else:
                    new_lines.append(line)

            if not found_inference:
                new_lines.append(f"INFERENCE_MODE={inference_mode}\n")
            if not found_active:
                new_lines.append(f"SERVERLESS_ACTIVE={serverless_active}\n")

            with open(ENV_FILE_PATH, "w") as f:
                f.writelines(new_lines)

            logger.info(f"GPU switched to {mode} by {username}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update .env: {e}")
    else:
        logger.warning(f".env file not found at {ENV_FILE_PATH}")

    # Restart queue-manager to apply new config
    restart_result = "skipped (no Docker)"
    if DOCKER_AVAILABLE:
        try:
            qm = docker_client.containers.get("comfy-queue-manager")
            qm.restart(timeout=30)
            restart_result = "restarted"
            logger.info("Queue manager restarted after GPU switch")
        except Exception as e:
            restart_result = f"failed: {e}"
            logger.error(f"Queue manager restart failed: {e}")

    return {
        "status": "switched",
        "mode": mode,
        "inference_mode": inference_mode,
        "serverless_active": serverless_active,
        "queue_manager_restart": restart_result,
    }


# ============================================================================
# Storage Management (Phase 3 - Issue #67)
# ============================================================================

@app.get("/api/storage/disk")
async def storage_disk(username: str = Depends(verify_admin)):
    """Disk usage breakdown by directory"""
    usage = shutil.disk_usage("/")

    dirs = {}
    check_paths = [
        ("/outputs", "User Outputs"),
        ("/inputs", "User Inputs"),
        ("/models", "Models"),
        ("/workflows", "Workflows"),
    ]

    for path, label in check_paths:
        if os.path.exists(path):
            try:
                total = 0
                count = 0
                for f in Path(path).rglob("*"):
                    if f.is_file():
                        total += f.stat().st_size
                        count += 1
                dirs[label] = {
                    "path": path,
                    "size_gb": round(total / (1024**3), 2),
                    "size_human": _human_size(total),
                    "file_count": count,
                }
            except PermissionError:
                dirs[label] = {"path": path, "error": "permission denied"}
        else:
            dirs[label] = {"path": path, "error": "not mounted"}

    return {
        "disk": {
            "total_gb": round(usage.total / (1024**3), 1),
            "used_gb": round(usage.used / (1024**3), 1),
            "free_gb": round(usage.free / (1024**3), 1),
            "percent_used": round(usage.used / usage.total * 100, 1),
        },
        "directories": dirs,
    }


@app.get("/api/storage/r2")
async def storage_r2(username: str = Depends(verify_admin)):
    """R2 bucket sizes and object counts"""
    if not BOTO3_AVAILABLE or not R2_ENDPOINT:
        return {"error": "R2 not configured (set R2_ENDPOINT, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY)", "buckets": []}

    try:
        s3 = boto3.client(
            "s3",
            endpoint_url=R2_ENDPOINT,
            aws_access_key_id=R2_ACCESS_KEY,
            aws_secret_access_key=R2_SECRET_KEY,
        )

        buckets = []
        for bucket_name in R2_BUCKETS:
            try:
                total_size = 0
                total_objects = 0
                paginator = s3.get_paginator("list_objects_v2")
                for page in paginator.paginate(Bucket=bucket_name):
                    for obj in page.get("Contents", []):
                        total_size += obj["Size"]
                        total_objects += 1

                buckets.append({
                    "name": bucket_name,
                    "objects": total_objects,
                    "size_gb": round(total_size / (1024**3), 2),
                    "size_human": _human_size(total_size),
                    "status": "ok",
                })
            except Exception as e:
                buckets.append({
                    "name": bucket_name,
                    "error": str(e),
                    "status": "error",
                })

        return {"buckets": buckets}
    except Exception as e:
        return {"error": str(e), "buckets": []}


@app.get("/api/storage/browse")
async def storage_browse(path: str = "/", username: str = Depends(verify_admin)):
    """Browse directory contents (restricted to allowed roots)"""
    allowed_roots = ["/outputs", "/inputs", "/models", "/workflows"]

    clean_path = os.path.normpath(path)

    # Security: prevent directory traversal
    if ".." in clean_path:
        raise HTTPException(status_code=403, detail="Directory traversal not allowed")

    if not any(clean_path.startswith(root) for root in allowed_roots) and clean_path != "/":
        raise HTTPException(status_code=403, detail="Access restricted to: /outputs, /inputs, /models, /workflows")

    if clean_path == "/":
        entries = []
        for root in allowed_roots:
            exists = os.path.exists(root)
            entries.append({
                "name": root.lstrip("/"),
                "type": "directory",
                "path": root,
                "exists": exists,
            })
        return {"path": "/", "entries": entries}

    if not os.path.exists(clean_path):
        raise HTTPException(status_code=404, detail=f"Path not found: {clean_path}")

    if not os.path.isdir(clean_path):
        stat = os.stat(clean_path)
        return {
            "path": clean_path,
            "type": "file",
            "size": stat.st_size,
            "size_human": _human_size(stat.st_size),
            "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        }

    entries = []
    try:
        with os.scandir(clean_path) as scanner:
            for entry in sorted(scanner, key=lambda e: (not e.is_dir(), e.name)):
                info = {
                    "name": entry.name,
                    "type": "directory" if entry.is_dir() else "file",
                    "path": entry.path,
                }
                if entry.is_file():
                    try:
                        stat = entry.stat()
                        info["size"] = stat.st_size
                        info["size_human"] = _human_size(stat.st_size)
                        info["modified"] = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()
                    except (PermissionError, OSError):
                        info["error"] = "stat failed"
                entries.append(info)
    except PermissionError:
        raise HTTPException(status_code=403, detail="Permission denied")

    return {"path": clean_path, "entries": entries}


def _human_size(size_bytes: int) -> str:
    """Convert bytes to human-readable size"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


# ============================================================================
# Queue Proxy (proxies to queue-manager for frontend use)
# ============================================================================

@app.get("/api/queue/status")
async def proxy_queue_status(username: str = Depends(verify_admin)):
    """Proxy queue status from queue-manager"""
    try:
        response = await http_client.get(f"{QUEUE_MANAGER_URL}/api/queue/status")
        return response.json()
    except Exception as e:
        logger.error(f"Queue status proxy failed: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/queue/jobs")
async def proxy_jobs(limit: int = 50, username: str = Depends(verify_admin)):
    """Proxy job list from queue-manager"""
    try:
        response = await http_client.get(f"{QUEUE_MANAGER_URL}/api/jobs?limit={limit}")
        return response.json()
    except Exception as e:
        logger.error(f"Jobs proxy failed: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.delete("/api/queue/jobs/{job_id}")
async def proxy_cancel_job(job_id: str, username: str = Depends(verify_admin)):
    """Proxy job cancellation to queue-manager"""
    try:
        response = await http_client.delete(f"{QUEUE_MANAGER_URL}/api/jobs/{job_id}")
        if response.status_code == 204:
            return {"status": "cancelled", "job_id": job_id}
        return JSONResponse(status_code=response.status_code, content=response.json())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/api/queue/jobs/{job_id}/priority")
async def proxy_update_priority(job_id: str, body: dict, username: str = Depends(verify_admin)):
    """Proxy priority update to queue-manager"""
    try:
        response = await http_client.patch(
            f"{QUEUE_MANAGER_URL}/api/jobs/{job_id}/priority",
            json=body
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8080, log_level="info")
