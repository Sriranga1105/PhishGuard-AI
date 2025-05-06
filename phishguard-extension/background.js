chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scan") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length === 0) return;

      const activeTabUrl = tabs[0].url;
      let domain;
      try {
        const urlObj = new URL(activeTabUrl);
        if (urlObj.protocol !== 'http:' && urlObj.protocol !== 'https:') {
          alert("Scanning is only available on HTTP/HTTPS pages.");
          return;
        }
        domain = urlObj.href;
      } catch (err) {
        console.error("Invalid URL:", err);
        return;
      }

      fetch("http://localhost:5000/detect", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: domain })
      })
      .then(res => res.json())
      .then(data => {
        let label = data.label === "1" ? "⚠ Phishing Detected!" : "✅ Legitimate";
        let risk = `${(data.confidence * 100).toFixed(2)}%`;
        let info = {
          domain: domain,
          riskLevel: label,
          detectionCount: `Confidence: ${risk}`,
          infoLink: domain
        };

        chrome.storage.local.set({
          lastScan: domain,
          lastRiskLevel: label,
          lastDetectionCount: risk
        }, () => {
          chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            function: showAlert,
            args: [info.domain, info.riskLevel, info.detectionCount]
          });
        });
      })
      .catch(error => console.error("Detection error:", error));
    });
  }
});

function showAlert(domain, riskLevel, detectionCount) {
  const message = `🔍 Phishing Detector\nWebsite: ${domain}\n${riskLevel}\n${detectionCount}`;
  alert(message);
}
