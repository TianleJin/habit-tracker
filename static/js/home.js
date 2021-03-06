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

// called upon page load
getRecords();