
import { TouchableOpacity, StyleSheet, Text, View, SafeAreaView, TextInput, Button } from 'react-native';
import { useState, useRef } from 'react';
import { useNavigation } from '@react-navigation/native';
import ProgressBar from 'react-native-progress/Bar';
import * as Yup from "yup";
import { Formik } from 'formik';
/*
Potential function for more randomised upload bar
const countInterval = useRef(null)
  const [count, setCount] = useState(0);
  useEffect(() => {
    countInterval.current = setInterval(() => setCount((prev) => prev + 5), 1000)
    return () => {
      clearInterval(countInterval);
    };
  }, []);
*/


const SignupSchema = Yup.object().shape({
  notes: Yup.string()
  .min(10, "Please enter at least 10 characters")
  .max(300, "Maximum of 300 characters allowed")
});


export default function UploadingScreen({ navigation }) {
  const [uploadCheck, setUploadCheck] = useState(false)
  const [submitCheck, setSubmitCheck] = useState(true)
  const [progress, setProgress] = useState(0);
  const handlePress = () => {
    setUploadCheck(true)
    for (let i = 0; i <= 100; i++) {
      setProgress(i)
      i = i + 0.10
    }
    setSubmitCheck(false)
  };
  
  return (
    <Formik
      initialValues={{
        notes: "Reflect on your session here",
      }}
      validationSchema={SignupSchema}
    >
      <SafeAreaView style={styles.wrapper}> 
        <View style={styles.formContainer}>
          <Text style={styles.title}>
            Session Notes
          </Text>
          
          <View style={styles.inputStyle}>
            <Text style={styles.inputWrapper}>Notes (optional)</Text>
              <TextInput multiline={true} maxLength={300} blurOnSubmit={true} style={styles.inputBox}>
              </TextInput>   
          </View>
                 
          <TouchableOpacity style={styles.submitBtn} onPress={handlePress}>
            <Text style={styles.submitBtnTxt}>Upload Session</Text>
          </TouchableOpacity>
          <View style={styles.progress}>
            <ProgressBar progress={progress} width={300} height={25}/>
          </View>
          
          <TouchableOpacity style={[styles.submitBtn, { backgroundColor: submitCheck ? "#D3D3D3" : "#008000" }]} onPress={() => navigation.navigate("Home", { language: "french" })} disabled={submitCheck}>
            <Text style={styles.submitBtnTxt}>Submit Session</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
      
    </Formik>
  )
  

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
    marginLeft: -5,
    padding: 30,
  },
  formContainer: {
    backgroundColor: "#F5EDDC",
    padding: 20,
    borderRadius: 20,
    width: "90%",
  },
  wrapper: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#423B3B",
    paddingHorizontal: 15,
  },
  title: {
    color: "#16213E",
    fontSize: 26,
    fontWeight: "700",
    marginBottom: 15,
    textAlign: "center",
  },
  inputWrapper: {
    marginBottom: 15,
  },
  inputStyle: {
    borderColor: "#16213E",
    borderWidth: 1,
    borderRadius: 5,
    padding: 15,
  },
  inputBox: {
    borderColor: "#16213E",
    borderWidth: 1,
    borderRadius: 5,
    padding: 15,
    height: 150,
    textAlign: 'left',
  },
  submitBtn: {
    backgroundColor: "#395B64",
    padding: 10,
    borderRadius: 15,
    justifyContent: "center",
    marginTop: 15,
  },
  submitBtnTxt: {
    textAlign: "center",
    fontSize: 18,
    fontWeight: "700",
  },
});
