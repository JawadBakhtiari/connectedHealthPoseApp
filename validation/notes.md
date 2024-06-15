## Notes from chatting with Rahm
  - bone types are 'keypoints', marker and bone marker types are not 'keypoints'
  - use position and not rotation


## A heuristic comparison between systems

### Mobile data
### At 17:31:24:343
```json
  {
    "x": 71.20784780997717,
    "y": 98.73078761334244,
    "z": 946.2736154453455,
    "score": 0.9999062103205987,
    "name": "left_shoulder"
  },
```
```json
  {
    "x": 0.16928645068762274,
    "y": -0.44030459023353513,
    "z": 0.0015459610446496622,
    "score": 0.9999131778970014,
    "name": "left_shoulder"
  },
```
After conversion to absolute values (from normalised values):
```json
  {
    "x": 20.31437408251473,
    "y": -93.78487771974298
  }
```

### At 17:31:30:147
```json
  {
    "x": 76.65144567946331,
    "y": 71.87025256282408,
    "z": -4430.67856827696,
    "score": 0.9999246330707783,
    "name": "left_shoulder"
  },
```
```json
  {
    "x": 0.17897597532043577,
    "y": -0.4176582666896209,
    "z": -0.19138605511921086,
    "score": 0.9998746624857435,
    "name": "left_shoulder"
  },
```
After conversion to absolute values (from normalised values):
```json
  {
    "x": 21.477117038452292,
    "y": -88.96121080488925
  }
```

### At 17:31:36:586
```json
  {
    "x": 74.61395624330436,
    "y": 64.99816076243849,
    "z": -247.4728172100148,
    "score": 0.9999107984718466,
    "name": "left_shoulder"
  },
```
```json
  {
    "x": 0.16916240187325227,
    "y": -0.4643509656251208,
    "z": -0.08318319447985188,
    "score": 0.9998736795756129,
    "name": "left_shoulder"
  },
```
After conversion to absolute values (from normalised values):
```json
  {
    "x": 20.299488224790274,
    "y": -98.90675567815073
  }
```


### Livability lab motion capture system data
### At 17:31:24:37, timestamp = 21.550000
```json
  {
    "x": 61.108246,
    "y": 1006.177063,
    "z": -846.725769
  }
```

### At 17:31:30:173667, timestamp = 27.291667
```json
  {
    "x": 52.230141,
    "y": 1282.140869,
    "z": -311.002258
  }
```

### At 17:31:36:565333, timestamp = 33.683333
```json
  {
    "x": 65.347435,
    "y": 1392.183228,
    "z": -385.27652
  }
```
