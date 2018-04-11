socket.on('joinedGroup', function(group){
    var groupJson = JSON.parse(group);                          // To JSON

     // Remove no members list item
    var noMembers = "noMembers_"+groupJson.position;
    $(jq(noMembers)).remove();

    // Add students to the list
    var students = groupJson.students;
    var membersListSelector = jq("members_" + groupJson.position);
    for (var i in students)
    {
        var studentHTML = '<li class=\"list-group-item \" id=\"' + students[i].db_id + '\">' + students[i].name + ' ' + students[i].lastName + '</li>';
        $(membersListSelector).append(studentHTML);
    }

    // Black border to new operating group
    $(jq(groupJson.position)).toggleClass('border-secondary border-dark');

    // Assigment progress
    changeProgress(groupJson);
//    $(jq("progress_" + groupJson.position)).text(groupJson.assigmentProgress);
    // Assigment progress color
    $(jq("progress_" + groupJson.position)).toggleClass('badge-dark badge-success');

});

socket.on('assigment_changeProgress', function(group){
    var groupJson = JSON.parse(group);                          // To JSON
    changeProgress(groupJson);
})

function jq( myid ) {
    return "#" + myid.replace( /(:|\.|\[|\]|,|=|@)/g, "\\$1" );
}

function changeProgress(groupJson){
    $(jq("progress_" + groupJson.position)).text(groupJson.assigmentProgress);
}

