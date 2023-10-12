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
    document.getElementById('2D-visualisation-tab').addEventListener('click', function() {
        const url = getFullUrl('/data/visualise2D/');
        window.location.href = url;
    });

    // Add jump to graph demo
    document.getElementById('graph-tab').addEventListener('click', function() {
        const url = getFullUrl('/chart/');
        window.location.href = url;
    });

});