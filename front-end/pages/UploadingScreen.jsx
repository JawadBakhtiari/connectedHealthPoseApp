
import { TouchableOpacity, StyleSheet, Text, View, SafeAreaView, TextInput, Button } from 'react-native';
import { useState } from 'react';
import { useNavigation } from '@react-navigation/native';
import ProgressBar from 'react-native-progress/Bar'



export default function UploadingScreen({ navigation }) {
  const [uploadCheck, setUploadCheck] = useState(false)
  const [submitCheck, setSubmitCheck] = useState(true)
  const [progress, setProgress] = useState(0);
  const handlePress = () => {
    setUploadCheck(true)
    for (let i = 0; i <= 100; i++) {
      setProgress(i)
      i = i + 0.25
    }
    setSubmitCheck(false)
  };
  
  

  return (
    <View style={styles.container}>
    <View style={styles.progress}>
        <ProgressBar progress={progress} width={300} height={25}/>
      </View>
    <View>
      <Button onPress={handlePress} title="Upload Video" disabled={uploadCheck}/>
    </View>
      <View style={styles.textContainer}>
        <Text>Additional Notes (optional):</Text>
      </View>
      <SafeAreaView>
        <TextInput
          style={styles.input}
          placeholder='Input notes here'
        />
        
      </SafeAreaView>
      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate("Home", { language: "french" })} disabled={submitCheck}>
        <Text>Submit Session</Text>
      </TouchableOpacity>
    </View>
  );  

}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 10,
    backgroundColor: "#423B3B",
    width: "100%",
    height: "100%",
  },
  button: {
    alignItems: 'center',
    backgroundColor: '#DDDDDD',
    padding: 10,
  },
  textContainer: {
    alignItems: 'center',
    padding: 10,
    color: "#FFFFFF",
    borderColor: "#FFFFFF",
  },
  input: {
    alignItems: "flex-start",
    height: 200,
    margin: 12,
    borderWidth: 2,
    padding: 10,
    borderColor: "#FFFFFF",
    color: "#FFFFFF",
    textAlign: "left",
  },
  progress: {
    margin: 'auto',
    right: -30,
    padding: 30,
    
  }
});