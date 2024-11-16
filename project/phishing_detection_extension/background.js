chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    if (changeInfo.status === "complete" && tab.url) {
        // Call the backend API to check if the URL is phishing
        try {
            const response = await fetch("http://localhost:5000/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url: tab.url })
            });
            const data = await response.json();

            // Display alert if URL is phishing
            if (data.prediction === "phishing") {
                chrome.scripting.executeScript({
                    target: { tabId },
                    func: () => alert("Warning: This site is potentially a phishing website!")
                });
            }
        } catch (error) {
            console.error("Error checking URL:", error);
        }
    }
});
