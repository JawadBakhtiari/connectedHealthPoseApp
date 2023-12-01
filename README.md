# connectedhealth
Backend application for Connected Health VIP UNSW, a web application aimed at providing healthcare professionals conducting remote sessions with more meaningful data, so that they can provide a higher level of care to clients in these sessions.

Video and [pose data](https://viso.ai/deep-learning/pose-estimation-ultimate-overview) received from a [mobile application](https://github.com/realRickyNguyen/ExpoCAMwithTensor) running on a patient's phone is processed and stored. These clips may be viewed by the healthcare professional at a later point, with the associated keypoints and graph indicating the angles between a given joint and the rest of the body at any given time.

Written in Django.

## Whole application and frontend
To clone and run the entire application (this repository and the associated mobile application), go [here](https://github.com/SIXRIP7ER/connectedHealthApp).
The frontend (mobile application) can be found [here](https://github.com/realRickyNguyen/ExpoCAMwithTensor).

## Run connectedhealth
To run the entire application, it is prefereable to follow the instructions [here](https://github.com/SIXRIP7ER/connectedHealthApp). However, if you want to clone and run this repository in isolation, this can be done as follows:

First:
```
git clone git@github.com:nick-maiden/connectedhealth.git
cd connectedhealth
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py makemigrations
```

Now, to run with mobile application (using ip on local network):
```
./startserver
```

To run on loopback ip (note that this won't work when running with mobile application):
```
python3 manage.py runserver
```

Visit [here](https://github.com/realRickyNguyen/ExpoCAMwithTensor) to clone and run the mobile application.
