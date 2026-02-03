"""
Configuration management for Queue Manager
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Redis Configuration
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_password: str
    redis_db: int = 0

    # Queue Configuration
    queue_mode: str = "fifo"
    enable_priority: bool = True
    job_timeout: int = 3600  # seconds
    max_queue_depth: int = 100

    # Inference Mode: "local" | "redis" | "serverless"
    # - local: GPU on same machine, workers poll Redis queue
    # - redis: Remote GPU via Tailscale, workers poll Redis queue
    # - serverless: Direct HTTP to Verda Serverless (auto-scaling)
    inference_mode: str = "local"

    # Serverless Configuration
    # Primary endpoint (used when serverless_active is not set or "default")
    serverless_endpoint: Optional[str] = None

    # Multi-GPU Serverless Endpoints
    # Usage: Set SERVERLESS_ACTIVE=h200 or SERVERLESS_ACTIVE=b300 to switch
    serverless_endpoint_h200: Optional[str] = None  # H200 SXM5 141GB - $3.29/hr (workshop)
    serverless_endpoint_b300: Optional[str] = None  # B300 SXM6 288GB - $4.95/hr (4K production)
    serverless_active: str = "default"  # "default" | "h200" | "b300"

    # Worker configuration (for local/redis modes)
    num_workers: int = 1

    @property
    def active_serverless_endpoint(self) -> Optional[str]:
        """Get the currently active serverless endpoint based on serverless_active setting"""
        if self.serverless_active == "h200" and self.serverless_endpoint_h200:
            return self.serverless_endpoint_h200
        elif self.serverless_active == "b300" and self.serverless_endpoint_b300:
            return self.serverless_endpoint_b300
        else:
            return self.serverless_endpoint

    @property
    def active_gpu_type(self) -> str:
        """Get human-readable GPU type for logging/health checks"""
        if self.inference_mode != "serverless":
            return "local"
        if self.serverless_active == "h200":
            return "H200-141GB"
        elif self.serverless_active == "b300":
            return "B300-288GB"
        else:
            return "serverless"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 3000
    log_level: str = "INFO"
    debug: bool = False

    # Worker Configuration
    worker_heartbeat_timeout: int = 60  # seconds
    worker_poll_interval: int = 1  # seconds

    # Storage paths
    outputs_path: str = "/outputs"
    inputs_path: str = "/inputs"

    # Application metadata
    app_name: str = "ComfyUI Queue Manager"
    app_version: str = "0.1.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"  # Allow extra fields in .env without validation errors
    )


# Singleton instance
settings = Settings()
