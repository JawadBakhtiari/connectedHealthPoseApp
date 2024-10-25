import json
from format.labdataformatter import LabDataFormatter

lab_data_filepath = 'example_data/20241023/exercises.csv'
formatted_data_filepath = 'example_data/20241023/tandem_walk.json'
exercise_start = 406.905
exercise_end = 440.882

ldf = LabDataFormatter(lab_data_filepath, exercise_start, exercise_end)
formatted_poses = ldf.format()

with open(formatted_data_filepath, 'w') as f:
    json.dump(formatted_poses, f, indent=4)

