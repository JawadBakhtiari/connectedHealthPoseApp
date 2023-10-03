
import { TouchableOpacity, StyleSheet, Text, View, SafeAreaView, TextInput } from 'react-native';
import { useState } from 'react';
import { useNavigation } from '@react-navigation/native';



export default function UploadingScreen({ navigation }) {
  const [isDisabled, setIsDisabled] = useState(true)

  const checkUploadStatus = () => {
    setIsDisabled(false)
  }

  return (
    <View style={styles.container}>
      <View style={styles.textContainer}>
        <Text>Additional Notes (optional):</Text>
      </View>
      <SafeAreaView>
        <TextInput
          style={styles.input}
          placeholder='Input notes here'
        />
        
      </SafeAreaView>
      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate("Home", { language: "french" })}>
        <Text>Submit Session</Text>
      </TouchableOpacity>
    </View>
  );
  // Finish Button -> Greyed out
  // Check for any frames that still need to be uploaded to backend
  // Once done - allow user to press finish back which navigates back to home screen.
  

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
});