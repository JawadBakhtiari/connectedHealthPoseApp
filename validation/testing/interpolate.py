#!/usr/bin/env python3

'''Interpolate missing values in lab data, excluding the joint names row from interpolation'''

import pandas as pd
import numpy as np
from io import StringIO

FILENAME = 'exercises.trc'
IN = f'data/{FILENAME}'
OUT = f'data/interpolated_{FILENAME}'

# Read the file and preserve header rows
with open(IN, 'r') as file:
    lines = file.readlines()

# Assuming first 3 lines are headers
header_lines = lines[:3]
data_lines = lines[3:]

# Read data into DataFrame, including the joint names row
data = pd.read_csv(StringIO(''.join(data_lines)), delimiter='\t', header=None)

# Extract the row with joint names (assuming it's the first row of the data)
joint_names_row = data.iloc[0].copy()

# Drop the row with joint names from the data for interpolation
data_no_names = data.drop(index=0).reset_index(drop=True)

# Interpolate missing values
data_no_names.replace('', np.nan, inplace=True)
data_no_names.interpolate(method='linear', inplace=True, limit_direction='forward', axis=0)
data_no_names.fillna(method='bfill', inplace=True)  # Backfill remaining NaN values

# Add the joint names row back to the DataFrame
data_fixed = pd.concat([pd.DataFrame([joint_names_row]), data_no_names], ignore_index=True)

# Write the output file
with open(OUT, 'w') as file:
    # Write header lines back
    file.writelines(header_lines)
    # Write interpolated data
    data_fixed.to_csv(file, sep='\t', index=False, header=False)

print(f'Interpolation (hopefully) worked ... check output in {OUT}')
