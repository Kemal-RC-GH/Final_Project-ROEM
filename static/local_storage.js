// Get the username input element
const username = document.getElementById('username');

// Check if the username input element exists
if (username) {
    // Add an event listener to save the name to localStorage when the input value changes
    username.addEventListener('input', () => {
        localStorage.setItem('name', username.value);
    });
}
