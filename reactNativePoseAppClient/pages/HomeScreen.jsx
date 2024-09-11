import {
  StyleSheet,
  Text,
  TextInput,
  View,
  SafeAreaView,
  StatusBar,
  TouchableOpacity,
  Alert,
} from "react-native";
import Axios from "axios";
import React, { useState } from "react";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

// Validation Schema //
const SignupSchema = Yup.object().shape({
  code: Yup.string()
    .min(3, "Too Short!")
    .max(100, "Too Long!")
    .required("Please enter connection code."),
  first_name: Yup.string()
    .min(5, "Too Short!")
    .max(20, "Too Long!")
    .required("Please enter first name."),
  last_name: Yup.string()
    .min(5, "Too Short!")
    .max(20, "Too Long!")
    .required("Please enter a last name."),
  session_name: Yup.string()
    .min(3, "Too Short!")
    .max(100, "Too Long!")
    .required("Please enter a session name."),
  session_description: Yup.string()
    .min(3, "Too Short!")
    .max(100, "Too Long!")
    .required("Please enter a session name."),
});

export default function HomeScreen({ navigation }) {
  return (
    <Formik
      initialValues={{
        code: "3.104.215.22:8000", // Enter IP Address and port of back-end i.e 192.168.0.137:8000
        first_name: "Ahmad",
        last_name: "Bakhtiari",
        session_name: "Elbow Physio",
        session_description: "elbow movement excercizes",
      }}
      validationSchema={SignupSchema}
      onSubmit={(values) => sendUserInit(values, navigation)}
    >
      {/* Props */}
      {({
        values,
        errors,
        touched,
        handleChange,
        setFieldTouched,
        isValid,
        handleSubmit,
      }) => (
        <SafeAreaView style={styles.wrapper}>
          <StatusBar barStyle={"light-content"} />

          {/* Form */}
          <View style={styles.formContainer}>
            <Text style={styles.title}>Session Details</Text>

            {/* Input: Code */}
            <View style={styles.inputWrapper}>
              <Text>Connection Code:</Text>
              <TextInput
                style={styles.inputStyle}
                value={values.code}
                onChangeText={handleChange("code")}
                onBlur={() => setFieldTouched("code")}
              />
              {touched.code && errors.code && (
                <Text style={styles.errorTxt}>{errors.code}</Text>
              )}
            </View>

            {/* Input: First Name */}
            <View style={styles.inputWrapper}>
              <Text>First Name:</Text>
              <TextInput
                style={styles.inputStyle}
                // placeholder={values.last_name}
                value={values.first_name}
                onChangeText={handleChange("first_name")}
                onBlur={() => setFieldTouched("first_name")}
              />
              {touched.first_name && errors.first_name && (
                <Text style={styles.errorTxt}>{errors.first_name}</Text>
              )}
            </View>

            {/* Input: Last Name */}
            <View style={styles.inputWrapper}>
              <Text>Last Name:</Text>
              <TextInput
                style={styles.inputStyle}
                // placeholder={values.last_name}
                value={values.last_name}
                onChangeText={handleChange("last_name")}
                onBlur={() => setFieldTouched("last_name")}
              />
              {touched.last_name && errors.last_name && (
                <Text style={styles.errorTxt}>{errors.last_name}</Text>
              )}
            </View>

            {/* Input: Session Name */}
            <View style={styles.inputWrapper}>
              <Text>Session Name:</Text>
              <TextInput
                style={styles.inputStyle}
                // placeholder={values.last_name}
                value={values.session_name}
                onChangeText={handleChange("session_name")}
                onBlur={() => setFieldTouched("session_name")}
              />
              {touched.session_name && errors.session_name && (
                <Text style={styles.errorTxt}>{errors.session_name}</Text>
              )}
            </View>

            {/* Input: Session Description */}
            <View style={styles.inputWrapper}>
              <Text>Session Description:</Text>
              <TextInput
                style={styles.inputStyle}
                // placeholder={values.last_name}
                value={values.session_description}
                onChangeText={handleChange("session_description")}
                onBlur={() => setFieldTouched("session_description")}
              />
              {touched.session_description && errors.session_description && (
                <Text style={styles.errorTxt}>
                  {errors.session_description}
                </Text>
              )}
            </View>

            {/* Button*/}
            <TouchableOpacity
              onPress={() => {
                handleSubmit();
              }}
              style={[
                styles.submitBtn,
                { backgroundColor: isValid ? "#B05D5D" : "#BB9393" },
              ]}
              disabled={!isValid}
            >
              <Text style={[styles.submitBtnTxt]}>Run Model</Text>
            </TouchableOpacity>
          </View>
        </SafeAreaView>
      )}
    </Formik>
  );
}

const sendUserInit = async (values, navigation) => {
  let code = values.code;
  let uid = "";
  let sid = "";

  // Initilize and Retrieve User
  try {
    const response = await Axios.post(
      "http://" + code + "/data/api/init_user/",
      {
        first_name: values.first_name,
        last_name: values.last_name,
      }
    ).then((response) => {
      uid = response.data.uid;
    });
    console.log("Sending User Details");
  } catch (err) {
    console.log(err);
  }

  // Initilize and Retrieve Session
  try {
    const response = await Axios.post(
      "http://" + code + "/data/session/init/",
      {
        session: {
          name: values.session_name,
          description: values.session_description,
        },
      }
    ).then((response) => {
      sid = response.data.sid;
    });
    console.log("Sending Session Details");
  } catch (err) {
    console.log(err);
  }

  navigation.navigate("VisionCamera", { code: code, sid: sid, uid: uid });
};

const styles = StyleSheet.create({
  wrapper: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#423B3B",
    paddingHorizontal: 15,
  },
  formContainer: {
    backgroundColor: "#F5EDDC",
    padding: 20,
    borderRadius: 20,
    width: "90%",
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
    borderRadius: 10,
    padding: 10,
  },
  submitBtn: {
    padding: 10,
    borderRadius: 15,
    justifyContent: "center",
  },
  submitBtnTxt: {
    color: "#fff",
    textAlign: "center",
    fontSize: 18,
    fontWeight: "700",
  },
  errorTxt: {
    fontSize: 12,
    color: "#FF0D10",
  },
});
