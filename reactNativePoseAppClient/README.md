# Running ExpoCamera and TensorFlow Posemodel

Requires:

- nodejs : https://nodejs.org/en/download
- yarn
- Expo Go App (ios/andriod)

First:

```
git clone https://github.com/realRickyNguyen/ExpoCAMwithTensor.git
cd ExpoCAMwithTensor
yarn install
```

Now, to run with mobile application (using ip on local network):

```
yarn expo start
```

Inside the application, for the code, enter the local IP Address and Port which the back-End is running on.
for example: 192.168.0.137:8000

## If expo is outdated:

```
yarn add expo@latest
npx expo install --fix
```

# Manually pick and choose which dependencies to upgrade

```
yarn upgrade-interactive --latest
```
