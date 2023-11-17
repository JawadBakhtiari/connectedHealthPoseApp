/* 
    Javascript code for the joint angle graph demo
    Handles session id and clip number input, sending a request to the backend to
    process this input and display a graph of the corresponding clip.
*/

import { getFullUrl } from './helper.js';



// Navigation Bar
let tablePopupOpened = false;
const numFrames = frameData.length;
const formatedAngles = formatAngleData();
const tableAngles = formatedAngles.tableAngles;
const graphAngles = formatedAngles.graphAngles;
const labels = getGraphLabels();
let leftChart, rightChart;

// Draw table and graph

// Vertical Line Indicator
let verticalLinePlugin = {
    afterDraw: function(chart) {
        console.log("BYE")
        const ctx = chart.ctx;
        const xAxis = chart.scales['x-axis-0'];
        const topY = chart.chartArea.top;
        const bottomY = chart.chartArea.bottom;

        console.log(xAxis)
    
        if (xAxis) {
            console.log("HERE")
            const labelz = chart.data.labels;
            console.log(labelz)
            const indexC = labels.indexOf('C');

            if (indexC !== -1) {
              const barWidth = xAxis.width / labels.length;
              const xValue = xAxis.left + (barWidth * (indexC + 0.5));
            }

            ctx.save();
            ctx.beginPath();
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 2;
            ctx.moveTo(xValue, topY);
            ctx.lineTo(xValue, bottomY);
            ctx.stroke();
            ctx.restore();
        }
    }
};

draw()

// Format Angle Data
function formatAngleData() {
    let tableAngles = [];
    let graphAngles = [];
    for (let i = 0; i < 8; i++) {
        let currentTableAngles = [];
        let currentGraphAngles = [];
        for (let j = 0; j < numFrames; j++) {
            let rounded = angleData[i][j].toFixed(2);
            currentTableAngles.push(rounded + '°');
            currentGraphAngles.push(rounded);
        }
        tableAngles.push(currentTableAngles);
        graphAngles.push(currentGraphAngles);
    }

    return { tableAngles, graphAngles };
}

// Get Graph Labels
function getGraphLabels() {
    var labels = ['C'];
    for (let i = 0; i < numFrames; i += 1) {
        labels.push(i);
    }

    return labels;
}

// Draw table and graph
function draw() {
    let data, leftData, rightData, leftConfig, rightConfig;
    if (dimensionData === '2d') {
        drawTable2d();
        data = get2dGraphData();
        leftData = data.leftData;
        rightData = data.rightData;
    } else {
        drawTable3d();
        data = get3dGraphData();
        leftData = data.leftData;
        rightData = data.rightData;
    }

    // Draw Graph
    leftConfig = getGraphConfig(leftData, "Left " + jointData);
    rightConfig = getGraphConfig(rightData, "Right " + jointData);
    const leftAngleChart = document.getElementById('chart-left');
    const rightAngleChart = document.getElementById('chart-right');
    leftChart = new Chart(leftAngleChart, leftConfig);
    rightChart = new Chart(rightAngleChart, rightConfig);
}


// Get Graph Configuration
function getGraphConfig(data, title) {
    return {
        type: 'line',
        data: data,
        options: {
            plugins: {
                title: {
                    display: true,
                    text: title
                },
                tooltip: {
                    enabled: true,
                    intersect: false,
                    mode: 'nearest',
                },
                verticalLine: verticalLinePlugin,
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time (Seconds)'
                    },
                },
                y: {
                    title: {
                        display: true,
                        text: 'Angle (°)'
                    },
                }
            },
            zoom: {
                zoom: {
                  wheel: {
                    enabled: true,
                  },
                  pinch: {
                    enabled: true
                  },
                  mode: 'xy'
                }
            }
        }
    };
}

// Get Graph Data
function get2dGraphData() {
    const leftData = {
        labels: labels,
        datasets: [{
            label: 'Roll',
            data: graphAngles[0],
            borderColor: 'red',
    
        },
        {
            label: 'Pitch',
            data: graphAngles[1],
            borderColor: 'green',
        },
        {
            label: 'Yaw',
            data: graphAngles[2],
            borderColor: 'blue',
        }]
    };

    const rightData = {
        labels: labels,
        datasets: [{
            label: 'Roll',
            data: graphAngles[3],
            borderColor: 'red',
    
        },
        {
            label: 'Pitch',
            data: graphAngles[4],
            borderColor: 'green',
        },
        {
            label: 'Yaw',
            data: graphAngles[5],
            borderColor: 'blue',
        }],
        options: {
            fill: false,
            borderWidth: 2
        }
    };

    return { leftData, rightData };
}

function get3dGraphData() {
    const leftData = {
        labels: labels,
        data: graphAngles[6]
    };

    const rightData = {
        labels: labels,
        data: graphAngles[7]
    };

    return { leftData, rightData };
}

// Draw Table
function drawTable2d() {
    let tbl = document.getElementById('angle-table-left');

    for (let i = 0; i < 4; i++) {
        const row = document.createElement("tr");

        for (let j = -1; j < numFrames; j++) {
            let cell = 0;
            if (j == -1 || i == 0) {
                cell = document.createElement("th");
            } else {
                cell = document.createElement("td");
            }
            
            let celltext = document.createTextNode(String(j));

            if (i == 0) {
                if (j == -1) {
                    celltext = document.createTextNode('Second');
                }
            }

            if (i == 1) {
                celltext = document.createTextNode(tableAngles[0][j]);
                if (j == -1) {
                    celltext = document.createTextNode('Roll');
                }
            }

            if (i == 2) {
                celltext = document.createTextNode(tableAngles[1][j]);
                if (j == -1) {
                    celltext = document.createTextNode('Pitch');
                }
            }

            if (i == 3) {
                celltext = document.createTextNode(tableAngles[2][j]);
                if (j == -1) {
                    celltext = document.createTextNode('Yaw');
                }
            }

            cell.appendChild(celltext);
            row.appendChild(cell);
        }

        tbl.appendChild(row);
    }

    tbl = document.getElementById('angle-table-right');

    for (let i = 0; i < 4; i++) {
        const row = document.createElement("tr");

        for (let j = -1; j < numFrames; j++) {
            let cell = 0;
            if (j == -1 || i == 0) {
                cell = document.createElement("th");
            } else {
                cell = document.createElement("td");
            }
            
            let celltext = document.createTextNode(String(j));

            if (i == 0) {
                if (j == -1) {
                    celltext = document.createTextNode('Second');
                }
            }

            if (i == 1) {
                celltext = document.createTextNode(tableAngles[3][j]);
                if (j == -1) {
                    celltext = document.createTextNode('Roll');
                }
            }

            if (i == 2) {
                celltext = document.createTextNode(tableAngles[4][j]);
                if (j == -1) {
                    celltext = document.createTextNode('Pitch');
                }
            }

            if (i == 3) {
                celltext = document.createTextNode(tableAngles[5][j]);
                if (j == -1) {
                    celltext = document.createTextNode('Yaw');
                }
            }

            cell.appendChild(celltext);
            row.appendChild(cell);
        }

        tbl.appendChild(row);
    }
}

function drawTable3d() {
    let tbl = document.getElementById('angle-table-left');

    for (let i = 0; i < 2; i++) {
        const row = document.createElement("tr");

        for (let j = -1; j < numFrames; j++) {
            let cell = 0;
            if (j == -1 || i == 0) {
                cell = document.createElement("th");
            } else {
                cell = document.createElement("td");
            }
            
            let celltext = document.createTextNode(String(j));

            if (i == 0) {
                if (j == -1) {
                    celltext = document.createTextNode('Second');
                }
            }

            if (i == 1) {
                celltext = document.createTextNode(tableAngles[6][j]);
                if (j == -1) {
                    celltext = document.createTextNode('Angle');
                }
            }

            cell.appendChild(celltext);
            row.appendChild(cell);
        }

        tbl.appendChild(row);
    }

    tbl = document.getElementById('angle-table-right');

    for (let i = 0; i < 2; i++) {
        const row = document.createElement("tr");

        for (let j = -1; j < numFrames; j++) {
            let cell = 0;
            if (j == -1 || i == 0) {
                cell = document.createElement("th");
            } else {
                cell = document.createElement("td");
            }
            
            let celltext = document.createTextNode(String(j));

            if (i == 0) {
                if (j == -1) {
                    celltext = document.createTextNode('Second');
                }
            }

            if (i == 1) {
                celltext = document.createTextNode(tableAngles[7][j]);
                if (j == -1) {
                    celltext = document.createTextNode('Angle');
                }
            }

            cell.appendChild(celltext);
            row.appendChild(cell);
        }

        tbl.appendChild(row);
    }
}

// Back Button
document.getElementById('back-button').addEventListener('click', function() {
    const url = getFullUrl(`/chart`);
    window.location.href = url;
});

// Table Button
document.getElementById('table-button').addEventListener('click', function() {
    if (!tablePopupOpened) {
        tablePopupOpened = true;
        document.getElementById('table-button').style.backgroundColor = "#6693F5";
        window.location.href = `http://127.0.0.1:8000/chart/result/#popup-table`;
    } else {
        tablePopupOpened = false;
        document.getElementById('table-button').style.backgroundColor = "white";
        window.location.href = `http://127.0.0.1:8000/chart/result/#`;
    }
});

document.getElementById('popup-table-close-button').addEventListener('click', function() {
    document.getElementById('table-button').style.backgroundColor = "white";
});

window.addEventListener('hashchange', function() {
    if (window.location.href.includes('popup-table')) {
        document.getElementById('table-button').style.backgroundColor = "#6693F5";
    } else {
        document.getElementById('table-button').style.backgroundColor = "white";
    }
});



// Control Bar
let currentFrame = 0;
let previousFrame = 0;
let paused = false;
let loop = false;
let forward = true;
let speed = 2;
let delay = 100;
updateFrame()

let myChart = document.getElementById("chart-left");
function moveLine(direction) {
    const xAxis = myChart.scales['x-axis-0'];
    const labels = myChart.data.labels;
    const currentIndex = labels.indexOf('C'); // Assuming initial position at label 'C'
  
    if (direction === 'left' && currentIndex > 0) {
      labels[currentIndex] = labels[currentIndex - 1];
      labels[currentIndex - 1] = 'C';
    } else if (direction === 'right' && currentIndex < labels.length - 1) {
      labels[currentIndex] = labels[currentIndex + 1];
      labels[currentIndex + 1] = 'C';
    }
  
    myChart.update();
}

document.getElementById('right-control-button').addEventListener('click', function() {
    document.getElementById('right-control-button').hidden = true;
    document.getElementById('left-control-button').hidden = false;
    forward = false;
});

document.getElementById('left-control-button').addEventListener('click', function() {
    document.getElementById('left-control-button').hidden = true;
    document.getElementById('right-control-button').hidden = false;
    forward = true;
    moveLine('left')
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
    moveLine('right')
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
    const image = document.getElementById("animation");
    image.src = "data:image/png;base64," + frameBase64Img;
}

function disableForwardBackward() {
    document.getElementById('backward-control-button').disabled = true;
    document.getElementById('backward-control-button').style.borderColor = "#D3D3D3";
    document.getElementById('backward-control-button').style.backgroundColor = "#E6F7FD";
    document.getElementById('backward-control-button').style.cursor = "default";
    document.getElementById('forward-control-button').disabled = true;
    document.getElementById('forward-control-button').style.borderColor = "#D3D3D3";
    document.getElementById('forward-control-button').style.backgroundColor = "#E6F7FD";
    document.getElementById('forward-control-button').style.cursor = "default";
}

function enableForwardBackward() {
    document.getElementById('backward-control-button').disabled = false;
    document.getElementById('backward-control-button').style.borderColor = "#ADD8E6";
    document.getElementById('backward-control-button').style.backgroundColor = "#ADD8E6";
    document.getElementById('backward-control-button').style.cursor = "pointer";
    document.getElementById('forward-control-button').disabled = false;
    document.getElementById('forward-control-button').style.borderColor = "#ADD8E6";
    document.getElementById('forward-control-button').style.backgroundColor = "#ADD8E6";
    document.getElementById('forward-control-button').style.cursor = "pointer";
    
}

function updatePlayPause() {
    document.getElementById('pause-control-button').hidden = true;
    document.getElementById('play-control-button').hidden = false;
    paused = false;
    enableForwardBackward()
    updateFrame()
}
