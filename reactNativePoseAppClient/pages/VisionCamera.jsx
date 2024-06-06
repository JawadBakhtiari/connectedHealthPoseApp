import { useEffect, useState, useRef } from "react";
import {
  View,
  Text,
  ActivityIndicator,
  StyleSheet,
  TouchableOpacity,
} from "react-native";
import {
  useCameraPermission,
  useCameraDevice,
  Camera,
  useFrameProcessor,
  useCameraFormat,
} from "react-native-vision-camera";
import { Fontisto } from "@expo/vector-icons";
import { date } from "yup";

import { useTensorflowModel } from "react-native-fast-tflite";
import { useResizePlugin } from "vision-camera-resize-plugin";
// import { resize } from "./resizePlugin";

const VisionCamera = () => {
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
  // const { resize } = resize();

  const plugin = useTensorflowModel(
    require("./assets/lite-model_movenet_singlepose_lightning_tflite_int8_4.tflite")
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

  // const frameProcessor = useFrameProcessor((frame) => {
  //   "worklet";
  //   console.log(`Frame: ${frame.width}x${frame.height} (${frame.pixelFormat})`);
  //   if (frame.pixelFormat === "rgb") {
  //     const buffer = frame.toArrayBuffer();
  //     const data = new Uint8Array(buffer);
  //     console.log(`Pixel at 0,0: RGB(${data[0]}, ${data[1]}, ${data[2]})`);
  //   }
  // }, []);

  const frameProcessor = useFrameProcessor(
    (frame) => {
      "worklet";
      console.log(
        `Frame: ${frame.width}x${frame.height} (${frame.pixelFormat})`
      );
      if (plugin.state === "loaded") {
        const resized = resize(frame, {
          scale: {
            width: 192,
            height: 192,
          },
          pixelFormat: "rgb",
          dataType: "uint8",
          rotation: rotation,
        });
        const outputs = plugin.model.runSync([resized]);
        console.log(`Received ${outputs.length} outputs!`);
        console.log(outputs);
      }
    },
    [plugin]
  );

  const takePhoto = async () => {
    const photo = await cameraRef.current?.takePhoto();
    console.log(photo);
  };

  const renderRecordButton = () => {
    return (
      <View style={styles.recordButton}>
        <TouchableOpacity style={styles.recordB} onPress={takePhoto}>
          <View style={[styles.inner, styles.activeInner]}></View>
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
      <Camera
        format={format}
        ref={cameraRef}
        style={styles.camera}
        device={device}
        isActive={true}
        frameProcessor={frameProcessor}
        photo={true}
        pixelFormat="rgb"
      />
      <View style={styles.bottom}>
        <View style={{ flex: 1 }}></View>
        <View style={styles.recordcontain}>{renderRecordButton()}</View>
        <View style={styles.switchcontain}>{renderSwitchCamButton()}</View>
      </View>
    </View>
  );
};

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

export default VisionCamera;
