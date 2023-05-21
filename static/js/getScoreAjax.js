$(document).ready(function(){
    $.ajax({
        url: '/get_score/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            allScore = data;
            location.href = '/view';
        },
        error: function(error) {
            console.log(error);
        }
    });
});
