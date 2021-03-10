var cal = null;
var data = null;
var total = null;
var cellSize = null;
var startDate = null;

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

function getCalendarData(cb) {
    total = 0;
    $.ajax({
        type: 'GET',
        url: '/calendar',
        dataType: 'json',
        success: function(res) {
            data = res;
            for (let timestamp in res) {
                total += res[timestamp];
            }
            $('.heatmap-container .heatmap-title').html(`Completed ${total} Habits this Year`);
            cb();
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        }
    })
}

function initHeatMap() {
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
        data: data,
        legendColors: {
            min: "#D8BFD8",
            max: "#833AB4",
            empty: "lavender"
        },
        legend: [1, 2, 3, 4]
    });
}

getCalendarData(initHeatMap);