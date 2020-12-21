#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:28:09 2019

@author: jonasg
"""
import pyaerocom as pya
import numpy as np
import os

if __name__ == '__main__':
    from datetime import datetime
    REANALYSE_EXISTING = False

    LAT_LON_RES = [(2,3)]#, (1,1)]
    STATS = ['mean', 'median']

    # Emission variables
    EMI_BASE_VARS = ['emidust', 'emiss', 'emiso4','emioa', 'emibc',
                     'emiso2', 'emidms']

    # Burden variables
    BURDEN_VARS = ['loaddust', 'loadss', 'loadso4', 'loadoa', 'loadbc',
                   'loadno3']

    WET_VARS = [x.replace('load', 'wet') for x in BURDEN_VARS]
    DRY_VARS = [x.replace('load', 'dry') for x in BURDEN_VARS]

    EXT_VARS_SURF = ['sc550dryaer', 'ac550aer']

    # AOD variables
    OD_VARS = ['od550aer', 'od440aer', 'od870aer',
               'od550dust', 'od550ss', 'od550so4', 'od550oa',
               'od550bc', 'od550no3', 'od550aerh2o', 'od550nh4']

    # AAOD variables
    ABS_VARS = ['abs550bc', 'abs550oa','abs550dust',
                'abs870aer', 'abs440aer', 'abs550aer']

    # Angstrom variables
    ANG_VARS = ['angabs4487aer']

    SURF_VARS = [] #EMI_BASE_VARS + WET_VARS + DRY_VARS
    COLUMN_VARS = BURDEN_VARS + ABS_VARS + ANG_VARS

    VC_SURF = ['Surface'] * len(SURF_VARS)
    VC_COLUMN = ['Column'] * len(COLUMN_VARS)

    VARS = SURF_VARS + COLUMN_VARS
    VC = VC_SURF + VC_COLUMN

    CONFIG_DIR = '/home/jonasg/github/aerocom_evaluation/data/config_files/'
    PROJ_ID = 'aerocom'
    EXP_ID = 'AP3-abs'

    ADD_NAME = '-v2'

    YEARS = [2010]

    YEARS_VARS = {1850 : (['abs550aer'], ['Column'])}

    match_models = {}

    TS_TYPE = 'monthly'

    SAVE = True

    IGNORE_MODELS = ['AEROCOM-MEDIAN', 'AEROCOM-MEAN',
                     'OsloCTM3-1.01']

    MODEL_USE_VARS = {
        'GEOS'  : {'abs550oa' : 'abs550oc'}
    }

    cfg = pya.web.AerocomEvaluation(proj_id=PROJ_ID,
                                    exp_id=EXP_ID,
                                    config_dir=CONFIG_DIR)

    for var in cfg.all_obs_vars:

        if not var in VARS:
            raise Exception('Please add',var,'to your setup and specify vertical code')

    VARS = ['abs550aer']
    VC = ['Column']

    USE_MODELS = None #['GEOS', 'TM5']
    if USE_MODELS is None:
        USE_MODELS = list(cfg.model_config.keys())

    print = pya.const.print_log.info

    pya.const.print_log.info('-------------------------------------------')
    pya.const.print_log.info('The following variables will be processed:')
    pya.const.print_log.info('-------------------------------------------')
    pya.const.print_log.info(VARS)
    pya.const.print_log.info('-------------------------------------------')
    pya.const.print_log.info('-------------------------------------------')
    pya.const.print_log.info('The following models will be considered:')
    pya.const.print_log.info('-------------------------------------------')
    pya.const.print_log.info([x for x in USE_MODELS])
    pya.const.print_log.info('-------------------------------------------')
    pya.const.print_log.info('')
    pya.const.print_log.info('')

    #VARS, VC = ['abs550oa', 'abs550aer'], ['Column', 'Column']
    #USE_MODELS = ['INCA', 'OsloCTM3-1.02']
    for (lat_res_deg, lon_res_deg) in LAT_LON_RES:
        resstr ='{}x{}'.format(lat_res_deg, lon_res_deg)

        for avg_how in STATS:

            data_id = f'AEROCOM-{avg_how.upper()}-{resstr}-{EXP_ID}{ADD_NAME}'

            if not data_id in IGNORE_MODELS:
                IGNORE_MODELS.append(data_id)

            OUT_BASE_DIR = os.path.join(pya.const.OUTPUTDIR, data_id)
            OUT_DIR = os.path.join(OUT_BASE_DIR, 'renamed')

            if not os.path.exists(OUT_BASE_DIR):
                os.mkdir(OUT_BASE_DIR)
            if not os.path.exists(OUT_DIR):
                os.mkdir(OUT_DIR)

            logfilename = ('{}.log'.format(datetime.today().strftime('%Y%m%d')))
            logp = os.path.join(OUT_BASE_DIR, logfilename)
            if os.path.exists(logp):
                os.remove(logp)
            logfile = open(logp, 'w')

            for year in YEARS:

                if year in YEARS_VARS:
                    varlist, vclist = YEARS_VARS[year]
                else:
                    varlist, vclist = VARS, VC

                reanalyse_existing = REANALYSE_EXISTING
                for var_name, vc in zip(varlist, vclist):
                    outname = pya.io.helpers.aerocom_savename(data_id,
                                                              var_name,
                                                              vc, year,
                                                              TS_TYPE)

                    models = USE_MODELS
                    if var_name in match_models:
                        if year in match_models[var_name]:
                            _year = match_models[var_name][year]
                            outname_other = outname.replace(str(year), str(_year))
                            fp = os.path.join(OUT_DIR, outname_other)
                            if not os.path.exists(fp):
                                raise ValueError(
                                    f'Please process {_year} before {year}')
                            data = pya.GriddedData(fp)
                            models = data.metadata['from_models']


                    pya.const.print_log.info(f'\nPROCESSING {outname}\n')
                    logfile.write('\n\n{}'.format(var_name))

                    if os.path.exists(os.path.join(OUT_DIR, outname)) and reanalyse_existing==False:
                        pya.const.print_log.info('exists... -> skipping.')
                        logfile.write(': SKIPPED')
                        continue

                    surf = vc=='Surface'

                    comment = (f'AeroCom {avg_how} model data for variable '
                               f'{var_name}')

                    try:
                        (mean,
                         delta,
                         q1,
                         q3,
                         std) = pya.web.compute_model_average_and_diversity(
                                 cfg,
                                 model_names=models,
                                 var_name=var_name,
                                 data_id=data_id,
                                 ts_type=TS_TYPE,
                                 lat_res_deg=lat_res_deg,
                                 lon_res_deg=lon_res_deg,
                                 year=year,
                                 avg_how=avg_how,
                                 extract_surface=surf,
                                 logfile=logfile,
                                 ignore_models=IGNORE_MODELS,
                                 comment=comment,
                                 vert_which=vc,
                                 model_use_vars=MODEL_USE_VARS)

                        if SAVE:
                            mean.to_netcdf(OUT_DIR, savename=outname)
                            sndiv = outname.replace(var_name, '{}div'.format(var_name))
                            delta.to_netcdf(OUT_DIR, savename=sndiv)
                            if avg_how=='median':
                                snq1 = outname.replace(var_name, '{}q1'.format(var_name))
                                snq3 = outname.replace(var_name, '{}q3'.format(var_name))

                                q1.to_netcdf(OUT_DIR, savename=snq1)
                                q3.to_netcdf(OUT_DIR, savename=snq3)
                            else:
                                snstd = outname.replace(var_name, '{}std'.format(var_name))
                                std.to_netcdf(OUT_DIR, savename=snstd)
                            pya.const.print_log.info(f'SAVED: {outname}')
                            logfile.write(f'\nSAVED: {outname}')

                    except Exception as e:
                        from traceback import format_exc
                        pya.const.print_log.info(f'FAILED: {outname}. Reason: {e})')
                        logfile.write(f'\nFAILED: {outname}\n{format_exc()})\n')

            logfile.close()