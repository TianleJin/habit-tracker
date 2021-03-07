var done = 0;
var total = 0;
var records = null;
var checkedBg = "rgba(214, 41, 118, 0.4)";
var uncheckedBg = "rgba(214, 41, 118, 0.8)";

function updateProgress() {
    if (total == 0) {
        $('#progress').hide();
        return;
    }

    $('#progress-text').html('Completed ' + done + ' / ' + total + ' Habits Today');
    let progressBar = $('#progress-bar');
    let percentage = Math.round(done / total * 100) + '%';
    progressBar.width(percentage);
    if (done > 0) {
        progressBar.html(percentage);
    }
    else {
        progressBar.html('');
    }
}

function displayRecord(elem, status) {
    let checkbox = elem.getElementsByTagName("input")[0];
    if (status) {
        elem.style.backgroundColor = checkedBg;
        checkbox.checked = true;
    }
    else {
        elem.style.backgroundColor = uncheckedBg;
        checkbox.checked = false;
    }
}

function updateStatus(record) {
    record['status'] ^= 1;
}

function updateDone(status) {
    if (status) {
        done++;
    }
    else {
        done--;
    }
}

function getRecords() {
    $.ajax({
        type: 'GET',
        url: '/records',
        dataType: 'json',
        success: function(data) {
            done = 0;
            records = data;
            total = records.length;
            for (let i = 0; i < total; i++) {
                let record = records[i];
                let status = record['status'];
                let habit_id = record['habit_id'];
                let record_date = record['record_date'];
                let elem = document.getElementById(`record-${record_date}-${habit_id}`);
                displayRecord(elem, status);
                if (status) {
                    done++;
                }
            }
            updateProgress();

            console.log(records);
            console.log('total: ' + total);
            console.log('done: ' + done);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        }
    });
}

function updateRecord(elem, habit_id, date_string) {
    let record;
    for (let i = 0; i < records.length; i++) {
        if (records[i]['habit_id'] == habit_id) {
            record = records[i]; break;
        }
    }

    $.ajax({
        type: 'POST',
        url: '/records/update',
        contentType: 'application/json',
        data: JSON.stringify({
            'habit_id': habit_id,
            'record_date': date_string,
            'status': record['status'] ^ 1
        }),
        success: function(res) {
            updateStatus(record);
            updateDone(record['status']);
            displayRecord(elem, record['status']);
            updateProgress();
            console.log('update response: ' + res);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        }
    });
}

getRecords();