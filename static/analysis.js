document.addEventListener("DOMContentLoaded", function() {
    // Hide result containers initially
    document.getElementById("analysis-results").style.display = "none";
    document.getElementById("reg-analysis-results").style.display = "none";
});

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
    
    // Assuming we have an endpoint to analyze tax
    fetch(`/analyze_tax?aastamaks=${encodeURIComponent(aastamaksValue)}`)
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner
            document.getElementById("loading-analysis").style.display = "none";
            
            if (data.error) {
                document.getElementById("analysis-error").textContent = data.error;
                document.getElementById("analysis-error").style.display = "block";
            } else {
                // Fill in analysis results
                document.getElementById("higher-tax-count").textContent = 
                    `${data.higher_count} auto eest (${data.higher_percentage}%) tuleb maksta rohkem aastamaksu.`;
                document.getElementById("lower-tax-count").textContent = 
                    `${data.lower_count} auto eest (${data.lower_percentage}%) tuleb maksta vähem aastamaksu.`;
                
                const comparisonText = data.is_below_average 
                    ? `Sinu auto aastamaksu on madalam kui keskmine (${data.average_tax}€).`
                    : `Sinu auto aastamaksu on kõrgem kui keskmine (${data.average_tax}€).`;
                document.getElementById("tax-comparison").textContent = comparisonText;

                // Set progress bar width and line position based on the aastamaks value
                const maxTax = 1700; // Set the maximum value of the tax range
                const minTax = 50;   // Set the minimum value of the tax range
                const taxPercentage = (aastamaksValue - minTax) / (maxTax - minTax) * 100;

                // Adjust the width of the progress bar fill
                document.getElementById("progress-fill").style.width = taxPercentage + '%';

                // Set the line position
                document.getElementById("progress-line").style.left = taxPercentage + '%';
                
                // Fill in similar cars
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


function analyzeRegTasu() {
    const regTasuValue = document.getElementById("regtasu-input").value;
    
    if (!regTasuValue || regTasuValue <= 0) {
        document.getElementById("reg-analysis-error").textContent = "Palun sisesta kehtiv registreerimistasu summa!";
        document.getElementById("reg-analysis-error").style.display = "block";
        return;
    }
    
    // Show loading spinner
    document.getElementById("loading-reg-analysis").style.display = "block";
    document.getElementById("reg-analysis-error").style.display = "none";
    document.getElementById("reg-analysis-results").style.display = "none";
    
    // Assuming we have an endpoint to analyze registration fee
    fetch(`/analyze_reg_fee?regtasu=${encodeURIComponent(regTasuValue)}`)
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner
            document.getElementById("loading-reg-analysis").style.display = "none";
            
            if (data.error) {
                document.getElementById("reg-analysis-error").textContent = data.error;
                document.getElementById("reg-analysis-error").style.display = "block";
            } else {
                // Fill in analysis results
                document.getElementById("higher-reg-count").textContent = 
                    `${data.higher_count} auto eest (${data.higher_percentage}%) tuleb maksta rohkem registreerimistasu.`;
                document.getElementById("lower-reg-count").textContent = 
                    `${data.lower_count} auto eest (${data.lower_percentage}%) tuleb maksta vähem registreerimistasu.`;
                
                const comparisonText = data.is_below_average 
                    ? `Sinu auto registreerimistasu on madalam kui keskmine (${data.average_reg}€).`
                    : `Sinu auto registreerimistasu on kõrgem kui keskmine (${data.average_reg}€).`;
                document.getElementById("reg-comparison").textContent = comparisonText;
                
                // Fill in similar cars
                const similarCarsContainer = document.getElementById("similar-reg-cars-container");
                similarCarsContainer.innerHTML = "";
                
                data.similar_cars.forEach(car => {
                    const carElement = document.createElement("div");
                    carElement.className = "car-result";
                    carElement.innerHTML = `
                        <div class="car-result-details">
                            <div class="car-result-detail">
                                <p><strong>${car.mark} ${car.mudel}</strong> Registreeritud: ${car.esmane_reg} 
                                   Võimsus: ${car.mootori_voimsus} kW Kütus: ${car.kytuse_tyyp} 
                                   Aastamaks: ${car.aastamaks}€ 
                                   Registreerimistasu: <strong>${car.registreerimistasu}€</strong></p>
                            </div>
                        </div>
                    `;
                    similarCarsContainer.appendChild(carElement);
                });
                
                // Show results
                document.getElementById("reg-analysis-results").style.display = "block";
            }
        })
        .catch(error => {
            document.getElementById("loading-reg-analysis").style.display = "none";
            document.getElementById("reg-analysis-error").textContent = "Viga andmete analüüsimisel. Palun proovi uuesti.";
            document.getElementById("reg-analysis-error").style.display = "block";
        });
}