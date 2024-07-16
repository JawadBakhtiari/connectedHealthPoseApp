/* 
    Javascript code for the visualisation demo
    Handles session id and clip number input, sending a request to the backend to
    process this input and display a visualisation of the corresponding clip.
*/

import { getFullUrl } from "./helper.js";

function requestVisualisation(sessionId, clipNum) {
  const url = getFullUrl(
    `/data/visualise2D/?sid=${sessionId}&clipNum=${clipNum}`
  );
  window.location.href = url;
}

export const doVisualisation = (frameData) => {
  /* Code to display the visualisation (create a video display) */
  let currentFrame = 0;

  function updateFrame() {
    const base64Img = frameData[currentFrame];
    if (!base64Img) {
      console.error("Invalid base64 image data:", base64Img);
      console.error("Current frame:", currentFrame);
      console.error("Frame data:", frameData);
      return;
    }

    const img = document.getElementById("animation");
    img.src = "data:image/png;base64," + base64Img;

    currentFrame++;
    if (currentFrame >= frameData.length) {
      currentFrame = 0;
    }
  }

  setInterval(updateFrame, 55); // Adjust the interval (in milliseconds) to control the animation speed
};

document.addEventListener("DOMContentLoaded", function () {
  /*  When start button is clicked, send session id and clip number in request 
        to backend. 
    */
  const sessionId = document.getElementById("session-id-input");
  const clipNum = document.getElementById("clip-num-input");
  const startButton = document.getElementById("start-visualisation-button");

  startButton.addEventListener("click", function () {
    requestVisualisation(sessionId.value, clipNum.value);
  });

  doVisualisation(frameData);
});
