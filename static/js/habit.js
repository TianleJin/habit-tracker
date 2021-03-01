$('#info-modal').on('show.bs.modal', function(event) {
    var modal = $(this);
    var button = $(event.relatedTarget);
    
    habit_id = button.data('id');
    habit_name = button.data('name');
    habit_desc = button.data('desc');

    $('#update-form').attr('action', `habit/${habit_id}/update`);

    modal.find('.modal-title').text(habit_name);
    modal.find('.modal-body input').val(habit_name);
    modal.find('.modal-body textarea').val(habit_desc);
});

$('#confirm-modal').on('show.bs.modal', function (event) {
    var modal = $(this);
    var button = $(event.relatedTarget);

    habit_id = button.data('id');
    habit_name = button.data('name');
    habit_desc = button.data('desc');

    $('#delete-form').attr('action', `habit/${habit_id}/delete`)

    modal.find('.modal-title').text(habit_name);
    modal.find('.modal-footer input').val(habit_name);
});