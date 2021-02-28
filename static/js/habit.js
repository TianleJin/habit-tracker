function removeHabit(habit_id) {
    $.ajax({
        url: `habit/${habit_id}`,
        type: 'DELETE',
        success: function(result) {
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