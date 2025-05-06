document.getElementById("scanBtn").addEventListener("click", function () {
    chrome.runtime.sendMessage({ action: "scan" });
});

// Stop Button
document.getElementById("stopBtn").addEventListener("click", function () {
    chrome.runtime.sendMessage({ action: "stop" });
});