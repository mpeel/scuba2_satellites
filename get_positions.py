import requests
import json
import numpy as np
from astropy.time import Time
from datetime import date, datetime

def get_positions(lat, lon, elevation, el_limit, noradid):
    # Determine time range we want to request
    today = date.today()
    ap_today = Time(str(today.year)+'-'+str(today.month)+'-'+str(today.day)+'T00:00:00',format='isot',scale='utc')
    jd_start = ap_today.jd
    jd_end = ap_today.jd+2
    jd_step = 1.0/24.0/20.0 # Every 3 minutes
    jd_step_zoom = jd_step / 3.0 / 12.0 # Every 5 seconds
    # print(jd_step)

    url = 'https://cps.iau.org/tools/satchecker/api/ephemeris/catalog-number-jdstep/'
    # url = 'http://satchecker-prod-alb-2093903284.us-east-1.elb.amazonaws.com/ephemeris/catalog-number-jdstep/'
    params = {'catalog': noradid,
                    'latitude': lat,
                    'longitude': lon,
                    'elevation': elevation,
                    'startjd': jd_start,
                    'stopjd': jd_end,
                    'stepjd': jd_step}
    r = requests.get(url, params=params)
    # print(r.content)
    first_entry = r.json()[0]
    print(first_entry)
    print('Satellite name: ' + first_entry['NAME'])
    print('TLE date: ' + first_entry['TLE-DATE'])
    print('Time (UTC)    JD   Azimuth (deg)   Altitude (deg)   RA (deg)    Declination (deg)   Phase angle (deg)')
    previous_time = 0
    for entry in r.json():
        if entry['ALTITUDE-DEG'] > 0 and (np.abs(previous_time - entry['JULIAN_DATE']) > 10.0*jd_step):
            previous_time = entry['JULIAN_DATE']
            sub_params = {'catalog': noradid,
                    'latitude': lat,
                    'longitude': lon,
                    'elevation': elevation,
                    'startjd': entry['JULIAN_DATE']-2*jd_step,
                    'stopjd': entry['JULIAN_DATE']+4*jd_step,
                    'stepjd': jd_step_zoom}
            sub_r = requests.get(url, params=sub_params)
            # print(r.content)
            showing_rows = 0
            for subentry in sub_r.json():
                if subentry['ALTITUDE-DEG'] > el_limit:
                    timestamp = Time(subentry['JULIAN_DATE'],format='jd')
                    timestamp.format = 'datetime'
                    showing_rows += 1
                    print(str(timestamp).split('.')[0] + '   ' + str(round(subentry['JULIAN_DATE'],5)) + '  ' + str(round(subentry['AZIMUTH-DEG'],5)) + '    ' + str(round(subentry['ALTITUDE-DEG'],5)) + '    ' + str(round(subentry['RIGHT_ASCENSION-DEG'],5)) + '    ' + str(round(subentry['DECLINATION-DEG'],5)) + '    ' + str(round(subentry['PHASE_ANGLE-DEG'],1)))
            if showing_rows > 0:
                print('\n')
