function analyzeAastamaks() {
    const aastamaksValue = document.getElementById("aastamaks-input").value;
    
    if (!aastamaksValue || aastamaksValue <= 0) {
        document.getElementById("analysis-error").textContent = "Palun sisesta kehtiv aastamaksu summa!";
        document.getElementById("analysis-error").style.display = "block";
        return;
    }

    // Show loading spinner
    document.getElementById("loading-analysis").style.display = "block";
    document.getElementById("analysis-error").style.display = "none";
    document.getElementById("analysis-results").style.display = "none";
    
    // Fetch data for tax analysis
    fetch(`/analyze_tax?aastamaks=${encodeURIComponent(aastamaksValue)}`)
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner
            document.getElementById("loading-analysis").style.display = "none";
            
            if (data.error) {
                document.getElementById("analysis-error").textContent = data.error;
                document.getElementById("analysis-error").style.display = "block";
            } else {
                // Special case for aastamaks = 50
                const aastamaksNum = parseFloat(aastamaksValue);
                if (aastamaksNum === 50) {
                    // For aastamaks = 50, we know this is the lowest possible value
                    // So we override certain values
                    document.getElementById("lower-tax-count").textContent = 
                        "0 auto eest (0%) tuleb maksta vähem aastamaksu.";
                    
                    // Keep the higher count from the API result
                    document.getElementById("higher-tax-count").textContent = 
                        `${data.higher_count} auto eest (${data.higher_percentage}%) tuleb maksta rohkem aastamaksu.`;
                    
                    // Keep the comparison text consistent with API
                    const comparisonText = data.is_below_average 
                        ? `Sinu auto aastamaksu on madalam kui keskmine (${data.average_tax}€).`
                        : `Sinu auto aastamaksu on kõrgem kui keskmine (${data.average_tax}€).`;
                    document.getElementById("tax-comparison").textContent = comparisonText;
                    
                    // Always show at 1% position for minimum tax
                    const percentilePosition = 1;
                    document.getElementById("progress-line").style.left = percentilePosition + '%';
                    
                    // Add percentile indicator
                    setPercentileIndicator(percentilePosition);
                } else {
                    // Normal case - use API results
                    document.getElementById("higher-tax-count").textContent = 
                        `${data.higher_count} auto eest (${data.higher_percentage}%) tuleb maksta rohkem aastamaksu.`;
                    document.getElementById("lower-tax-count").textContent = 
                        `${data.lower_count} auto eest (${data.lower_percentage}%) tuleb maksta vähem aastamaksu.`;
                    
                    const comparisonText = data.is_below_average 
                        ? `Sinu auto aastamaksu on madalam kui keskmine (${data.average_tax}€).`
                        : `Sinu auto aastamaksu on kõrgem kui keskmine (${data.average_tax}€).`;
                    document.getElementById("tax-comparison").textContent = comparisonText;

                    // Set the line position
                    document.getElementById("progress-line").style.left = data.lower_percentage + '%';
                    
                    // Add percentile indicator
                    setPercentileIndicator(data.lower_percentage);
                }
                
                // Fill in similar cars - same for both cases
                const similarCarsContainer = document.getElementById("similar-cars-container");
                similarCarsContainer.innerHTML = ""; // Clear previous results
                data.similar_cars.forEach(car => {
                    const carElement = document.createElement("div");
                    carElement.classList.add("car");
                    carElement.innerHTML = `
                        <h4>${car.mark} ${car.mudel}</h4>
                        <p>Aastamaks: ${car.aastamaks}€</p>
                        <p>Registreerimistasu: ${car.registreerimistasu}€</p>
                    `;
                    similarCarsContainer.appendChild(carElement);
                });

                // Show the analysis results
                document.getElementById("analysis-results").style.display = "block";
            }
        });
}

// Helper function to set the percentile indicator
function setPercentileIndicator(percentilePosition) {
    const percentileIndicator = document.getElementById("percentile-indicator") || document.createElement("div");
    percentileIndicator.id = "percentile-indicator";
    percentileIndicator.textContent = `${percentilePosition}%`;
    percentileIndicator.style.left = `${percentilePosition}%`;
    percentileIndicator.classList.add("percentile-text");
    
    const taxPositionChart = document.getElementById("tax-position-chart");
    if (!document.getElementById("percentile-indicator")) {
        taxPositionChart.appendChild(percentileIndicator);
    }
}
