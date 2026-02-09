Loki log aggregation on Verda — query logs with LogQL.

**Server:** root@95.216.229.236
**Port:** 3100
**Config:** `/etc/loki/config.yml`
**Promtail config:** `/etc/promtail/config.yml`
**Retention:** 7 days
**Services:** `systemctl {start|stop|restart|status} loki` / `promtail`

## Common Operations

```bash
# Check Loki is ready
ssh root@95.216.229.236 "curl -s localhost:3100/ready"

# Check Promtail is shipping logs
ssh root@95.216.229.236 "systemctl is-active promtail && curl -s localhost:9080/targets | python3 -m json.tool | head -20"

# Query logs via LogQL API
ssh root@95.216.229.236 "curl -s -G 'localhost:3100/loki/api/v1/query_range' --data-urlencode 'query={container_name=~\"comfy-.*\"}' --data-urlencode 'limit=20' | python3 -m json.tool | head -50"

# Check available labels
ssh root@95.216.229.236 "curl -s localhost:3100/loki/api/v1/labels"

# Check storage usage
ssh root@95.216.229.236 "du -sh /var/lib/loki/"
```

## LogQL Query Syntax

```logql
# All logs from a specific container
{container_name="comfy-queue-manager"}

# Filter by text
{container_name="comfy-queue-manager"} |= "error"

# Exclude pattern
{container_name="comfy-nginx"} != "health"

# Regex filter
{container_name=~"comfy-user.*"} |~ "model|path|mount"

# Multiple filters (AND)
{container_name="comfy-queue-manager"} |= "serverless" |= "error"

# JSON parsing
{container_name="comfy-queue-manager"} | json | level="error"

# Rate of errors (for alerting)
rate({container_name=~"comfy-.*"} |= "error" [5m])
```

## Useful Queries for Our Issues

```logql
# Model path errors (#101)
{container_name=~"comfy-.*"} |~ "No such file|model.*not found|symlink"

# Queue manager serverless errors
{container_name="comfy-queue-manager"} |= "serverless" |= "error"

# Nginx auth/routing issues
{container_name="comfy-nginx"} |~ "401|403|502|504"

# All errors across all containers
{container_name=~"comfy-.*"} |= "error" != "favicon"
```

## Grafana Integration

View logs in Grafana at `http://localhost:3001` → Explore → Select Loki data source → Enter LogQL query.

If $ARGUMENTS provided, treat as a LogQL query or log operation.
