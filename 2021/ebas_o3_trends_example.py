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
