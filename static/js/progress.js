var cal = null;
var total = null;
var barChart = null;
var cellSize = null;
var startDate = null;
var chartData = null;
var calendarData = null;
var chartTitle = {
    'year': 'Yearly Statistics',
    'month': 'Monthly Statistics',
    'week': 'Weekly Statistics'
};

function getStartDate() {
    return new Date(new Date().getFullYear(), 0, 1);
}

function extractNumerical(value) {
    return parseFloat(value.substring(0, value.length - 2));
}

function getInnerDivWidth() {
    let width = $('.inner').width();
    let padding = extractNumerical($('.inner').css('padding'));
    return width - 2 * padding;
}

function getCellSize() {
    return (getInnerDivWidth() - 104) / 53; 
}

function getCalendarData() {
    total = 0;
    $.ajax({
        type: 'GET',
        url: '/calendar',
        dataType: 'json',
        success: function(res) {
            calendarData = res;
            for (let timestamp in res) {
                total += res[timestamp];
            }
            $('.heatmap-container .heatmap-title').html(`Completed ${total} Habits this Year`);
            updateHeatMap();
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        }
    });
}

function updateHeatMap() {
    cal = new CalHeatMap();
    startDate = getStartDate();
    cellSize = Math.max(5, getCellSize());

    cal.init({ 
        itemSelector: "#heatmap",
        domain: "year",
        itemName: ["completed habit", "completed habits"],
        subDomain: "day",
        cellSize: cellSize,
        legendCellSize: cellSize,
        start: startDate,
        range: 1,
        tooltip: true,
        data: calendarData,
        legendColors: {
            min: "#D8BFD8",
            max: "#833AB4",
            empty: "lavender"
        },
        legend: [1, 2, 3, 4]
    });
}

function getChartData() {
    let interval = document.getElementById('interval-selector').value;
    $.ajax({
        type: 'GET',
        url: `/chart/${interval}`,
        dataType: 'json',
        success: function(res) {
            chartData = res;
            $('.chart-container .chart-title').html(chartTitle[interval]);
            updateChart();
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        }
    });
}

function updateChart() {
    if (barChart != null) {
        barChart.destroy();
    }

    let labels = [];
    let data = [];
    for (let name in chartData) {
        labels.push(name);
        data.push(chartData[name]);
    }

    var ctx = document.getElementById('bar-chart');
    barChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'completion frequency',
                data: data,
                backgroundColor: 'rgba(131, 58, 180, 0.2)',
                borderColor: 'rgba(131, 58, 180, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            legend: {
                onClick: (e) => e.stopPropagation()
            }
        }
    });
}

$('#interval-selector').on('change', function() {
    getChartData();
})

getCalendarData();
getChartData();