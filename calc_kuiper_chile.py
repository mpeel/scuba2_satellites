from get_positions import *

# Telescope info
lat = -30.168861 # deg
lon = -70.806628 # deg
elevation = 2241 # m
el_limit = 20.0 # deg

# Satellite info
# satname = 'KUIPER-P2'
noradid = '58013'
get_positions(lat, lon, elevation, el_limit, noradid)

# Satellite info
# satname = 'KUIPER-P1'
noradid = '58014'
get_positions(lat, lon, elevation, el_limit, noradid)
