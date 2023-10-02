import * as React from 'react';
import TouchableOpacity from 'react-native';


export default function UploadingScreen({ uploading }) {
  const [isDisabled, setIsDisabled] = useState(false)

  const checkUploadStatus = () => {
    setIsDisabled(false)
  }

  return (
  <TouchableOpacity
    onPress={() =>
      navigation.navigate("HomeScreen", { language: "french" })
    }
    style={[
      styles.submitBtn,
      { backgroundColor: isValid ? "#B05D5D" : "#BB9393" },
    ]}
    disabled={isDisabled}
  >
    <Text style={[styles.submitBtnTxt]}>Return to Main Menu</Text>
  </TouchableOpacity>

  )
  // Finish Button -> Greyed out
  // Check for any frames that still need to be uploaded to backend
  // Once done - allow user to press finish back which navigates back to home screen.
}
