import React, { useEffect, useState, useRef } from 'react';
import { StyleSheet, Text, View, Platform, Image, Button } from 'react-native';
import { Camera } from 'expo-camera';
import * as tf from '@tensorflow/tfjs';
import * as posedetection from '@tensorflow-models/pose-detection';
import { cameraWithTensors } from '@tensorflow/tfjs-react-native';
import * as FileSystem from 'expo-file-system';
import * as jpeg from 'jpeg-js';
import * as MediaLibrary from 'expo-media-library'


const TensorCamera = cameraWithTensors(Camera);

const IS_IOS = Platform.OS === 'ios';

const OUTPUT_TENSOR_WIDTH = 180;
const OUTPUT_TENSOR_HEIGHT = OUTPUT_TENSOR_WIDTH / (IS_IOS ? 9 / 16 : 3 / 4);


export default function App() {
  const cameraRef = useRef(null);
  const [tfReady, setTfReady] = useState(false);
  const [model, setModel] = useState();
  const [uri, setUri] = useState();
  const [poses, setPoses] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [cameraType, setCameraType] = useState(Camera.Constants.Type.front);
  const rafId = useRef(null);
  
  useEffect(() => {
    async function prepare() {
      rafId.current = null;

      await Camera.requestCameraPermissionsAsync();
      await tf.ready();
      
      const detectorConfig = {
        runtime: 'tfjs',
        enableSmoothing: true,
        modelType: 'lite'
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

  useEffect(() => {
    return () => {
      if (rafId.current != null && rafId.current !== 0) {
        cancelAnimationFrame(rafId.current);
        rafId.current = 0;
      }
    };
  }, []);

  const handleCameraStream = async (images) => {

    const loop = async () => {
      const tensor = images.next().value;
      
    
      const [height, width] = tensor.shape
      const data = new Buffer.from(
        // concat with an extra alpha channel and slice up to 4 channels to handle 3 and 4 channels tensors
        tf.concat([tensor, tf.ones([height, width, 1]).mul(255)], [-1])
          .slice([0], [height, width, 4])
          .dataSync(),
      )
      const rawImageData = {data, width, height};
      const jpegImageData = jpeg.encode(rawImageData, 200);

      const imgBase64 = tf.util.decodeString(jpegImageData.data, "base64")
      const salt = `${Date.now()}-${Math.floor(Math.random() * 10000)}`
      const uri = FileSystem.documentDirectory + `tensor-${salt}.jpg`;
      await FileSystem.writeAsStringAsync(uri, imgBase64, {
        encoding: FileSystem.EncodingType.Base64,
      });
      setUri(uri)
      console.log(uri)
      //await MediaLibrary.saveToLibraryAsync(uri); To test result off the tensor image

      const poses = await model.estimatePoses(
        tensor,
        undefined,
        Date.now()
      );
      setPoses(poses);
      tf.dispose([tensor]);
  
      if (rafId.current === 0) {
        return;
      }
  
      rafId.current = requestAnimationFrame(loop);
    };
  
    loop();
    
  };

  const renderPose = () => {
    if (poses != null && poses.length > 0 && isRecording) {
      let data = poses.find(poses => poses.keypoints)
      console.log(data)
 
    }
  };



  const renderCameraTypeSwitcher = () => {
    return (
      <View
        style={styles.cameraTypeSwitcher}
        onTouchEnd={handleSwitchCameraType}
      >
        <Text>
          Switch to{' '}
          {cameraType === Camera.Constants.Type.front ? 'back' : 'front'} camera
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
      <View
        style={styles.recordButton}
        onTouchEnd={handleRecording}
      >
        <Text style={styles.recordText}>{isRecording ? 'Stop' : 'Record'}</Text>
      </View>
    );
  };
  
  const handleRecording = () => {
    if (!isRecording) {
      setIsRecording(true);
    } else {
      setIsRecording(false)
    }
  };
 
  
  if (!tfReady) {
    return (
      <View style={styles.loadingMsg}>
        <Text>Loading...</Text>
      </View>
    );
  } else {
    return (
      <View style={styles.container}
      >
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
        
        {renderCameraTypeSwitcher()}
        {renderRecordButton()}
      </View>
    );
  }}

  const styles = StyleSheet.create({
    container: {
     flex: 1
    },
    loadingMsg: {
      position: 'absolute',
      width: '100%',
      height: '100%',
      alignItems: 'center',
      justifyContent: 'center',
    },
    camera: {
      width: '100%',
      height: '100%',
      flex: 1,
    },
    cameraTypeSwitcher: {
      position: 'absolute',
      top: 100,
      right: 10,
      width: 180,
      alignItems: 'center',
      backgroundColor: 'rgba(255, 255, 255, .7)',
      borderRadius: 2,
      padding: 8,
      zIndex: 20,
    },
    recordButton: {
      position: 'absolute',
      bottom: 16,
      right: 16,
      backgroundColor: 'red',
      borderRadius: 30,
      width: 60,
      height: 60,
      justifyContent: 'center',
      alignItems: 'center',
      zIndex: 20,
    },
    recordText: {
      color: 'white',
      fontSize: 18,
    },
  });