#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 15:10:42 2020

@author: jonasg
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import pyaerocom as pya

plt.close('all')

obsid = 'Aeronet.Inv.V3L2.0.daily'
datadir = '/home/jonasg/MyPyaerocom/data/obsdata/Aeronet.Inv.V3L2.0.daily/renamed'

var = 'angabs4487aer'

pya.const.add_ungridded_obs(obsid, datadir,
                            reader=pya.io.ReadAeronetInvV3)

reader = pya.io.ReadUngridded(obsid)

print(reader)
all_vars = [var, 'ang4487aer', 'abs550aer', 'od550aer']
data = reader.read(obsid, all_vars)

data = data.merge_common_meta(ignore_keys=['variables', 'var_info'])

start, stop = 2010, 2011

stats = data.to_station_data_all(all_vars,
                                 start=start, stop=stop)

vardata = {}
for varname in all_vars:
    vardata[varname] = []

snum = 0

lats, lons, numvals, avg = [], [], [], []
for stat in stats['stats']:
    if not var in stat:
        continue

    angabs = stat[var]
    notnan = ~np.isnan(angabs)
    if notnan.sum()>0:
        snum += 1
        vals = angabs[notnan]
        vardata[var].extend(vals)

        lats.append(stat.latitude)
        lons.append(stat.longitude)
        numvals.append(notnan.sum())
        avg.append(np.nanmean(vals))
        for addvar in all_vars:
            if addvar == var:
                continue
            addts = stat[addvar]
            assert len(addts) == len(angabs)
            vardata[addvar].extend(addts[notnan])

for _var, vals in vardata.items():
    vardata[_var] = np.asarray(vals)

result = []

vardata['ssa550aer'] = (vardata['od550aer'] - vardata['abs550aer']) / vardata['od550aer']


startstop = pya.helpers.start_stop_str(start, stop)
for _var, values in vardata.items():
    result.append([startstop, 'No', _var, snum, len(values),
                   np.mean(values),
                   np.median(values),
                   np.quantile(values, .05),
                   np.quantile(values, .95),
                   np.min(values),
                   np.max(values)])

df = pd.DataFrame(result, columns=['Period', 'Clim', 'Var', '#st', '#', 'Mean',
                                   'Median', 'q5', 'q95', 'Min', 'Max'])

print(df)

df.to_csv('AERONET_INV_V3_Lev2_Daily_stats.csv')

lbl = 'AERONET AAE sites (2010, {} sites)'.format(snum)
ax = data.plot_station_coordinates(var_name=var,
                                     start=2010,
                                     stop=None, ts_type=None, color='g',
                                     marker='o', markersize=20,
                                     fontsize_base=10,
                                     legend=True, add_title=False,
                                     label=lbl)


ax1 = pya.plot.mapping.init_map()
bounds = [0, 5, 15, 30, 60, 120, 180]
cmap = plt.get_cmap('viridis')
from matplotlib.colors import BoundaryNorm
norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N, clip=False)
sc = ax1.scatter(lons, lats, c=numvals, marker='o', s=30, cmap=cmap,
                 norm=norm)
cb = ax1.figure.colorbar(sc)
cb.ax.set_ylabel('AAE number of 2010 daily values')


ax.figure.savefig('AERONET_2010_{}_sitemap.png',
                  dpi=300)