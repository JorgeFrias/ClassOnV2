socket.on('doubt_new', function(doubt)
{
    var doubtJson = JSON.parse(doubt);                          // To JSON
    appendDoubt(doubtJson);
});

function appendDoubt( doubtJson )
{
    let doubts = $("#doubts");                      // Locate doubts container
    const newDoubtHTML = '<div class=\"list-group-item flex-column align-items-start\" id=\"doubt_' + doubtJson.db_id + '\">' +
                         '<p class =\"mb-1\">' +
                         doubtJson.text +
                         '</p>' +
                         '<div>' +
                         '<span class=\"badge badge-info\">' + doubtJson.section + '</span>' +
                         '<button type=\"button\" class=\"btn btn-primary float-right\">Solve doubt</button>' +
                         '<div><div>';
    doubts.append(newDoubtHTML);
}

function doubt_click(text)
{
    socket.emit('doubt_post', text);
}

function queryDoubts()
{
    socket.emit('doubt_query');
}

socket.on('doubt_query_result', function(doubts)
{
    var doubtsJson = JSON.parse(doubts);
    var doubts = doubtsJson.doubts;

    for(var i in doubts)
    {
        appendDoubt(doubts[i]);
    }
})

window.onload = queryDoubts();