document.addEventListener('DOMContentLoaded', function () {
    // Initialize checkboxStates
    let checkboxStates = [
        document.getElementById("box1").checked,
        document.getElementById("box2").checked,
        document.getElementById("box3").checked,
        document.getElementById("box4").checked,
        document.getElementById("box5").checked
    ];

    // Function to update checkbox states
    function updateCheckboxStates() {
        // Update the checkboxStates array based on the current checkbox status
        checkboxStates = [
            document.getElementById("box1").checked,
            document.getElementById("box2").checked,
            document.getElementById("box3").checked,
            document.getElementById("box4").checked,
            document.getElementById("box5").checked
        ];

        // Send updated data to the Flask backend
        fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ states: checkboxStates })
        })
        .then(response => response.json())
        .then(data => {
            // Display the checkbox response in the appropriate section
            document.getElementById("checkbox-response").innerText = data.checkbox_message;
        })
        .catch(error => console.error('Error:', error));
    }

    // Attach event listeners to each checkbox to update states when clicked
    document.getElementById("box1").addEventListener('change', updateCheckboxStates);
    document.getElementById("box2").addEventListener('change', updateCheckboxStates);
    document.getElementById("box3").addEventListener('change', updateCheckboxStates);
    document.getElementById("box4").addEventListener('change', updateCheckboxStates);
    document.getElementById("box5").addEventListener('change', updateCheckboxStates);

    // Function to draw poker hand when "Draw" button is clicked
    document.getElementById("drawButton").addEventListener('click', function() {
        fetch('/draw', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            // Display the poker hand response in the appropriate section
            document.getElementById("poker-hand").innerText = data.hand_message;
        })
        .catch(error => console.error('Error:', error));
    });
});