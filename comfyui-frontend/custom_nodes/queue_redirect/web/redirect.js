/**
 * Queue Redirect Extension - ComfyUI v0.11.0
 * Intercepts job submission and redirects to queue-manager
 *
 * CRITICAL: Uses v0.11.0 app.registerExtension() API
 * ❌ OLD (v0.8.2): Standalone script import - BROKEN in v0.9.0+
 * ✅ NEW (v0.9.0+): app.registerExtension() - STABLE API
 */

app.registerExtension({
    name: "comfy.queueRedirect",

    async setup() {
        console.log("[QueueRedirect] Extension loaded (v0.11.0 API)");

        // Get user ID from container environment (set by docker-compose)
        // Each user container has USER_ID env variable (user001, user002, etc.)
        const USER_ID = window.USER_ID || 'unknown';
        console.log(`[QueueRedirect] User ID: ${USER_ID}`);

        // Store original queuePrompt function
        const originalQueuePrompt = app.queuePrompt;

        // Override queuePrompt to redirect to queue-manager
        app.queuePrompt = async function(number, batchCount = 1) {
            console.log(`[QueueRedirect] Intercepting job submission (${batchCount} jobs)`);

            try {
                // Serialize current workflow graph
                const workflow = app.graph.serialize();

                // Submit to queue-manager via /api/queue/submit
                const response = await fetch('/api/queue/submit', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        workflow: workflow,
                        user: USER_ID,
                        batchCount: batchCount
                    })
                });

                if (!response.ok) {
                    const errorText = await response.text();
                    throw new Error(`Queue submission failed (${response.status}): ${errorText}`);
                }

                const result = await response.json();
                console.log(`[QueueRedirect] ✅ Job submitted to queue:`, result);

                // Return result to caller (maintains compatibility with ComfyUI expectations)
                return result;

            } catch (error) {
                console.error("[QueueRedirect] ❌ Failed to submit job:", error);

                // Show user-friendly error in ComfyUI UI
                app.ui.dialog.show(`Job submission failed: ${error.message}`);

                throw error;
            }
        };

        console.log("[QueueRedirect] ✅ Queue interception active");
    }
});
