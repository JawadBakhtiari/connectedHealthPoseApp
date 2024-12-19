# connectedhealth
Backend application for Connected Health VIP UNSW, a web application aimed at providing healthcare professionals conducting remote sessions with more meaningful data, so that they can provide a higher level of care to clients in these sessions.

Video and [pose data](https://viso.ai/deep-learning/pose-estimation-ultimate-overview) received from a [mobile application](https://github.com/realRickyNguyen/ExpoCAMwithTensor) running on a patient's phone is processed and stored. These clips may be viewed by the healthcare professional at a later point, with the associated keypoints and graph indicating the angles between a given joint and the rest of the body at any given time.

Written in Django.

## Run connectedhealth back-end
To clone and run the back-end, this can be done as follows:

First:
```
git clone git@github.com:nick-maiden/connectedhealth.git
cd connectedhealth
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py makemigrations
```

get local IP Address:
```
./getip
```
insert local IP -> connectedhealth/settings -> ALLOWED_HOSTS = ['127.0.0.1', '192.168.0.137']


To run (using ip on local network):
```
./startserver
```

To run on loopback ip (note that this won't work when running with mobile application):
```
python3 manage.py runserver
```
Note the ip address and port number that is returned, this is needed on the front-end to connect to the back-end.
