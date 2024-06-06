import { Header } from "react-native/Libraries/NewAppScreen";
import HomeScreen from "./pages/HomeScreen";
import SecondScreen from "./pages/SecondScreen";
import UploadingScreen from "./pages/UploadingScreen";
import VisionCamera from "./pages/VisionCamera";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { ScreenStackHeaderCenterView } from "react-native-screens";

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="VisionCamera"
          component={VisionCamera}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: "SessionStart", headerShown: false }}
        />
        <Stack.Screen
          name="Second"
          component={SecondScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Uploading"
          component={UploadingScreen}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
