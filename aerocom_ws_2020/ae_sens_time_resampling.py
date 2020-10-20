#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 15:58:59 2020

@author: jonasg
"""

import pyaerocom as pya

mid = 'ECMWF-IFS-CY46R1-CAMS-CTRL-met2010_AP3-CTRL'

obsid = 'AeronetSunV3Lev2.0.daily'
obsdir = '/home/jonasg/MyPyaerocom/data/obsdata/AeronetSunV3Lev2.0.daily/renamed/'

pya.const.add_ungridded_obs(obsid, obsdir,
                            pya.io.ReadAeronetSunV3)

odata = pya.io.ReadUngridded().read(obsid, ['od440aer', 'od870aer',
                                            'ang44&87aer', 'ang4487aer'])

raise NotImplementedError
