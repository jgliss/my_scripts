#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 13:52:42 2020

@author: jonasg
"""

# NOTE: these were extracted from one of the NetCDF files, quite a few site
# locations do not contain obsdata (only NaNs), I added a print below in
# case you choose one of such sites accidentally =)
ALL_SITES = ['ATHENS-NOA' 'Agoufou' 'Alta_Floresta' 'Appledore_Island' 'Arcachon'
             'Arica' 'Aubiere_LAMP' 'Autilla' 'Avignon' 'BONDVILLE' 'Bac_Lieu'
             'Bach_Long_Vy' 'Baengnyeong' 'Bambey-ISRA' 'Bandung' 'Banizoumbou'
             'Barcelona' 'Beijing' 'Beijing_RADI' 'Belsk' 'Billerica' 'Blida'
             'Bonanza_Creek' 'Bratts_Lake' 'Brussels' 'Bucharest_Inoe' 'Burjassot'
             'CARTEL' 'CCNY' 'CEILAP-BA' 'CLUJ_UBB' 'COVE_SEAPRISM' 'CRPSM_Malindi'
             'CUIABA-MIRANDA' 'Cabauw' 'Cabo_da_Roca' 'Caceres' 'Cairo_EMA_2'
             'CalTech' 'Camaguey' 'Campo_Grande_SONDA' 'Cape_San_Juan' 'Capo_Verde'
             'Carpentras' 'Cart_Site' 'Chapais' 'Chen-Kung_Univ' 'Chiang_Mai_Met_Sta'
             'Chilbolton' 'Cordoba-CETT' 'DMN_Maine_Soroa' 'Dakar' 'Dayton' 'Dhadnah'
             'Dongsha_Island' 'Dunkerque' 'Dushanbe' 'EPA-NCU' 'Easton_Airport'
             'Eforie' 'Egbert' 'Ersa' 'Evora' 'Fresno' 'GSFC' 'Gandhi_College'
             'Granada' 'Guadeloup' 'Gual_Pahari' 'Gustav_Dalen_Tower' 'Gwangju_GIST'
             'Halifax' 'Hamburg' 'Harvard_Forest' 'Helgoland' 'Helsinki'
             'Hong_Kong_Hok_Tsui' 'Hong_Kong_PolyU' 'Huelva' 'Hyytiala' 'IER_Cinzana'
             'IMS-METU-ERDEMLI' 'Irkutsk' 'Ispra' 'Jaipur' 'Ji_Parana_SE' 'KONZA_EDC'
             'Kanpur' 'Karachi' 'Karlsruhe' 'Kellogg_LTER' 'Kelowna_UAS' 'Kuopio'
             'Kuwait_University' 'Kyiv' 'LISCO' 'LSU' 'La_Laguna' 'La_Parguera'
             'Laegeren' 'Lahore' 'Lake_Argyle' 'Lampedusa' 'Lecce_University'
             'Leipzig' 'Lille' 'London-UCL-UAO' 'MCO-Hanimaadhoo' 'MD_Science_Center'
             'MVCO' 'Mainz' 'Malaga' 'Manila_Observatory' 'Messina' 'Mezaira' 'Minsk'
             'Modena' 'Moldova' 'Moscow_MSU_MO' 'Munich_University' 'Mussafa'
             'NCU_Taiwan' 'NGHIA_DO' 'Nes_Ziona' 'Noto' 'Oostende' 'Osaka' 'Palaiseau'
             'Paris' 'Pickle_Lake' 'Pokhara' 'Pune' 'Ragged_Point' 'Red_River_Delta'
             'Resolute_Bay' 'Rio_Branco' 'Rome_Tor_Vergata' 'SAGRES'
             'SANTA_CRUZ_UTEPSA' 'SEDE_BOKER' 'SERC' 'Saada' 'Santa_Cruz_Tenerife'
             'Sao_Martinho_SONDA' 'Sao_Paulo' 'Saturn_Island' 'Sevastopol' 'Seysses'
             'Shirahama' 'Silpakorn_Univ' 'Singapore' 'Skukuza' 'Solar_Village'
             'Songkhla_Met_Sta' 'TUBITAK_UZAY_Ankara' 'Taihu' 'Taipei_CWB'
             'Thessaloniki' 'Thompson_Farm' 'Tomsk' 'Toravere' 'Toulon' 'UMBC'
             'Ubon_Ratchathani' 'Univ_of_Houston' 'Univ_of_Lethbridge' 'Ussuriysk'
             'Venise' 'Vientiane' 'Villefranche' 'Wallops' 'WaveCIS_Site_CSI_6'
             'Xanthi' 'XiangHe' 'Xinglong' 'Yekaterinburg' 'Zinder_Airport']
result = []

import glob, os
import numpy as np
import pandas as pd
import xarray as xr

data_dir = '/lustre/storeA/project/aerocom/aerocom-users-database/PYAEROCOM_COLDATA/WEB_EVAL/aerocom/AP3-abs'
var_mask = 'abs550' # there is also some called abs550csaer or abs550aercs
exp = '25COV'

# INSERT HERE THE SITES THAT YOU ARE INTERESTED IN
sitenames = ['Alta_Floresta', 'Dakar']

result = {}
for mod in os.listdir(data_dir):
    print(mod)
    files = glob.glob(f'{data_dir}/{mod}/{var_mask}*{exp}*.nc')
    if not len(files) > 0: # ignore folders without data
        print(f'Skip {mod}')
        continue

    # make sure only one filematch
    assert len(files) == 1
    file = files[0]
    var_name = os.path.basename(files[0]).split('_')[0]
    data = xr.open_dataset(file)[var_name]

    print(data.station_name.data)
    raise Exception
    #make sure this is in monthly resolution
    assert data.ts_type == 'monthly'

    result[mod] = {}

    timestamps = data.time.data

    for i, site in enumerate(sitenames):
        result[mod][site] = {}
        # get plot axes for this site

        sitedata = data.sel(station_name=site)
        obs_numpy = sitedata.data[0]
        if all(np.isnan(obs_numpy)):
            print(f'No obsdata available at {site}')

        mod_numpy = sitedata.data[1]

        obs_ts = pd.Series(obs_numpy, timestamps)
        mod_ts = pd.Series(obs_numpy, timestamps)

        result[mod][site]['obs'] = obs_ts
        result[mod][site]['mod'] = mod_ts




