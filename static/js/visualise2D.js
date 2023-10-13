/* 
    Javascript code for the visualisation demo
    Handles session id and clip number input, sending a request to the backend to
    process this input and display a visualisation of the corresponding clip.
*/

import { getFullUrl } from './helper.js';

document.addEventListener('DOMContentLoaded', function() {
    /*  When start button is clicked, send session id and clip number in request 
        to backend. 
    */
    const sessionId = document.getElementById('session-id-input');
    const clipNum = document.getElementById('clip-num-input');
    const startButton = document.getElementById('start-visualisation-button');

    startButton.addEventListener('click', function() {
        requestVisualisation(sessionId.value, clipNum.value);
    });
});

function requestVisualisation(sessionId, clipNum) {
    const url = getFullUrl('/data/visualise2D/');

    //const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    //xhr.setRequestHeader('X-CSRFToken', csrfToken);

    xhr.onerror = function() {
        console.error('Request failed');
    };

    const data = JSON.stringify({ sid: sessionId, clip_num: clipNum });
    xhr.send(data);
}




