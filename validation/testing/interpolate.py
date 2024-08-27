#!/usr/bin/env python3

'''Interpolate missing values in lab data'''

#import pandas as pd
import re
from collections import defaultdict

IN = 'data/sample_lab_data.trc'
OUT = 'data/cleaned_lab_data.trc'

with open(IN, 'r') as f:
    lines = f.readlines()

data_lines = lines[3:]
del data_lines[1]
fourth_row = re.split(r'\t+', data_lines[0].strip())
print(fourth_row)
columns_to_remove = [i for i, val in enumerate(fourth_row) if 'Unlabeled' in val]
print(columns_to_remove)

cleaned_lines = []
debug = defaultdict(int)
for line in data_lines:
    columns = re.split(r'\t+', line.strip())
    cleaned_columns = [col for i, col in enumerate(columns) if i not in columns_to_remove]
    debug[len(cleaned_columns)] += 1
    cleaned_lines.append(' '.join(cleaned_columns) + '\n')

with open(OUT, 'w') as f:
    f.writelines(cleaned_lines)

print(debug)

# df = pd.read_csv('data/sample_lab_data.trc', sep='\s+', skiprows=6)
# df.interpolate(method='linear', axis=0, inplace=True)
# df.to_csv('data/sample_lab_data.trc', sep='\t', index=False)

