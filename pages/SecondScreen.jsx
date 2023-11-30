import React, { useEffect, useState, useRef, useCallback } from "react";
import {
  StyleSheet,
  Text,
  View,
  Platform,
  Image,
  Dimensions,
  Modal,
  Button,
  TouchableOpacity,
} from "react-native";
import { Camera } from "expo-camera";
import { GLView } from "expo-gl";
import * as tf from "@tensorflow/tfjs";
import * as posedetection from "@tensorflow-models/pose-detection";
import { cameraWithTensors } from "@tensorflow/tfjs-react-native";
import * as FileSystem from "expo-file-system";
import * as jpeg from "jpeg-js";
import * as MediaLibrary from "expo-media-library";
import { encode, decode } from "base64-arraybuffer";
import Axios from "axios";
import { Fontisto } from "@expo/vector-icons";

const TensorCamera = cameraWithTensors(Camera);

const IS_IOS = Platform.OS === "ios";

// The size of the resized output from TensorCamera.
const OUTPUT_TENSOR_WIDTH = 120;
const OUTPUT_TENSOR_HEIGHT = OUTPUT_TENSOR_WIDTH / (IS_IOS ? 9 / 16 : 3 / 4);

export default function SecondScreen({ route, navigation }) {
  const cameraRef = useRef(null);
  const [tfReady, setTfReady] = useState(false);
  const [recorded, setRecorded] = useState(false);
  const [model, setModel] = useState(null);
  //const [poses, setPoses] = useState([]);
  const [cameraType, setCameraType] = useState(Camera.Constants.Type.front);
  const rafId = useRef(null);
  const [fps, setFps] = useState(0);
  let lastSendTime = Date.now();
  const poses = [];
  const tensorAsArray = [];
  const [activateEffect, setActivateEffect] = useState(false);
  const [timer, setTimer] = useState(0);
  const { uid } = route.params;
  const { sid } = route.params;
  const { code } = route.params;

  /**
   * This is a React useEffect hook that runs when the component is mounted.
   * The dependency array ([activateEffect]) ensures that the effect is run every time we press the button.
   * Inside this effect, an asynchronous function prepare() is defined.
   **/
  useEffect(() => {
    /**
     * This is an asynchronous function named prepare(), defined inside the useEffect hook.
     * It initializes the camera permissions, waits for TensorFlow.js to be ready,
     * and prepares the pose detection model.
     **/
    async function prepare() {
      rafId.current = null;

      await Camera.requestCameraPermissionsAsync();
      await tf.ready();
      /**
       * Pose Detection Setup:
       * The code sets up the configuration object for the pose detector, specifying runtime, smoothing, and model type.
       * It then calls the createDetector() function provided by the posedetection module to create the pose detection model.
       * The created model is stored in the state using the setModel() function.
       * The state variable tfReady is set to true using the setTfReady() function.
       **/
      const detectorConfig = {
        runtime: "tfjs",
        enableSmoothing: true,
        modelType: "lite",
      };

      const model = await posedetection.createDetector(
        posedetection.SupportedModels.BlazePose,
        detectorConfig
      );
      setModel(model);
      setTfReady(true);
    }
    if (activateEffect) {
      prepare();
    } else {
      // If activateEffect is false, setModel to empty and setTfReady to false
      setModel(null);
      setTfReady(false);
    }
  }, [activateEffect]);

  /**
   * This is another useEffect hook that runs when the component is mounted.
   * Inside this effect, a cleanup function is defined.
   **/
  useEffect(() => {
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

  useEffect(() => {
    let interval;

    if (tfReady) {
      interval = setInterval(() => {
        setTimer((prevTimer) => prevTimer + 1);
      }, 1000);
    } else {
      clearInterval(interval);
      setTimer(0);
    }

    return () => clearInterval(interval);
  }, [tfReady]);

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
      sendLastData();
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

  const sendLastData = async () => {
    try {
      const response = Axios.post("http://" + code + "/data/frames/upload/", {
        // uid: "ahmad232",
        sid,
        // clipNum: "1",
        clipFinished: true,
        poses,
        tensorAsArray,
      });
      // Empty Data
      poses.splice(0, poses.length);
      tensorAsArray.splice(0, tensorAsArray.length);
      console.log("sending last data:");
    } catch (err) {
      console.log(err);
    }
  };

  const sendData = async () => {
    try {
      const response = Axios.post("http://" + code + "/data/frames/upload/", {
        // uid: "ahmad232",
        sid,
        // clipNum: "1",
        clipFinished: false,
        poses,
        tensorAsArray,
      });
      // Empty Data
      poses.splice(0, poses.length);
      tensorAsArray.splice(0, tensorAsArray.length);
      console.log("sending data:");
    } catch (err) {
      console.log(err);
    }
  };

  const encodeJPG = async (tensor) => {
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
    tensorAsArray.push(base64jpeg);
    if (tensorAsArray.length == 15) {
      sendData();
      // console.log("sending data");
    }
  };

  const encodeRGB = async (tensor) => {
    const data = tensor.arraySync();
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

  const handleSwitchCameraType = () => {
    if (cameraType === Camera.Constants.Type.front) {
      setCameraType(Camera.Constants.Type.back);
    } else {
      setCameraType(Camera.Constants.Type.front);
    }
  };

  const renderRecordButton = () => {
    return (
      <View style={styles.recordButton}>
        <TouchableOpacity style={styles.recordB} onPress={handleTf}>
          <View style={[styles.inner, tfReady && styles.activeInner]}></View>
        </TouchableOpacity>
      </View>
    );
  };

  const renderExitButton = () => {
    return (
      <View
        style={styles.ExitButton}
        onTouchEnd={() => navigation.navigate("Home", { language: "french" })}
      >
        <Image
          source={require("./assets/exitB.png")}
          style={styles.ExitImage}
        />
      </View>
    );
  };

  const renderSwitchCamButton = () => {
    return (
      <View style={styles.SwitchButton} onTouchEnd={handleSwitchCameraType}>
        <Fontisto name="arrow-swap" size={24} color="white" />
      </View>
    );
  };

  const rendertimer = () => {
    return (
      <View style={styles.timercontain}>
        {tfReady ? (
          <View style={styles.activeTimer}>
            <Text style={styles.timerText}>{formatTime(timer)}</Text>
          </View>
        ) : (
          <View style={styles.notactiveTimer}>
            <Text style={styles.timerText}>{formatTime(timer)}</Text>
          </View>
        )}
      </View>
    );
  };

  if (!tfReady) {
    return (
      <View style={styles.container}>
        <View style={styles.top}>
          {renderExitButton()}
          <View style={styles.timercontain}>{rendertimer()}</View>
          <View style={{ flex: 1 }}></View>
        </View>
        <Camera ref={cameraRef} style={styles.camera} type={cameraType} />
        <View style={styles.bottom}>
          <View style={{ flex: 1 }}></View>
          <View style={styles.recordcontain}>{renderRecordButton()}</View>
          <View style={styles.switchcontain}>{renderSwitchCamButton()}</View>
        </View>
      </View>
    );
  } else {
    return (
      <View style={styles.container}>
        <View style={styles.top}>
          <View style={{ flex: 1 }}></View>
          <View style={styles.timercontain}>{rendertimer()}</View>
          <View style={{ flex: 1 }}></View>
        </View>
        <TensorCamera
          ref={cameraRef}
          style={styles.tcamera}
          autorender={true}
          type={cameraType}
          // tensor related props
          resizeWidth={OUTPUT_TENSOR_WIDTH}
          resizeHeight={OUTPUT_TENSOR_HEIGHT}
          resizeDepth={3}
          onReady={handleCameraStream}
        />
        {/*renderPose()*/}
        {renderFps()}
        <View style={styles.bottom}>
          <View style={{ flex: 1 }}></View>
          <View style={styles.recordcontain}>{renderRecordButton()}</View>
          <View style={styles.switchcontain}>{renderSwitchCamButton()}</View>
        </View>
      </View>
    );
  }
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
