$(document).ready(function(){
    $.ajax({
        url: '/get_score/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            location.href = '/view';
        },
        error: function(error) {
            location.href = '/';
            console.log(error);
        }
    });
});