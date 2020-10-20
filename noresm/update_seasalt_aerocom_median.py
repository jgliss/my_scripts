#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 19:43:07 2020

@author: jonasg
"""

import pyaerocom as pya
import os


OUT_ID = 'NorESM2-AODSSMEDIAN-met2010_AP3-CTRL'

outdir_rel = 'data/modeldata/{}/renamed'.format(OUT_ID)
outdir = os.path.join(pya.const.OUTPUTDIR, outdir_rel)

if not os.path.exists(outdir):
    raise FileNotFoundError(outdir)

print(42)
start = 2010
freq='monthly'

median_id = 'AEROCOM-MEDIAN-2x3-GLISSETAL2020-1_AP3-CTRL'
noresm_id = 'NorESM2-met2010_AP3-CTRL'

median_dir = '/home/jonasg/MyPyaerocom/AEROCOM-MEDIAN-2x3-GLISSETAL2020-1_AP3-CTRL/renamed/'
reader = pya.io.ReadGridded(median_id,
                            data_dir=median_dir)

medss = reader.read_var('od550ss', start=start, ts_type=freq)

odvars = ['od550bc','od550dust','od550so4', 'od550oa']

noresmdir = '/lustre/storeA/project/aerocom/aerocom-users-database/AEROCOM-PHASE-III-2019/NorESM2-met2010_AP3-CTRL/renamed/'
reader = pya.io.ReadGridded(noresm_id,
                            data_dir=noresmdir)

loaded = []

for var in odvars:
    print(var)
    data = reader.read_var(var, start=start, ts_type=freq)
    if not data.ts_type == 'monthly':
        data = data.resample_time('monthly')

    loaded.append(data)


print('Regrid median SS to Noresm res.')
first = loaded[0]
medss = medss.regrid(first)
medss.time.units = first.time.units
medss.time.points = first.time.points
medss.time.attributes = first.time.attributes
medss.time.standard_name = first.time.standard_name

for data in loaded:
    print('Adding', data.var_name)
    added = pya.io.aux_read_cubes.add_cubes(medss.cube, data.cube)
    medss = pya.GriddedData(added)

medss.var_name = 'od550aer'

medss.cube.attributes = {}
medss.cube.attributes['data_id'] = OUT_ID
medss.cube.attributes['ts_type'] = 'monthly'

print(medss.time_stamps())
medss.to_netcdf(outdir, vert_code='Column')
