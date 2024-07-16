import { Header } from "react-native/Libraries/NewAppScreen";
import HomeScreen from "./pages/HomeScreen";
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
          name="Home"
          component={HomeScreen}
          options={{ title: "SessionStart", headerShown: false }}
        />
        <Stack.Screen
          name="VisionCamera"
          component={VisionCamera}
          options={{ headerShown: false }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
