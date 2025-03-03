document.addEventListener('DOMContentLoaded', function() {
    const aastamaksForm = document.getElementById('aastamaks-form');
    const regtasuForm = document.getElementById('regtasu-form');
    const aastamaksInput = document.getElementById('aastamaks');
    const regtasuInput = document.getElementById('regtasu');
    const resultsContainer = document.getElementById('results-container');
    const carResults = document.getElementById('car-results');
    const resultsCount = document.getElementById('results-count');
    const loadingElement = document.getElementById('loading');
    
    // Tab switching
    const aastamaksTab = document.getElementById('aastamaks-tab');
    const regtasuTab = document.getElementById('regtasu-tab');
    
    aastamaksTab.addEventListener('click', function() {
        aastamaksTab.classList.add('active');
        regtasuTab.classList.remove('active');
        aastamaksForm.classList.add('active');
        regtasuForm.classList.remove('active');
    });
    
    regtasuTab.addEventListener('click', function() {
        regtasuTab.classList.add('active');
        aastamaksTab.classList.remove('active');
        regtasuForm.classList.add('active');
        aastamaksForm.classList.remove('active');
    });
    
    // Aastamaks search form handling
    aastamaksForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const aastamaks = parseFloat(aastamaksInput.value);
        const range = 10;
        
        if (isNaN(aastamaks) || aastamaks < 0) {
            alert('Palun sisestage kehtiv aastamaksu summa');
            return;
        }
        
        // Show loading spinner
        loadingElement.style.display = 'block';
        resultsContainer.style.display = 'none';
        
        // Fetch matching cars
        fetch(`/find_cars_by_tax?aastamaks=${aastamaks}&range=${range}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Hide loading spinner
                loadingElement.style.display = 'none';
                
                // Show results
                displayResults(data, 'aastamaks');
            })
            .catch(error => {
                loadingElement.style.display = 'none';
                alert('Viga andmete laadimisel: ' + error.message);
            });
    });
    
    // Registration fee search form handling
    regtasuForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const regtasu = parseFloat(regtasuInput.value);
        const range = 50; // Larger range for registration fee
        
        if (isNaN(regtasu) || regtasu < 0) {
            alert('Palun sisestage kehtiv registreerimistasu summa');
            return;
        }
        
        // Show loading spinner
        loadingElement.style.display = 'block';
        resultsContainer.style.display = 'none';
        
        // Fetch matching cars
        fetch(`/find_cars_by_regtasu?regtasu=${regtasu}&range=${range}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Hide loading spinner
                loadingElement.style.display = 'none';
                
                // Show results
                displayResults(data, 'regtasu');
            })
            .catch(error => {
                loadingElement.style.display = 'none';
                alert('Viga andmete laadimisel: ' + error.message);
            });
    });
    
    function displayResults(data, type) {
        carResults.innerHTML = '';
        
        if (data.count === 0) {
            if (type === 'aastamaks') {
                resultsCount.textContent = 'Kahjuks ei leitud ühtegi autot vastava aastamaksuga.';
            } else {
                resultsCount.textContent = 'Kahjuks ei leitud ühtegi autot vastava registreerimistasuga.';
            }
        } else {
            if (type === 'aastamaks') {
                resultsCount.textContent = `Leitud ${data.count} autot aastamaksuga ligikaudu ${data.target_tax}€`;
            } else {
                resultsCount.textContent = `Leitud ${data.count} autot registreerimistasuga ligikaudu ${data.target_fee}€`;
            }
            
            data.cars.forEach(car => {
                const carElement = document.createElement('div');
                carElement.className = 'car-result';
                
                const yearFromDate = car.esmane_reg ? car.esmane_reg.split('-')[0] : 'Teadmata';
                
                carElement.innerHTML = `
                    <div class="car-result-title">${car.mark} ${car.mudel} (${yearFromDate})</div>
                    <div class="car-result-details">
                        <div class="car-result-detail">
                            <div class="detail-label">Värv:</div>
                            <div>${car.varv || 'Teadmata'}</div>
                        </div>
                        <div class="car-result-detail">
                            <div class="detail-label">Mootori maht:</div>
                            <div>${car.mootori_maht || 'Teadmata'} cm³</div>
                        </div>
                        <div class="car-result-detail">
                            <div class="detail-label">Võimsus:</div>
                            <div>${car.mootori_voimsus || 'Teadmata'} kW</div>
                        </div>
                        <div class="car-result-detail">
                            <div class="detail-label">Kütuse tüüp:</div>
                            <div>${car.kytuse_tyyp || 'Teadmata'}</div>
                        </div>
                        <div class="car-result-detail">
                            <div class="detail-label">Aastamaks:</div>
                            <div class="${type === 'aastamaks' ? 'tax-highlight' : ''}">${car.aastamaks.toFixed(2)}€</div>
                        </div>
                        <div class="car-result-detail">
                            <div class="detail-label">Registreerimistasu:</div>
                            <div class="${type === 'regtasu' ? 'tax-highlight' : ''}">${car.registreerimistasu.toFixed(2)}€</div>
                        </div>
                    </div>
                `;
                
                carResults.appendChild(carElement);
            });
        }
        
        resultsContainer.style.display = 'block';
    }
});