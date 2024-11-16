document.getElementById("checkButton").addEventListener("click", async () => {
    const urlInput = document.getElementById("urlInput").value;
    const resultElement = document.getElementById("result");

    if (!urlInput) {
        resultElement.textContent = "Please enter a URL.";
        resultElement.style.color = "red";
        return;
    }

    // Make API request to backend for phishing detection
    try {
        const response = await fetch("http://localhost:5000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: urlInput })
        });
        const data = await response.json();
        if (data.prediction === "phishing") {
            resultElement.textContent = "This URL is likely a phishing site!";
            resultElement.style.color = "red";
        } else {
            resultElement.textContent = "This URL is likely safe.";
            resultElement.style.color = "green";
        }
    } catch (error) {
        resultElement.textContent = "Error connecting to the server.";
        resultElement.style.color = "red";
    }
});
