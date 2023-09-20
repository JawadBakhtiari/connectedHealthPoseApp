'''Constants for views.py'''

'''Keypoint connections used in visualisations of pose data.'''
KP_CONNS = [
    (0, 4), (0, 1), (4, 5), (5, 6), (6, 8), (1, 2), (2, 3), (3, 7),
    (10, 9), (12, 11), (12, 14), (14, 16), (16, 22), (16, 20), (16, 18), (18, 20),
    (11, 13), (13, 15), (15, 21), (15, 19), (15, 17), (17, 19), (12, 24),
    (11, 23), (24, 23), (24, 26), (23, 25), (26, 28), (25, 27), (28, 32), 
    (28, 30), (30, 32), (27, 29), (27, 31), (29, 31)
]

# Azure blob storage constants
AZ_ACCOUNT_NAME = "connectedhealthunsw"
AZ_ACCOUNT_KEY = "ByogeEDjYWdSoG+kCY1uR+KXHQwullTwi3F6kZ7QSZQoWshzq/wHXkgdBHlwmGYOg3MyI9NKh+iF+AStjaqaYw=="
AZ_CON_STR = f"DefaultEndpointsProtocol=https;AccountName={AZ_ACCOUNT_NAME};AccountKey={AZ_ACCOUNT_KEY};EndpointSuffix=core.windows.net"
AZ_CONTAINER_NAME = "framedata"
