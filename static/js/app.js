$(document).ready(function() {
    // Compare two passwords and validate
    $('#password2').keyup(function() {
        if ($('#password1').val() != $('#password2').val()) {
            $('#msg-passwords').html("Contraseñas no coinciden").css({'color': 'red', 'font-size': '15px', 'font-weight': 'bold'});
        } else {
            $('#msg-passwords').html("Contraseñas coinciden").css({'color': 'green', 'font-size': '15px', 'font-weight': 'bold'});
        }
    });

    // Hide alert message after 1.5 seconds
    $('#alert').delay(1500).fadeOut('slow');
});