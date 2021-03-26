#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example reading EBAS O3 data and calculating trends

Author: jgliss
Date: 26.3.2021

pyaerocom branch main-dev
"""
import os
import pyaerocom as pya

ebas_local = '/home/jonasg/MyPyaerocom/data/obsdata/EBASMultiColumn/data'

if os.path.exists(ebas_local):
    data_dir = ebas_local
else:
    data_dir = None
    assert pya.const.has_access_lustre

reader = pya.io.ReadUngridded('EBASMC', data_dir=data_dir)

conco3 = reader.read(vars_to_retrieve='conco3')

all_sites = conco3.to_station_data_all('conco3', start=2000,
                                       stop=2020)

# EVERYTHING BELOW COULD GO IN A LOOP OVER all_sites['stats']

first_station = all_sites['stats'][0]

print(first_station)

min_num_obs = pya.const.OBS_MIN_NUM_RESAMPLE # roughly 25% coverage requirement

print('Resampling coverage requirement:')
print(min_num_obs)

# O3 max from hourly data
resample_how = 'max'

# make sure data is hourly (not necessarily all are)
assert first_station.ts_type == 'hourly'

# reample to daily and use max aggregator to get O3 max
first_station_d = first_station.resample_time('conco3', 'daily',
                                              apply_constraints=True,
                                              min_num_obs=min_num_obs,
                                              how=resample_how,
                                              inplace=False)


te = pya.trends_engine.TrendsEngine()

te.var_name = 'conco3'
tseries = first_station_d['conco3']
# this contains all that is there between 2000 -> 2020
te.daily = tseries

# e.g. compute trend for 2005 -> 2015
trend = te.compute_trend(2005, 2015)

ax = te.plot(season='all')

ax.figure.savefig('o3max_trend_first_site_2005-2015.png')





