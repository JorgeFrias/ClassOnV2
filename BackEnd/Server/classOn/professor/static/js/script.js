var timer;

$(document).ready(function() {
    /* Stuff needed when the page loads */
    // Request credentials
    socket.emit('updateCredentials');                       
    
    // Query state information
    querySession();       

    // To solve a doubt
    $("#btn_answer").click (answerDoubt);                   

    /* 
       Dialog with doubt information:
       - Doubt text
       - Time counter and utils
    */
    $('#modal_answer').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget);                // Button that triggered the modal
        doubtId = button.data('doubtid');                   // Extract info from data-* attributes and store in global variable
        timer.start();                                      // Timing start

        var modal = $(this);                                // Add doubt text to the modal
        var doubtSelector = '#doubt_' + doubtId;
        var doubtText = $(doubtSelector + '.card .card-body .card-text').text()
        modal.find(".modal-body #modal_doubt_text").text(doubtText);
    });

    /* ----- Time control code ----- */
    timer = new Timer();
    $('#chronoExample .startButton').click(function () {
        timer.start();
    });
    $('#chronoExample .pauseButton').click(function () {
        timer.pause();
    });
    $('#chronoExample .resetButton').click(function () {
        timer.reset();
    });
    timer.addEventListener('secondsUpdated', function (e) {
        $('#chronoExample .values').html(timer.getTimeValues().toString());
    });
    timer.addEventListener('started', function (e) {
        $('#chronoExample .values').html(timer.getTimeValues().toString());
    });
    timer.addEventListener('reset', function (e) {
        $('#chronoExample .values').html(timer.getTimeValues().toString());
    });
    // $('#chronoExample .stopButton').click(function () {
    //     timer.stop();
    // });
    /* ----- Time control code ----- */

    /* Student position click */
    $('.card').on('click', function(event) {
        alert('You clicked the Bootstrap Card');
   });
}); 

/**
 * Sets the interface "pop-up" window for the professor to answer a doubt and measure the time spent.
 * @param {*} event 
 */
function answerDoubt(event)
{
    // Only God and I did know from where doubtId comes from.
    // Now only God knows.
    time = timer.getTimeValues().toString()                 // Get time
    timer.stop();                                           // Stop timer
    socket.emit('professor_time', doubtId, time);           // Send time to server
    $('#modal_answer').modal('hide');                       // Hide he modal
}

/**
 * Adds a group to a given place in the UI
 */
function addGroup(group)
{
    var noMembers = "noMembers_"+ group.position;           // Remove no members list item
    $(jq(noMembers)).remove();

    var students = group.students;                          // Add students to the list
    var membersListSelector = jq("members_" + group.position);
    for (var i in students)
    {
        var studentHTML = '<li class=\"list-group-item \" id=\"' + students[i].db_id + '\">' + students[i].name + ' ' + students[i].lastName + '</li>';
        $(membersListSelector).append(studentHTML);
    }

    // Black border to new operating group
    $(jq(group.position)).toggleClass('border-secondary border-dark');

    changeProgress(group);                                  // Assigment progress
    // Assigment progress color
    $(jq("progress_" + group.position)).toggleClass('badge-dark badge-success');
}

socket.on('joinedGroup', function(groupJson){
    var group = JSON.parse(groupJson);
    addGroup(group);
});

/**
 * Listens to students progress changes.
 */
socket.on('assigment_changeProgress', function(groupJson){
    var group = JSON.parse(groupJson);                      // obj from JSON
    changeProgress(group);
});

/**
 * Listens to students new doubts.
 */
socket.on('doubt_new', function(doubtJson){
    var doubt = JSON.parse(doubtJson);                      // obj from JSON
    appendDoubt(doubt);
});

/**
 *  Renders doubt HTML.
 */
function appendDoubt( doubtJson )
{
    const newDoubtHTML = 
    '<div class="card" id=\"doubt_' + doubtJson.db_id + '\">' + 
        '<div class="card-body">' +
            '<span class="badge badge-info">Section: ' + doubtJson.section + '</span>' + 
            '<span class="badge">Group: ' + doubtJson.group + '</span>' + 
            '<p class="card-text">' + doubtJson.text + '</p>' + 
        '</div>' + 
        '<ul class="list-group list-group-flush">' +
            // '<li class="list-group-item list-group-item-secondary">Cras justo odio</li>' +        
        '</ul>' +
        '<div class="card-body">' +
            '<button type=\"button\" class=\"btn btn-primary float-right\"' +
            ' data-toggle=\"modal\" data-target=\"#modal_answer\" ' +
            'data-doubtid=\"'+ doubtJson.db_id + '\">Solve doubt</button>' +            
        '</div>' +
    '</div>' +
    '<br>';
    let doubts = $("#doubts");                              // Locate doubts container
    doubts.append(newDoubtHTML);                            // Add doubt to doubts container
}

/**
 * Listens to new answers.
 */
socket.on('new_answer', function(anwserJson)
{
    var answer = JSON.parse(anwserJson);
    var doubtId = answer.doubtid;
    var text = answer.text;
    appendAnswer(doubtId, text);
})

/**
 * Renders answer HTML.
 */
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

/**
 * Ask for the session state to the server.
 */
function querySession()
{
    socket.emit('classroom_query');
}

/** 
 * Session query result to interface.
 */
socket.on('classroom_query_result', function(stateResultJson)
{
    var state = JSON.parse(stateResultJson);
    var groups = state.groups;
    var doubts = state.doubts;

    for(var i in groups)                                    // Render groups
    {
        addGroup(groups[i]);
    }

    for(var i in doubts)                                    // Render doubts
    {
        appendDoubt(doubts[i]);

        for(var j in doubts[i].answers)                     // Render doubts' answers
        {
            appendAnswer(doubts[i].db_id, doubts[i].answers[j].text);
        }
    }
});

