function getstatic(hours) {
    var url = '/films/static/';
    $.ajax({
        url: url,
        type: "GET",
        data: null,
        dataType: "json"
    }).done(function(data) {
        if (data.last_hour_yield_p < 80) {
            $('.progress-bar').css('width', data.last_hour_yield_p+'%').attr('class', 'progress-bar progress-bar-danger progress-bar-striped').attr('aria-valuenow', data.last_hour_yield_p);
        } else {
            $('.progress-bar').css('width', data.last_hour_yield_p+'%').attr('class', 'progress-bar progress-bar-success progress-bar-striped').attr('aria-valuenow', data.last_hour_yield_p);
        }
        
        $('.progress-bar').text('');
        $('.progress-bar').append(data.last_hour_yield_p+'%');
        $('.panel2').text('');
        $('.panel2').append("<strong><big>"+data.last_hour_yield+"/小時</big></strong>");
        $('.panel3').text('');
        $('.panel3').append("<strong><big>"+data.downtime+" 秒</big></strong>")
    })
}
$(document).ready(function() {
    getstatic(1);
    setInterval(function() { getstatic(1); }, 10000); /* update every 10 seconds*/
});