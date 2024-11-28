document.getElementById('carForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const carData = {
        name: document.getElementById('carName').value,
        manufacturer: document.getElementById('manufacturer').value,
        segment: document.getElementById('segment').value,
        features: document.getElementById('features').value.split(',').map(f => f.trim()),
        price_range: document.getElementById('priceRange').value,
        competitors: document.getElementById('competitors').value.split(',').map(c => c.trim()),
        market_position: document.getElementById('marketPosition').value
    };

    try {
        const response = await fetch('/api/add_car', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(carData)
        });
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        alert('Error adding car: ' + error);
    }
});

document.getElementById('queryForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const queryData = {
        query: document.getElementById('query').value,
        top_k: parseInt(document.getElementById('topK').value)
    };

    try {
        const response = await fetch('/api/query_market', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(queryData)
        });
        const results = await response.json();
        document.getElementById('queryResults').innerHTML = formatResults(results);
    } catch (error) {
        document.getElementById('queryResults').innerHTML = 'Error: ' + error;
    }
});

// Example for the add car form
document.getElementById('carForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoading();
    
    const carData = {
        name: document.getElementById('carName').value,
        manufacturer: document.getElementById('manufacturer').value,
        segment: document.getElementById('segment').value,
        features: document.getElementById('features').value.split(',').map(f => f.trim()),
        price_range: document.getElementById('priceRange').value,
        competitors: document.getElementById('competitors').value.split(',').map(c => c.trim()),
        market_position: document.getElementById('marketPosition').value
    };

    try {
        const response = await fetch('/api/add_car', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(carData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to add car');
        }
        
        const result = await response.json();
        alert(result.message);
        e.target.reset();
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding car: ' + error.message);
    } finally {
        hideLoading();
    }
});

function formatResults(results) {
    return results.map(result => `
        
            ${result.car}
            Similarity: ${(result.similarity * 100).toFixed(2)}%
            Insight: ${result.insight}
            Competitors: ${result.competitors.join(', ')}
        
    `).join('');
}

function formatAnalysis(analysis) {
    return `
        
            ${analysis.car}
            Competitors: ${analysis.competitors.join(', ')}
            Analysis: ${analysis.analysis}
        
    `;
}

