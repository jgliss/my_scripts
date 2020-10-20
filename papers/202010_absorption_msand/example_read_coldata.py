#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 11:38:16 2020

@author: jonasg
"""
import numpy as np
import xarray as xr

# Path to example file (needs to be modified)
path = '/lustre/storeA/project/aerocom/aerocom-users-database/PYAEROCOM_COLDATA/WEB_EVAL/aerocom/AP3-abs/OsloCTM3v1.01-met2010_AP3-CTRL/'
file = 'abs550aer_REF-Aeronet-25COV_MOD-OsloCTM3_20100101_20101231_monthly_WORLD-noMOUNTAINS.nc'

ds = xr.open_dataset(path+file)

data = ds.abs550aer

print(data)

# 2d numpy array containing obsdata (may have NaNs)
obsdata = data.data[0]

# 2d numpy array containing modeldata (shouldn't have NaNs)
modeldata = data.data[1]

# mask specifying where no observation values are available
obsnan_mask = np.isnan(obsdata)

obsmean = np.nanmean(obsdata)
modelmean_all = np.mean(modeldata)

modeldata_obsnotnan = modeldata.copy()
modeldata_obsnotnan[obsnan_mask] = np.nan

modelmean_obsnotnan = np.nanmean(modeldata_obsnotnan)


print('Obs mean: {:.3f}'.format(obsmean))
print('Model mean (all): {:.3f}'.format(modelmean_all))
print('Model mean (obs available): {:.3f}'.format(modelmean_obsnotnan))