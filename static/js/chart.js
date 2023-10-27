/* 
    Javascript code for the joint angle graph demo
    Handles session id and clip number input, sending a request to the backend to
    process this input and display a graph of the corresponding clip.
*/

let currentFrame = 0;
let numFrames = frameData.length;
let loop = false;

const image = document.getElementById("animation");
image.src = "data:image/png;base64," + frameData[currentFrame];

const chart = document.getElementById("chart")
chart.src =  "data:image/png;base64," + chartData[currentFrame];

document.getElementById('rewind-control-button').addEventListener('click', function() {
    currentFrame = 0;
});

document.getElementById('backward-control-button').addEventListener('click', function() {
    currentFrame--;

    if (currentFrame < 0) {
        currentFrame = 0
    }
});

document.getElementById('play-control-button').addEventListener('click', function() {
    document.getElementById('play-control-button').style.visibility = 'hidden';
    console.log("HERE")
    document.getElementById('pause-control-button').style.visibility = 'visable';
    console.log("HERE")
    doGraphVisualisation()
});

document.getElementById('pause-control-button').addEventListener('click', function() {
    document.getElementById('pause-control-button').style.visibility = 'hidden';
    document.getElementById('play-control-button').style.visibility = 'visable';
});

document.getElementById('forward-control-button').addEventListener('click', function() {
    currentFrame++;

    if (currentFrame >= numFrames) {
        currentFrame = 0
    }
});

//
document.getElementById('loop-control-button').addEventListener('click', function() {
    document.getElementById('play-control-button').style.visibility = 'hidden';
    document.getElementById('pause-control-button').style.visibility = 'visable';
    looping = true;
});

function doGraphVisualisation() {
    setInterval(updateFrame, 100);

    function updateFrame() {
        const frameBase64Img = frameData[currentFrame];
        const chartBase46Img = chartData[currentFrame];
    
        const image = document.getElementById("animation");
        image.src = "data:image/png;base64," + frameBase64Img;

        const chart = document.getElementById("chart")
        chart.src =  "data:image/png;base64," + chartBase46Img
    }

    while (true) {
        updateFrame();

        currentFrame++;
        if (currentFrame >= numFrames) {
            currentFrame = 0;

            if (!loop) {
                document.getElementById('pause-control-button').style.visibility = 'hidden';
                document.getElementById('play-control-button').style.visibility = 'visable';
    
                const image = document.getElementById("animation");
                image.src = "data:image/png;base64," + frameData[currentFrame];
        
                const chart = document.getElementById("chart")
                chart.src =  "data:image/png;base64," + chartData[currentFrame];
            }
        }
    }
};

// function doGraphVisualisation(frameData, chartData) {
//     function updateFrame() {
//         const frameBase64Img = frameData[currentFrame];
//         if (!frameBase64Img) {
//             console.error('Invalid base64 image data:', frameBase64Img);
//             console.error('Current frame:', currentFrame);
//             console.error('Frame data:', frameData);
//             return;
//         }

//         const chartBase46Img = chartData[currentFrame];
//         if (!chartBase46Img) {
//             console.error('Invalid base64 chart data:', chartBase46Img);
//             console.error('Current frame:', currentFrame);
//             console.error('Frame data:', chartData);
//             return;
//         }
        
//         const image = document.getElementById("animation");
//         image.src = "data:image/png;base64," + frameBase64Img;

//         const chart = document.getElementById("chart")
//         chart.src =  "data:image/png;base64," + chartBase46Img

//         currentFrame++;
//         if (currentFrame >= frameData.length) {
//             currentFrame = 0;
//         }
//     }

//     setInterval(updateFrame, 100);  // Adjust the interval (in milliseconds) to control the animation speed
// };
