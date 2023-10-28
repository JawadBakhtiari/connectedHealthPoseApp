/* 
    Javascript code for the joint angle graph demo
    Handles session id and clip number input, sending a request to the backend to
    process this input and display a graph of the corresponding clip.
*/

import { getFullUrl } from './helper.js';


// Navigation Bar
let tablePopupOpened = false;
let numFrames = frameData.length;
let keypoints = []

formatAngleData()
drawTable();

document.getElementById('back-button').addEventListener('click', function() {
    const url = getFullUrl(`/chart`);
    window.location.href = url;
});


document.getElementById('table-button').addEventListener('click', function() {
    if (!tablePopupOpened) {
        tablePopupOpened = true;
        window.location.href = `http://127.0.0.1:8000/chart/result/#popup-table`;
    } else {
        tablePopupOpened = false;
        window.location.href = `http://127.0.0.1:8000/chart/result/#`;
    }
});

function formatAngleData() {
    for (let i = 0; i < 8; i++) {
        let angles = []
        for (let j = 0; j < numFrames; j++) {
            angles.push(angleData[i][j].toFixed(2))
        }
        keypoints.push(angles)
    }
}

function drawTable() {
    const tblbody = document.getElementById('angle-table-body');

    if (dimensionData === '2d') {
        for (let i = 0; i < 7; i++) {
            const row = document.createElement("tr");

            for (let j = 0; j < numFrames; j++) {
                const cell = document.createElement("td");
                let celltext = document.createTextNode(String(j));

                if (i === 0) {
                    celltext = document.createTextNode(String(j));
                    if (j === 0) {
                        celltext = document.createTextNode('Frames');
                    }
                }

                if (i === 1) {
                    celltext = document.createTextNode(keypoints[0][j]);
                    if (j === 0) {
                        celltext = document.createTextNode('Left Roll');
                    }
                }

                if (i === 2) {
                    celltext = document.createTextNode(keypoints[1][j]);
                    if (j === 0) {
                        celltext = document.createTextNode('Left Pitch');
                    }
                }

                if (i === 3) {
                    celltext = document.createTextNode(keypoints[2][j]);
                    if (j === 0) {
                        celltext = document.createTextNode('Left Yaw');
                    }
                }

                if (i === 4) {
                    celltext = document.createTextNode(keypoints[3][j]);
                    if (j === 0) {
                        celltext = document.createTextNode('Right Roll');
                    }
                }

                if (i === 5) {
                    celltext = document.createTextNode(keypoints[4][j]);
                    if (j === 0) {
                        celltext = document.createTextNode('Right Pitch');
                    }
                }

                if (i === 6) {
                    celltext = document.createTextNode(keypoints[5][j]);
                    if (j === 0) {
                        celltext = document.createTextNode('Right Yaw');
                    }
                }

                cell.appendChild(celltext);
                row.appendChild(cell);
            }

            tblbody.appendChild(row);
        }

    } else {

    }
}


// Control Bar
let currentFrame = 0;
let previousFrame = 0;
let paused = false;
let loop = false;
let forward = true;
let speed = 2;
let delay = 100;
updateFrame()

document.getElementById('right-control-button').addEventListener('click', function() {
    document.getElementById('right-control-button').hidden = true;
    document.getElementById('left-control-button').hidden = false;
    forward = false;
});

document.getElementById('left-control-button').addEventListener('click', function() {
    document.getElementById('left-control-button').hidden = true;
    document.getElementById('right-control-button').hidden = false;
    forward = true;
});

document.getElementById('rewind-control-button').addEventListener('click', function() {
    currentFrame = 0;
    updateFrame();
});

document.getElementById('backward-control-button').addEventListener('click', function() {
    currentFrame--;
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

document.getElementById('speed-control-button').addEventListener('click', function() {
    speed++;
    if (speed > 4) {
        speed = 0
    }

    switch (speed) {
        case (0):
            document.getElementById('speed-control-button').innerHTML = "x0.25";
            delay = 400;
            break;
        case (1):
            document.getElementById('speed-control-button').innerHTML = "x0.5";
            delay = 200;
            break;
        case (2):
            document.getElementById('speed-control-button').innerHTML = "x1";
            delay = 100;
            break;
        case (3):
            document.getElementById('speed-control-button').innerHTML = "x2";
            delay = 50;
            break;
        case (4):
            document.getElementById('speed-control-button').innerHTML = "x4";
            delay = 25;
            break;
    }
});

const sleep = (delay) => {
    return new Promise(resolve => setTimeout(resolve, delay))
}

const doGraphVisualisation = async() => {
    while (true) {
        if (paused) {
            currentFrame = previousFrame;
            break;
        }

        updateFrame()

        if (forward) {
            previousFrame = currentFrame;
            currentFrame++;

            if (currentFrame >= numFrames) {
                currentFrame = 0;
    
                if (!loop) {
                    updatePlayPause();
                    break;
                }
            }
        } else {
            previousFrame = currentFrame;
            currentFrame--;

            if (currentFrame < 0) {
                currentFrame = numFrames - 1;
    
                if (!loop) {
                    updatePlayPause();
                    break;
                }
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

function updatePlayPause() {
    document.getElementById('pause-control-button').hidden = true;
    document.getElementById('play-control-button').hidden = false;
    paused = false;
    enableForwardBackward()
    updateFrame()
}
