import React, { useEffect, useState, useRef, useCallback } from "react";
import { StyleSheet, Text, View, Platform, Dimensions } from "react-native";
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

const TensorCamera = cameraWithTensors(Camera);

const IS_IOS = Platform.OS === "ios";

// The size of the resized output from TensorCamera.
const OUTPUT_TENSOR_WIDTH = 120;
const OUTPUT_TENSOR_HEIGHT = OUTPUT_TENSOR_WIDTH / (IS_IOS ? 9 / 16 : 3 / 4);

export default function App() {
  const cameraRef = useRef(null);
  const [tfReady, setTfReady] = useState(false);
  const [model, setModel] = useState();
  const [uri, setUri] = useState();
  // const [poses, setPoses] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [cameraType, setCameraType] = useState(Camera.Constants.Type.front);
  const rafId = useRef(null);
  const [fps, setFps] = useState(0);
  let lastSendTime = Date.now();
  const poses = [];
  const tensorAsArray = [];

  /**
   * This is a React useEffect hook that runs once when the component is mounted.
   * The empty dependency array ([]) ensures that the effect only runs once.
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
    prepare();
  }, []);

  /**
   * This is another useEffect hook that runs once when the component is mounted.
   * The empty dependency array ([]) ensures that the effect only runs once.
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
  }, []);

  /**
   * This toggles the isRecording state variable using the setIsRecording() function.
   **/
  const handleRecording = () => {
    setIsRecording((prevRecording) => !prevRecording);
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
      poses.push(newPoses);

      // Encode Image Data
      // encodeJPG(tensor);
      encodeRGB(tensor);

      // Disposes image tensoor to free memery resources after used
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

  // Function not working
  // const loadModel = async (tensor) => {
  //   const poses = await model.estimatePoses(tensor, undefined, Date.now());
  //   setPoses(poses);
  // };

  const renderFps = () => {
    return (
      <View style={styles.fpsContainer}>
        <Text>FPS: {fps}</Text>
      </View>
    );
  };

  const sendData = async () => {
    try {
      const response = Axios.post("http://192.168.0.137:9090/send/get_tensor", {
        poses,
        tensorAsArray,
      });
      // Empty Data
      poses.splice(0, poses.length);
      tensorAsArray.splice(0, tensorAsArray.length);
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
  };

  const encodeRGB = async (tensor) => {
    const data = tensor.arraySync();
    tensorAsArray.push(data);
    // Send 15 frames per request
    if (tensorAsArray.length == 15) {
      sendData();
    }
  };

  const encodeJpeg = async (tensor) => {
    /**
     * Prepare RGB Image Data
     * Concatenate the input tensor with an alpha channel tensor (if necessary) and extract RGB pixel values
     * Returns a flat array of RGB pixel values representing the image data
     **/
    const [height, width] = tensor.shape;
    const data = new Buffer.from(
      tf
        .concat([tensor, tf.ones([height, width, 1]).mul(255)], [-1])
        .slice([0], [height, width, 4])
        .dataSync()
    );
    /**
     * The jpeg.encode() function is called with two arguments: rawImageData and 100.
     * rawImageData: This object contains the raw image data, width, and height of the image.
     * 100: This parameter represents the quality setting for JPEG encoding.
     * Higher values (up to 100) indicate better quality but larger file sizes.
     **/
    const rawImageData = { data, width, height };
    const jpegImageData = jpeg.encode(rawImageData, 100);

    /**
     * Convert Encoded Image to Base64 and Save to File
     *  - Decode the base64-encoded image data from `jpegImageData.data`
     * - Generate a unique file name with a timestamp and random number (`salt`)
     * - Create the URI for the file in the document directory
     * - Write the base64-encoded image data to the file using `FileSystem.writeAsStringAsync()`
     * The resulting URI can be used to access the saved image file
     **/
    // console.log()
    const imgBase64 = tf.util.decodeString(jpegImageData.data, "base64");
    const salt = `${Date.now()}-${Math.floor(Math.random() * 10000)}`;
    const uri = FileSystem.documentDirectory + `tensor-${salt}.jpg`;
    await FileSystem.writeAsStringAsync(uri, imgBase64, {
      encoding: FileSystem.EncodingType.Base64,
    });
    setUri(uri);

    //await MediaLibrary.saveToLibraryAsync(uri); // To test result of the tensor image
  };

  const renderPose = () => {
    if (poses != null && poses.length > 0) {
      let data = poses.find((poses) => poses.keypoints3D);
      data["frame_image"] = uri;
      console.log(data);
    }
  };

  const renderCameraTypeSwitcher = () => {
    return (
      <View
        style={styles.cameraTypeSwitcher}
        onTouchEnd={handleSwitchCameraType}
      >
        <Text>
          Switch to{" "}
          {cameraType === Camera.Constants.Type.front ? "back" : "front"} camera
        </Text>
      </View>
    );
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
      <View style={styles.recordButton} onTouchEnd={handleRecording}>
        <Text style={styles.recordText}>{isRecording ? "Stop" : "Record"}</Text>
      </View>
    );
  };

  if (!tfReady) {
    return (
      <View style={styles.loadingMsg}>
        <Text>Loading...</Text>
      </View>
    );
  } else {
    return (
      <View style={styles.container}>
        <TensorCamera
          ref={cameraRef}
          style={styles.camera}
          autorender={true}
          type={cameraType}
          // tensor related props
          resizeWidth={OUTPUT_TENSOR_WIDTH}
          resizeHeight={OUTPUT_TENSOR_HEIGHT}
          resizeDepth={3}
          onReady={handleCameraStream}
        />
        {/* {renderPose()} */}
        {renderFps()}
        {renderCameraTypeSwitcher()}
        {renderRecordButton()}
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingMsg: {
    position: "absolute",
    width: "100%",
    height: "100%",
    alignItems: "center",
    justifyContent: "center",
  },
  camera: {
    width: "100%",
    height: "100%",
    flex: 1,
  },
  cameraTypeSwitcher: {
    position: "absolute",
    top: 100,
    right: 10,
    width: 180,
    alignItems: "center",
    backgroundColor: "rgba(255, 255, 255, .7)",
    borderRadius: 2,
    padding: 8,
    zIndex: 20,
  },
  recordButton: {
    position: "absolute",
    bottom: 16,
    right: 16,
    backgroundColor: "red",
    borderRadius: 30,
    width: 60,
    height: 60,
    justifyContent: "center",
    alignItems: "center",
    zIndex: 20,
  },
  recordText: {
    color: "white",
    fontSize: 18,
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
});
