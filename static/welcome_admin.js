const dashboardUser = document.getElementById('dashboard-user'); // here we get the dashboard user element

const user = localStorage.getItem('name'); // here we get the user name from localStorage


if (dashboardUser) {
    dashboardUser.innerHTML = user;
}           //  here we check if the dashboardUser element exists before setting its innerHTML
