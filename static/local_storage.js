const username = document.getElementById('username');
// here we check if the username input element exists
if (username) {
    // here we add an event listener to save the name to localStorage when the input value changes
    username.addEventListener('input', () => {
        localStorage.setItem('name', username.value);
    });
}

const logoutButton = document.getElementById('logout-button');
// here we check if the logout button element exists
if (logoutButton) {
    // here we add an event listener to clear localStorage when the user clicks the logout button
    logoutButton.addEventListener('click', () => {
        localStorage.removeItem('name'); // here we remove the username from local storage
    });
}

