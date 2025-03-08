$(document).ready(function () {

    $("#btnCreateAccount").click(function (e) { 
        e.preventDefault();

        let regName = $.trim($("#regName").val());
        let regEmail = $.trim($("#regEmail").val());
        let regPassword = $.trim($("#regPassword").val());

        let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/; // Email RegEx

        if (regName === "") {
            alertify.error('Name is Required!');
            return;
        }
        if (regEmail === "") {
            alertify.error('Email is Required!');
            return;
        }
        if (!emailPattern.test(regEmail)) {  // Check email format
            alertify.error('Invalid Email Format!');
            return;
        }
        if (regPassword === "") {
            alertify.error('Password is Required!');
            return;
        }

    });

});
