var cal = null;
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

function initHeatMap() {
    cal = new CalHeatMap();
    startDate = getStartDate();
    cellSize = getCellSize();
    if (cellSize < 5) {
        cellSize = 5;
    }

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
        data: '/calendar',
        legendColors: {
            min: "#D8BFD8",
            max: "#833AB4",
            empty: "lavender"
        },
        legend: [1, 2, 3, 4]
    });
}

initHeatMap();