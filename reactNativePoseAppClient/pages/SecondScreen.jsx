import React, { useEffect, useState, useRef } from "react";
import { StyleSheet, Text, View } from "react-native";
import * as tf from "@tensorflow/tfjs";
import * as jpeg from "jpeg-js";
import Axios from "axios";
import { useCameraPermission, useCameraDevice, Camera, useFrameProcessor } from "react-native-vision-camera";
import { loadTensorflowModel } from "react-native-fast-tflite";
import { useResizePlugin } from "vision-camera-resize-plugin";

const MODEL_NAME = 'movenetLightning.tflite';
const MODEL_PATH = `./assets/${MODEL_NAME}`

export default async function SecondScreen({ route, navigation }) {
  const [model, setModel] = useState(null);
  const [recorded, setRecorded] = useState(false);
  const { requestPermission } = useCameraPermission();
  // const [cameraType, setCameraType] = useState('back');
  const device = useCameraDevice('back');
  const rafId = useRef(null);
  const [fps, setFps] = useState(0);
  const poses = [];
  const tensorAsArray = [];
  const [activateEffect, setActivateEffect] = useState(false);
  const { resize } = useResizePlugin();
  const { sid, code } = route.params;

  useEffect(() => {
    /**
     * Request camera permission from user and load pose detection model.
     **/
    const loadModel = async () => {
        rafId.current = null;
        await requestPermission();
        const poseDetection = await loadTensorflowModel(require(MODEL_PATH));
        setModel(poseDetection);
    };

    loadModel();

    return () => {
      /**
       * The cleanup function checks if the rafId (requestAnimationFrame ID) is set
       * and cancels the animation frame using cancelAnimationFrame() if needed.
       * It ensures that any pending animation frames are cleared when the component is unmounted.
       **/
      if (rafId.current != null && rafId.current !== 0) {
        cancelAnimationFrame(rafId.current);
        rafId.current = 0;
      }
    };
  }, [activateEffect]);

  const frameProcessor = useFrameProcessor((frame) => {
    'worklet'
    if (model == null) return

    // Resize 4k Frame to 192x192x3 using vision-camera-resize-plugin
    const resized = resize(frame, {
        scale: {
          width: 192,
          height: 192,
        },
        pixelFormat: 'rgb',
        dataType: 'uint8',
    });

    // Run model with given input buffer synchronously
    const outputs = model.runSync([resized]);
    console.log(outputs);

    // TODO : now what ???

}, [model])

  const formatTime = (timeInSeconds) => {
    const hours = Math.floor(timeInSeconds / 3600);
    const minutes = Math.floor((timeInSeconds % 3600) / 60);
    const seconds = timeInSeconds % 60;

    return `${hours.toString().padStart(2, "0")}:${minutes
      .toString()
      .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
  };

  /**
   * This toggles the activateeffect state variable
   **/
  const handleTf = () => {
    setActivateEffect((prevEffect) => !prevEffect);

    setRecorded(true);

    if (recorded == true) {
      // Send rest of data once user has ended recording and switch to next screen
      sendData(true);
      setRecorded(false);
      // navigation.navigate("Uploading", { language: "french " });
    }
  };

  /**
   * Takes an images parameter.
   * Responsible for processing the camera stream and running the BlazePose model on the captured images.
   **/
  const handleCameraStream = async (images) => {
    const loop = async () => {
      // This marks the starting time of the image processing for measuring latency.
      const startTs = Date.now();

      /**
       * This line retrieves the next image from the images object using the next() method.
       * The value property contains the actual image tensor data.
       **/
      const tensor = images.next().value;

      // KeyPoint Calculation
      const newPoses = await model.estimatePoses(tensor, undefined, Date.now());
      if (newPoses.length != 0) {
        poses.push(newPoses);
        encodeJPG(tensor);
        // encodeRGB(tensor);
      }

      // Disposes image tensor to free memery resources after used
      tf.dispose([tensor]);

      // Calculates the latency in order to get the FPS
      const latency = Date.now() - startTs;
      setFps(Math.floor(1000 / latency));

      // If current animation frame is no longer processing then exit
      if (rafId.current === 0) {
        return;
      }
      rafId.current = requestAnimationFrame(loop);
    };
    loop();
  };

  const renderFps = () => {
    return (
      <View style={styles.fpsContainer}>
        <Text>FPS: {fps}</Text>
      </View>
    );
  };

  const sendData = async (last = false) => {
    try {
      const response = Axios.post("http://" + code + "/data/frames/upload/", {
        // uid: "ahmad232",
        sid,
        // clipNum: "1",
        clipFinished: last,
        poses,
        tensorAsArray,
      });
      // Empty Data
      poses.splice(0, poses.length);
      tensorAsArray.splice(0, tensorAsArray.length);
      console.log(last ? "sending last data" : "sending data");
    } catch (err) {
      console.log(err);
    }
  };
  12;

  const encodeJPG = async (tensor) => {
    // Get Time photo was taken
    var today = new Date();
    var date =
      today.getFullYear() +
      "-" +
      (today.getMonth() + 1) +
      "-" +
      today.getDate();
    var time =
      today.getHours() +
      ":" +
      today.getMinutes() +
      ":" +
      today.getSeconds() +
      ":" +
      today.getMilliseconds();
    var dateTime = date + " " + time;

    // JPEG conversion
    const [height, width] = tensor.shape;
    const data = new Buffer.from(
      tf
        .concat([tensor, tf.ones([height, width, 1]).mul(255)], [-1])
        .slice([0], [height, width, 4])
        .dataSync()
    );
    const rawImageData = { data, width, height };
    const jpegImageData = jpeg.encode(rawImageData, 100);
    const base64jpeg = tf.util.decodeString(jpegImageData.data, "base64");

    tensorAsArray.push([base64jpeg, dateTime]);
    console.log(dateTime);
    if (tensorAsArray.length == 15) {
      sendData();
      // console.log("sending data");
    }
  };

  const encodeRGB = async (tensor) => {
    const data = [tensor.arraySync(), Date.now()];
    tensorAsArray.push(data);
    // Send 15 frames per request
    if (tensorAsArray.length == 15) {
      sendData();
      // console.log("sending data");
    }
  };

  const renderPose = () => {
    if (poses != null && poses.length > 0) {
      let data = poses.find((poses) => poses.keypoints3D);
      console.log(data);
    }
  };

  // const handleSwitchCameraType = () => {
  //   cameraType === 'front' ? setCameraType('back') : setCameraType('front');
  // };

  return (
      <Camera
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        frameProcessor={frameProcessor}
      />
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "column",
  },
  top: {
    flex: 1,
    width: "100%",
    height: "100%",
    backgroundColor: "#423B3B",
    flexDirection: "row",
    justifyContent: "space-evenly",
  },
  bottom: {
    flex: 1,
    flexDirection: "row",
    justifyContent: "space-evenly",
    width: "100%",
    height: "100%",
    backgroundColor: "#423B3B",
  },
  camera: {
    width: "100%",
    height: "100%",
    flex: 6,
  },
  tcamera: {
    width: "100%",
    height: "100%",
    flex: 8,
  },
  ExitButton: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  ExitImage: {
    width: 40,
    height: 40,
    right: 40,
    top: 10,
  },
  timercontain: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  timerText: {
    top: 5,
    fontSize: 20,
    marginBottom: 16,
    color: "white",
  },
  activeTimer: {
    top: 20,
    backgroundColor: "red",
    alignItems: "center",
    borderRadius: 5,
    width: 100,
    height: 35,
  },
  notactiveTimer: {
    top: 20,
    alignItems: "center",
    borderRadius: 5,
    width: 120,
    height: 50,
  },
  recordcontain: {
    flex: 1,
    justifyContent: "center",
  },
  recordButton: {
    alignSelf: "center",
    bottom: 5,
  },
  recordB: {
    width: 60,
    height: 60,
    borderColor: "white",
    borderWidth: 5,
    borderRadius: 50,
  },
  inner: {
    backgroundColor: "#9e1919",
    width: "100%",
    height: "100%",
    borderRadius: "50%",
    transitionProperty: "all",
    transitionDuration: 200,
    transitionTimingFunction: "ease",
    transform: [{ scale: 0.94 }],
  },
  activeInner: {
    backgroundColor: "#9e1919",
    width: "100%",
    height: "100%",
    transform: [{ scale: 0.5 }],
    borderRadius: "12%",
  },
  fpsContainer: {
    position: "absolute",
    top: 100,
    left: 10,
    width: 80,
    alignItems: "center",
    backgroundColor: "rgba(255, 255, 255, .7)",
    borderRadius: 2,
    padding: 8,
    zIndex: 20,
  },
  switchcontain: {
    flex: 1,
    justifyContent: "center",
  },
  SwitchButton: {
    alignSelf: "flex-end",
    right: 25,
    backgroundColor: "#796A6A",
    borderRadius: 30,
    width: 50,
    height: 50,
    justifyContent: "center",
    alignItems: "center",
  },
});
