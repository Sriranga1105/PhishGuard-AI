chrome.storage.local.get(["lastScan", "lastRiskLevel", "lastDetectionCount"], function (result) {
  if (result.lastScan && result.lastRiskLevel) {
      let banner = document.createElement("div");
      banner.id = "phishing-banner";
      banner.style.position = "fixed";
      banner.style.top = "0";
      banner.style.left = "0";
      banner.style.width = "100%";
      banner.style.background = "#ff4d4d";
      banner.style.color = "white";
      banner.style.padding = "10px";
      banner.style.textAlign = "center";
      banner.style.zIndex = "9999";
      banner.innerHTML = `⚠ ${result.lastRiskLevel} - Detections: ${result.lastDetectionCount || 'N/A'} ⚠ <a href='https://www.urlvoid.com/scan/${result.lastScan}/' target='_blank' style='color:yellow; text-decoration:underline;'>Info</a>`;
      document.body.prepend(banner);
  }
});