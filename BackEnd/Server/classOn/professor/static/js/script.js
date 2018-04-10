socket.on('joinedGroup', function(group){
    var element = document.getElementById(group.position);
    var groupJson = JSON.parse(group);

    // Members
    var elem = element.getElementById("noMembers");     // Remove "No members"
    elem.parentNode.removeChild(elem);

    var students = groupJson.students.data;
    for (var student in students)
    {
        var studentHTML = '<li className=\"list-group-item\" id=\"student.db_id\">' + student.name + student.lastname + '</li>';
        $("members li:last").append(studentHTML);
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