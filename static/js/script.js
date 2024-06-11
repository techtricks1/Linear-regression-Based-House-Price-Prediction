document.getElementById('house-price-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(prediction => {
        if (prediction && prediction.predicted_price !== undefined) {
            document.getElementById('prediction-result').innerText = `Predicted Price: $${prediction.predicted_price}`;
        } else {
            document.getElementById('prediction-result').innerText = `Error: ${prediction.error || 'Unable to get predicted price'}`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('prediction-result').innerText = 'Error: Unable to get predicted price';
    });
});
