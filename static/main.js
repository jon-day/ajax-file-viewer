$(function() {
    $('#myfile').change(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/uploadajax',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                $("#detail").html(data);
                console.log('success stuff');
            },
        });
    });
});