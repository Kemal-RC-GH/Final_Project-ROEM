// Get the dashboard user element
const dashboardUser = document.getElementById('dashboard-user');
// Get the user name from localStorage
const user = localStorage.getItem('name');
console.log(user);
// Check if the dashboardUser element exists before setting its innerHTML
if (dashboardUser) {
    dashboardUser.innerHTML = user;
}
