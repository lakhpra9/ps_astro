// get the first table element on the page
const table = document.querySelector("table");

// get all the rows of the table
// const rows = table.getElementsByTagName("tbody tr");
const rows = table.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

for (let i = 0; i < rows.length; i++) {
    if ((i + 1) % 4 === 0) {
        rows[i].style.borderBottom = "1px solid grey";
    }
}

// loop through the rows and add a bottom border to every 9th row
for (let i = 0; i < rows.length; i++) {
    if ((i + 1) % 9 === 0) {
        rows[i].style.borderBottom = "4px solid black";
    }
}