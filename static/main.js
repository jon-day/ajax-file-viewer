$(function() {
    $('#myfile').change(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/get_fieldnames',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                $("#detail").html(data);
            },
        });
    });
});