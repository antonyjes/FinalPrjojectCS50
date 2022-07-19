$(document).ready(function() {
    // Compare two passwords and validate
    $('#password2').keyup(function() {
        if ($('#password1').val() != $('#password2').val()) {
            $('#msg-passwords').html("Password do not match").css('background-color', 'red');
        } else {
            $('#msg-passwords').html("Password matched").css('background-color', 'green');
        }
    });
});