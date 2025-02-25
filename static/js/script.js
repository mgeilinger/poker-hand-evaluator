document.addEventListener('DOMContentLoaded', function () {
    let checkboxStates = [false, false, false, false, false];

    function updateCheckboxStates() {
        checkboxStates = [
            document.getElementById("box1").checked,
            document.getElementById("box2").checked,
            document.getElementById("box3").checked,
            document.getElementById("box4").checked,
            document.getElementById("box5").checked
        ];

        fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ states: checkboxStates })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("checkbox-response").innerText = "Probabilities:";
            document.getElementById("probability-display").innerHTML = Object.entries(data)
                .map(([handType, prob]) => `${handType}: ${prob}%`)
                .join("<br>");
        })
        .catch(error => console.error('Error:', error));
    }

    document.getElementById("box1").addEventListener('change', updateCheckboxStates);
    document.getElementById("box2").addEventListener('change', updateCheckboxStates);
    document.getElementById("box3").addEventListener('change', updateCheckboxStates);
    document.getElementById("box4").addEventListener('change', updateCheckboxStates);
    document.getElementById("box5").addEventListener('change', updateCheckboxStates);

    document.getElementById("drawButton").addEventListener('click', function() {
        fetch('/draw', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            document.getElementById("poker-hand").innerText = data.hand_message;
        })
        .catch(error => console.error('Error:', error));
    });
});