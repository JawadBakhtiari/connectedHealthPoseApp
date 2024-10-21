import json
from format.labdataformatter import LabDataFormatter

lab_data_filepath = 'example_data/20240926/tuag.csv'
formatted_data_filepath = 'example_data/20240926/formatted_tuag.json'
exercise_start = 15.368
exercise_end = 43.956

ldf = LabDataFormatter(lab_data_filepath, exercise_start, exercise_end)
formatted_poses = ldf.format()

with open(formatted_data_filepath, 'w') as f:
    json.dump(formatted_poses, f, indent=4)

