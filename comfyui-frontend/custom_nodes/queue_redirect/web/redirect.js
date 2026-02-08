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

        // Extract user ID from URL path (e.g. /user001/ → user001)
        // Falls back to window.USER_ID or 'unknown'
        const pathMatch = window.location.pathname.match(/\/(user\d+)\//);
        const USER_ID = (pathMatch && pathMatch[1]) || window.USER_ID || 'unknown';
        console.log(`[QueueRedirect] User ID: ${USER_ID}`);

        // Store original queuePrompt function
        const originalQueuePrompt = app.queuePrompt;

        // Override queuePrompt to redirect to queue-manager
        // Queue manager endpoint: POST /api/jobs (via nginx /api/ → queue-manager:3000/)
        // nginx strips /api/ prefix, so /api/jobs → queue-manager:3000/api/jobs
        app.queuePrompt = async function(number, batchCount = 1) {
            console.log(`[QueueRedirect] Intercepting job submission (${batchCount} jobs)`);

            try {
                // Serialize current workflow graph
                const workflow = app.graph.serialize();

                // Submit each batch item as a separate job
                let lastResult = null;
                for (let i = 0; i < batchCount; i++) {
                    const response = await fetch('/api/jobs', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            user_id: USER_ID,
                            workflow: workflow,
                            priority: 5,
                            metadata: { batch_index: i, batch_total: batchCount }
                        })
                    });

                    if (!response.ok) {
                        const errorText = await response.text();
                        throw new Error(`Queue submission failed (${response.status}): ${errorText}`);
                    }

                    lastResult = await response.json();
                    console.log(`[QueueRedirect] Job ${i+1}/${batchCount} submitted:`, lastResult);
                }

                console.log(`[QueueRedirect] All ${batchCount} job(s) submitted`);
                return lastResult;

            } catch (error) {
                console.error("[QueueRedirect] Failed to submit job:", error);

                // Show user-friendly error in ComfyUI UI
                app.ui.dialog.show(`Job submission failed: ${error.message}`);

                throw error;
            }
        };

        console.log("[QueueRedirect] ✅ Queue interception active");
    }
});
