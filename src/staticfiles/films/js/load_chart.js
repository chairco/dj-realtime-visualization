var mChart, mChart2;

function loadEcharts(mChart, name) {
    var template = 'id_echarts_container_' + name
    var url = '/films/options/' + 'dash_' + name + '/';
    if (mChart != null) {
        mChart.clear();
    }
    mChart = echarts.init(document.getElementById(template));
    mChart.showLoading();
    $.ajax({
        url: url,
        type: "GET",
        data: null,
        dataType: "json"
    }).done(function(data) {
        mChart.hideLoading();
        mChart.setOption(data);
        console.log(data);
    });
}
$(document).ready(function() {
    $('a[data-echarts-name]').on('click', function() {
        var name = $(this).data('echartsName');
        switch (name) {
            case 'yield':
                loadEcharts(mChart, name);
            case 'scatter':
                loadEcharts(mChart2, name);
            default:
                break;
        }
    });
    loadEcharts(mChart, 'yield');
    loadEcharts(mChart2, 'scatter');

    setInterval(function() { loadEcharts(mChart, 'yield'); }, 60000); /* update every 6 seconds*/
    setInterval(function() { loadEcharts(mChart2, 'scatter'); }, 100000); /* update every 10 seconds*/
});