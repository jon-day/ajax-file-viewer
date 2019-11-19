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

    $('#testClick').click(function() {
        var firstName = $("#firstName :selected").text();
        var lastName = $("#lastName :selected").text();
        var form_data = new FormData($('#upload-file')[0]);
        form_data.append("firstName", firstName);
        form_data.append("lastName", lastName);

        $.ajax({
            type: 'POST',
            url: '/test_route',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(retData) {
                console.log(retData.url);
            },
        });
    });
});