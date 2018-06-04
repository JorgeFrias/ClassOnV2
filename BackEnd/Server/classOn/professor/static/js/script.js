$(document).ready(function() {
    socket.emit('updateCredentials');
    querySession();
}); 

function addGroup(group)
{
//    var groupJson = JSON.parse(group);                          // To JSON

     // Remove no members list item
    var noMembers = "noMembers_"+ group.position;
    $(jq(noMembers)).remove();

    // Add students to the list
    var students = group.students;
    var membersListSelector = jq("members_" + group.position);
    for (var i in students)
    {
        var studentHTML = '<li class=\"list-group-item \" id=\"' + students[i].db_id + '\">' + students[i].name + ' ' + students[i].lastName + '</li>';
        $(membersListSelector).append(studentHTML);
    }

    // Black border to new operating group
    $(jq(group.position)).toggleClass('border-secondary border-dark');

    // Assigment progress
    changeProgress(group);
//    $(jq("progress_" + groupJson.position)).text(groupJson.assigmentProgress);
    // Assigment progress color
    $(jq("progress_" + group.position)).toggleClass('badge-dark badge-success');
}

socket.on('joinedGroup', function(groupJson){
    var group = JSON.parse(groupJson);
    addGroup(group);
});

socket.on('assigment_changeProgress', function(groupJson){
    var group = JSON.parse(groupJson);                          // To JSON
    changeProgress(group);
});

socket.on('doubt_new', function(doubtJson){
    var doubt = JSON.parse(doubtJson);                          // To JSON
    appendDoubt(doubt);
});

function appendDoubt( doubt ) {
    let doubts = $("#doubts");                      // Locate doubts container
    const newDoubtHTML = '<div class=\"list-group-item flex-column align-items-start\" id=\"doubt_' + doubt.db_id + '\">' +
                         '<p class =\"mb-1\">' +
                         doubt.text +
                         '</p>' +
                         '<div>' +
                         '<span class=\"badge badge-info\">' + doubt.section + '</span>' +
                         '<button type=\"button\" class=\"btn btn-primary float-right\">Solve doubt</button>' +
                         '<div><div>';
    doubts.append(newDoubtHTML);
}

function jq( myid ) {
    return "#" + myid.replace( /(:|\.|\[|\]|,|=|@)/g, "\\$1" );
}

function changeProgress(groupJson){
    $(jq("progress_" + groupJson.position)).text(groupJson.assigmentProgress);
}

// Ask for the session state to the server
function querySession()
{
    socket.emit('classroom_query');
}

// Session query result to interface
socket.on('classroom_query_result', function(stateResultJson)
{
    var state = JSON.parse(stateResultJson);
    var groups = state.groups;
    var doubts = state.doubts;

    for(var i in groups)
    {
        addGroup(groups[i]);
    }

    for(var i in doubts)
    {
        appendDoubt(doubts[i]);
    }
});
