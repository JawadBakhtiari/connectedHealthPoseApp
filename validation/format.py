import json
from format.labdataformatter import LabDataFormatter

lab_data_filepath = 'example_data/20240926/sbta.csv'
formatted_data_filepath = 'example_data/20240926/formatted_sbta.json'
exercise_start = 17.613
exercise_end = 33.137

ldf = LabDataFormatter(lab_data_filepath, exercise_start, exercise_end)
formatted_poses = ldf.format()

with open(formatted_data_filepath, 'w') as f:
    json.dump(formatted_poses, f, indent=4)

