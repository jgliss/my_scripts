#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 09:37:52 2020

@author: jonasg
"""
import xarray as xr
import pyaerocom as pya

print(pya.const.has_access_lustre)

dd = '/lustre/storeA/project/fou/kl/CAMS61/MONARCH.cams61.rerun/renamed'
reader = pya.io.ReadGridded('MONARCH.cams61.rerun')


#xr.open_dataset(reader.data_dir + '/aerocom3_MONARCH.cams61.rerun_vmro3_ModelLevel_2018_hourly.nc')
#print(reader)

data = reader.read_var('vmro3')

print('Blaaaaaaaaaaaaaa')
surf = data.extract_surface_level()