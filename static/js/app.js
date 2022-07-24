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

    // Fecth data from tasks table and display in table
    var table = $('#tasks-table').DataTable({
        "processing": true,
        "serverSide": true,
        'serverMethod': 'post',
        'ajax': {
            'url' : '/fetchtasks'
        },
        'lengthMenu': [[5, 10, 25, 50, -1], [5, 10, 25, 50, "All"]],
        searching: true,
        sort: false,
        'columns': [
            { data: 'name' },
            { data: 'status' },
            {
                mRender : function(data, type, row) {
                    return '<div class="acciones"><a href="/tasks/' + row.id + '" class="btn btn-primary btn-sm">Ver</a>' + '<a href="/tasks/' + row.id + '/edit" class="btn btn-warning btn-sm">Editar</a>' + '<a href="/tasks/' + row.id + '/delete" class="btn btn-danger btn-sm">Eliminar</a></div>';
                }
            }
        ],
    });
});