#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 09:12:15 2020

@author: jonasg
"""
import pyaerocom as pya
import xarray as xr

models = ['EMEP.cams50.u3all', 'EMEP.cams61.rerun', 'CHIMERE.cams61.rerun',
          'SILAM.cams61.rerun', 'MONARCH.cams61.rerun', 'EURAD-IM.cams61.rerun',
          'MINNI.cams61.rerun', 'DEHM.cams61.rerun', 'LOTOSEUROS.cams61.rerun']


testvars = ['wetoxs']

head = ['var', 'model', 't0-xarray', 't0-pya', 'auto-updated']
tab = []
for var in testvars:
    for model in models:
        print(model)

        reader = pya.io.ReadGridded(model)
        gd = reader.read_var(var, start=2018)

        t0 = gd.time_stamps()[0]
        t0_str_pya = pya.helpers.to_pandas_timestamp(t0).strftime('%Y-%m-%d %H:%M:%S')

        ff = gd.from_files
        if len(ff) != 1:
            raise ValueError
        arr = xr.open_dataset(ff[0])
        t0 = arr.time.data[0]
        t0_str_xr = pya.helpers.to_pandas_timestamp(t0).strftime('%Y-%m-%d %H:%M:%S')

        if 'timedim-corrected' in gd.cube.attributes:
            tdc = 'Y'
        else:
            tdc = 'N'

        tab.append([var, model, t0_str_xr, t0_str_pya, tdc])

import pandas as pd
df = pd.DataFrame(tab, columns=head)
df.to_csv('tab_timedimcheck_models.csv', index=False)






