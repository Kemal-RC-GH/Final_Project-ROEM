const today = new Date();   // here we get the current date
const year = today.getFullYear();  // here we extract a complete year
const month = String(today.getMonth() + 1).padStart(2, '0');  // here we extract a month, add 1 as months are zero based also padding
const day = String(today.getDate()).padStart(2, '0');       // pading to meet standard YYYY-MM-DD for day
const formattedToday = `${year}-${month}-${day}`;

const dateInput = document.getElementById('myDate');    // get date by id
dateInput.min = formattedToday;         // set minimum to today