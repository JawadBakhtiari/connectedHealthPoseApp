/* 
    Javascript code for the joint angle graph demo
    Handles session id and clip number input, sending a request to the backend to
    process this input and display a graph of the corresponding clip.
*/

import { getFullUrl } from './helper.js';

// Navigation bar
document.getElementById('back-button').addEventListener('click', function() {
    const url = getFullUrl(`/chart`);
    window.location.href = url;
});

document.getElementById('table-button').addEventListener('click', function() {
    const url = getFullUrl(`/chart`);
    window.location.href = url;
});


// Set initial variables for control bar
let currentFrame = 0;
let numFrames = frameData.length;
let paused = false;
let loop = false;
let delay = 100;
updateFrame()

document.getElementById('rewind-control-button').addEventListener('click', function() {
    currentFrame = 0;
    updateFrame();
});

document.getElementById('backward-control-button').addEventListener('click', function() {
    currentFrame-=2;
    if (currentFrame < 0) {
        currentFrame = numFrames - 1
    }
    updateFrame();
});

document.getElementById('play-control-button').addEventListener('click', function() {
    document.getElementById('play-control-button').hidden = true;
    document.getElementById('pause-control-button').hidden = false;
    paused = false;
    disableForwardBackward()
    doGraphVisualisation()
});

document.getElementById('pause-control-button').addEventListener('click', function() {
    document.getElementById('pause-control-button').hidden = true;
    document.getElementById('play-control-button').hidden = false;
    paused = true;
    enableForwardBackward()
});

document.getElementById('forward-control-button').addEventListener('click', function() {
    currentFrame++;
    if (currentFrame >= numFrames) {
        currentFrame = 0
    }
    updateFrame();
});

document.getElementById('loop-control-button').addEventListener('click', function() {
    if (loop) {
        loop = false;
        document.getElementById('loop-control-button').style.backgroundColor = "#ADD8E6";
    } else {
        loop = true;
        document.getElementById('loop-control-button').style.backgroundColor = "#6693F5";
    }
});

const sleep = (delay) => {
    return new Promise(resolve => setTimeout(resolve, delay))
}

const doGraphVisualisation = async() => {
    while (true) {
        if (paused) {
            break;
        }

        updateFrame()

        currentFrame++;
        if (currentFrame >= numFrames) {
            currentFrame = 0;

            if (!loop) {
                document.getElementById('pause-control-button').hidden = true;
                document.getElementById('play-control-button').hidden = false;
                paused = false;
                enableForwardBackward()
                updateFrame()
                break;
            }
        }

        await sleep(delay);
    }
};

function updateFrame() {
    const frameBase64Img = frameData[currentFrame];
    const chartBase46Img = chartData[currentFrame];
    const image = document.getElementById("animation");
    image.src = "data:image/png;base64," + frameBase64Img;
    const chart = document.getElementById("chart")
    chart.src =  "data:image/png;base64," + chartBase46Img
}

function disableForwardBackward() {
    document.getElementById('backward-control-button').disabled = true;
    document.getElementById('backward-control-button').style.borderColor = "#D3D3D3";
    document.getElementById('backward-control-button').style.backgroundColor = "#E6F7FD";
    document.getElementById('forward-control-button').disabled = true;
    document.getElementById('forward-control-button').style.borderColor = "#D3D3D3";
    document.getElementById('forward-control-button').style.backgroundColor = "#E6F7FD";
}

function enableForwardBackward() {
    document.getElementById('backward-control-button').disabled = false;
    document.getElementById('backward-control-button').style.borderColor = "#ADD8E6";
    document.getElementById('backward-control-button').style.backgroundColor = "#ADD8E6";
    document.getElementById('forward-control-button').disabled = false;
    document.getElementById('forward-control-button').style.borderColor = "#ADD8E6";
    document.getElementById('forward-control-button').style.backgroundColor = "#ADD8E6";
}
