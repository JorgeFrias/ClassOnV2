socket.on('joinedGroup', function(group){
    var groupJson = JSON.parse(group);                          // To JSON
//    var element = document.getElementById(groupJson.position);
//    $element = $('#'+groupJson.position)
    // Members
//    var elem = element.getElementById("noMembers");     // Remove "No members"
//    elem.parentNode.removeChild(elem);

    $("#noMembers"+groupJson.position).remove();       // Remove no members

    var students = groupJson.students;
    for (var i in students)
    {
        var studentHTML = '<li className=\"list-group-item\" id=\"' + students[i].db_id + '\">' + students[i].name + ' ' + students[i].lastName + '</li>';
        $("#members li:last").append(studentHTML);
    }

    // <div class="card border-secondary" id="{{ row ~ ',' ~ column }}">
    //     <div class="card-body">
    //         <!--<h5 class="card-title" >Progress:</h5>-->
    //         <h5>
    //             <span class="badge badge-dark" id="progress">0</span>
    //             <span class="badge badge-warning" id="doubt">Doubt</span>
    //         </h5>
    //     </div>
    //     <ul class="list-group list-group-flush" id="members">
    //         <li class="list-group-item" id="noMembers"><small>No members yet</small></li>
    //     </ul>
    // </div>

});