$(document).ready(function () {

    $("#frmLoginAccount").submit(function (e) {
        e.preventDefault();

        let email = $.trim($("#logEmail").val());
        let password = $.trim($("#logPassword").val());

        let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/; // Email RegEx

        if (email === "") {
            alertify.error('Email is Required!');
            return;
        }
        if (!emailPattern.test(email)) {  // Check email format
            alertify.error('Invalid Email Format!');
            return;
        }

        if (password === "") {
            alertify.error('Password is Required!');
            return;
        }


        $('#spinner').show();
        $('#btnLoginAccount').prop('disabled', true);

      

        var formData = {
            email: email,
            password: password
        };

        $.ajax({
            type: "POST",
            url: "/LoginAccount",
            contentType: "application/json",
            data: JSON.stringify(formData),
            success: function (response) {
                console.log(response);
                $('#spinner').hide();
                $('#btnLoginAccount').prop('disabled', false);

                if (response.status === "success") {
                    alertify.success(response.message);
                    setTimeout(function () {
                        window.location.href = "/user/home";
                    }, 1000);
                } else {
                    alertify.error(response.message);
                }
            },
        });
    });





    $("#change-password-form").submit(function (e) {
        e.preventDefault();


        $('#spinner').show();

        let newpassword = $.trim($("#new-password").val());
        let confirmpassword = $.trim($("#confirm-password").val());
        let currentpassword = $.trim($("#current-password").val());


        if (currentpassword === "") {
            alertify.error("Current password cannot be empty.");
            $('#spinner').hide();
            return;
        }
        
        if (newpassword === "") {
            alertify.error("New password cannot be empty.");
            $('#spinner').hide();
            return;
        }
        
        if (newpassword !== confirmpassword) {
            alertify.error("Passwords do not match.");
            $('#spinner').hide();
            return;
        }
        
        $.ajax({
            type: "POST",
            url: "/check_password",
            contentType: "application/json",
            data: JSON.stringify({ currentpassword: currentpassword,newpassword:newpassword }), 
            success: function (response) {
                $('#spinner').hide();
                $('#btnUpdatePassword').prop('disabled', false);
        
                if (response.correct) {
                    alertify.success("Update Successfully.");
                    setTimeout(function () {
                        location.reload();
                    }, 1000);

                } else {
                    alertify.error("Incorrect password.");
                }
            },
            error: function (xhr) {
                $('#spinner').hide();
                $('#btnUpdatePassword').prop('disabled', false);
                alertify.error("Error checking password.");
            }
        });
        

        console.log("click");

        // var formData = {
        //     currentpassword: currentpassword,
        //     newpassword: newpassword,
        //     confirmpassword: confirmpassword
        // };


       
    });

    

    $("#frmCreateAccount").submit(function (e) {
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


        $('#spinner').show();
        $('#btnCreateAccount').prop('disabled', true);
           
        var fullname = $("#regName").val().trim();
        var email = $("#regEmail").val().trim();
        var password = $("#regPassword").val().trim();

      

        var formData = {
            fullname: fullname, // Fixed field name
            email: email,
            password: password
        };

        $.ajax({
            type: "POST",
            url: "/createAccount",
            contentType: "application/json",
            data: JSON.stringify(formData), // Convert object to JSON
            success: function (response) {
                $('#spinner').hide();
                $('#btnCreateAccount').prop('disabled', false);

                if (response.status === "success") {
                    alertify.success(response.message);
                    setTimeout(function () {
                        window.location.href = "/verify";
                    }, 1000);
                } else {
                    alertify.error(response.message);
                }
            },
        });
    });





    $(document).ready(function () {
        // Verify OTP
        $("#verifyOtpBtn").click(function () {
            var otp = $("#code").val().trim();
            if (!otp) {
                alertify.error("Please enter the verification code.");
                return;
            }

            $("#spinner").fadeIn();

            $.ajax({
                type: "POST",
                url: "/verify",
                contentType: "application/json",
                data: JSON.stringify({ otp: otp }),
                success: function (response) {
                    $("#spinner").fadeOut();
                    if (response.status === "success") {
                        alertify.success("Account verified successfully!");
                        setTimeout(function () {
                            window.location.href = "/";
                        }, 1000);
                    } else {
                        alertify.error(response.message);
                    }
                },
                error: function () {
                    $("#spinner").fadeOut();
                    alertify.error("Verification failed. Please try again.");
                }
            });
        });

        // Resend OTP
        $("#resendOtpBtn").click(function () {
            $("#spinner").fadeIn();

            $.ajax({
                type: "POST",
                url: "/resendOtp",
                success: function (response) {
                    $("#spinner").fadeOut();
                    if (response.status === "success") {
                        alertify.success("New OTP sent to your email!");
                    } else {
                        alertify.error("Failed to resend OTP. Please try again.");
                    }
                },
                error: function () {
                    $("#spinner").fadeOut();
                    alertify.error("Something went wrong. Please try again.");
                }
            });
        });
    });






});
