#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 09:07:51 2021

@author: jonasg
"""

import pyaerocom as pya
import pandas as pd

MODELS = {
    'CAM5-ATRAS_AP3-CTRL' : 'CAM5-ATRAS',
    'GFDL-AM4-met2010_AP3-CTRL' : 'GFDL-AM4',
    'AEROCOM-MEDIAN-2x3-GLISSETAL2020-1_AP3-CTRL': 'AEROCOM-MEDIAN',
    'EC-Earth3-AerChem-met2010_AP3-CTRL2019':  'EC-Earth3',
    'NorESM2-met2010_AP3-CTRL' : 'NorESM2'
}

tab = []

kg_to_ug = 1e9
for model, name in MODELS.items():

    reader = pya.io.ReadGridded(model)

    dry_du = reader.read_var('drydust', start=2010).resample_time('yearly')
    wet_du = reader.read_var('wetdust', start=2010).resample_time('yearly')

    dry_du_mean = dry_du.mean() * kg_to_ug
    wet_du_mean = wet_du.mean() * kg_to_ug

    if dry_du_mean < 0:
        dry_du_mean = -dry_du_mean

    if wet_du_mean < 0:
        wet_du_mean = -wet_du_mean

    print(name)
    print('Dry: ', dry_du_mean)
    print('Wet: ', wet_du_mean)


    tot = dry_du_mean + wet_du_mean

    frac_dry = dry_du_mean / tot * 100



    tab.append([name, dry_du_mean, wet_du_mean, tot, frac_dry])

df = pd.DataFrame(tab, columns=['Model', 'Dry DU', 'Wet DU', 'Tot DU', 'Dry frac (%)'])
print(df)