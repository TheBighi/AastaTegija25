document.addEventListener("DOMContentLoaded", function () {
    const markSelect = document.getElementById("mark");
    const mudelSelect = document.getElementById("mudel");

    markSelect.innerHTML = '<option value="">Laeb...</option>';
    mudelSelect.innerHTML = '<option value="">Laeb...</option>';
    
    fetch("/get_brands")
        .then(response => response.json())
        .then(data => {
            const markSelect = document.getElementById("mark");
            data.forEach(brand => {
                let option = document.createElement("option");
                option.value = brand;
                option.textContent = brand;
                markSelect.appendChild(option);
            });
        });
});

function fetchModels() {
    const mark = document.getElementById("mark").value;
    const mudelSelect = document.getElementById("mudel");

    mudelSelect.disabled = !mark;
    mudelSelect.innerHTML = '<option value="">Vali mudel</option>';

    mudelSelect.innerHTML = '<option value="">Laeb...</option>';

    if (mark) {
        fetch(`/get_models?mark=${encodeURIComponent(mark)}`)
            .then(response => response.json())
            .then(data => {
                mudelSelect.innerHTML = '<option value="">Vali mudel</option>'; // Reset with default
                mudelSelect.disabled = false;
                data.forEach(model => {
                    let option = document.createElement("option");
                    option.value = model;
                    option.textContent = model;
                    mudelSelect.appendChild(option);
                });
            });
    }
}

function getTaxOverview() {
    const mark = document.getElementById("mark").value;
    const mudel = document.getElementById("mudel").value;

    if (!mark || !mudel) {
        document.getElementById("error").textContent = "Palun vali mark ja mudel!";
        document.getElementById("error").style.display = "block";
        return;
    }

    // Show loading spinner
    document.getElementById("loading").style.display = "block";
    document.getElementById("error").style.display = "none";
    document.getElementById("results").style.display = "none";

    fetch(`/get_taxes?mark=${encodeURIComponent(mark)}&mudel=${encodeURIComponent(mudel)}`)
        .then(response => response.json())
        .then(data => {
            // Hide loading spinner
            document.getElementById("loading").style.display = "none";
            
            if (data.error) {
                document.getElementById("error").textContent = data.error;
                document.getElementById("error").style.display = "block";
            } else {
                // Display tax information
                document.getElementById("aastamaks").textContent = data.aastamaks;
                document.getElementById("regtasu").textContent = data.regtasu;
                
                // Display car information
                document.getElementById("car-title").textContent = `${data.sample_car.mark} ${data.sample_car.mudel}`;
                document.getElementById("car-year").textContent = data.sample_car.esmane_reg;
                document.getElementById("car-color").textContent = data.sample_car.varv;
                document.getElementById("car-engine").textContent = data.sample_car.mootori_maht;
                document.getElementById("car-power").textContent = data.sample_car.mootori_voimsus;
                document.getElementById("car-fuel").textContent = data.sample_car.kytuse_tyyp;
                
                // Show results
                document.getElementById("results").style.display = "block";
            }
        })
        .catch(error => {
            document.getElementById("loading").style.display = "none";
            document.getElementById("error").textContent = "Viga andmete laadimisel. Palun proovi uuesti.";
            document.getElementById("error").style.display = "block";
        });
}