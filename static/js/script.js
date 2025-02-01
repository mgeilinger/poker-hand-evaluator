document.addEventListener('DOMContentLoaded', function () {
    function submitSelection() {
        // Store checkbox states in an array
        let checkboxStates = [
            document.getElementById("box1").checked,
            document.getElementById("box2").checked,
            document.getElementById("box3").checked,
            document.getElementById("box4").checked,
            document.getElementById("box5").checked
        ];

        // Send data to the Flask backend
        fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ states: checkboxStates })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("response").innerText = data.message; // Display response
        })
        .catch(error => console.error('Error:', error));
    }

    // Ensure the button event listener calls the function
    document.querySelector('button').addEventListener('click', submitSelection);
});