const RESPONSE_STYLES = {
    ok: "border rounded p-3 alert-success",
    error: "border rounded p-3 alert-danger",
    pending: "border rounded p-3 bg-light text-muted",
};

function showResponse(message, style) {
    const box = document.getElementById("system_response");
    box.className = RESPONSE_STYLES[style];
    box.textContent = message;
}

async function RunEmotionDetection() {
    const text = document.getElementById("textToAnalyze").value;
    const button = document.getElementById("analyzeButton");

    button.disabled = true;
    showResponse("Analyzing...", "pending");
    try {
        const response = await fetch(
            "emotionDetector?textToAnalyze=" + encodeURIComponent(text)
        );
        showResponse(await response.text(), response.ok ? "ok" : "error");
    } catch (err) {
        showResponse("Could not reach the server. Please try again.", "error");
    } finally {
        button.disabled = false;
    }
}

// Name used by the original course template.
const RunSentimentAnalysis = RunEmotionDetection;

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("textToAnalyze").addEventListener("keydown", (event) => {
        if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
            RunEmotionDetection();
        }
    });
});
