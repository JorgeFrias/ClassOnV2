/* Functions */
// Add a doubt to the HTML
function appendDoubt( doubtJson )
{
    let doubts = $("#doubts");                      // Locate doubts container
    const newDoubtHTML = '<div class=\"list-group-item flex-column align-items-start\" id=\"doubt_' + doubtJson.db_id + '\">' +
                         '<p class =\"mb-1\">' +
                         doubtJson.text +
                         '</p>' +
                         '<div>' +
                         '<span class=\"badge badge-info\">' + doubtJson.section + '</span>' +
                         '<button type=\"button\" class=\"btn btn-primary float-right\"' +
                         ' data-toggle=\"modal\" data-target=\"#modal_answer\">Solve doubt</button>' +
                         '<div><div>';
    doubts.append(newDoubtHTML);
}

/* Socket.io */
/** Emits  **/
// Generated new doubt --> upload to server
function doubt_click(text)
{
    socket.emit('doubt_post', text);

    // Give a lille time to the server
    var delayInMilliseconds = 10; //0.01 second
    setTimeout(function() {
      //your code to be executed after 0.01 second
    }, delayInMilliseconds);

    queryDoubts();
}

// Ask for doubts
function queryDoubts()
{
    socket.emit('doubt_query');
}

function answerDoubt()
{
    var answ = $("#text_answer").val();
    if (answ.length > 0)
    {
        socket.emit('answer_post', answ);
        $('#modal_answer').modal('hide');
    } else
    {
        
    }

}

/** Responses **/
// New doubt from server
socket.on('doubt_new', function(doubt)
{
    var doubtJson = JSON.parse(doubt);              // To JSON
    appendDoubt(doubtJson);
});
// Doubts query result
socket.on('doubt_query_result', function(doubts)
{
    var doubtsJson = JSON.parse(doubts);
    var doubts = doubtsJson.doubts;

    for(var i in doubts)
    {
        appendDoubt(doubts[i]);
    }
})

/* Plain JS Code */
window.onload = queryDoubts();                      // When page loads ask for doubts.

$(document).ready(function() {
    $("#btn_answer").click (answerDoubt);
});