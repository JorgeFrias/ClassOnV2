socket.on('joinedGroup', function(group){
    var groupJson = JSON.parse(group);                          // To JSON
    $("#noMembers_"+groupJson.position).remove();       // Remove no members

    var students = groupJson.students;
    for (var i in students)
    {
        var studentHTML = '<li className=\"list-group-item\" id=\"' + students[i].db_id + '\">' + students[i].name + ' ' + students[i].lastName + '</li>';
        $("#members_" + groupJson.position + " li:last").append(studentHTML);
    }
});