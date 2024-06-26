$(document).ready(function () {
    $('#productoForm').on('submit', function(event) {
        event.preventDefault();
        var form = $(this)[0];
        var formData= new formData(form)
        $.ajax({
            type: 'POST',
            url: '{% url "Agregar_Producto" %}',
            data: form.serialize(),
            processData: false,
            proccesType: false,
            success: function(response) {
                if (response.success) {
                    $('#staticBackdrop1').modal('hide');
                    alert('Producto agregado exitosamente');
                    location.reload();
                } else {
                    alert('Error: ' + JSON.stringify(response.errors));
                }
            },
            error: function(xhr, status, error) {
                
                alert('Error al enviar el formulario. ' + error);
            }
        });
    });
});

