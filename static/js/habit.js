function removeHabit(habit_id, habit_name) {
    if (confirm(`Do you wish to remove habit '${habit_name}'? This action will be permanent.`)) {
        $.ajax({
            url: `habit/${habit_id}`,
            type: 'DELETE',
            success: function(result) {
                console.log(result);
                document.getElementById(`habit-${habit_id}`).style.opacity = 0;
                setTimeout(function () {
                    document.getElementById(`habit-${habit_id}`).style.display = "none";
                }, 300);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) { 
                alert("Status: " + textStatus); alert("Error: " + errorThrown); 
            }
        });
    }
}