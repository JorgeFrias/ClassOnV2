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
});

socket.on('doubt_new', function(doubt){
    var doubtJson = JSON.parse(doubt);                          // To JSON
    appendDoubt(doubtJson);
});

function appendDoubt( doubtJson ) {
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

    {/*<div className="container">*/}
        {/*<h2>Doubts</h2>*/}
        {/*<!--Doubts container-->*/}
        {/*<div className="list-group" id="doubts">*/}
            {/*<!--This is a doubt-->*/}
            {/*<div className="list-group-item flex-column align-items-start" id="doubt_id">*/}
                {/*<p className="mb-1">*/}
                    {/*Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam dapibus leo ut suscipit dapibus.*/}
                    {/*Proin dignissim mollis tellus, et condimentum massa convallis et. Vivamus orci nisl, luctus nec*/}
                    {/*dapibus eget, cursus a velit. Nulla eget bibendum libero. Suspendisse ullamcorper vehicula mi in*/}
                    {/*ullamcorper. Mauris quam turpis, lacinia et purus a, tempus hendrerit mauris. Aliquam sed ex quam.*/}
                {/*</p>*/}
                {/*<div>*/}
                    {/*<span className="badge badge-info">Section 1</span>*/}
                    {/*<button type="button" className="btn btn-primary float-right">Solve doubt</button>*/}
                {/*</div>*/}
            {/*</div>*/}

        {/*</div>*/}
    {/*</div>*/}
}



function jq( myid ) {
    return "#" + myid.replace( /(:|\.|\[|\]|,|=|@)/g, "\\$1" );
}

function changeProgress(groupJson){
    $(jq("progress_" + groupJson.position)).text(groupJson.assigmentProgress);
}

