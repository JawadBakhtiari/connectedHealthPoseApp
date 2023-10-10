/*
    Make the application sidebar dynamic.
*/

import { getFullUrl } from './helper.js';

document.addEventListener('DOMContentLoaded', function() {
    // Link source code
    document.getElementById('source-code-tab').addEventListener('click', function() {
        window.open('https://github.com/nick-maiden/connectedhealth', '_blank');
    });

    // Add jump to 2D visualisation demo
    document.getElementById('2D-animation-demo-tab').addEventListener('click', function() {
    const url = getFullUrl('/data/visualise2D/');

    const xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');

    // Send empty request to get to demo page
    const data = JSON.stringify({ sid: null, clip_num: null});
    xhr.send(data);
    });
});