function removeHabit(habit_id) {
    $.ajax({
        url: `habit/${habit_id}/delete`,
        type: 'POST',
        success: function(result) {
            console.log(result);
            document.getElementById(`habit-${habit_id}`).style.opacity = 0;
            setTimeout(function() {
                document.getElementById(`habit-${habit_id}`).style.display = "none";
            }, 500);
        },
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
            alert("Status: " + textStatus); alert("Error: " + errorThrown); 
        }
    });
}

$('#info-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var name = button.data('name');
    var desc = button.data('desc');
    var modal = $(this);
    modal.find('.modal-title').text(name);
    modal.find('.modal-body textarea').text(desc);
});

$('#confirm-modal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var name = button.data('name');
    var id = button.data('id');
    var modal = $(this);
    modal.find('.modal-title').text(name);
    $('#delete-btn').on('click', function() {
        $('#confirm-modal').modal('hide');
        removeHabit(id);
    });
});