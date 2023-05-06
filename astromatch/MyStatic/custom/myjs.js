// Submit form data using AJAX
$(document).ready(function () {
    $("#myForm").submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: "POST",
            data: {
                csrfmiddlewaretoken: $(this).data("csrf"),
                action: "post",
                dob: $("#dob").val(),
                tob: $("#tob").val(),
                timezone: $("#timezone").val(),
            },
            success: function (response) {
                console.log(response);
                $("#output").html(JSON.stringify(response["moondf"]));
            },
        });
    });
});
