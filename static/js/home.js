var records;
var total;
var done;

function getRecords() {
    $.ajax({
        type: 'GET',
        url: '/records',
        dataType: 'json',
        success: function(data) {
            records = data;
            done = 0;
            total = records.length;
            for (let i = 0; i < total; i++) {
                if (records[i]['status']) {
                    let elem = document.getElementById(`record-${records[i]['record_date']}-${records[i]['habit_id']}`);
                    let checkbox = elem.getElementsByTagName("input")[0];
                    elem.style.backgroundColor = "rgba(214, 41, 118, 0.4)";
                    checkbox.checked = true;
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
            record = records[i];
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
            console.log(res);
            let checkbox = elem.getElementsByTagName("input")[0];
            if (record['status'] == 0) {
                elem.style.backgroundColor = "rgba(214, 41, 118, 0.4)";
                checkbox.checked = true;
                done++;
            }
            else {
                elem.style.backgroundColor = "rgba(214, 41, 118, 0.8)";
                checkbox.checked = false;
                done--;
            }
            record['status'] ^= 1;
            updateProgress();
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        }
    });
}

function updateProgress() {
    if (total == 0) {
        $('#progress').hide();
        return;
    }

    $('#progress-text').html('Progress: ' + done + ' / ' + total);
    let progressBar = $('#progress-bar');
    let percentage = Math.round(done / total * 100) + '%';
    progressBar.width(percentage);
    if (done > 0) {
        progressBar.html(percentage);
    }
}