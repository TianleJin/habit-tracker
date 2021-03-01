function displayAlert(message, category) {
    $('#message-box').empty();
    $('#message-box').append(
        `<div class="alert alert-${category} alert-dismissible fade show" role="alert" style="margin-bottom:0;">
            ${message}
            <button type="button" class="close" data-dismiss="alert" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
        </div>`
    );
}

function deleteHabit(habit_id, habit_name) {
    $.ajax({
        url: `habit/${habit_id}/delete`,
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({
            'name': habit_name
        }), 
        success: function(result) {
            displayAlert(result, "success");
            document.getElementById(`habit-${habit_id}`).style.opacity = 0;
            setTimeout(function() {
                document.getElementById(`habit-${habit_id}`).style.display = "none";
            }, 500);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            displayAlert(errorThrown, "danger");
        }
    });
}

function updateHabit(habit_id, habit_name) {
    $.ajax({
        url: `habit/${habit_id}/update`,
        type: 'POST',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({ 
            'name': habit_name,
            'desc': document.getElementById('desc-area').value 
        }),
        success: function(result) {
            displayAlert(result, "success");
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            displayAlert(errorThrown, "danger");
        }
    });
}

$('#info-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var name = button.data('name');
    var desc = button.data('desc');
    var id = button.data('id');
    var modal = $(this);
    modal.find('.modal-title').text(name);
    modal.find('.modal-body textarea').text(desc);

    $('#update-btn').on('click', function() {
        updateHabit(id, name);
        $('#info-modal').modal('hide');
    });
});

$('#confirm-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var name = button.data('name');
    var id = button.data('id');
    var modal = $(this);
    modal.find('.modal-title').text(name);

    $('#delete-btn').on('click', function() {
        $('#confirm-modal').modal('hide');
        deleteHabit(id, name);
    });
});