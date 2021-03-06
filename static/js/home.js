var records;
var total;
var done;

function getRecords() {
    $.ajax({
        type: 'GET',
        url: '/home/records',
        dataType: 'json',
        success: function(data) {
            records = data;
            done = 0;
            total = records.length;
            for (let i = 0; i < total; i++) {
                if (records[i]['status']) {
                    done++;
                }
            }
            console.log('total: ' + total);
            console.log('done: ' + done);
            updateProgress();
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        }
    });
}

function updateProgress() {
    $('#progress-text').html('Progress: ' + done + ' / ' + total);
    var progressBar = $('#progress-bar');
    if (total == 0) {
        progressBar.width('0%');
    }
    else {
        let percentage = Math.round(done / total * 100) + '%';
        progressBar.width(percentage);
        if (done > 0) {
            progressBar.html(percentage);
        }
    }
}

// called upon page load
getRecords();