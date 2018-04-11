socket.on('joinedGroup', function(group){
    var groupJson = JSON.parse(group);                          // To JSON

    var noMembers = "noMembers_"+groupJson.position;
    $(jq(noMembers)).remove();               // Remove no members

    var students = groupJson.students;
    var membersListSelector = jq("members_" + groupJson.position);
    for (var i in students)
    {
        var studentHTML = '<li class=\"list-group-item\" id=\"' + students[i].db_id + '\">' + students[i].name + ' ' + students[i].lastName + '</li>';
        $(membersListSelector).append(studentHTML);
    }

});

function jq( myid ) {
    return "#" + myid.replace( /(:|\.|\[|\]|,|=|@)/g, "\\$1" );
}