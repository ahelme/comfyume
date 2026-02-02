# Backup Checklist for Verda → R2 Restore

**Project:** ComfyuME v0.11.0
**Created:** 2026-02-02
**Purpose:** Files needed for setup-verda-solo-script.sh restore
**Issue:** #40

---
## Verda SFS Cache & Models Structure

/mnt/sfs/cache/
/mnt/sfs/models/shared/

## R2 Bucket Structure (.env v0.3.2)

```
comfyume-model-vault-backups      (~45GB, Oceania) - Models
comfyume-cache-backups            (~14MB, EU)      - Configs only
comfyume-worker-container-backups (~2.5GB, EU)     - Worker images
comfyume-user-files-backups       (~1GB, EU)       - User data (mello)
```

---

## Files to Backup (Verda → SFS Cache + R2)

### 1. Worker Container → `comfyume-worker-container-backups`

**Source:** Verda GPU instance
**Build & Export:**
```bash
cd /home/dev/comfyume/comfyui-worker
docker build -t comfyume-worker:v0.11.0 .
docker save comfyume-worker:v0.11.0 | gzip > worker-image.tar.gz
md5sum worker-image.tar.gz > worker-image.tar.gz.md5
```
**Copy to SFS Cache**
/mnt/sfs/cache/

**Upload to R2:**
```bash
aws s3 cp worker-image.tar.gz s3://comfyume-worker-container-backups/ --endpoint-url=$R2_ENDPOINT
aws s3 cp worker-image.tar.gz.md5 s3://comfyume-worker-container-backups/ --endpoint-url=$R2_ENDPOINT
```

**Expected:** `worker-image.tar.gz` (~2.5GB compressed)

---

### 2. Portainer Edge Agent → `comfyume-worker-container-backups`

**Source:** Verda GPU instance
**Export:**
```bash
docker save portainer/agent:latest | gzip > portainer-edge-agent.tar.gz
md5sum portainer-edge-agent.tar.gz > portainer-edge-agent.tar.gz.md5
```

**Copy to SFS Cache:** `/mnt/sfs/cache/`

**Upload to R2:**
```bash
aws s3 cp portainer-edge-agent.tar.gz s3://comfyume-worker-container-backups/ --endpoint-url=$R2_ENDPOINT
aws s3 cp portainer-edge-agent.tar.gz.md5 s3://comfyume-worker-container-backups/ --endpoint-url=$R2_ENDPOINT
```

**Expected:** `portainer-edge-agent.tar.gz` (~200MB compressed)

**Note:** Connects via HTTP over Tailscale (not HTTPS)

---

### 3. Config Backup → SFS Cache & R2 `comfyume-cache-backups`

**Source:** Verda GPU instance
**Create tarball:**
```bash
sudo tar -czf verda-config-backup-$DATE.tar.gz \
  -C / \
  var/lib/tailscale \
  etc/ssh/ssh_host_* \
  etc/fail2ban \
  etc/ufw \
  home/dev/ \
  home/root/bash.rc

# From project directory
tar -czf comfyume-project-$DATE.tar.gz \
  -C /home/dev \
  comfyume/.env \
  comfyume/comfyui-worker/docker-compose.yml \
  comfyume/comfyui-worker/worker.py \
  comfyume/comfyui-worker/vram_monitor.py

```
**Copy to SFS Cache**
/mnt/sfs/cache/

**Upload to R2:**
```bash
aws s3 cp verda-config-backup-$DATE.tar.gz s3://comfyume-cache-backups/ --endpoint-url=$R2_ENDPOINT
aws s3 cp comfyume-project-$DATE.tar.gz s3://comfyume-cache-backups/ --endpoint-url=$R2_ENDPOINT
```

**Expected:** `verda-config-backup.tar.gz` (~14MB)

**Contents:**
- `/var/lib/tailscale/` - Preserves Tailscale IP 100.89.38.43
- `/etc/ssh/ssh_host_*` - SSH host keys
- `/etc/fail2ban/` - Security config
- `/etc/ufw/` - Firewall rules
- `/home/dev/.zshrc` - Shell config
- `/home/dev/.oh-my-zsh/custom/` - Bullet-train theme
- `/home/dev/comfyume/.env` - Secrets (REDIS_PASSWORD, etc.)
- `/home/dev/comfyume/comfyui-worker/` - Worker code

---

### 4. Models → SFS Models/Share + R2 `comfyume-model-vault-backups`

**Source:** Copy from SFS `/mnt/sfs/models/` to R2
**Status:** ⚠️ SFS models directory is EMPTY - must populate first!

**Models (v0.11.0 compatible):**
- `checkpoints/ltx-2-19b-dev-fp8.safetensors` (~25GB)
- `checkpoints/flux2_klein_9b.safetensors` (~18GB)
- `checkpoints/flux2_klein_4b.safetensors` (~8GB)
- `text_encoders/gemma_3_12B_it.safetensors` (~20GB)
- `latent_upscale_models/ltx-2-spatial-upscaler-x2-1.0.safetensors` (~2GB)
- `loras/*.safetensors` (camera controls, distilled)

**Step 1: RUNNING NOW! Download models from legacy R2 to SFS (on Verda):**
```bash
# Download from legacy bucket to SFS
aws s3 sync s3://comfy-multi-model-vault-backup/ /mnt/sfs/models/shared/ --endpoint-url=$R2_ENDPOINT
```

**Step 2: Copy from SFS to new R2 bucket:**
```bash
# Upload to new bucket
aws s3 sync /mnt/sfs/models/shared/ s3://comfyume-model-vault-backups/ --endpoint-url=$R2_ENDPOINT
```

**Why two steps?**
- SFS acts as cache for future fast restores (10 Gbps local)
- R2 is permanent backup (internet download speed)
- During workshop: restore from SFS (~5 min) vs R2 (~30+ min)

**Expected:** ~45GB total

---

### 5. User Files (Mello → SFS Cache + R2) → `comfyume-user-files-backups`

**Source:** Mello VPS `/home/dev/projects/comfyume/data/`
**Run on Mello:**
```bash
cd ~/projects/comfymulti-scripts
./backup-mello.sh
```

**Contents:**
- `user_data/user001-020/` - User preferences, settings
- `workflows/*.json` - 5 validated templates (Flux2 Klein, LTX-2)

**Expected:** ~1GB total

**Copy to SFS Cache**
/mnt/sfs/cache
via scp

**Upload to R2**
(repeat steps above for other files - but to comfyume-user-files-backups bucket


### Report to User When Complete & Update GH issue #40


---

## Quick Reference: What Goes Where

| File Type | Source Location | R2 Bucket | Size |
|-----------|----------------|-----------|------|
| Worker container | Verda: docker image | worker-container-backups | ~2.5GB |
| Portainer edge agent | Verda: docker image | worker-container-backups | ~200MB |
| Tailscale identity | Verda: /var/lib/tailscale | cache-backups | ~1MB |
| SSH keys | Verda: /etc/ssh | cache-backups | ~10KB |
| Project .env | Verda: ~/comfyume/.env | cache-backups | ~13KB |
| Worker code | Verda: ~/comfyume/comfyui-worker | cache-backups | ~50KB |
| Shell config | Verda: ~/.zshrc | cache-backups | ~15KB |
| Models | SFS: /mnt/sfs/models OR legacy R2 | model-vault-backups | ~45GB |
| User data | Mello: ~/projects/comfyume/data | user-files-backups | ~1GB |

---

## Backup Order (Recommended)

1. ✅ **Build worker container** (Issue #40 current task)
2. ✅ **Export & upload worker image to R2**
3. ✅ **Export & upload Portainer edge agent to R2**
4. ✅ **Create config backup from Verda**
5. ✅ **Upload config to R2**
6. ⏭️ **Verify models in R2** (reuse legacy OR copy from SFS)
7. ⏭️ **Run backup-mello.sh** (user files from Mello)
8. ✅ **Test restore** - Provision fresh GPU instance

---

## Validation Checklist

Before provisioning GPU instance:
- [ ] Worker image exists in `comfyume-worker-container-backups`
- [ ] Worker image md5 checksum matches
- [ ] Portainer edge agent exists in `comfyume-worker-container-backups`
- [ ] Portainer md5 checksum matches
- [ ] Config backup exists in `comfyume-cache-backups`
- [ ] Tailscale identity in config backup
- [ ] Models exist in `comfyume-model-vault-backups` (~45GB)
- [ ] User files exist in `comfyume-user-files-backups`

---

## Notes

- **Tailscale identity is CRITICAL** - Without it, new instance gets new IP
- **Models can be reused** from legacy comfy-multi bucket (v0.11.0 compatible)
- **Worker must be built on Verda** to ensure CUDA compatibility
- **Config backup must be created BEFORE deleting instance**
