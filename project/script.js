// Function to handle form submission and make a prediction request
async function scanUrl() {
    const url = document.getElementById("urlInput").value;

    if (url) {
        try {
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            });

            const result = await response.json();
            displayResult(result.prediction);

            document.getElementById("urlInput").value = '';
        } catch (error) {
            console.error("Error during the request:", error);
            alert("There was an error processing your request. Please try again.");
        }
    }
}

function displayResult(prediction) {
    const resultDiv = document.getElementById("result");
    if (prediction === "phishing") {
        resultDiv.innerHTML = `<p class="text-red-600 font-bold">WARNING: This URL is likely phishing!</p>`;
    } else {
        resultDiv.innerHTML = `<p class="text-green-600 font-bold">This URL appears legitimate.</p>`;
    }
}



function showPage(page) {
    const homePage = document.getElementById('homePage');
    const reportPage = document.getElementById('reportPage');
    const homeLink = document.getElementById('homeLink');
    const reportLink = document.getElementById('reportLink');
  
    if (page === 'home') {
        homePage.classList.remove('hidden');
        reportPage.classList.add('hidden');
        homeLink.classList.add('active-tab');
        reportLink.classList.remove('active-tab');
    } else if (page === 'report') {
        homePage.classList.add('hidden');
        reportPage.classList.remove('hidden');
        homeLink.classList.remove('active-tab');
        reportLink.classList.add('active-tab');
    }
  }
  
  function toggleForm(formType) {
    const bulkForm = document.getElementById('bulkForm');
    const anonymousForm = document.getElementById('anonymousForm');
  
    if (formType === 'bulk') {
        bulkForm.classList.remove('hidden');
        anonymousForm.classList.add('hidden');
    } else if (formType === 'anonymous') {
        anonymousForm.classList.remove('hidden');
        bulkForm.classList.add('hidden');
    }
  }
