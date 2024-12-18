import pandas as pd

data = pd.read_csv('../example_data/random/sync_test.csv', skiprows=2, low_memory=False)

sync_marker_cols = [
    col for col in data.columns
    if col.startswith('Marker') and str(data.iloc[0, data.columns.get_loc(col)]).startswith('Sync')
] + ['Type']

data = data[sync_marker_cols]

light_off_index = data.loc[(data.drop('Type', axis=1).isnull().all(axis=1))].index[0]
light_back_on_index = data.loc[light_off_index + 1:, :].loc[(data.drop('Type', axis=1).notnull().all(axis=1))].index[0]

light_off_time = data.loc[light_off_index, 'Type']
light_back_on_time = data.loc[light_back_on_index, 'Type']

print(light_off_time, light_back_on_time)
