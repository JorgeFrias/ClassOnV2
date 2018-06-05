$(document).ready(function() {
    socket.emit('updateCredentials');
    querySession();
}); 

function addGroup(group)
{
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
    // Assigment progress color
    $(jq("progress_" + group.position)).toggleClass('badge-dark badge-success');
}

socket.on('joinedGroup', function(groupJson){
    var group = JSON.parse(groupJson);
    addGroup(group);
});

socket.on('assigment_changeProgress', function(groupJson){
    var group = JSON.parse(groupJson);                      // To JSON
    changeProgress(group);
});

socket.on('doubt_new', function(doubtJson){
    var doubt = JSON.parse(doubtJson);                      // To JSON
    appendDoubt(doubt);
});

// Add a doubt to the HTML
function appendDoubt( doubtJson )
{
    let doubts = $("#doubts");                              // Locate doubts container
    const newDoubtHTML = 
    '<div class="card" id=\"doubt_' + doubtJson.db_id + '\">' + 
        '<div class="card-body">' +
            '<span class="badge badge-info">Section: ' + doubtJson.section + '</span>' + 
            '<p class="card-text">' + doubtJson.text + '</p>' + 
        '</div>' + 
        '<ul class="list-group list-group-flush">' +
            // '<li class="list-group-item list-group-item-secondary">Cras justo odio</li>' +        
        '</ul>' +
        // Professors are not supported to solve doubts (yet)
        // '<div class="card-body">' +
        //     '<button type=\"button\" class=\"btn btn-primary float-right\"' +
        //     ' data-toggle=\"modal\" data-target=\"#modal_answer\" ' +
        //     'data-doubtid=\"'+ doubtJson.db_id + '\">Solve doubt</button>' +            
        // '</div>' +
    '</div>' +
    '<br>'
    doubts.append(newDoubtHTML);
}

socket.on('new_answer', function(anwserJson)
{
    var answer = JSON.parse(anwserJson);
    var doubtId = answer.doubtid;
    var text = answer.text;
    appendAnswer(doubtId, text);
})

function appendAnswer(doubtId, anwser)
{
    var li = '<li class="list-group-item list-group-item-secondary">'+ anwser +'</li>';        
    $('#doubt_' + doubtId + '> ul').append(li);
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
