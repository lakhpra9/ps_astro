// for (let i = 0; i < rows.length; i++) {
//     if ((i + 1) % 9 === 0) {
//         rows[i].style.borderBottom = "3px solid black";
//         for (let j = i - 8; j <= i; j++) {
//             rows[j].style.backgroundColor = (i / 9) % 2 === 0 ? "#f5f5f5" : "#ebebeb";
//         }
//     }
// }


// for (let i = 0; i < rows.length; i++) {
//     if ((i + 1) % 9 === 0) {
//         rows[i].style.borderBottom = "3px solid black";
//         const color = (i / 9) % 2 === 0 ? "blue" : "green";
//         for (let j = i - 8; j <= i; j++) {
//             rows[j].style.backgroundColor = color;
//         }
//     }
// }

// const table = document.getElementsByClassName("rashi_table");
// const rows = table.getElementsByTagName("tr");

// for (let i = 0; i < rows.length; i++) {
//     // Add thick bottom border after every 9 rows
//     if ((i + 1) % 9 === 0) {
//         rows[i].style.borderBottom = "thick solid black";
//     }
// }

// document.addEventListener("DOMContentLoaded", function () {
//     const table = document.getElementsByClassName("rashi_table");
//     const rows = table.getElementsByTagName("tr");
//     for (let i = 0; i < rows.length; i++) {
//         // Add thick bottom border after every 9 rows
//         if ((i + 1) % 9 === 0) {
//             rows[i].style.borderBottom = "thick solid black";
//         }
//     }
// });


// // Submit form data using AJAX
// $(document).ready(function () {
//     $("#myForm").submit(function (event) {
//         event.preventDefault();
//         $.ajax({
//             url: $(this).attr("action"),
//             type: "POST",
//             data: {
//                 csrfmiddlewaretoken: $(this).data("csrf"),
//                 action: "post",
//                 dob: $("#dob").val(),
//                 tob: $("#tob").val(),
//                 timezone: $("#timezone").val(),
//             },
//             success: function (response) {
//                 console.log(response);
//                 $("#output").html(JSON.stringify(response["moondf"]));
//             },
//         });
//     });
// });
