Manage Verda serverless containers. Uses the Verda Python SDK on the Verda server.

**Server:** root@95.216.229.236
**Docs:** https://docs.verda.com/containers/overview
**SDK:** https://github.com/verda-cloud/sdk-python

**Current serverless endpoints (from .env):**
- H200 Spot: `https://containers.datacrunch.io/comfyume-vca-ftv-h200-spot`
- H200 On-Demand: `https://containers.datacrunch.io/comfyume-vca-ftv-h200-on-demand`
- B300 Spot: `https://containers.datacrunch.io/comfyume-vca-ftv-b300-spot`
- B300 On-Demand: `https://containers.datacrunch.io/comfyume-vca-ftv-b300-on-demand`
- Active: `SERVERLESS_ACTIVE=h200-spot`
- API Key: `SERVERLESS_API_KEY` in .env

**Operations (via SSH + Python):**

1. **List deployments:**
```python
ssh root@95.216.229.236 "python3 -c \"
from verda import VerdaClient
import os
client = VerdaClient(os.environ['VERDA_CLIENT_ID'], os.environ['VERDA_CLIENT_SECRET'])
# List all container deployments
print(client.containers.get())
\""
```

2. **Check container health:** Call the endpoint directly:
```bash
ssh root@95.216.229.236 "curl -s -H 'Authorization: Bearer \$SERVERLESS_API_KEY' https://containers.datacrunch.io/comfyume-vca-ftv-h200-spot/health 2>&1 || echo 'No health endpoint'"
```

3. **View container logs:** Check Verda console or use SDK if supported.

4. **OpenTofu management:** See `/verda-terraform` or `/verda-open-tofu` for IaC-based container management.

If $ARGUMENTS is provided, treat it as a specific operation (list, health, logs, restart).
Otherwise show current deployment status.
