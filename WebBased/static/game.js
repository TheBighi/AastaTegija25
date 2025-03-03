document.addEventListener('DOMContentLoaded', function() {
    const carElements = [
        document.getElementById('car-0'),
        document.getElementById('car-1')
    ];
    
    const messageElement = document.getElementById('message');
    const scoreElement = document.querySelector('#score span');
    const nextRoundButton = document.getElementById('next-round');
    const restartButton = document.getElementById('restart');
    
    let score = 0;
    let currentCorrectIndex = null;
    
    // Initialize game
    loadNewRound();
    
    // Button event listeners
    document.querySelectorAll('.select-button').forEach(button => {
        button.addEventListener('click', function() {
            const selectedIndex = parseInt(this.getAttribute('data-index'));
            checkAnswer(selectedIndex);
        });
    });
    
    nextRoundButton.addEventListener('click', function() {
        blankOutCarDetails(); // Blank out details when new round starts
        resetCarStyles();
        loadNewRound();
        this.style.display = 'none';
    });
    
    restartButton.addEventListener('click', function() {
        score = 0;
        scoreElement.textContent = score;
        blankOutCarDetails();
        resetCarStyles();
        loadNewRound();
        this.style.display = 'none';
        messageElement.textContent = '';
    });
    
    function loadNewRound() {
        fetch('/get_car_options')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Store the correct answer
                currentCorrectIndex = data.correct_index;
                
                // Update target values
                document.querySelector('#target-aastamaks span').textContent = 
                    data.target.aastamaks.toFixed(2);
                document.querySelector('#target-registreerimistasu span').textContent = 
                    data.target.registreerimistasu.toFixed(2);
                
                // Update car info
                for (let i = 0; i < 2; i++) {
                    const car = data.cars[i];
                    carElements[i].querySelector('.car-title').textContent = 
                        `${car.mark} ${car.mudel}`;
                    carElements[i].querySelector('.car-year').textContent = 
                        car.esmane_reg.split('-')[0]; // Extract year
                    carElements[i].querySelector('.car-color').textContent = 
                        car.varv || 'Teadmata';
                    carElements[i].querySelector('.car-engine-size').textContent = 
                        car.mootori_maht || 'Teadmata';
                    carElements[i].querySelector('.car-power').textContent = 
                        car.mootori_voimsus || 'Teadmata';
                    carElements[i].querySelector('.car-fuel').textContent = 
                        car.kytuse_tyyp || 'Teadmata';
                }
                
                // Enable buttons
                document.querySelectorAll('.select-button').forEach(button => {
                    button.disabled = false;
                });
            })
            .catch(error => {
                console.error('Error fetching car options:', error);
                messageElement.textContent = 'Viga andmete laadimisel. Palun proovi uuesti.';
                messageElement.style.color = 'red';
            });
    }
    
    function checkAnswer(selectedIndex) {
        // Disable all buttons to prevent multiple selections
        document.querySelectorAll('.select-button').forEach(button => {
            button.disabled = true;
        });
        
        if (selectedIndex === currentCorrectIndex) {
            // Correct answer
            score++;
            scoreElement.textContent = score;
            carElements[selectedIndex].classList.add('correct');
            messageElement.textContent = 'Õige vastus! Tubli!';
            messageElement.style.color = '#2ecc71';
            nextRoundButton.style.display = 'inline-block';
        } else {
            // Wrong answer
            carElements[selectedIndex].classList.add('incorrect');
            carElements[currentCorrectIndex].classList.add('correct');
            messageElement.textContent = 'Vale vastus! Mäng on läbi!';
            messageElement.style.color = '#e74c3c';
            restartButton.style.display = 'inline-block';
        }
    }
    
    function resetCarStyles() {
        carElements.forEach(car => {
            car.classList.remove('correct', 'incorrect');
        });
        messageElement.textContent = '';
        nextRoundButton.style.display = 'none';
        restartButton.style.display = 'none';
    }
    
    function blankOutCarDetails() {

        document.querySelector('#target-aastamaks span').textContent = 
            "Laeb...";
        document.querySelector('#target-registreerimistasu span').textContent = 
            "Laeb...";

        carElements.forEach(car => {
            car.querySelector('.car-title').textContent = 'Laeb...';
            car.querySelector('.car-year').textContent = '';
            car.querySelector('.car-color').textContent = '';
            car.querySelector('.car-engine-size').textContent = '';
            car.querySelector('.car-power').textContent = '';
            car.querySelector('.car-fuel').textContent = '';
        });
    }
});
