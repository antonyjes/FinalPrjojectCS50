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
        'language': { 'url': '//cdn.datatables.net/plug-ins/1.10.19/i18n/Spanish.json' },
        'ajax': {
            'url' : '/fetchtasks'
        },
        'lengthMenu': [[8], [8]],
        searching: true,
        sort: false,
        'columns': [
            { data: 'name' },
            { data: 'status' },
            {
                mRender : function(data, type, row) {
                    return '<div class="acciones"><button type="button" class="btn btn-warning btn-sm view-data" data-id="'+row.id+'" data-bs-toggle="modal" data-bs-target="#modaledit">Editar</button>' + '<a href="/deletetask/' + row.id + '"class="btn btn-danger btn-sm">Eliminar</a></div>';
                }
            }
        ],
    });

    $(document).on("click", '.view-data', function(){
        var id = $(this).data('id');

        $.ajax({
            url: '/selecttask/' + id,
            type: "POST",
            dataType: "json",
            success: function(data) {
                $('#view_task').val(data[0]['name']);
                $('#view_status').val(data[0]['status']);
                $('#view_id').val(data[0]['id']);
            }
        })
    })
});