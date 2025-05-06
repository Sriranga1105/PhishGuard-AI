// Modified background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scan") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs.length === 0) return;
      
      const activeTabUrl = tabs[0].url;
      let domain;
      try {
        const urlObj = new URL(activeTabUrl);
        // Only proceed for HTTP/HTTPS URLs
        if (urlObj.protocol !== 'http:' && urlObj.protocol !== 'https:') {
          console.error("Invalid protocol for URL scanning:", activeTabUrl);
          alert("Scanning is only available on regular web pages.");
          return;
        }
        domain = urlObj.hostname;
        // Remove "www." prefix if present
        if (domain.startsWith("www.")) {
          domain = domain.substring(4);
        }
      } catch (err) {
        console.error("Error processing URL:", err);
        return;
      }
      
      // Fetch scan data using the extracted domain name
      fetch(`https://www.urlvoid.com/scan/${domain}/`)
        .then(response => response.text())
        .then(data => {
          const detectionCount = parseDetectionCount(data);
          let riskLevel = "Unknown";
          if (detectionCount) {
            const count = parseInt(detectionCount.split("/")[0]);
            if (count === 1) riskLevel = "⚠ Warning";
            else if (count === 2) riskLevel = "⚠ Maybe Phishing";
            else if (count > 2) riskLevel = "⚠ Dangerous!";
            else riskLevel = "Safe";
          }
          chrome.storage.local.set({ lastScan: domain }, () => {
            chrome.scripting.executeScript({
              target: { tabId: tabs[0].id },
              function: showAlert,
              args: [domain, riskLevel, detectionCount]
            });
          });
        })
        .catch(error => console.error("Error fetching scan data:", error));
    });
  }
});

function parseDetectionCount(html) {
  let regex = /Detections Counts.*?<td[^>]*>.*?<span[^>]*>([\d\/]+)<\/span>/i;
  let match = html.match(regex);
  if (match && match[1]) {
    return match[1].trim();
  }
  return null;
}

function showAlert(domain, riskLevel, detectionCount) {
  const infoUrl = `https://www.urlvoid.com/scan/${domain}/`;
  const message = `🔍 PhishGuard AI\nWebsite: ${domain}\nDetections: ${detectionCount || 'N/A'}\nStatus: ${riskLevel}\n\nMore info: ${infoUrl}`;
  alert(message);
}