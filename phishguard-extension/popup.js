function checkURL(url) {
  document.getElementById("url").textContent = url;
  document.getElementById("status").textContent = "⏳ Analyzing...";
  document.getElementById("risk").textContent = "N/A";

  fetch("http://localhost:5000/detect", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ url: url })
  })
    .then(response => response.json())
    .then(data => {
      if (data.label === "1") {
        document.getElementById("status").innerHTML = "⚠️ <b>Phishing Detected</b>";
        document.getElementById("risk").textContent = `${(data.confidence * 100).toFixed(2)}%`;
        document.body.style.backgroundColor = "#ffdddd";
      } else {
        document.getElementById("status").innerHTML = "✅ <b>Legitimate</b>";
        document.getElementById("risk").textContent = `${(data.confidence * 100).toFixed(2)}%`;
        document.body.style.backgroundColor = "#ddffdd";
      }
    })
    .catch(err => {
      document.getElementById("status").textContent = "❌ Error checking site";
      document.getElementById("risk").textContent = "N/A";
      document.body.style.backgroundColor = "#f8d7da";
    });
}

chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  const url = tabs[0].url;
  checkURL(url);
});
