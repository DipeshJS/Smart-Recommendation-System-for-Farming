function startPrediction() {
    window.location.href = "input_page.html";
}

function navigateToOutputPage(event) {
    // Prevent the default form submission behavior
    event.preventDefault();
    
    // Navigate to the output page
    window.location.href = "output_page.html";
}


function predict() {
    // Get form data
    var formData = {
        Rainfall: parseFloat(document.getElementById('Rainfall').value),
        Temperature: parseFloat(document.getElementById('Temperature').value),
        Humidity: parseFloat(document.getElementById('Humidity').value),
        Nitrogen: parseFloat(document.getElementById('Nitrogen').value),
        Phosporus: parseFloat(document.getElementById('Phosporus').value),
        Potassium: parseFloat(document.getElementById('Potassium').value),
        Ph: parseFloat(document.getElementById('Ph').value)
    };

    console.log(formData);

    // Send form data to the server for prediction
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
    return response.text();
    })
    .then(html => {
        // Replace current page content with the output page content
        document.open();
        document.write(html);
        document.close();
    })
    .catch(error => console.error('Error:', error));
}

function redirectToHomepage() {
    window.location.href = "index.html";
}

