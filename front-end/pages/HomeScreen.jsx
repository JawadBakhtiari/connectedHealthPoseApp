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
  name: Yup.string()
    .min(6, "Too Short!")
    .max(50, "Too Long!")
    .required("Please enter your full name."),
  email: Yup.string()
    .email("Invalid email")
    .required("Please enter your email"),
  mobile: Yup.string()
    .min(8, "Too Short!")
    .max(20, "Too Long!")
    .matches(/^[0-9]+$/, "Must be only digits"),
  sessionCode: Yup.string().min(5, "Too Short!").max(20, "Too Long!"),
});

export default function HomeScreen({ navigation }) {
  return (
    <Formik
      initialValues={{
        name: "",
        email: "",
        mobile: "",
        sessionCode: "",
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

            {/* Input: Session Code */}
            <View style={styles.inputWrapper}>
              <TextInput
                style={styles.inputStyle}
                placeholder="Session Code"
                value={values.sessionCode}
                onChangeText={handleChange("sessionCode")}
                onBlur={() => setFieldTouched("sessionCode")}
              />
              {touched.sessionCode && errors.sessionCode && (
                <Text style={styles.errorTxt}>{errors.sessionCode}</Text>
              )}
            </View>
            {/* Input: Full Name */}
            <View style={styles.inputWrapper}>
              <TextInput
                style={styles.inputStyle}
                placeholder="Participant Full Name"
                value={values.name}
                onChangeText={handleChange("name")}
                onBlur={() => setFieldTouched("name")}
              />
              {touched.name && errors.name && (
                <Text style={styles.errorTxt}>{errors.name}</Text>
              )}
            </View>
            {/* Input: Email */}
            <View style={styles.inputWrapper}>
              <TextInput
                style={styles.inputStyle}
                placeholder="Email Address"
                autoCapitalize={false}
                value={values.email}
                onChangeText={handleChange("email")}
                onBlur={() => setFieldTouched("email")}
              />
              {touched.email && errors.email && (
                <Text style={styles.errorTxt}>{errors.email}</Text>
              )}
            </View>
            {/* Input: Mobile Number */}
            <View style={styles.inputWrapper}>
              <TextInput
                style={styles.inputStyle}
                placeholder="Mobile Number"
                keyboardType="phone-pad"
                value={values.mobile}
                onChangeText={handleChange("mobile")}
                onBlur={() => setFieldTouched("mobile")}
              />
              {touched.mobile && errors.mobile && (
                <Text style={styles.errorTxt}>{errors.mobile}</Text>
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
              <Text style={[styles.submitBtnTxt]}>Start Session</Text>
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
