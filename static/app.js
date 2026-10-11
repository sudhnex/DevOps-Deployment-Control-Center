const logs = document.getElementById("logs");

function addLog(message) {
    const line = document.createElement("div");
    line.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    logs.prepend(line);
}

async function refreshDashboard() {
    try {
        const [healthResponse, statusResponse, deploymentsResponse] =
            await Promise.all([
                fetch("/health"),
                fetch("/api/status"),
                fetch("/api/deployments")
            ]);

        if (!healthResponse.ok || !statusResponse.ok ||
            !deploymentsResponse.ok) {
            throw new Error("API returned an unsuccessful response");
        }

        const health = await healthResponse.json();
        const status = await statusResponse.json();
        const deployments = await deploymentsResponse.json();

        document.getElementById("app-status").textContent =
            health.status.toUpperCase();
        document.getElementById("uptime").textContent =
            `${status.uptime_seconds} sec`;
        document.getElementById("deployment-count").textContent =
            deployments.length;

        document.getElementById("deployment-table").innerHTML =
            deployments.map(item => `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.service}</td>
                    <td>${item.environment}</td>
                    <td><span class="status ${item.status === "PENDING" ? "pending" : ""}">
                        ${item.status}
                    </span></td>
                </tr>
            `).join("");

        addLog("Health check successful");
    } catch (error) {
        document.getElementById("app-status").textContent = "OFFLINE";
        addLog(`ERROR: ${error.message}`);
    }
}

function clearLogs() {
    logs.replaceChildren();
    addLog("Activity log cleared");
}

function updateClock() {
    document.getElementById("clock").textContent =
        new Date().toLocaleString();
}

refreshDashboard();
updateClock();
setInterval(updateClock, 1000);
setInterval(refreshDashboard, 15000);
