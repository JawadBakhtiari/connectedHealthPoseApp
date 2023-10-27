/* 
    Javascript code for the joint angle graph demo
    Handles session id and clip number input, sending a request to the backend to
    process this input and display a graph of the corresponding clip.
*/

let currentFrame = 0;
let numFrames = frameData.length;
let playing = false;
let looping = false;

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
    document.getElementById('pause-control-button').style.visibility = 'visable';
    playing = true;
    doGraphVisualisation()
});

document.getElementById('pause-control-button').addEventListener('click', function() {
    document.getElementById('pause-control-button').style.visibility = 'hidden';
    document.getElementById('play-control-button').style.visibility = 'visable';
    playing = false;
});

document.getElementById('forward-control-button').addEventListener('click', function() {
    currentFrame++;

    if (currentFrame > numFrames) {
        currentFrame = 0
    }
});

document.getElementById('loop-control-button').addEventListener('click', function() {
    document.getElementById('play-control-button').style.visibility = 'hidden';
    document.getElementById('pause-control-button').style.visibility = 'visable';
    looping = true;
});

function doGraphVisualisation(frameData, chartData) {
    /* Code to display the visualisation (create a video display) */
    let currentFrame = 0;
        
    function updateFrame() {
        const frameBase64Img = frameData[currentFrame];
        if (!frameBase64Img) {
            console.error('Invalid base64 image data:', frameBase64Img);
            console.error('Current frame:', currentFrame);
            console.error('Frame data:', frameData);
            return;
        }

        const chartBase46Img = chartData[currentFrame];
        if (!chartBase46Img) {
            console.error('Invalid base64 chart data:', chartBase46Img);
            console.error('Current frame:', currentFrame);
            console.error('Frame data:', chartData);
            return;
        }
        
        const image = document.getElementById("animation");
        image.src = "data:image/png;base64," + frameBase64Img;

        const chart = document.getElementById("chart")
        chart.src =  "data:image/png;base64," + chartBase46Img

        currentFrame++;
        if (currentFrame >= frameData.length) {
            currentFrame = 0;
        }
    }

    setInterval(updateFrame, 100);  // Adjust the interval (in milliseconds) to control the animation speed
};
