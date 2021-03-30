#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Example reading EBAS O3 data and calculating trends

Author: jgliss
Date: 26.3.2021

pyaerocom branch main-dev
"""
import numpy as np
import os
import pyaerocom as pya

ebas_local = '/home/jonasg/MyPyaerocom/data/obsdata/EBASMultiColumn/data'

if os.path.exists(ebas_local):
    data_dir = ebas_local
else:
    data_dir = None
    assert pya.const.has_access_lustre

reader = pya.io.ReadUngridded('EBASMC', data_dir=data_dir)

cso4_pm25 = reader.read(vars_to_retrieve='concso4pm25')
cso4_pm25 = cso4_pm25.apply_filters(set_flags_nan=True,
                                    data_level=2)

cso4_pm10 = reader.read(vars_to_retrieve='concso4pm10')
cso4_pm10 = cso4_pm10.apply_filters(set_flags_nan=True,
                                    data_level=2)


fmfso4 = pya.combine_vardata_ungridded.combine_vardata_ungridded(
    [(cso4_pm25, 'EBASMC', 'concso4pm25'),
     (cso4_pm10, 'EBASMC', 'concso4pm10')],
    merge_how='eval',
    merge_eval_fun='fmfso4=EBASMC;concso4pm25/EBASMC;concso4pm10'
    )

tab = []
var = 'fmfso4'
for stat in fmfso4:
    if var in stat:
        print(stat.station_name)
        ts = stat[var]
        notnan = ~np.isnan(ts)
        notzerof = stat['concso4pm25'] != 0
        notzeroc = stat['concso4pm10'] != 0

        mask = notnan * notzerof * notzeroc
        if not mask.any():
            print('all NaN or 0')
            continue

        data = ts[mask]
        num = len(data)
        start = data.index[0].strftime('%Y-%m-%d')
        stop = data.index[-1].strftime('%Y-%m-%d')
        tst = stat.get_var_ts_type(var)

        avg = np.mean(data)
        row = [stat.station_name, start, stop, tst, num, avg]
        tab.append(row)

import pandas as pd
df = pd.DataFrame(tab, columns=['Station', 'start', 'stop', 'freq', '#', 'mean'])
df.to_csv('EBASMC_fmfso4_sites.csv')
