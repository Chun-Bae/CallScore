$(document).ready(function(){
    $.ajax({
        url: '/del_score/',
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            
        },
        error: function(error) {
            console.log(error);
        }
    });
});
