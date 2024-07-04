import { useEffect, useState, useRef } from "react";
import Axios from "axios";
import {
  View,
  Text,
  ActivityIndicator,
  StyleSheet,
  TouchableOpacity,
  Image,
} from "react-native";
import {
  useCameraPermission,
  useCameraDevice,
  Camera,
  useFrameProcessor,
  useCameraFormat,
  enableFpsGraph,
} from "react-native-vision-camera";
import { Fontisto } from "@expo/vector-icons";
import { date } from "yup";
import { CameraRoll } from "@react-native-camera-roll/camera-roll";
import { useTensorflowModel } from "react-native-fast-tflite";
import { useResizePlugin } from "vision-camera-resize-plugin";
import { useSharedValue } from "react-native-worklets-core";
import { VideoCodec } from "expo-camera";
import { time } from "@tensorflow/tfjs";

// import { resize } from "./resizePlugin";

export default function VisionCamera({ route, navigation }) {
  const { hasPermission, requestPermission } = useCameraPermission();
  const front = useCameraDevice("front");
  const back = useCameraDevice("back");
  const [device, setDevice] = useState(front);
  const cameraRef = useRef(null);
  const format = useCameraFormat(device, [
    { videoResolution: { width: 320, height: 240 } },
  ]);
  const rotation = Platform.OS === "ios" ? "0deg" : "270deg"; // hack to get android oriented properly
  const { resize } = useResizePlugin();
  const [picture, setPicture] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const isAlsoRecording = useSharedValue(0);
  const [video, setVideo] = useState(null);
  const poses = useSharedValue([]);
  const timeStarted = useSharedValue(0);
  const { sid } = route.params;
  const { code } = route.params;
  const tensorAsArray = [];
  const plugin = useTensorflowModel(
    require("./assets/pose_landmark_lite.tflite")
  );

  // Request for permission
  useEffect(() => {
    if (!hasPermission) {
      requestPermission();
    }
  }, [hasPermission]);

  // Render spinner while it doesent have permission
  if (!hasPermission) {
    return <ActivityIndicator />;
  }

  console.log("Vision Camera has permission: ", hasPermission);

  const sendData = async () => {
    "worklet";
    const poses3 = poses.value;
    try {
      const response = await Axios.post(
        "http://" + code + "/data/poses/upload/",
        {
          // uid: "ahmad232",
          sid,
          poses: JSON.stringify(poses3),
          tensorAsArray,
        }
      );
      // Empty Data
      // console.log(response.data);
      console.log("sending data:");
      poses.value = [];
    } catch (err) {
      console.log(err);
    }
  };

  const startSendingData = () => {
    intervalId = setInterval(() => {
      if (poses.value.length > 0) {
        sendData();
      }
    }, 1000); // Run every 1 second
  };

  const stopSendingData = async () => {
    clearInterval(intervalId);
    poses.value = [];
  };

  const frameProcessor = useFrameProcessor(
    (frame) => {
      "worklet";
      // console.log(
      //   `Frame: ${frame.width}x${frame.height} (${frame.pixelFormat})`
      // );

      const timestamp = Date.now();

      if (timeStarted.value == 0) {
        timeStarted.value = timestamp;
      }

      if (plugin.state === "loaded" && isAlsoRecording.value === 1) {
        const resized = resize(frame, {
          scale: {
            width: 256,
            height: 256,
          },
          pixelFormat: "rgb",
          dataType: "float32",
          rotation: rotation,
        });
        const outputs = plugin.model.runSync([resized]);
        outputs[0]["timestamp"] = timestamp;
        poses.value.push(outputs[0]);
        console.log(poses.value.length);
      }
    },
    [plugin]
  );

  const takePhoto = async () => {
    "worklet";
    const photo = await cameraRef.current?.takePhoto();
    console.log(photo);
    setPicture(photo);
    await CameraRoll.save(`file://${photo.path}`, {
      type: "photo",
    });
  };

  const onStartRecording = async () => {
    if (!cameraRef.current) {
      return;
    }
    if (isRecording) {
      await stopSendingData();
      isAlsoRecording.value = 0;
      cameraRef.current.stopRecording();
      return;
    }
    setIsRecording(true);
    isAlsoRecording.value = 1;
    startSendingData(); // Start sending data when recording starts

    console.log("Recording");
    cameraRef.current.startRecording({
      onRecordingFinished: async (video) => {
        console.log(video);
        setIsRecording(false);
        setVideo(video);

        const path = video.path;

        const data = new FormData();

        data.append("video", {
          name: "mobile-video-upload",
          type: "video/quicktime",
          uri: path,
        });

        data.append("sid", sid);

        try {
          const res = await fetch("http://" + code + "/data/video/upload/", {
            method: "post",
            body: data,
          });
        } catch (e) {
          console.error(e);
        }

        await CameraRoll.save(`file://${path}`, {
          type: "video",
        });
      },
      onRecordingError: (error) => {
        console.error(error);
        isAlsoRecording.value = 0;
        setIsRecording(false);
        stopSendingData();
      },
    });
  };

  const renderRecordButton = () => {
    return (
      <View style={styles.recordButton}>
        <TouchableOpacity style={styles.recordB} onPress={onStartRecording}>
          <View style={isRecording ? styles.activeInner : styles.inner}></View>
        </TouchableOpacity>
      </View>
    );
  };

  const handleSwitchCameraType = () => {
    if (device === front) {
      setDevice(back);
    } else {
      setDevice(front);
    }
  };

  const renderSwitchCamButton = () => {
    return (
      <View style={styles.SwitchButton} onTouchEnd={handleSwitchCameraType}>
        <Fontisto name="arrow-swap" size={24} color="white" />
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {picture ? (
        <Image source={{ uri: picture.path }} style={StyleSheet.absoluteFill} />
      ) : (
        <>
          <Camera
            format={format}
            ref={cameraRef}
            style={styles.camera}
            device={device}
            isActive={true && !picture}
            frameProcessor={frameProcessor}
            photo={true}
            video={true}
            pixelFormat="rgb"
            enableFpsGraph={true}
          />
          <View style={styles.bottom}>
            <View style={{ flex: 1 }}></View>
            <View style={styles.recordcontain}>{renderRecordButton()}</View>
            <View style={styles.switchcontain}>{renderSwitchCamButton()}</View>
          </View>
        </>
      )}
    </View>
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
    borderRadius: 50,
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
