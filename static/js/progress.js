var cal = null;
var cellSize = null;
var startDate = null;
var vertical = false;

function getStartDate() {
    return new Date(new Date().getFullYear(), 0, 1);
}

function isLeapYear() {
    let year = new Date().getFullYear();
    return year % 100 != 0 && year % 4 == 0 || year % 400 == 0;
}

function getHorizontalMultiplier() {
    return isLeapYear() ? 62 : 61; 
}

function getVerticalMultiplier() {
    return 6;
}

function extractNumerical(value) {
    return parseFloat(value.substring(0, value.length - 2));
}

function getInnerDivWidth(sub) {
    let width = $('.inner').width();
    let padding;
    if (sub) {
        padding = extractNumerical($('.inner').css('padding'));
    }
    else {
        padding = 0;
    }
    return width - 2 * padding;
}

function getHorizontalCellSize() {
    return (getInnerDivWidth(1) - 142) / getHorizontalMultiplier(); 
}

function getVerticalCellSize() {
    return (getInnerDivWidth(0) - 10) / getVerticalMultiplier();
}

function initHeatMap() {
    cal = new CalHeatMap();
    startDate = getStartDate();
    cellSize = getHorizontalCellSize();
    if (cellSize < 9) {
        vertical = true;
        cellSize = getVerticalCellSize();
        console.log(cellSize);
    }

    cal.init({ 
        itemSelector: "#heatmap",
        domain: "month",
        cellSize: cellSize,
        start: startDate,
        tooltip: true,
        verticalOrientation: vertical
    });
}

initHeatMap();