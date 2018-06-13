import * as $ from 'jquery';
import { Timer } from 'easytimer';
import { DataStructures } from './DataStructures';
import * as io from 'socket.io-client';

export class Connector
{
    private socket: SocketIOClient.Socket;

    constructor()
    {
        this.socket = io.connect('http://127.0.0.1:5000');
        this.setEventListerners();
    }

    /** Event listeners */
    setEventListerners(): void
    {    
        this.socket.on('connect', this.connect);
        this.socket.on('joinedGroup', this.joinedGroup);
        this.socket.on('assigment_changeProgress', this.changeProgress);
    }

    connect() : void
    {
        this.socket.emit('connection', { data: 'I\'m connected!' })
    }

    joinedGroup(groupJson: string): void
    {
        var group = JSON.parse(groupJson);
        addGroup(group);
    }

    changeProgress(): void
    {

    }

    /**
 * Listens to students progress changes.
 */
    socket.on('assigment_changeProgress', function(groupJson)
    {
        var group = JSON.parse(groupJson);                      // obj from JSON
        changeProgress(group);
    });

    /**
     * Listens to students new doubts.
     */
    socket.on('doubt_new', function(doubtJson)
    {
        var doubt = JSON.parse(doubtJson);                      // obj from JSON
        appendDoubtStudent(doubt);
        appendDoubt(doubt);
    });
/**
 * Keeps updated global variables
 * dictDoubtGroup
 * dictGroupDoubt
 */
function appendDoubtStudent(doubt)
{
    let id = doubt.db_id;
    let group = doubt.group;
    dictDoubtGroup[id.toString()] = group;
    dictGroupDoubt[group.toString()] = id;
}
function getGroup(doubt_id)
{
    let group = dictDoubtGroup[doubt_id.toString()]
    return group;
}

/**
 *  Renders doubt HTML.
 */
function appendDoubt(doubtJson)
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
        'data-doubtid=\"' + doubtJson.db_id + '\">Solve doubt</button>' +
        '</div>' +
        '</div>' +
        '<br>';
    let doubts = $("#doubts");                              // Locate doubts container
    doubts.append(newDoubtHTML);                            // Add doubt to doubts container
}

/**
 * Listens to new answers.
 */
socket.on('new_answer', function (anwserJson)
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
    var li = '<li class="list-group-item list-group-item-secondary">' + anwser + '</li>';
    $('#doubt_' + doubtId + '> ul').append(li);
}

function jq(myid)
{
    return "#" + myid.replace(/(:|\.|\[|\]|,|=|@)/g, "\\$1");
}

function changeProgress(groupJson)
{
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
socket.on('classroom_query_result', function (stateResultJson)
{
    var state = JSON.parse(stateResultJson);
    var groups = state.groups;
    var doubts = state.doubts;

    for (var i in groups)                                    // Render groups
    {
        addGroup(groups[i]);
    }

    for (var i in doubts)                                    // Render doubts
    {
        appendDoubt(doubts[i]);

        for (var j in doubts[i].answers)                     // Render doubts' answers
        {
            appendAnswer(doubts[i].db_id, doubts[i].answers[j].text);
        }
    }
});
}
