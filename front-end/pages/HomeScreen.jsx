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
import React, { useState } from "react";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

// Validation Schema //
const SignupSchema = Yup.object().shape({
  uid: Yup.string()
    .min(5, "Too Short!")
    .max(15, "Too Long!")
    .required("Please enter uid."),
  sid: Yup.string()
    .min(1, "Too Short!")
    .max(15, "Too Long!")
    .required("Please enter sid."),
  clipNum: Yup.string()
    .min(1, "Too Short!")
    .max(100, "Too Long!")
    .required("Please enter clip Num.")
    .matches(/^[0-9]+$/, "Must be only digits"),
  name: Yup.string().min(5, "Too Short!").max(15, "Too Long!"),
  // .required("Please enter full name."),

  // email: Yup.string()
  //   .email("Invalid email")
  //   .required("Please enter your email"),

  // mobile: Yup.string()
  //   .min(8, "Too Short!")
  //   .max(20, "Too Long!")
  //   .matches(/^[0-9]+$/, "Must be only digits"),
});

export default function HomeScreen({ navigation }) {
  return (
    <Formik
      initialValues={{
        uid: "",
        sid: "",
        clipNum: "",
        name: "",
      }}
      validationSchema={SignupSchema}
      onSubmit={(values) => Alert.alert(JSON.stringify(values))}
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

            {/* Input: UID */}
            <View style={styles.inputWrapper}>
              <Text>uID:</Text>
              <TextInput
                style={styles.inputStyle}
                // placeholder="Participant Full Name"
                value={values.uid}
                onChangeText={handleChange("uid")}
                onBlur={() => setFieldTouched("uid")}
              />
              {touched.uid && errors.uid && (
                <Text style={styles.errorTxt}>{errors.uid}</Text>
              )}
            </View>

            {/* Input: sID */}
            <View style={styles.inputWrapper}>
              <Text>sID:</Text>
              <TextInput
                style={styles.inputStyle}
                // placeholder="Email Address"
                autoCapitalize={false}
                value={values.sid}
                onChangeText={handleChange("sid")}
                onBlur={() => setFieldTouched("sid")}
              />
              {touched.sid && errors.sid && (
                <Text style={styles.errorTxt}>{errors.sid}</Text>
              )}
            </View>
            {/* Input: clipNum */}
            <View style={styles.inputWrapper}>
              <Text>Clip Number:</Text>
              <TextInput
                style={styles.inputStyle}
                // placeholder="Mobile Number"
                keyboardType="phone-pad"
                value={values.clipNum}
                onChangeText={handleChange("clipNum")}
                onBlur={() => setFieldTouched("clipNum")}
              />
              {touched.clipNum && errors.clipNum && (
                <Text style={styles.errorTxt}>{errors.clipNum}</Text>
              )}
            </View>
            {/* Input: Full Name */}
            <View style={styles.inputWrapper}>
              <Text>Full Name:</Text>
              <TextInput
                style={styles.inputStyle}
                // placeholder="Participant Full Name"
                value={values.name}
                onChangeText={handleChange("name")}
                onBlur={() => setFieldTouched("name")}
              />
              {touched.name && errors.name && (
                <Text style={styles.errorTxt}>{errors.name}</Text>
              )}
            </View>

            {/* Button*/}
            <TouchableOpacity
              onPress={() =>
                navigation.navigate("Second", { language: "french" })
              }
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
    //backgroundColor: "#395B64",
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
