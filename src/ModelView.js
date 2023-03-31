import * as mobilenet from '@tensorflow-models/mobilenet';
import { Camera } from 'expo-camera';
import React from 'react';
import { StyleSheet, useWindowDimensions, View } from 'react-native';

import { CustomTensorCamera } from './CustomTensorCamera';
import { LoadingView } from './LoadingView';
import { PredictionList } from './PredictionList';
import { useTensorFlowModel } from './useTensorFlow';
import * as movenet from '@tensorflow-models/pose-detection'

export function ModelView() {
  const model = movenet.SupportedModels.BlazePose;
  const [predictions, setPredictions] = React.useState([]);

  if (!model) {
    return <LoadingView message="Loading TensorFlow model" />;
  }

  return (
    <View
      style={{ flex: 1, backgroundColor: "black", justifyContent: "center" }}
    >
      <PredictionList predictions={predictions} />
      <View style={{ borderRadius: 20, overflow: "hidden" }}>
        <ModelCamera model={model} setPredictions={setPredictions} />
      </View>
    </View>
  );
}

function ModelCamera({ model, setPredictions }) {
  const raf = React.useRef(null);
  const size = useWindowDimensions();

  React.useEffect(() => {
    return () => {
      cancelAnimationFrame(raf.current);
    };
  }, []);

  const onReady = React.useCallback(
    (images) => {
      const loop = async () => {
        const nextImageTensor = images.next().value;
        const detectorConfig = {
          modelType: 'lite',
          runtime: 'tfjs'
        };
        const timestamp = performance.now();
        const detector = await movenet.createDetector(model, detectorConfig);
        const predictions = await detector.estimatePoses(nextImageTensor, undefined, timestamp);
        let poses  = predictions.find(predictions => predictions.score)
        console.log(poses)
        //setPredictions(predictions);
        raf.current = requestAnimationFrame(loop);
      };
      loop();
    },
    //[setPredictions]
  );

  return React.useMemo(
    () => (
      <CustomTensorCamera
        width={size.width}
        style={styles.camera}
        type={Camera.Constants.Type.front}
        onReady={onReady}
        autorender
      />
    ),
    [onReady, size.width]
  );
}

const styles = StyleSheet.create({
  camera: {
    zIndex: 0,
  },
});
