import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import medfilt
from pykalman import KalmanFilter
from scipy.ndimage import gaussian_filter1d
import json
from collections import defaultdict
file_path_tmp = r'C:\Users\WiesmuellerF\Documents\TCC_Telereha\tpr_test_20240904_blazepose.csv'
file_path_tandem = r'C:\Users\WiesmuellerF\Documents\TCC_Telereha\tandem_stand.csv'
file_paths = [r'C:\Users\WiesmuellerF\Documents\TCC_Telereha\sts_thunder.json', r'C:\Users\WiesmuellerF\Documents\TCC_Telereha\spin_thunder.json']

def find_outliers(first_derivative):
    first_derivative_series = pd.Series(first_derivative)

    # Identify outliers using the IQR method
    Q1 = first_derivative_series.quantile(0.25)
    Q3 = first_derivative_series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    #outliers = first_derivative_series[(first_derivative_series < lower_bound) | (first_derivative_series > upper_bound)]
    outliers = first_derivative_series > upper_bound
    return outliers

def replace_with_neighbors(series, mask):
    new_series = series.copy()
    for i in range(len(series)):
        if mask[i]:
            # Find previous and next valid values (where mask is False)
            prev_index = next((j for j in range(i-1, -1, -1) if not mask[j]), None)
            next_index = next((j for j in range(i+1, len(series)) if not mask[j]), None)
            
            # Calculate mean of the neighbors
            neighbors = []
            if prev_index is not None:
                neighbors.append(series[prev_index])
            if next_index is not None:
                neighbors.append(series[next_index])
                
            # Replace with mean if neighbors exist
            if neighbors:
                new_series[i] = np.mean(neighbors)
    
    return new_series

def filter_based_on_outliers(x_coord, y_coord, z_coord = None, confidence_score = None):
    x_derivative = np.diff(x_coord)
    x_is_outlier = find_outliers(x_derivative)
    y_derivative = np.diff(y_coord)
    y_is_outlier = find_outliers(y_derivative)
    if z_coord != None:
        z_derivative = np.diff(z_coord)
        z_is_outlier = find_outliers(z_derivative)
    else: 
        z_is_outlier = np.full(len(y_is_outlier), False)
    if confidence_score != None:
        conf_derivative = np.diff(confidence_score)
        conf_is_outlier = find_outliers(conf_derivative)
    else: 
        conf_is_outlier= np.full(len(y_is_outlier), False)
    
    is_outlier = x_is_outlier | y_is_outlier | z_is_outlier | conf_is_outlier
    is_outlier = pd.concat([pd.Series([False]), is_outlier], ignore_index=True)
    x_filtered = replace_with_neighbors(x_coord,is_outlier)
    y_filtered = replace_with_neighbors(y_coord, is_outlier)
    return [x_filtered, y_filtered]

def filter_based_on_smoothing(data, method='mean', window_size = 3):
    data = pd.Series(data)
    if method == 'mean':
        smoothed_data = data.rolling(window=window_size).mean()
    if method == 'median': 
         smoothed_data = medfilt(data, kernel_size=window_size)
    if method == 'kalman':
        # Kalman Filter initialization
        n = len(data)  # Number of measurements
        x = np.zeros(n)  # Filtered state estimates
        P = np.zeros(n)  # Filter uncertainties
        x_pred = np.zeros(n)  # Predictions
        P_pred = np.zeros(n)

        x[0] = 0  # Initial position guess
        P[0] = 1  # Initial uncertainty

        # Kalman Filter parameters
        R = 1  # Measurement noise
        Q = 0.01  # Process noise
        F = 1  # State transition model
        H = 1  # Observation model

        # Forward pass (Kalman Filter)
        for k in range(1, n):
            # Predict
            x_pred[k] = F * x[k - 1]
            P_pred[k] = F * P[k - 1] * F + Q
            
            # Update
            K = P_pred[k] * H / (H * P_pred[k] * H + R)  # Kalman gain
            x[k] = x_pred[k] + K * (data[k] - H * x_pred[k])  # Update estimate
            P[k] = (1 - K * H) * P_pred[k]  # Update uncertainty

        # Backward pass (Smoother)
        x_s = np.copy(x)  # Smoothed state estimates
        P_s = np.copy(P)  # Smoothed uncertainties
        for k in range(n - 2, -1, -1):  # Iterate backward
            A = P[k] * F / P_pred[k + 1]  # Smoothing gain
            x_s[k] = x[k] + A * (x_s[k + 1] - x_pred[k + 1])  # Smoothed estimate
            P_s[k] = P[k] + A * (P_s[k + 1] - P_pred[k + 1]) * A  # Smoothed uncertainty
        return x_s
    if method == 'gaussian':
        sigma = 1.0  # Standard deviation of the Gaussian kernel
        smoothed_data = gaussian_filter1d(data, sigma)    
    return smoothed_data
def plot_coords(title,time_values,x_values,y_values,x_filtered,y_filtered, z_values=None,z_values_filtered=None):
    if z_values!=None:
        fig, axs = plt.subplots(2, 3, figsize=(14, 6), sharex=True)  # 1 row, 2 columns
    else: 
        fig, axs = plt.subplots(2, 2, figsize=(14, 6), sharex=True)  # 1 row, 2 columns
    # Plot X values
    axs[0, 0].plot(time_values, x_values, marker='o', linestyle='-', color='blue', label='x coordinates')
    axs[0, 0].set_title("X Coordinates Over Time", fontsize=14)
    axs[0, 0].set_xlabel("Time Since Start (s)", fontsize=12)
    axs[0, 0].set_ylabel("X Coordinate", fontsize=12)
    axs[0, 0].grid(True)
    axs[0, 0].legend(fontsize=10)

    # Plot Y values
    axs[0, 1].plot(time_values, y_values, marker='o', linestyle='-', color='green', label='y coordinates')
    axs[0, 1].set_title("Y Coordinates Over Time", fontsize=14)
    axs[0, 1].set_xlabel("Time Since Start (s)", fontsize=12)
    axs[0, 1].set_ylabel("Y Coordinate", fontsize=12)
    axs[0, 1].grid(True)
    axs[0, 1].legend(fontsize=10)
    if z_values!=None:
        axs[1, 0].plot(time_values, z_values, marker='o', linestyle='-', color='red', label='z coordinates')
        axs[1, 0].set_title("Z Coordinates Over Time", fontsize=14)
        axs[1, 0].set_xlabel("Time Since Start (s)", fontsize=12)
        axs[1, 0].set_ylabel("Z Coordinate", fontsize=12)
        axs[1, 0].grid(True)
        axs[1, 0].legend(fontsize=10)

        axs[1, 1].plot(time_values, x_filtered, marker='o', linestyle='-', color='blue', label='x-filtered coordinates')
        axs[1, 1].set_title("X-filtered Coordinates Over Time", fontsize=14)
        axs[1, 1].set_xlabel("Time Since Start (s)", fontsize=13)
        axs[1, 1].set_ylabel("X-filtered Coordinate", fontsize=13)
        axs[1, 1].grid(True)
        axs[1, 1].legend(fontsize=10)

        axs[4].plot(time_values, y_filtered, marker='o', linestyle='-', color='green', label='y-filtered coordinates')
        axs[4].set_title("Y-filtered Coordinates Over Time", fontsize=14)
        axs[4].set_xlabel("Time Since Start (s)", fontsize=13)
        axs[4].set_ylabel("Y-filtered Coordinate", fontsize=13)
        axs[4].grid(True)
        axs[4].legend(fontsize=10)

        axs[5].plot(time_values, z_values_filtered, marker='o', linestyle='-', color='red', label='z-filtered coordinates')
        axs[5].set_title("Z-filtered Coordinates Over Time", fontsize=14)
        axs[5].set_xlabel("Time Since Start (s)", fontsize=12)
        axs[5].set_ylabel("Z-filtered Coordinate", fontsize=12)
        axs[5].grid(True)
        axs[5].legend(fontsize=10)


    else: 
        axs[1, 0].plot(time_values, x_filtered, marker='o', linestyle='-', color='blue', label='x-filtered coordinates')
        axs[1, 0].set_title("X-filtered Coordinates Over Time", fontsize=14)
        axs[1, 0].set_xlabel("Time Since Start (s)", fontsize=12)
        axs[1, 0].set_ylabel("X-filtered Coordinate", fontsize=12)
        axs[1, 0].grid(True)
        axs[1, 0].legend(fontsize=10)

        axs[1, 1].plot(time_values, y_filtered, marker='o', linestyle='-', color='green', label='y-filtered coordinates')
        axs[1, 1].set_title("Y-filtered Coordinates Over Time", fontsize=14)
        axs[1, 1].set_xlabel("Time Since Start (s)", fontsize=12)
        axs[1, 1].set_ylabel("Y-filtered Coordinate", fontsize=12)
        axs[1, 1].grid(True)
        axs[1, 1].legend(fontsize=10)

    # Adjust layout
    plt.tight_layout()
    fig.suptitle(title)
    # Show the plot
    plt.show()

def main_plot(time_values,x_values,y_values,joint):
    [x_filtered, y_filtered] = filter_based_on_outliers(x_values,y_values,None,None)
    plot_coords(joint + ' outliers',time_values,x_values,y_values,x_filtered,y_filtered)
    [x_filtered, y_filtered] = [filter_based_on_smoothing(x_values), filter_based_on_smoothing(y_values)]
    plot_coords(joint + ' mean window_size 3',time_values,x_values,y_values,x_filtered,y_filtered)
    [x_filtered, y_filtered] = [filter_based_on_smoothing(x_values,window_size=10), filter_based_on_smoothing(y_values,window_size=10)]
    plot_coords(joint + ' mean window_size 10',time_values,x_values,y_values,x_filtered,y_filtered)
    [x_filtered, y_filtered] = [filter_based_on_smoothing(x_values,method='median',window_size=5), filter_based_on_smoothing(y_values,method='median',window_size=5)]
    plot_coords(joint + ' median window_size 5',time_values,x_values,y_values,x_filtered,y_filtered)
    
    [x_filtered, y_filtered] = [filter_based_on_smoothing(x_values,'gaussian'), filter_based_on_smoothing(y_values,'gaussian')]
    plot_coords(joint + ' gaussian smoothing', time_values,x_values,y_values,x_filtered,y_filtered)

def preprocess(df):
    right_knee = df['right_knee']
    right_knee_structured = {"x": [], "y": [], "confidence": [], "time": []}
    for time, values in right_knee.items():
        right_knee_structured["time"].append(time)
        right_knee_structured["x"].append(values["x"])
        right_knee_structured["y"].append(values["y"])
        right_knee_structured["confidence"].append(values["confidence"])

    right_elbow = df['right_elbow']
    right_elbow_structured = {"x": [], "y": [], "confidence": [], "time": []}
    for time, values in right_elbow.items():
        right_elbow_structured["time"].append(time)
        right_elbow_structured["x"].append(values["x"])
        right_elbow_structured["y"].append(values["y"])
        right_elbow_structured["confidence"].append(values["confidence"])

    left_hip = df['left_hip']
    left_hip_structured = {"x": [], "y": [], "confidence": [], "time": []}
    for time, values in left_hip.items():
        left_hip_structured["time"].append(time)
        left_hip_structured["x"].append(values["x"])
        left_hip_structured["y"].append(values["y"])
        left_hip_structured["confidence"].append(values["confidence"])
        
    left_shoulder = df['left_hip']
    left_shoulder_structured = {"x": [], "y": [], "confidence": [], "time": []}
    for time, values in left_shoulder.items():
        left_shoulder_structured["time"].append(time)
        left_shoulder_structured["x"].append(values["x"])
        left_shoulder_structured["y"].append(values["y"])
        left_shoulder_structured["confidence"].append(values["confidence"])


    time_values = right_elbow_structured['time']
    x_values = right_elbow_structured['x']
    y_values = right_elbow_structured['y']
    main_plot(time_values,x_values,y_values,'right_elbow')

    time_values = right_knee_structured['time']
    x_values = right_knee_structured['x']
    y_values = right_knee_structured['y']
    main_plot(time_values,x_values,y_values,'right_knee')

    time_values = left_hip_structured['time']
    x_values = left_hip_structured['x']
    y_values = left_hip_structured['y']
    main_plot(time_values,x_values,y_values,'left_hip')

    time_values = left_shoulder_structured['time']
    x_values = left_shoulder_structured['x']
    y_values = left_shoulder_structured['y']
    main_plot(time_values,x_values,y_values,'left_shoulder')


for file_path in file_paths:
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)  
    elif file_path.endswith(".json"): 
        with open(file_path, 'r') as file:
            json_file = json.load(file)
            df = defaultdict(lambda: defaultdict(dict))
    
            for entry in json_file:
                time = entry["time_since_start"]
                for keypoint in entry["keypoints"]:
                    name = keypoint.pop("name")  # Remove 'name' from keypoint and use it as the key
                    df[name][time] = keypoint
    
            # Convert defaultdict to a regular dict for cleaner display
            df = {key: dict(value) for key, value in df.items()}
    preprocess(df)


