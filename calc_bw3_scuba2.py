from get_positions import *

# Telescope info
lat = 19.8228 # deg
lon = -155.477 # deg
elevation = 4092 # m
el_limit = 20.0 # deg

# Satellite info
# satname = 'BLUEWALKER3'
noradid = '53807'

get_positions(lat, lon, elevation, el_limit, noradid)
