## Overview

Remote Rehab is an innovative platform designed to seamlessly integrate into clinical workflows and facilitate remote physiotherapy assessment and monitoring to aid in patient recovery.

#### React Native Mobile Application for clients
At its core lies a React Native mobile application tailored for clients, allowing them to record exercise sessions. The app utilizes the Vision Camera to capture frames, which are then processed by the Blaze Pose model to generate key points reflecting the client's movements. These key points, along with the frames, are transmitted in real-time to a Django backend and stored securely in the cloud.

#### Web Application for clinicians
Clinicians can then leverage a web application to access the stored data, enabling precise evaluation of posture, alignment, and range of motion. This functionality supports the creation of targeted treatment plans, ensuring personalized care for each client.

# Installation Instructions

First clone and navigate into Github Repository

```
git clone https://github.com/JawadBakhtiari/connectedHealthPoseApp.git
cd connectedHealthPoseApp/
```

# Running using Docker

1. get ConnectionCode (local IP address):

```
./getip
```

2. run docker:

```
docker-compose up
```

delete old docker build after making changes:

```
docker-compose down -v --rmi 'all'
```

# Inside React Native App : Patient

1. Download Expo App on smartphone
2. Follow link on browser: (Connection code is your local IP address not docker IP address)

```
exp://ConnectionCode:19000
```

3. Enter connection code (local IP-address) and back-end port inside app.

```
ConnectionCode:8000
```

4. Press record button and allow permission for recording for the first time, small delay before recording starts.

5. Press record button again to clip recording, session id and session clip should be printed in the back-end.

# Inside Web App : Staff

1. Access web app via:

```
http://ConnectionCode:8000/data/visualise2D/
```

2. Use session id and clip num to view pose skeleton and graph analysis
