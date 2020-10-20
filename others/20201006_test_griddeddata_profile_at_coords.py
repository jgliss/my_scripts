#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 13:11:37 2020

@author: jonasg
"""

import pyaerocom as pya

dd = '/home/jonasg/MyPyaerocom/data/modeldata/OsloCTM3v1.01-met2010_AP3-CTRL/renamed'

reader = pya.io.ReadGridded('OsloCTM3v1.01-met2010_AP3-CTRL',
                            data_dir=dd)

print(reader)

data = reader.read_var('ec550aer', vert_which='ModelLevel')

print(data)

lats = (10, 20, 30)
lons = (10, 20, 30)


#stats = data.to_time_series(latitude=lats, longitude=lons,
#                            vert_scheme='profile')

arr = data.to_xarray()

subset = pya.helpers.extract_latlon_dataarray(arr, lats, lons,
                                              lat_dimname=None,
                                              lon_dimname=None, method='nearest',
                                              new_index_name='latlon',
                                              check_domain=True)


print(subset)