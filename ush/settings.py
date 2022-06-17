from datetime import datetime, timedelta as td

class Toggle():
    def __init__(self):
        self.plot_settings = {
            'x_min_limit': -9999.,
            'x_max_limit': 9999.,
            'x_lim_lock': False,
            'y_min_limit': -9999.,
            'y_max_limit': 9999.,
            'y_lim_lock': False,
            'ci_lev': .95,
            'bs_nrep': 5000,
            'bs_method': 'FORECASTS',
            'bs_min_samp': 30,
            'display_averages': False,
            'event_equalization': False,
        }

class Templates():
    def __init__(self):
        '''
        Custom template used to find .stat files in OUTPUT_BASE_DIR.
        lookfor_template must be a string. Use curly braces {} to enclose variable
        names that will be substituted with the appropriate value according to
        the current plotting request.   

        Current possible variable names:    Example substituted values:
        ================================    ===========================
        RUN_CASE                            grid2obs
        RUN_TYPE                            conus_sfc
        LINE_TYPE                           sl1l2
        VX_MASK                             conus
        FCST_VAR_NAME                       VIS
        VAR_NAME                            VISsfc
        MODEL                               HRRR
        EVAL_PERIOD                         PAST30DAYS
        valid?fmt=%Y%m or VALID?fmt=%Y%m    202206

        Additionally, variable names may have the _LOWER or _UPPER suffix to 
        substitute a lower- or upper-case conversion of the desired string.

        Finally, use asterisk * as a wildcard to match with and use data from
        several .stat files, or for portions of the .stat file name that vary but 
        are inconsequential.

        Example: 
        "{RUN_CASE_LOWER}/{MODEL}/{valid?fmt=%Y%m}/{MODEL}_{valid?fmt=%Y%m%d}*"
        '''
        self.lookfor_template = "{RUN_CASE_LOWER}/{MODEL}/{valid?fmt=%Y%m}/{MODEL}_{valid?fmt=%Y%m%d}*"

class Presets():
    def __init__(self):
        self.date_presets = {
            'PAST30DAYS': {
                'valid_beg': (datetime.now()-td(days=30)).strftime('%Y%m%d'),
                'valid_end': (datetime.now()-td(days=1)).strftime('%Y%m%d'),
                'init_beg': (datetime.now()-td(days=30)).strftime('%Y%m%d'),
                'init_end': (datetime.now()-td(days=1)).strftime('%Y%m%d')
            },
            'PAST7DAYS': {
                'valid_beg': (datetime.now()-td(days=7)).strftime('%Y%m%d'),
                'valid_end': (datetime.now()-td(days=1)).strftime('%Y%m%d'),
                'init_beg': (datetime.now()-td(days=7)).strftime('%Y%m%d'),
                'init_end': (datetime.now()-td(days=1)).strftime('%Y%m%d')
            },
            'PAST3DAYS': {
                'valid_beg': (datetime.now()-td(days=3)).strftime('%Y%m%d'),
                'valid_end': (datetime.now()-td(days=1)).strftime('%Y%m%d'),
                'init_beg': (datetime.now()-td(days=3)).strftime('%Y%m%d'),
                'init_end': (datetime.now()-td(days=1)).strftime('%Y%m%d')
            },
            '2020': {
                'valid_beg': '20200101',
                'valid_end': '20201231',
                'init_beg': '20200101',
                'init_end': '20201231'
            },
            '2021': {
                'valid_beg': '20210101',
                'valid_end': '20211231',
                'init_beg': '20210101',
                'init_end': '20211231'
            },
            'DJF': {
                'valid_beg': (datetime.now()-td(days=365)).strftime('%Y1201'),
                'valid_end': datetime.now().strftime('%Y0228'),
                'init_beg': (datetime.now()-td(days=365)).strftime('%Y1201'),
                'init_end': datetime.now().strftime('%Y0228')
            },
            'MAM': {
                'valid_beg': datetime.now().strftime('%Y0301'),
                'valid_end': datetime.now().strftime('%Y0531'),
                'init_beg': datetime.now().strftime('%Y0301'),
                'init_end': datetime.now().strftime('%Y0531')
            },
            'JJA': {
                'valid_beg': datetime.now().strftime('%Y0601'),
                'valid_end': datetime.now().strftime('%Y0831'),
                'init_beg': datetime.now().strftime('%Y0601'),
                'init_end': datetime.now().strftime('%Y0831')
            },
            'SON': {
                'valid_beg': datetime.now().strftime('%Y0901'),
                'valid_end': datetime.now().strftime('%Y1130'),
                'init_beg': datetime.now().strftime('%Y0901'),
                'init_end': datetime.now().strftime('%Y1130')
            }
        }
            
class ModelSpecs():
    def __init__(self):
        self.model_alias = {
            'ARW': {
                'settings_key':'HRW_ARW', 
                'plot_name':'HiResW ARW'
            },
            'ARW2': {
                'settings_key':'HRW_ARW2', 
                'plot_name':'HiResW ARW2'
            },
            'FV3': {
                'settings_key':'HRW_FV3', 
                'plot_name':'HiResW FV3'
            },
            'NMMB': {
                'settings_key':'HRW_NMMB', 
                'plot_name':'HiResW NMMB'
            },
            'AKARW': {
                'settings_key':'HRW_ARW', 
                'plot_name':'HiResW ARW'
            },
            'AKARW2': {
                'settings_key':'HRW_ARW2', 
                'plot_name':'HiResW ARW2'
            },
            'AKFV3': {
                'settings_key':'HRW_FV3', 
                'plot_name':'HiResW FV3'
            },
            'AKNEST': {
                'settings_key':'NAM_NEST', 
                'plot_name':'NAM Nest'
            },
            'AKNMMB': {
                'settings_key':'HRW_NMMB', 
                'plot_name':'HiResW NMMB'
            },
            'CONUSARW': {
                'settings_key':'HRW_ARW', 
                'plot_name':'HiResW ARW'
            },
            'CONUSARW2': {
                'settings_key':'HRW_ARW2', 
                'plot_name':'HiResW ARW2'
            },
            'CONUSFV3': {
                'settings_key':'HRW_FV3', 
                'plot_name':'HiResW FV3'
            },
            'CONUSNEST': {
                'settings_key':'NAM_NEST', 
                'plot_name':'NAM Nest'
            },
            'CONUSNMMB': {
                'settings_key':'HRW_NMMB', 
                'plot_name':'HiResW NMMB'
            },
            'HREF_MEAN':{
                'settings_key':'HREF_MEAN', 
                'plot_name':'HREF Mean'
            },
            'HREF_AVRG':{
                'settings_key':'HREF_AVRG', 
                'plot_name':'HREF Average of MEAN and PMMN'
            },
            'HREF_LPMM':{
                'settings_key':'HREF_LPMM', 
                'plot_name':'HREF Local Probability-Matched Mean'
            },
            'HREF_PMMN':{
                'settings_key':'HREF_PMMN', 
                'plot_name':'HREF Probability-Matched Mean'
            },
            'HREF_PROB':{
                'settings_key':'HREF_PROB', 
                'plot_name':'HREF Probability'
            },
            'HREFX_MEAN':{
                'settings_key':'HREFX_MEAN', 
                'plot_name':'HREF-X Mean'
            },
            'CONUSHREF_MEAN':{
                'settings_key':'HREF_MEAN', 
                'plot_name':'HREF Mean'
            },
            'CONUSHREF_AVRG':{
                'settings_key':'HREF_AVRG', 
                'plot_name':'HREF Average of MEAN and PMMN'
            },
            'CONUSHREF_LPMM':{
                'settings_key':'HREF_LPMM', 
                'plot_name':'HREF Local Probability-Matched Mean'
            },
            'CONUSHREF_PMMN':{
                'settings_key':'HREF_PMMN', 
                'plot_name':'HREF Probability-Matched Mean'
            },
            'CONUSHREF_PROB':{
                'settings_key':'HREF_PROB', 
                'plot_name':'HREF Probability'
            },
            'CONUSHREFX_MEAN':{
                'settings_key':'HREFX_MEAN', 
                'plot_name':'HREF-X Mean'
            },
            'AKHREF_MEAN':{
                'settings_key':'HREF_MEAN', 
                'plot_name':'HREF Mean'
            },
            'AKHREF_AVRG':{
                'settings_key':'HREF_AVRG', 
                'plot_name':'HREF Average of MEAN and PMMN'
            },
            'AKHREF_LPMM':{
                'settings_key':'HREF_LPMM', 
                'plot_name':'HREF Local Probability-Matched Mean'
            },
            'AKHREF_PMMN':{
                'settings_key':'HREF_PMMN', 
                'plot_name':'HREF Probability-Matched Mean'
            },
            'AKHREF_PROB':{
                'settings_key':'HREF_PROB', 
                'plot_name':'HREF Probability'
            },
            'AKHREFX_MEAN':{
                'settings_key':'HREFX_MEAN', 
                'plot_name':'HREF-X Mean'
            },
            'PRHREF_MEAN':{
                'settings_key':'HREF_MEAN', 
                'plot_name':'HREF Mean'
            },
            'PRHREF_AVRG':{
                'settings_key':'HREF_AVRG', 
                'plot_name':'HREF Average of MEAN and PMMN'
            },
            'PRHREF_LPMM':{
                'settings_key':'HREF_LPMM', 
                'plot_name':'HREF Local Probability-Matched Mean'
            },
            'PRHREF_PMMN':{
                'settings_key':'HREF_PMMN', 
                'plot_name':'HREF Probability-Matched Mean'
            },
            'PRHREF_PROB':{
                'settings_key':'HREF_PROB', 
                'plot_name':'HREF Probability'
            },
            'PRHREFX_MEAN':{
                'settings_key':'HREFX_MEAN', 
                'plot_name':'HREF-X Mean'
            },
            'HIHREF_MEAN':{
                'settings_key':'HREF_MEAN', 
                'plot_name':'HREF Mean'
            },
            'HIHREF_AVRG':{
                'settings_key':'HREF_AVRG', 
                'plot_name':'HREF Average of MEAN and PMMN'
            },
            'HIHREF_LPMM':{
                'settings_key':'HREF_LPMM', 
                'plot_name':'HREF Local Probability-Matched Mean'
            },
            'HIHREF_PMMN':{
                'settings_key':'HREF_PMMN', 
                'plot_name':'HREF Probability-Matched Mean'
            },
            'HIHREF_PROB':{
                'settings_key':'HREF_PROB', 
                'plot_name':'HREF Probability'
            },
            'HIHREFX_MEAN':{
                'settings_key':'HREFX_MEAN', 
                'plot_name':'HREF-X Mean'
            },
            'NARRE_MEAN':{
                'settings_key':'NARRE_MEAN', 
                'plot_name':'NARRE Mean'
            },
            'HIARW': {
                'settings_key':'HRW_ARW', 
                'plot_name':'HiResW ARW'
            },
            'HIARW2': {
                'settings_key':'HRW_ARW2', 
                'plot_name':'HiResW ARW2'
            },
            'HIFV3': {
                'settings_key':'HRW_FV3', 
                'plot_name':'HiResW FV3'
            },
            'HINMMB': {
                'settings_key':'HRW_NMMB', 
                'plot_name':'HiResW NMMB'
            },
            'HAWAIINEST': {
                'settings_key':'NAM_NEST', 
                'plot_name':'NAM Nest'
            },
            'PRARW': {
                'settings_key':'HRW_ARW', 
                'plot_name':'HiResW ARW'
            },
            'PRARW2': {
                'settings_key':'HRW_ARW2', 
                'plot_name':'HiResW ARW2'
            },
            'PRFV3': {
                'settings_key':'HRW_FV3', 
                'plot_name':'HiResW FV3'
            },
            'PRNMMB': {
                'settings_key':'HRW_NMMB', 
                'plot_name':'HiResW NMMB'
            },
            'PRICONEST': {
                'settings_key':'NAM_NEST', 
                'plot_name':'NAM Nest'
            },
            'FV3LAMDA': {
                'settings_key':'LAMDA', 
                'plot_name':'FV3LAM-DA'
            },
            'FV3LAMDAX': {
                'settings_key':'LAMDAX', 
                'plot_name':'FV3LAM-DAX'
            },
            'FV3LAMDAXAK': {
                'settings_key':'LAMDAX', 
                'plot_name':'FV3LAM-DAX'
            },
            'FV3LAMDAXHI': {
                'settings_key':'LAMDAX', 
                'plot_name':'FV3LAM-DAX'
            },
            'FV3LAMDAXNA': {
                'settings_key':'LAMDAX', 
                'plot_name':'FV3LAM-DAX'
            },
            'FV3LAMDAXPR': {
                'settings_key':'LAMDAX', 
                'plot_name':'FV3LAM-DAX'
            },
            'FV3LAM': {
                'settings_key':'LAM', 
                'plot_name':'FV3LAM'
            },
            'FV3LAMAK': {
                'settings_key':'LAM', 
                'plot_name':'FV3LAM'
            },
            'FV3LAMHI': {
                'settings_key':'LAM', 
                'plot_name':'FV3LAM'
            },
            'FV3LAMNA': {
                'settings_key':'LAM', 
                'plot_name':'FV3LAM'
            },
            'FV3LAMPR': {
                'settings_key':'LAM', 
                'plot_name':'FV3LAM'
            },
            'FV3LAMX': {
                'settings_key':'LAMX', 
                'plot_name':'FV3LAM-X'
            },
            'FV3LAMXAK': {
                'settings_key':'LAMX', 
                'plot_name':'FV3LAM-X'
            },
            'FV3LAMXHI': {
                'settings_key':'LAMX', 
                'plot_name':'FV3LAM-X'
            },
            'FV3LAMXNA': {
                'settings_key':'LAMX', 
                'plot_name':'FV3LAM-X'
            },
            'FV3LAMXPR': {
                'settings_key':'LAMX', 
                'plot_name':'FV3LAM-X'
            },
            'NAM_NEST': {
                'settings_key':'NAM_NEST', 
                'plot_name':'NAM Nest'
            },
            'HRRRAK': {
                'settings_key':'HRRR', 
                'plot_name':'HRRR'
            },
            'NAMNA': {
                'settings_key':'NAM', 
                'plot_name':'NAM'
            },
            'RAPAK': {
                'settings_key':'RAP', 
                'plot_name':'RAP'
            },
            'RAPNA': {
                'settings_key':'RAP', 
                'plot_name':'RAP'
            },
            'RRFS_A': {
                'settings_key':'RRFS_A', 
                'plot_name':'RRFS-A'
            }
        }
        self.model_settings = {
            'model1': {'color': '#000000',
                       'marker': 'o', 'markersize': 12,
                       'linestyle': 'solid', 'linewidth': 3.},
            'model2': {'color': '#fb2020',
                       'marker': '^', 'markersize': 14,
                       'linestyle': 'solid', 'linewidth': 3.},
            'model3': {'color': '#1e3cff',
                       'marker': 'X', 'markersize': 14,
                       'linestyle': 'solid', 'linewidth': 3.},
            'model4': {'color': '#00dc00',
                       'marker': 'P', 'markersize': 14,
                       'linestyle': 'solid', 'linewidth': 3.},
            'model5': {'color': '#e69f00',
                       'marker': 'o', 'markersize': 12,
                       'linestyle': 'solid', 'linewidth': 3.},
            'model6': {'color': '#56b4e9',
                       'marker': 'o', 'markersize': 12,
                       'linestyle': 'solid', 'linewidth': 3.},
            'model7': {'color': '#696969',
                       'marker': 's', 'markersize': 12,
                       'linestyle': 'solid', 'linewidth': 3.},
            'model8': {'color': '#8400c8',
                       'marker': 'D', 'markersize': 12,
                       'linestyle': 'solid', 'linewidth': 3.},
            'model9': {'color': '#d269c1',
                       'marker': 's', 'markersize': 12,
                       'linestyle': 'solid', 'linewidth': 3.},
            'model10': {'color': '#f0e492',
                        'marker': 'o', 'markersize': 12,
                        'linestyle': 'solid', 'linewidth': 3.},
            'obs': {'color': '#aaaaaa',
                    'marker': 'None', 'markersize': 0,
                    'linestyle': 'solid', 'linewidth': 4.},
            'LAM': {'color': '#00dc00',
                      'marker': 'o', 'markersize': 12,
                      'linestyle': 'solid', 'linewidth': 3.},
            'LAMDA': {'color': '#8400c8',
                      'marker': 'o', 'markersize': 12,
                      'linestyle': 'solid', 'linewidth': 3.},
            'LAMX': {'color': '#00dc00',
                       'marker': 'P', 'markersize': 14,
                       'linestyle': 'dashed', 'linewidth': 3.},
            'LAMDAX': {'color': '#8400c8',
                       'marker': 'P', 'markersize': 14,
                       'linestyle': 'dashed', 'linewidth': 3.},
            'HWRF': {'color': '#00dc00',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'HMON': {'color': '#8400c8',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'HRW_ARW': {'color': '#00dc00',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'HRW_ARW2': {'color': '#e69f00',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'HRW_FV3': {'color': '#56b4e9',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'HREF_MEAN': {'color': '#000000',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'HREF_AVRG': {'color': '#696969',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'HREF_PMMN': {'color': '#8400c8',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'HREF_LPMM': {'color': '#d269c1',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'HREFX_MEAN': {'color': '#000000',
                     'marker': 'P', 'markersize': 14,
                     'linestyle': 'dashed', 'linewidth': 3.},
            'HRRR': {'color': '#fb2020',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'NAM': {'color': '#1e3cff',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'NAM_NEST': {'color': '#1e3cff',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'RRFS_A': {'color': '#00dc00',
                      'marker': 'o', 'markersize': 12,
                      'linestyle': 'solid', 'linewidth': 3.},
            'GFS': {'color': '#000000',
                    'marker': 'o', 'markersize': 12,
                    'linestyle': 'solid', 'linewidth': 5.},
            'GFS_DASHED': {'color': '#000000',
                           'marker': 'o', 'markersize': 12,
                           'linestyle': 'dashed', 'linewidth': 5.},
            'GEFS': {'color': '#000000',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 5.},
            'NARRE_MEAN': {'color': '#000000',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 5.},
            'EC': {'color': '#fb2020',
                   'marker': 'o', 'markersize': 12,
                   'linestyle': 'solid', 'linewidth': 3.},
            'CMC': {'color': '#1e3cff',
                    'marker': 'o', 'markersize': 12,
                    'linestyle': 'solid', 'linewidth': 3.},
            'CTCX': {'color': '#56b4e9',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.},
            'OFCL': {'color': '#696969',
                     'marker': 'o', 'markersize': 12,
                     'linestyle': 'solid', 'linewidth': 3.}
        }    
      
    def get_color_dict(self, name):
        color_dict = self.model_settings[name]
        return color_dict

class Reference():
    def __init__(self):
        self.variable_translator = {'TMP': 'Temperature',
                                    'TMP_Z0_mean': 'Temperature',
                                    'HGT': 'Geopotential Height',
                                    'HGT_WV1_0-3': ('Geopotential Height:' 
                                                    + ' Waves 0-3'),
                                    'HGT_WV1_4-9': ('Geopotential Height:'
                                                    + ' Waves 4-9'),
                                    'HGT_WV1_10-20': ('Geopotential Height:'
                                                      + ' Waves 10-20'),
                                    'HGT_WV1_0-20': ('Geopotential Height:'
                                                     + ' Waves 0-20'),
                                    'RH': 'Relative Humidity',
                                    'SPFH': 'Specific Humidity',
                                    'DPT': 'Dewpoint Temperature',
                                    'UGRD': 'Zonal Wind Speed',
                                    'VGRD': 'Meridional Wind Speed',
                                    'UGRD_VGRD': 'Vector Wind Speed',
                                    'GUST': 'Wind Gust',
                                    'CAPE': ('Convective Available Potential'
                                             + ' Energy'),
                                    'PRES': 'Pressure',
                                    'PRMSL': 'Pressure Reduced to MSL',
                                    'O3MR': 'Ozone Mixing Ratio',
                                    'TOZNE': 'Total Ozone',
                                    'OZCON1': 'OZCON1',
                                    'HPBL': 'Planetary Boundary Layer Height',
                                    'TSOIL': 'Soil Temperature',
                                    'SOILW': ('Volumetric Soil Moisture'
                                              + ' Content'),
                                    'WEASD': 'Accum. Snow Depth Water Equiv.',
                                    'APCP': ('Accumulated'
                                                + ' Precipitation'),
                                    'APCP_01': ('1-hour Accumulated'
                                                + ' Precipitation'),
                                    'APCP_03': ('3-hour Accumulated'
                                                + ' Precipitation'),
                                    'APCP_06': ('6-hour Accumulated'
                                                + ' Precipitation'),
                                    'APCP_24': ('24-hour Accumulated'
                                                + ' Precipitation'),
                                    'PWAT': 'Precipitable Water',
                                    'CWAT': 'Cloud Water',
                                    'TCDC': 'Cloud Area Fraction',
                                    'HGTCLDCEIL': 'Cloud Ceiling Height',
                                    'VIS': 'Visibility',
                                    'ICEC_Z0_mean': 'Sea Ice Concentration',
                                    'REFC': 'Composite Reflectivity',
                                    'REFD': 'Above Ground Level Reflectivity',
                                    'RETOP': 'Echo Top Height'}
        self.domain_translator = {'NHX': 'Northern Hemisphere 20N-80N',
                                  'SHX': 'Southern Hemisphere 20S-80S',
                                  'TRO': 'Tropics 20S-20N',
                                  'PNA': 'Pacific North America',
                                  'N60': '60N-90N',
                                  'S60': '60S-90S',
                                  'NPO': 'Northern Pacific Ocean',
                                  'SPO': 'Southern Pacific Ocean',
                                  'NAO': 'Northern Atlantic Ocean',
                                  'SAO': 'Southern Atlantic Ocean',
                                  'NH': 'Northern Hemisphere 20N-90N',
                                  'SH': 'Southern Hemisphere 20S-90S',
                                  'G002': 'Global',
                                  'G003': 'Global',
                                  'G130': 'CONUS - NCEP Grid 130',
                                  'G211': 'CONUS - NCEP Grid 211',
                                  'G236': 'CONUS - NCEP Grid 236',
                                  'G223': 'CONUS - NCEP Grid 223',
                                  'CONUS': 'CONUS',
                                  'POLAR': 'Polar 60-90 N/S',
                                  'ARCTIC': 'Arctic',
                                  'EAST': 'Eastern US',
                                  'WEST': 'Western US',
                                  'NWC': 'Northwest Coast',
                                  'SWC': 'Southwest Coast',
                                  'NMT': 'Northern Mountain Region',
                                  'GRB': 'Great Basin',
                                  'SMT': 'Southern Mountain Region',
                                  'SWD': 'Southwest Desert',
                                  'NPL': 'Northern Plains',
                                  'SPL': 'Southern Plains',
                                  'MDW': 'Midwest',
                                  'LMV': 'Lower Mississippi Valley',
                                  'APL': 'Appalachians',
                                  'NEC': 'Northeast Coast',
                                  'SEC': 'Southeast Coast',
                                  'GMC': 'Gulf of Mexico Coast',
                                  'NAK': 'Northern Alaska',
                                  'SAK': 'Southern Alaska',
                                  'SEA_ICE': 'Global - Sea Ice',
                                  'SEA_ICE_FREE': 'Global - Sea Ice Free',
                                  'SEA_ICE_POLAR': 'Polar - Sea Ice',
                                  'SEA_ICE_FREE_POLAR': ('Polar - Sea Ice'
                                                         + ' Free')}
        self.linetype_cols = {'FHO':['TOTAL','F_RATE','H_RATE','O_RATE'],
                              'CTC':['TOTAL','FY_OY','FY_ON','FN_OY','FN_ON'],
                              'CTS':['TOTAL','BASER','BASER_NCL','BASER_NCU',
                                     'BASER_BCL','BASER_BCU','FMEAN',
                                     'FMEAN_NCL','FMEAN_NCU','FMEAN_BCL',
                                     'FMEAN_BCU','ACC','ACC_NCL','ACC_NCU',
                                     'ACC_BCL','ACC_BCU','FBIAS','FBIAS_BCL',
                                     'FBIAS_BCU','PODY','PODY_NCL','PODY_NCU',
                                     'PODY_BCL','PODY_BCU','PODN','PODN_NCL',
                                     'PODN_NCU','PODN_BCL','PODN_BCU','POFD',
                                     'POFD_NCL','POFD_NCU','POFD_BCL',
                                     'POFD_BCU','FAR','FAR_NCL','FAR_NCU',
                                     'FAR_BCL','FAR_BCU','CSI','CSI_NCL',
                                     'CSI_NCU','CSI_BCL','CSI_BCU','GSS',
                                     'GSS_BCL','GSS_BCU','HK','HK_NCL',
                                     'HK_NCU','HK_BCL','HK_BCU','HSS',
                                     'HSS_BCL','HSS_BCU','ODDS','ODDS_NCL',
                                     'ODDS_NCU','ODDS_BCL','ODDS_BCU','LODDS',
                                     'LODDS_NCL','LODDS_NCU','LODDS_BCL',
                                     'LODDS_BCU','ORSS','ORSS_NCL','ORSS_NCU',
                                     'ORSS_BCL','ORSS_BCU','EDS','EDS_NCL',
                                     'EDS_NCU','EDS_BCL','EDS_BCU','SEDS',
                                     'SEDS_NCL','SEDS_NCU','SEDS_BCL',
                                     'SEDS_BCU','EDI','EDI_NCL','EDI_NCU',
                                     'EDI_BCL','EDI_BCU','SEDI','SEDI_NCL',
                                     'SEDI_NCU','SEDI_BCL','SEDI_BCU','BAGSS',
                                     'BAGSS_BCL','BAGSS_BCU'],
                              'CNT':['TOTAL','FBAR','FBAR_NCL','FBAR_NCU',
                                     'FBAR_BCL','FBAR_BCU','FSTDEV',
                                     'FSTDEV_NCL','FSTDEV_NCU','FSTDEV_BCL',
                                     'FSTDEV_BCU','OBAR','OBAR_NCL',
                                     'OBAR_NCU','OBAR_BCL','OBAR_BCU',
                                     'OSTDEV','OSTDEV_NCL','OSTDEV_NCU',
                                     'OSTDEV_BCL','OSTDEV_BCU','PR_CORR',
                                     'PR_CORR_NCL','PR_CORR_NCU',
                                     'PR_CORR_BCL','PR_CORR_BCU','SP_CORR', 
                                     'KT_CORR','RANKS','FRANK_TIES',
                                     'ORANK_TIES','ME','ME_NCL','ME_NCU',
                                     'ME_BCL','ME_BCU','ESTDEV','ESTDEV_NCL',
                                     'ESTDEV_NCU','ESTDEV_BCL','ESTDEV_BCU',
                                     'MBIAS','MBIAS_BCL','MBIAS_BCU',
                                     'MAE','MAE_BCL','MAE_BCU',
                                     'MSE','MSE_BCL','MSE_BCU',
                                     'BCMSE','BCMSE_BCL','BCMSE_BCU',
                                     'RMSE','RMSE_BCL','RMSE_BCU',
                                     'E10','E10_BCL','E10_BCU',
                                     'E25','E25_BCL','E25_BCU',
                                     'E50','E50_BCL','E50_BCU',
                                     'E75','E75_BCL','E75_BCU',
                                     'E90','E90_BCL','E90_BCU',
                                     'IQR','IQR_BCL','IQR_BCU',
                                     'MAD','MAD_BCL','MAD_BCU',
                                     'ANOM_CORR','ANOM_CORR_NCL',
                                     'ANOM_CORR_NCU','ANOM_CORR_BCL',
                                     'ANOM_CORR_BCU',
                                     'ME2','ME2_BCL','ME2_BCU',
                                     'MSESS','MSESS_BCL','MSESS_BCU',
                                     'RMSFA','RMSFA_BCL','RMSFA_BCU',
                                     'RMSOA','RMSOA_BCL','RMSOA_BCU',
                                     'ANOM_CORR_UNCNTR',
                                     'ANOM_CORR_UNCNTR_BCL',
                                     'ANOM_CORR_UNCNTR_BCU'],
                              'MCTC':['TOTAL','N_CAT','Fi_Oj'],
                              'MCTS':['TOTAL','N_CAT','ACC','ACC_NCL',
                                      'ACC_NCU','ACC_BCL','ACC_BCU',
                                      'HK','HK_BCL','HK_BCU',
                                      'GER','GER_BCL','GER_BCU'],
                              'PCT':['TOTAL','N_THRESH','THRESH_i','OY_i',
                                      'ON_i','THRESH_n'],
                              'PSTD':['TOTAL','N_THRESH','BASER','BASER_NCL',
                                      'BASER_NCU','RELIABILITY','RESOLUTION',
                                      'UNCERTAINTY','ROC_AUC','BRIER',
                                      'BRIER_NCL','BRIER_NCU','BRIERCL',
                                      'BRIERCL_NCL','BRIERCL_NCU',
                                      'BSS','BSS_SMPL','THRESH_i'],
                              'PJC':['TOTAL','N_THRESH','THRESH_i','OY_TP_i',
                                     'ON_TP_i','CALIBRATION_i','REFINEMENT_i',
                                     'LIKELIHOOD_i','BASER_i','THRESH_n'],
                              'PRC':['TOTAL','N_THRESH','THRESH_i','PODY_i',
                                      'POFD_i','THRESH_n'],
                              'ECLV':['TOTAL','BASER','VALUE_BASER','N_PNT',
                                      'CL_i','VALUE_i'],
                              'SL1L2':['TOTAL','FBAR','OBAR','FOBAR','FFBAR',
                                       'OOBAR','MAE'],
                              'SAL1L2':['TOTAL','FABAR','OABAR','FOABAR',
                                        'FFABAR','OOABAR','MAE'],
                              'VL1L2':['TOTAL','UFBAR','VFBAR','UOBAR',
                                       'VOBAR','UVFOBAR','UVFFBAR','UVOOBAR',
                                       'F_SPEED_BAR','O_SPEED_BAR'],
                              'VAL1L2':['TOTAL','UFABAR','VFABAR','UOABAR',
                                        'VOABAR','UVFOABAR','UVFFABAR',
                                        'UVOOABAR'],
                              'VCNT':['TOTAL','FBAR','OBAR','FS_RMS','OS_RMS',
                                      'MSVE','RMSVE','FSTDEV','OSTDEV',
                                      'FDIR','ODIR','FBAR_SPEED','OBAR_SPEED',
                                      'VDIFF_SPEED','VDIFF_DIR','SPEED_ERR',
                                      'SPEED_ABSERR','DIR_ERR','DIR_ABSERR'],
                              'MPR':['TOTAL','INDEX','OBS_SID','OBS_LAT',
                                     'OBS_LON','OBS_LVL','OBS_ELV','FCST',
                                     'OBS','OBS_QC','CLIMO_MEAN',
                                     'CLIMO_STDEV','CLIMO_CDF'],
                              'NBRCTC':['TOTAL','FY_OY','FY_ON','FN_OY',
                                        'FN_ON'],
                              'NBRCTS':['TOTAL','BASER','BASER_NCL',
                                        'BASER_NCU','BASER_BCL','BASER_BCU',
                                        'FMEAN','FMEAN_NCL','FMEAN_NCU',
                                        'FMEAN_BCL','FMEAN_BCU','ACC',
                                        'ACC_NCL','ACC_NCU','ACC_BCL',
                                        'ACC_BCU','FBIAS','FBIAS_BCL',
                                        'FBIAS_BCU','PODY','PODY_NCL',
                                        'PODY_NCU','PODY_BCL','PODY_BCU',
                                        'PODN','PODN_NCL','PODN_NCU',
                                        'PODN_BCL','PODN_BCU','POFD',
                                        'POFD_NCL','POFD_NCU','POFD_BCL',
                                        'POFD_BCU','FAR','FAR_NCL','FAR_NCU',
                                        'FAR_BCL','FAR_BCU','CSI','CSI_NCL',
                                        'CSI_NCU','CSI_BCL','CSI_BCU','GSS',
                                        'GSS_BCL','GSS_BCU','HK','HK_NCL',
                                        'HK_NCU','HK_BCL','HK_BCU','HSS',
                                        'HSS_BCL','HSS_BCU','ODDS','ODDS_NCL',
                                        'ODDS_NCU','ODDS_BCL','ODDS_BCU',
                                        'LODDS','LODDS_NCL','LODDS_NCU',
                                        'LODDS_BCL','LODDS_BCU','ORSS',
                                        'ORSS_NCL','ORSS_NCU','ORSS_BCL',
                                        'ORSS_BCU','EDS','EDS_NCL','EDS_NCU',
                                        'EDS_BCL','EDS_BCU','SEDS','SEDS_NCL',
                                        'SEDS_NCU','SEDS_BCL','SEDS_BCU',
                                        'EDI','EDI_NCL','EDI_NCU','EDI_BCL',
                                        'EDI_BCU','SEDI','SEDI_NCL',
                                        'SEDI_NCU','SEDI_BCL','SEDI_BCU',
                                        'BAGSS','BAGSS_BCL','BAGSS_BCU'],
                              'NBRCNT':['TOTAL','FBS','FBS_BCL','FBS_BCU',
                                        'FSS','FSS_BCL','FSS_BCU',
                                        'AFSS','AFSS_BCL','AFSS_BCU',
                                        'UFSS','UFSS_BCL','UFSS_BCU',
                                        'F_RATE','F_RATE_BCL','F_RATE_BCU',
                                        'O_RATE','O_RATE_BCL','O_RATE_BCU'],
                              'GRAD':['TOTAL','FGBAR','OGBAR','MGBAR','EGBAR',
                                      'S1','S1_OG','FGOG_RATIO','DX','DY'],
                              'DMAP':['TOTAL','FY','OY','FBIAS','BADDELEY',
                                      'HAUSDORFF','MED_FO','MED_OF','MED_MIN',
                                      'MED_MAX','MED_MEAN','FOM_FO','FOM_OF',
                                      'FOM_MIN','FROM_MAX','FOM_MEAN','ZHU_FO',
                                      'ZHU_OF','ZHU_MIN','ZHU_MAX','ZHU_MEAN'],
        }
        self.case_type = {
            'grid2grid_anom': {
                'SAL1L2': {
                    'plot_stats_list': 'acc',
                    'interp': 'NEAREST',
                    'vx_mask_list' : ['NHX', 'SHX', 'PNA', 'TRO'],
                    'var_dict': {
                        'HGT': {'fcst_var_name': 'HGT',
                                'fcst_var_levels': [
                                    'P1000', 'P700', 'P500', 'P250'
                                ],
                                'fcst_var_thresholds': '',
                                'fcst_var_options': '',
                                'obs_var_name': 'HGT',
                                'obs_var_levels': [
                                    'P1000', 'P700', 'P500', 'P250'
                                ],
                                'obs_var_thresholds': '',
                                'obs_var_options': '',
                                'plot_group':'sfc_upper'},
                        'HGT_WV1_0-20': {'fcst_var_name': 'HGT',
                                         'fcst_var_levels': [
                                             'P1000', 'P700', 'P500', 'P250'
                                         ],
                                         'fcst_var_thresholds': '',
                                         'fcst_var_options': '',
                                         'obs_var_name': 'HGT',
                                         'obs_var_levels': [
                                             'P1000', 'P700', 'P500', 'P250'
                                         ],
                                         'obs_var_thresholds': '',
                                         'obs_var_options': '',
                                         'plot_group':'sfc_upper'},
                        'HGT_WV1_0-3': {'fcst_var_name': 'HGT',
                                        'fcst_var_levels': [
                                            'P1000', 'P700', 'P500', 'P250'
                                        ],
                                        'fcst_var_thresholds': '',
                                        'fcst_var_options': '',
                                        'obs_var_name': 'HGT',
                                        'obs_var_levels': [
                                            'P1000', 'P700', 'P500', 'P250'
                                        ],
                                        'obs_var_thresholds': '',
                                        'obs_var_options': '',
                                        'plot_group':'sfc_upper'},
                        'HGT_WV1_4-9': {'fcst_var_name': 'HGT',
                                        'fcst_var_levels': [
                                            'P1000', 'P700', 'P500', 'P250'
                                        ],
                                        'fcst_var_thresholds': '',
                                        'fcst_var_options': '',
                                        'obs_var_name': 'HGT',
                                        'obs_var_levels': [
                                            'P1000', 'P700', 'P500', 'P250'
                                        ],
                                        'obs_var_thresholds': '',
                                        'obs_var_options': '',
                                        'plot_group':'sfc_upper'},
                        'HGT_WV1_10-20': {'fcst_var_name': 'HGT',
                                          'fcst_var_levels': [
                                              'P1000', 'P700', 'P500', 'P250'
                                          ],
                                          'fcst_var_thresholds': '',
                                          'fcst_var_options': '',
                                          'obs_var_name': 'HGT',
                                          'obs_var_levels': [
                                              'P1000', 'P700', 'P500', 'P250'
                                          ],
                                          'obs_var_thresholds': '',
                                          'obs_var_options': '',
                                          'plot_group':'sfc_upper'},
                        'TMP': {'fcst_var_name': 'TMP',
                                'fcst_var_levels': ['P850', 'P500', 'P250'],
                                'fcst_var_thresholds': '',
                                'fcst_var_options': '',
                                'obs_var_name': 'TMP',
                                'obs_var_levels': ['P850', 'P500', 'P250'],
                                'obs_var_thresholds': '',
                                'obs_var_options': '',
                                'plot_group':'sfc_upper'},
                        'UGRD': {'fcst_var_name': 'UGRD',
                                 'fcst_var_levels': ['P850', 'P500', 'P250'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'UGRD',
                                 'obs_var_levels': ['P850', 'P500', 'P250'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'VGRD': {'fcst_var_name': 'VGRD',
                                 'fcst_var_levels': ['P850', 'P500', 'P250'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'VGRD',
                                 'obs_var_levels': ['P850', 'P500', 'P250'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'PRMSL': {'fcst_var_name': 'PRMSL',
                                  'fcst_var_levels': ['Z0'],
                                  'fcst_var_thresholds': '',
                                  'fcst_var_options': '',
                                  'obs_var_name': 'PRMSL',
                                  'obs_var_levels': ['Z0'],
                                  'obs_var_thresholds': '',
                                  'obs_var_options': '',
                                  'plot_group':'sfc_upper'}
                    }
                },
                'VAL1L2': {
                    'plot_stats_list': 'acc',
                    'interp': 'NEAREST',
                    'vx_mask_list' : ['NHX', 'SHX', 'PNA', 'TRO'],
                    'var_dict': {
                        'UGRD_VGRD': {'fcst_var_name': 'UGRD_VGRD',
                                      'fcst_var_levels': [
                                          'P850', 'P500', 'P250'
                                      ],
                                      'fcst_var_thresholds': '',
                                      'fcst_var_options': '',
                                      'obs_var_name': 'UGRD_VGRD',
                                      'obs_var_levels': [
                                          'P850', 'P500', 'P250'
                                      ],
                                      'obs_var_thresholds': '',
                                      'obs_var_options': '',
                                      'plot_group':'sfc_upper'}
                    }
                }
            },
            'grid2grid_pres': {
                'SL1L2': {
                    'plot_stats_list': ('bias, rmse, msess, rsd, rmse_md,'
                                        + ' rmse_pv'),
                    'interp': 'NEAREST',
                    'vx_mask_list' : ['NHX', 'SHX', 'PNA', 'TRO'],
                    'var_dict': {
                        'HGT': {'fcst_var_name': 'HGT',
                                'fcst_var_levels': [
                                    'P1000', 'P850', 'P700', 'P500', 'P200', 
                                    'P100', 'P50', 'P20', 'P10', 'P5', 'P1'
                                ],
                                'fcst_var_thresholds': '',
                                'fcst_var_options': '',
                                'obs_var_name': 'HGT',
                                'obs_var_levels': [
                                    'P1000', 'P850', 'P700', 'P500', 'P200', 
                                    'P100', 'P50', 'P20', 'P10', 'P5', 'P1'
                                ],
                                'obs_var_thresholds': '',
                                'obs_var_options': '',
                                'plot_group':'sfc_upper'},
                        'TMP': {'fcst_var_name': 'TMP',
                                'fcst_var_levels': [
                                    'P1000', 'P850', 'P700', 'P500', 'P200', 
                                    'P100', 'P50', 'P20', 'P10', 'P5', 'P1'
                                ],
                                'fcst_var_thresholds': '',
                                'fcst_var_options': '',
                                'obs_var_name': 'TMP',
                                'obs_var_levels': [
                                    'P1000', 'P850', 'P700', 'P500', 'P200', 
                                    'P100', 'P50', 'P20', 'P10', 'P5', 'P1'
                                ],
                                'obs_var_thresholds': '',
                                'obs_var_options': '',
                                'plot_group':'sfc_upper'},
                        'UGRD': {'fcst_var_name': 'UGRD',
                                 'fcst_var_levels': [
                                     'P1000', 'P850', 'P700', 'P500', 'P200', 
                                     'P100', 'P50', 'P20', 'P10', 'P5', 'P1'
                                 ],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'UGRD',
                                 'obs_var_levels': [
                                     'P1000', 'P850', 'P700', 'P500', 'P200', 
                                     'P100', 'P50', 'P20', 'P10', 'P5', 'P1'
                                 ],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'VGRD': {'fcst_var_name': 'VGRD',
                                 'fcst_var_levels': [
                                     'P1000', 'P850', 'P700', 'P500', 'P200', 
                                     'P100', 'P50', 'P20', 'P10', 'P5', 'P1'
                                 ],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'VGRD',
                                 'obs_var_levels': [
                                     'P1000', 'P850', 'P700', 'P500', 'P200', 
                                     'P100', 'P50', 'P20', 'P10', 'P5', 'P1'
                                 ],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'O3MR': {'fcst_var_name': 'O3MR',
                                 'fcst_var_levels': [
                                     'P100', 'P70', 'P50', 'P30', 'P20', 
                                     'P10', 'P5', 'P1'
                                 ],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'O3MR',
                                 'obs_var_levels': [
                                     'P100', 'P70', 'P50', 'P30', 'P20', 
                                     'P10', 'P5', 'P1'
                                 ],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'}
                    }
                },
                'VL1L2': {
                    'plot_stats_list': ('bias, rmse, msess, rsd, rmse_md,'
                                        + ' rmse_pv'),
                    'interp': 'NEAREST',
                    'vx_mask_list' : ['NHX', 'SHX', 'PNA', 'TRO'],
                    'var_dict': {
                        'UGRD_VGRD': {'fcst_var_name': 'UGRD_VGRD',
                                      'fcst_var_levels': [
                                          'P1000', 'P850', 'P700', 'P500', 
                                          'P200', 'P100', 'P50', 'P20', 'P10', 
                                          'P5', 'P1'
                                      ],
                                      'fcst_var_thresholds': '',
                                      'fcst_var_options': '',
                                      'obs_var_name': 'UGRD_VGRD',
                                      'obs_var_levels': [
                                          'P1000', 'P850', 'P700', 'P500', 
                                          'P200', 'P100', 'P50', 'P20', 'P10', 
                                          'P5', 'P1'
                                      ],
                                      'obs_var_thresholds': '',
                                      'obs_var_options': '',
                                      'plot_group':'sfc_upper'}
                    }
                }
            },
            'grid2grid_sfc': {
                'SL1L2': {
                    'plot_stats_list': 'fbar',
                    'interp': 'NEAREST',
                    'vx_mask_list' : [
                        'NHX', 'SHX', 'N60', 'S60', 'TRO', 'NPO', 'SPO', 
                        'NAO', 'SAO', 'G130', 'CONUS'
                    ],
                    'var_dict': {
                        'TMP2m': {'fcst_var_name': 'TMP',
                                  'fcst_var_levels': ['Z2'],
                                  'fcst_var_thresholds': '',
                                  'fcst_var_options': '',
                                  'obs_var_name': 'TMP',
                                  'obs_var_levels': ['Z2'],
                                  'obs_var_thresholds': '',
                                  'obs_var_options': '',
                                  'plot_group':'sfc_upper'},
                        'TMPsfc': {'fcst_var_name': 'TMP',
                                   'fcst_var_levels': ['Z0'],
                                   'fcst_var_thresholds': '',
                                   'fcst_var_options': '',
                                   'obs_var_name': 'TMP',
                                   'obs_var_levels': ['Z0'],
                                   'obs_var_thresholds': '',
                                   'obs_var_options': '',
                                   'plot_group':'sfc_upper'},
                        'TMPtrops': {'fcst_var_name': 'TMP',
                                     'fcst_var_levels': ['L0'],
                                     'fcst_var_thresholds': '',
                                     'fcst_var_options': 'GRIB_lvl_typ = 7;',
                                     'obs_var_name': 'TMP',
                                     'obs_var_levels': ['L0'],
                                     'obs_var_thresholds': '',
                                     'obs_var_options': 'GRIB_lvl_typ = 7;',
                                     'plot_group':'sfc_upper'},
                        'RH2m': {'fcst_var_name': 'RH',
                                 'fcst_var_levels': ['Z2'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'RH',
                                 'obs_var_levels': ['Z2'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'SPFH2m': {'fcst_var_name': 'SPFH',
                                   'fcst_var_levels': ['Z2'],
                                   'fcst_var_thresholds': '',
                                   'fcst_var_options': '',
                                   'obs_var_name': 'SPFH',
                                   'obs_var_levels': ['Z2'],
                                   'obs_var_thresholds': '',
                                   'obs_var_options': '',
                                   'plot_group':'sfc_upper'},
                        'HPBL': {'fcst_var_name': 'HPBL',
                                 'fcst_var_levels': ['L0'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'HPBL',
                                 'obs_var_levels': ['L0'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'PRESsfc': {'fcst_var_name': 'PRES',
                                    'fcst_var_levels': ['Z0'],
                                    'fcst_var_thresholds': '',
                                    'fcst_var_options': '',
                                    'obs_var_name': 'PRES',
                                    'obs_var_levels': ['Z0'],
                                    'obs_var_thresholds': '',
                                    'obs_var_options': '',
                                    'plot_group':'sfc_upper'},
                        'PREStrops': {'fcst_var_name': 'PRES',
                                      'fcst_var_levels': ['L0'],
                                      'fcst_var_thresholds': '',
                                      'fcst_var_options': 'GRIB_lvl_typ = 7;',
                                      'obs_var_name': 'PRES',
                                      'obs_var_levels': ['L0'],
                                      'obs_var_thresholds': '',
                                      'obs_var_options': 'GRIB_lvl_typ = 7;',
                                      'plot_group':'sfc_upper'},
                        'PRMSL': {'fcst_var_name': 'PRMSL',
                                  'fcst_var_levels': ['Z0'],
                                  'fcst_var_thresholds': '',
                                  'fcst_var_options': '',
                                  'obs_var_name': 'PRMSL',
                                  'obs_var_levels': ['Z0'],
                                  'obs_var_thresholds': '',
                                  'obs_var_options': '',
                                  'plot_group':'sfc_upper'},
                        'UGRD10m': {'fcst_var_name': 'UGRD',
                                    'fcst_var_levels': ['Z10'],
                                    'fcst_var_thresholds': '',
                                    'fcst_var_options': '',
                                    'obs_var_name': 'UGRD',
                                    'obs_var_levels': ['Z10'],
                                    'obs_var_thresholds': '',
                                    'obs_var_options': '',
                                    'plot_group':'sfc_upper'},
                        'VGRD10m': {'fcst_var_name': 'VGRD',
                                    'fcst_var_levels': ['Z10'],
                                    'fcst_var_thresholds': '',
                                    'fcst_var_options': '',
                                    'obs_var_name': 'VGRD',
                                    'obs_var_levels': ['Z10'],
                                    'obs_var_thresholds': '',
                                    'obs_var_options': '',
                                    'plot_group':'sfc_upper'},
                        'TSOILtop': {'fcst_var_name': 'TSOIL',
                                     'fcst_var_levels': ['Z10-0'],
                                     'fcst_var_thresholds': '',
                                     'fcst_var_options': '',
                                     'obs_var_name': 'TSOIL',
                                     'obs_var_levels': ['Z10-0'],
                                     'obs_var_thresholds': '',
                                     'obs_var_options': '',
                                     'plot_group':'sfc_upper'},
                        'SOILWtop': {'fcst_var_name': 'SOILW',
                                     'fcst_var_levels': ['Z10-0'],
                                     'fcst_var_thresholds': '',
                                     'fcst_var_options': '',
                                     'obs_var_name': 'SOILW',
                                     'obs_var_levels': ['Z10-0'],
                                     'obs_var_thresholds': '',
                                     'obs_var_options': '',
                                     'plot_group':'sfc_upper'},
                        'WEASD': {'fcst_var_name': 'WEASD',
                                  'fcst_var_levels': ['Z0'],
                                  'fcst_var_thresholds': '',
                                  'fcst_var_options': '',
                                  'obs_var_name': 'WEASD',
                                  'obs_var_levels': ['Z0'],
                                  'obs_var_thresholds': '',
                                  'obs_var_options': '',
                                  'plot_group':'precip'},
                        'CAPE': {'fcst_var_name': 'CAPE',
                                 'fcst_var_levels': ['Z0'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'CAPE',
                                 'obs_var_levels': ['Z0'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'cape'},
                        'PWAT': {'fcst_var_name': 'PWAT',
                                 'fcst_var_levels': ['L0'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'PWAT',
                                 'obs_var_levels': ['L0'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'CWAT': {'fcst_var_name': 'CWAT',
                                 'fcst_var_levels': ['L0'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'CWAT',
                                 'obs_var_levels': ['L0'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'HGTtrops': {'fcst_var_name': 'HGT',
                                     'fcst_var_levels': ['L0'],
                                     'fcst_var_thresholds': '',
                                     'fcst_var_options': 'GRIB_lvl_typ = 7;',
                                     'obs_var_name': 'HGT',
                                     'obs_var_levels': ['L0'],
                                     'obs_var_thresholds': '',
                                     'obs_var_options': 'GRIB_lvl_typ = 7;',
                                     'plot_group':'sfc_upper'},
                        'TOZNEclm': {'fcst_var_name': 'TOZNE',
                                     'fcst_var_levels': ['L0'],
                                     'fcst_var_thresholds': '',
                                     'fcst_var_options': '',
                                     'obs_var_name': 'TOZNE',
                                     'obs_var_levels': ['L0'],
                                     'obs_var_thresholds': '',
                                     'obs_var_options': '',
                                     'plot_group':'sfc_upper'}
                    }
                }
            },
            'grid2grid_mrms':{
                'CTC': {
                    'plot_stats_list': ('fss, csi, fbias, pod, faratio,'
                                        + ' sratio'),
                    'interp': 'NEAREST, NBRHD_CIRCLE, BILIN',
                    'vx_mask_list' : [
                        'CONUS', 'G130', 'APL', 'GMC', 'GRB', 'LMV', 'MDW', 'NEC', 
                        'NMT', 'NPL', 'NWC', 'SEC', 'SMT', 'SPL', 'SWC', 
                        'SWD', 'DAY1_1200_TSTM', 'DAY2_1730_TSTM'
                    ],
                    'var_dict': {
                        'REFC': {'fcst_var_name': 'REFC',
                                 'fcst_var_levels': ['L0'],
                                 'fcst_var_thresholds': ('>=20, >=30, >=40,'
                                                         + ' >=50'),
                                 'fcst_var_options': '',
                                 'obs_var_name': ('MergedReflectivityQC'
                                                  + 'Composite'),
                                 'obs_var_levels': ['Z500'],
                                 'obs_var_thresholds': ('>=20, >=30, >=40,'
                                                        + ' >=50'),
                                 'obs_var_options': '',
                                 'plot_group':'radar'},
                        'RETOP': {'fcst_var_name': 'RETOP',
                                 'fcst_var_levels': ['L0','Z1000'],
                                 'fcst_var_thresholds': ('>=20, >=30, >=40,'
                                                         + ' >=50'),
                                 'fcst_var_options': '',
                                 'obs_var_name': 'EchoTop18',
                                 'obs_var_levels': ['L0','Z500'],
                                 'obs_var_thresholds': ('>=20, >=30, >=40,'
                                                        + ' >=50'),
                                 'obs_var_options': '',
                                 'plot_group':'radar'},
                        'REFD': {'fcst_var_name': 'REFD',
                                 'fcst_var_levels': ['L0','Z1000'],
                                 'fcst_var_thresholds': ('>=20, >=30, >=40,'
                                                         + ' >=50'),
                                 'fcst_var_options': '',
                                 'obs_var_name': 'SeamlessHSR',
                                 'obs_var_levels': ['L0','Z500'],
                                 'obs_var_thresholds': ('>=20, >=30, >=40,'
                                                        + ' >=50'),
                                 'obs_var_options': '',
                                 'plot_group':'radar'}
                    }
                }
            },
            'radar_mrms':{
                'CTC': {
                    'plot_stats_list': ('fss, csi, fbias, pod, faratio,'
                                        + ' sratio'),
                    'interp': 'NEAREST, NBRHD_CIRCLE, BILIN',
                    'vx_mask_list' : [
                        'CONUS', 'G130', 'APL', 'GMC', 'GRB', 'LMV', 'MDW', 'NEC', 
                        'NMT', 'NPL', 'NWC', 'SEC', 'SMT', 'SPL', 'SWC', 
                        'SWD', 'DAY1_1200_TSTM', 'DAY2_1730_TSTM'
                    ],
                    'var_dict': {
                        'REFC': {'fcst_var_name': 'REFC',
                                 'fcst_var_levels': ['L0'],
                                 'fcst_var_thresholds': ('>=20, >=30, >=40,'
                                                         + ' >=50'),
                                 'fcst_var_options': '',
                                 'obs_var_name': ('MergedReflectivityQC'
                                                  + 'Composite'),
                                 'obs_var_levels': ['Z500'],
                                 'obs_var_thresholds': ('>=20, >=30, >=40,'
                                                        + ' >=50'),
                                 'obs_var_options': '',
                                 'plot_group':'radar'},
                        'RETOP': {'fcst_var_name': 'RETOP',
                                 'fcst_var_levels': ['L0','Z1000'],
                                 'fcst_var_thresholds': ('>=20, >=30, >=40,'
                                                         + ' >=50'),
                                 'fcst_var_options': '',
                                 'obs_var_name': 'EchoTop18',
                                 'obs_var_levels': ['L0','Z500'],
                                 'obs_var_thresholds': ('>=20, >=30, >=40,'
                                                        + ' >=50'),
                                 'obs_var_options': '',
                                 'plot_group':'radar'},
                        'REFD': {'fcst_var_name': 'REFD',
                                 'fcst_var_levels': ['L0','Z1000'],
                                 'fcst_var_thresholds': ('>=20, >=30, >=40,'
                                                         + ' >=50'),
                                 'fcst_var_options': '',
                                 'obs_var_name': 'SeamlessHSR',
                                 'obs_var_levels': ['L0','Z500'],
                                 'obs_var_thresholds': ('>=20, >=30, >=40,'
                                                        + ' >=50'),
                                 'obs_var_options': '',
                                 'plot_group':'radar'}
                    }
                }
            },
            'grid2obs_upper_air': {
                'SL1L2': {
                    'plot_stats_list': ('bias, rmse, bcrmse, fbar_obar, fbar,'
                                        + ' obar'),
                    'interp': 'NEAREST, BILIN',
                    'vx_mask_list' : [
                        'CONUS', 'G130', 'NH', 'SH', 'TRO', 'G236', 'POLAR', 'ARCTIC', 
                        'NAK', 'SAK'
                    ],
                    'var_dict': {
                        'TMP': {'fcst_var_name': 'TMP',
                                'fcst_var_levels': ['P1000', 'P925', 'P850',
                                                    'P700', 'P500', 'P400',
                                                    'P300', 'P250', 'P200',
                                                    'P150', 'P100', 'P50',
                                                    'P10', 'P5', 'P1'],
                                'fcst_var_thresholds': '',
                                'fcst_var_options': '',
                                'obs_var_name': 'TMP',
                                'obs_var_levels': ['P1000', 'P925', 'P850',
                                                   'P700', 'P500', 'P400',
                                                   'P300', 'P250', 'P200',
                                                   'P150', 'P100', 'P50',
                                                   'P10', 'P5', 'P1'],
                                'obs_var_thresholds': '',
                                'obs_var_options': '',
                                'plot_group':'sfc_upper'},
                        'RH': {'fcst_var_name': 'RH',
                               'fcst_var_levels': ['P1000', 'P925', 'P850',
                                                   'P700', 'P500', 'P400',
                                                   'P300', 'P250', 'P200',
                                                   'P150', 'P100', 'P50',
                                                   'P10', 'P5', 'P1'],
                               'fcst_var_thresholds': '',
                               'fcst_var_options': '',
                               'obs_var_name': 'RH',
                               'obs_var_levels': ['P1000', 'P925', 'P850',
                                                  'P700', 'P500', 'P400',
                                                  'P300', 'P250', 'P200',
                                                  'P150', 'P100', 'P50',
                                                  'P10', 'P5', 'P1'],
                               'obs_var_thresholds': '',
                               'obs_var_options': '',
                               'plot_group':'sfc_upper'},
                        'SPFH': {'fcst_var_name': 'SPFH',
                                 'fcst_var_levels': ['P1000', 'P925', 'P850',
                                                     'P700', 'P500', 'P400',
                                                     'P300', 'P250', 'P200',
                                                     'P150', 'P100', 'P50',
                                                     'P10', 'P5', 'P1'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'SPFH',
                                 'obs_var_levels': ['P1000', 'P925', 'P850',
                                                    'P700', 'P500', 'P400',
                                                    'P300', 'P250', 'P200',
                                                    'P150', 'P100', 'P50',
                                                    'P10', 'P5', 'P1'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'HGT': {'fcst_var_name': 'HGT',
                                'fcst_var_levels': ['P1000', 'P925', 'P850',
                                                    'P700', 'P500', 'P400',
                                                    'P300', 'P250', 'P200',
                                                    'P150', 'P100', 'P50',
                                                    'P10', 'P5', 'P1'],
                                'fcst_var_thresholds': '',
                                'fcst_var_options': '',
                                'obs_var_name': 'HGT',
                                'obs_var_levels': ['P1000', 'P925', 'P850',
                                                   'P700', 'P500', 'P400',
                                                   'P300', 'P250', 'P200',
                                                   'P150', 'P100', 'P50',
                                                   'P10', 'P5', 'P1'],
                                'obs_var_thresholds': '',
                                'obs_var_options': '',
                                'plot_group':'sfc_upper'},
                    }
                },
                'VL1L2': {
                    'plot_stats_list': ('bias, rmse, bcrmse, fbar_obar, fbar,'
                                        + ' obar'),
                    'interp': 'NEAREST, BILIN',
                    'vx_mask_list' : [
                        'CONUS', 'G130', 'NH', 'SH', 'TRO', 'G236', 'POLAR', 'ARCTIC', 
                        'NAK', 'SAK'
                    ],
                    'var_dict': {
                        'UGRD_VGRD': {'fcst_var_name': 'UGRD_VGRD',
                                      'fcst_var_levels': [
                                          'P1000', 'P925', 'P850', 'P700', 
                                          'P500', 'P400','P300', 'P250', 
                                          'P200', 'P150', 'P100', 'P50', 
                                          'P10', 'P5', 'P1'
                                      ],
                                      'fcst_var_thresholds': '',
                                      'fcst_var_options': '',
                                      'obs_var_name': 'UGRD_VGRD',
                                      'obs_var_levels': [
                                          'P1000', 'P925', 'P850', 'P700', 
                                          'P500', 'P400', 'P300', 'P250', 
                                          'P200', 'P150', 'P100', 'P50', 
                                          'P10', 'P5', 'P1'
                                      ],
                                      'obs_var_thresholds': '',
                                      'obs_var_options': '',
                                      'plot_group':'sfc_upper'}
                    }
                }
            },
            'grid2obs_conus_sfc': {
                'SL1L2': {
                    'plot_stats_list': ('bias, rmse, bcrmse, fbar_obar, fbar,'
                                        + ' obar'),
                    'interp': 'NEAREST, BILIN',
                    'vx_mask_list' : [
                        'CONUS', 'G130', 'G214', 'WEST', 'EAST', 'MDW', 'NPL', 'SPL', 'NEC', 
                        'SEC', 'NWC', 'SWC', 'NMT', 'SMT', 'SWD', 'GRB', 
                        'LMV', 'GMC', 'APL', 'NAK', 'SAK'
                    ],
                    'var_dict': {
                        'TMP2m': {'fcst_var_name': 'TMP',
                                  'fcst_var_levels': ['Z2'],
                                  'fcst_var_thresholds': '',
                                  'fcst_var_options': '',
                                  'obs_var_name': 'TMP',
                                  'obs_var_levels': ['Z2'],
                                  'obs_var_thresholds': '',
                                  'obs_var_options': '',
                                  'plot_group':'sfc_upper'},
                        'RH2m': {'fcst_var_name': 'RH',
                                 'fcst_var_levels': ['Z2'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'RH',
                                 'obs_var_levels': ['Z2'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'DPT2m': {'fcst_var_name': 'DPT',
                                  'fcst_var_levels': ['Z2'],
                                  'fcst_var_thresholds': '',
                                  'fcst_var_options': '',
                                  'obs_var_name': 'DPT',
                                  'obs_var_levels': ['Z2'],
                                  'obs_var_thresholds': '',
                                  'obs_var_options': '',
                                  'plot_group':'sfc_upper'},
                        'TCDC': {'fcst_var_name': 'TCDC',
                                 'fcst_var_levels': ['L0'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': 'GRIB_lvl_typ = 200;',
                                 'obs_var_name': 'TCDC',
                                 'obs_var_levels': ['L0'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'PRMSL': {'fcst_var_name': 'PRMSL',
                                  'fcst_var_levels': ['Z0'],
                                  'fcst_var_thresholds': '',
                                  'fcst_var_options': '',
                                  'obs_var_name': 'PRMSL',
                                  'obs_var_levels': ['Z0'],
                                  'obs_var_thresholds': '',
                                  'obs_var_options': '',
                                  'plot_group':'sfc_upper'},
                        'VISsfc': {'fcst_var_name': 'VIS',
                                   'fcst_var_levels': ['L0'],
                                   'fcst_var_thresholds': '',
                                   'fcst_var_options': '',
                                   'obs_var_name': 'VIS',
                                   'obs_var_levels': ['L0'],
                                   'obs_var_thresholds': '',
                                   'obs_var_options': '',
                                   'plot_group':'ceil_vis'},
                        'HGTcldceil': {'fcst_var_name': 'HGT',
                                       'fcst_var_levels': ['L0'],
                                       'fcst_var_thresholds': '',
                                       'fcst_var_options': ('GRIB_lvl_typ ='
                                                            + ' 215;'),
                                       'obs_var_name': 'CEILING',
                                       'obs_var_levels': ['L0'],
                                       'obs_var_thresholds': '',
                                       'obs_var_options': '',
                                       'plot_group':'ceil_vis'},
                        'CAPEsfc': {'fcst_var_name': 'CAPE',
                                    'fcst_var_levels': ['L0'],
                                    'fcst_var_thresholds': '',
                                    'fcst_var_options': '',
                                    'obs_var_name': 'CAPE',
                                    'obs_var_levels': ['L100000-0'],
                                    'obs_var_thresholds': '',
                                    'obs_var_options': '',
                                    'plot_group':'cape'},
                        'GUSTsfc': {'fcst_var_name': 'GUST',
                                    'fcst_var_levels': ['Z0'],
                                    'fcst_var_thresholds': '',
                                    'fcst_var_options': '',
                                    'obs_var_name': 'GUST',
                                    'obs_var_levels': ['Z0'],
                                    'obs_var_thresholds': '',
                                    'obs_var_options': '',
                                    'plot_group':'sfc_upper'},
                        'HPBL': {'fcst_var_name': 'HPBL',
                                 'fcst_var_levels': ['L0'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'HPBL',
                                 'obs_var_levels': ['L0'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'},
                        'UGRD10m': {'fcst_var_name': 'UGRD',
                                    'fcst_var_levels': ['Z10'],
                                    'fcst_var_thresholds': '',
                                    'fcst_var_options': '',
                                    'obs_var_name': 'UGRD',
                                    'obs_var_levels': ['Z10'],
                                    'obs_var_thresholds': '',
                                    'obs_var_options': '',
                                    'plot_group':'sfc_upper'},
                        'VGRD10m': {'fcst_var_name': 'VGRD',
                                    'fcst_var_levels': ['Z10'],
                                    'fcst_var_thresholds': '',
                                    'fcst_var_options': '',
                                    'obs_var_name': 'VGRD',
                                    'obs_var_levels': ['Z10'],
                                    'obs_var_thresholds': '',
                                    'obs_var_options': '',
                                    'plot_group':'sfc_upper'},
                    }
                },
                'VL1L2': {
                    'plot_stats_list': ('bias, rmse, bcrmse, fbar_obar, fbar,'
                                        + ' obar'),
                    'interp': 'NEAREST, BILIN',
                    'vx_mask_list' : [
                        'CONUS', 'G130', 'G214', 'WEST', 'EAST', 'MDW', 'NPL', 'SPL', 'NEC', 
                        'SEC', 'NWC', 'SWC', 'NMT', 'SMT', 'SWD', 'GRB', 
                        'LMV', 'GMC', 'APL', 'NAK', 'SAK'
                    ],
                    'var_dict': {
                        'UGRD_VGRD10m': {'fcst_var_name': 'UGRD_VGRD',
                                         'fcst_var_levels': ['Z10'],
                                         'fcst_var_thresholds': '',
                                         'fcst_var_options': '',
                                         'obs_var_name': 'UGRD_VGRD',
                                         'obs_var_levels': ['Z10'],
                                         'obs_var_thresholds': '',
                                         'obs_var_options': '',
                                         'plot_group':'sfc_upper'},
                    }
                },
                'CTC': {
                    'plot_stats_list': ('csi, fbias, fss, fbar, obar, pod,'
                                        + ' faratio, sratio'),
                    'interp': 'NEAREST, BILIN',
                    'vx_mask_list' : [
                        'CONUS', 'G130', 'G214', 'WEST', 'EAST', 'MDW', 'NPL', 'SPL', 'NEC', 
                        'SEC', 'NWC', 'SWC', 'NMT', 'SMT', 'SWD', 'GRB', 
                        'LMV', 'GMC', 'APL', 'NAK', 'SAK'
                    ],
                    'var_dict': {
                        'VISsfc': {'fcst_var_name': 'VIS',
                                   'fcst_var_levels': ['L0'],
                                   'fcst_var_thresholds': ('<=800, <805, <=1600, <1609,'
                                                           + ' <=4800, <4828, <=8000, <8045,'
                                                           + ' >=8045,'
                                                           + ' <=16000, <16090'),
                                   'fcst_var_options': '',
                                   'obs_var_name': 'VIS',
                                   'obs_var_levels': ['L0'],
                                   'obs_var_thresholds': ('<=800, <805, <=1600, <1609,'
                                                          + ' <=4800, <4828, <=8000, <8045,'
                                                          + ' >=8045,'
                                                          + ' <=16000, <16090'),
                                   'obs_var_options': '',
                                   'plot_group':'ceil_vis'},
                        'HGTcldceil': {'fcst_var_name': 'HGT',
                                       'fcst_var_levels': ['L0'],
                                       'fcst_var_thresholds': ('<152, <=152, <305,'
                                                               + ' <=305, <914,'
                                                               + ' >=914, <=916,'
                                                               + ' <1520, <=1524, '
                                                               + ' <3040, <=3048'),
                                       'fcst_var_options': ('GRIB_lvl_typ ='
                                                            + ' 215;'),
                                       'obs_var_name': 'CEILING',
                                       'obs_var_levels': ['L0'],
                                       'obs_var_thresholds': ('<152, <=152, <305,'
                                                              + ' <=305, <914, '
                                                              + '>=914, <=916, '
                                                              + '<1520, <=1524, '
                                                              + '<3040, <=3048'),
                                       'obs_var_options': '',
                                       'plot_group':'ceil_vis'},
                        'CAPEsfc': {'fcst_var_name': 'CAPE',
                                    'fcst_var_levels': ['L0'],
                                    'fcst_var_thresholds': ('>500, >1000,'
                                                            + ' >1500, >2000,'
                                                            + ' >3000,'
                                                            + ' >4000'),
                                    'fcst_var_options': '',
                                    'obs_var_name': 'CAPE',
                                    'obs_var_levels': ['L100000-0'],
                                    'obs_var_thresholds': ('>500, >1000,'
                                                           + ' >1500, >2000,'
                                                           + ' >3000,'
                                                           + ' >4000'),
                                    'obs_var_options': '',
                                    'plot_group':'cape'},
                    }
                }
            },
            'grid2obs_aq': {
                'CTC': {
                    'plot_stats_list': ('csi, fbias, fss, fbar, obar, pod,'
                                        + ' faratio, sratio'),
                    'interp': 'BILIN',
                    'vx_mask_list' : [
                        'CONUS', 'G130', 'G214', 'WEST', 'EAST', 'MDW', 'NPL', 'SPL', 'NEC', 
                        'SEC', 'NWC', 'SWC', 'NMT', 'SMT', 'SWD', 'GRB', 
                        'LMV', 'GMC', 'APL', 'NAK', 'SAK'
                    ],
                    'var_dict': {
                        'OZCON1': {'fcst_var_name': 'OZCON1',
                                  'fcst_var_levels': ['A1'],
                                  'fcst_var_thresholds': ('>50, >60, >65, >70,'
                                                          + '>75, >85, >105,'
                                                          + '>125, >150'),
                                  'fcst_var_options': '',
                                  'obs_var_name': 'COPO',
                                  'obs_var_levels': ['A1'],
                                  'obs_var_thresholds': ('>50, >60, >65, >70,'
                                                         + '>75, >85, >105,'
                                                         + '>125, >150'),
                                  'obs_var_options': '',
                                  'plot_group':'aq'},
                        'OZCON2': {'fcst_var_name': 'OZCON2',
                                  'fcst_var_levels': ['A2'],
                                  'fcst_var_thresholds': ('>50, >60, >65, >70,'
                                                          + '>75, >85, >105,'
                                                          + '>125, >150'),
                                  'fcst_var_options': '',
                                  'obs_var_name': 'COPO',
                                  'obs_var_levels': ['A2'],
                                  'obs_var_thresholds': ('>50, >60, >65, >70,'
                                                         + '>75, >85, >105,'
                                                         + '>125, >150'),
                                  'obs_var_options': '',
                                  'plot_group':'aq'},
                        'OZCON3': {'fcst_var_name': 'OZCON3',
                                  'fcst_var_levels': ['A3'],
                                  'fcst_var_thresholds': ('>50, >60, >65, >70,'
                                                          + '>75, >85, >105,'
                                                          + '>125, >150'),
                                  'fcst_var_options': '',
                                  'obs_var_name': 'COPO',
                                  'obs_var_levels': ['A3'],
                                  'obs_var_thresholds': ('>50, >60, >65, >70,'
                                                         + '>75, >85, >105,'
                                                         + '>125, >150'),
                                  'obs_var_options': '',
                                  'plot_group':'aq'},
                        'OZCON4': {'fcst_var_name': 'OZCON4',
                                  'fcst_var_levels': ['A4'],
                                  'fcst_var_thresholds': ('>50, >60, >65, >70,'
                                                          + '>75, >85, >105,'
                                                          + '>125, >150'),
                                  'fcst_var_options': '',
                                  'obs_var_name': 'COPO',
                                  'obs_var_levels': ['A4'],
                                  'obs_var_thresholds': ('>50, >60, >65, >70,'
                                                         + '>75, >85, >105,'
                                                         + '>125, >150'),
                                  'obs_var_options': '',
                                  'plot_group':'aq'},
                        'OZCON5': {'fcst_var_name': 'OZCON5',
                                  'fcst_var_levels': ['A5'],
                                  'fcst_var_thresholds': ('>50, >60, >65, >70,'
                                                          + '>75, >85, >105,'
                                                          + '>125, >150'),
                                  'fcst_var_options': '',
                                  'obs_var_name': 'COPO',
                                  'obs_var_levels': ['A5'],
                                  'obs_var_thresholds': ('>50, >60, >65, >70,'
                                                         + '>75, >85, >105,'
                                                         + '>125, >150'),
                                  'obs_var_options': '',
                                  'plot_group':'aq'},
                        'OZCON6': {'fcst_var_name': 'OZCON6',
                                  'fcst_var_levels': ['A6'],
                                  'fcst_var_thresholds': ('>50, >60, >65, >70,'
                                                          + '>75, >85, >105,'
                                                          + '>125, >150'),
                                  'fcst_var_options': '',
                                  'obs_var_name': 'COPO',
                                  'obs_var_levels': ['A6'],
                                  'obs_var_thresholds': ('>50, >60, >65, >70,'
                                                         + '>75, >85, >105,'
                                                         + '>125, >150'),
                                  'obs_var_options': '',
                                  'plot_group':'aq'},
                        'OZCON7': {'fcst_var_name': 'OZCON7',
                                  'fcst_var_levels': ['A7'],
                                  'fcst_var_thresholds': ('>50, >60, >65, >70,'
                                                          + '>75, >85, >105,'
                                                          + '>125, >150'),
                                  'fcst_var_options': '',
                                  'obs_var_name': 'COPO',
                                  'obs_var_levels': ['A7'],
                                  'obs_var_thresholds': ('>50, >60, >65, >70,'
                                                         + '>75, >85, >105,'
                                                         + '>125, >150'),
                                  'obs_var_options': '',
                                  'plot_group':'aq'},
                        'OZCON8': {'fcst_var_name': 'OZCON8',
                                  'fcst_var_levels': ['A8'],
                                  'fcst_var_thresholds': ('>50, >60, >65, >70,'
                                                          + '>75, >85, >105,'
                                                          + '>125, >150'),
                                  'fcst_var_options': '',
                                  'obs_var_name': 'COPO',
                                  'obs_var_levels': ['A8'],
                                  'obs_var_thresholds': ('>50, >60, >65, >70,'
                                                         + '>75, >85, >105,'
                                                         + '>125, >150'),
                                  'obs_var_options': '',
                                  'plot_group':'aq'},
                    }
                }
            },
            'grid2obs_polar_sfc': {
                'SL1L2': {
                    'plot_stats_list': 'bias, rmse, fbar_obar',
                    'interp': 'NEAREST',
                    'vx_mask_list' : ['ARCTIC'],
                    'var_dict': {
                        'TMP2m': {'fcst_var_name': 'TMP',
                                  'fcst_var_levels': ['Z2'],
                                  'fcst_var_thresholds': '',
                                  'fcst_var_options': '',
                                  'obs_var_name': 'TMP',
                                  'obs_var_levels': ['Z2'],
                                  'obs_var_thresholds': '',
                                  'obs_var_options': '',
                                  'plot_group':'sfc_upper'},
                        'TMPsfc': {'fcst_var_name': 'TMP',
                                   'fcst_var_levels': ['Z0'],
                                   'fcst_var_thresholds': '',
                                   'fcst_var_options': '',
                                   'obs_var_name': 'TMP',
                                   'obs_var_levels': ['Z0'],
                                   'obs_var_thresholds': '',
                                   'obs_var_options': '',
                                   'plot_group':'sfc_upper'},
                        'PRESsfc': {'fcst_var_name': 'PRES',
                                    'fcst_var_levels': ['Z0'],
                                    'fcst_var_thresholds': '',
                                    'fcst_var_options': '',
                                    'obs_var_name': 'PRES',
                                    'obs_var_levels': ['Z0'],
                                    'obs_var_thresholds': '',
                                    'obs_var_options': '',
                                    'plot_group':'sfc_upper'}
                    }
                }
            },
            'precip_ccpa': {
                'CTC': {
                    'plot_stats_list': ('bias, ets, fss, csi, fbias, fbar,'
                                        + ' obar, pod, faratio, sratio'),
                    'interp': 'NEAREST',
                    'vx_mask_list' : ['CONUS', 'EAST', 'WEST'],
                    'var_dict': {
                        'APCP_01': {'fcst_var_name': 'APCP',
                                    'fcst_var_levels': ['A01','A1'],
                                    'fcst_var_thresholds': ('>=0.254, >=1.27,'
                                                            + ' >=2.54,'
                                                            + ' >=6.35,'
                                                            + ' >=12.7,'
                                                            + ' >=19.05,'
                                                            + ' >=25.4,'),
                                    'fcst_var_options': '',
                                    'obs_var_name': 'APCP',
                                    'obs_var_levels': ['A01','A1'],
                                    'obs_var_thresholds': ('>=0.254, >=1.27,'
                                                           + ' >=2.54,'
                                                           + ' >=6.35,'
                                                           + ' >=12.7,'
                                                           + ' >=19.05,'
                                                           + ' >=25.4,'),
                                    'obs_var_options': '',
                                    'plot_group':'precip'},
                        'APCP_03': {'fcst_var_name': 'APCP',
                                    'fcst_var_levels': ['A03','A3'],
                                    'fcst_var_thresholds': ('>=0.254, >=1.27,'
                                                            + ' >=2.54,'
                                                            + ' >=6.35,'
                                                            + ' >=12.7,'
                                                            + ' >=19.05,'
                                                            + ' >=25.4,'
                                                            + ' >=50.8,'),
                                    'fcst_var_options': '',
                                    'obs_var_name': 'APCP',
                                    'obs_var_levels': ['A03','A3'],
                                    'obs_var_thresholds': ('>=0.254, >=1.27,'
                                                           + ' >=2.54,'
                                                           + ' >=6.35,'
                                                           + ' >=12.7,'
                                                           + ' >=19.05,'
                                                           + ' >=25.4,'
                                                           + ' >=50.8,'),
                                    'obs_var_options': '',
                                    'plot_group':'precip'},
                        'APCP_06': {'fcst_var_name': 'APCP',
                                    'fcst_var_levels': ['A06','A6'],
                                    'fcst_var_thresholds': ('>=0.254, >=2.54,'
                                                            + ' >=6.35,'
                                                            + ' >=12.7,'
                                                            + ' >=19.05,'
                                                            + ' >=25.4,'
                                                            + ' >=38.1,'
                                                            + ' >=50.8,'
                                                            + ' >=76.2,'
                                                            + ' >=101.6'),
                                    'fcst_var_options': '',
                                    'obs_var_name': 'APCP',
                                    'obs_var_levels': ['A06','A6'],
                                    'obs_var_thresholds': ('>=0.254, >=2.54,'
                                                           + ' >=6.35,'
                                                           + ' >=12.7,'
                                                           + ' >=19.05,'
                                                           + ' >=25.4,'
                                                           + ' >=38.1,'
                                                           + ' >=50.8,'
                                                           + ' >=76.2,'
                                                           + ' >=101.6'),
                                    'obs_var_options': '',
                                    'plot_group':'precip'},
                        'APCP_24': {'fcst_var_name': 'APCP',
                                    'fcst_var_levels': ['A24'],
                                    'fcst_var_thresholds': ('>=0.254, >=2.54,'
                                                            + ' >=6.35,'
                                                            + ' >=12.7,'
                                                            + ' >=25.4,'
                                                            + ' >=38.1,'
                                                            + ' >=50.8,'
                                                            + ' >=76.2,'
                                                            + ' >=101.6'
                                                            + ' >=152.4'),
                                    'fcst_var_options': '',
                                    'obs_var_name': 'APCP',
                                    'obs_var_levels': ['A24'],
                                    'obs_var_thresholds': ('>=0.254, >=2.54,'
                                                           + ' >=6.35,'
                                                           + ' >=12.7,'
                                                           + ' >=25.4,'
                                                           + ' >=38.1,'
                                                           + ' >=50.8,'
                                                           + ' >=76.2,'
                                                           + ' >=101.6'
                                                           + ' >=152.4'),
                                    'obs_var_options': '',
                                    'plot_group':'precip'}
                    }
                }
            },
            'satellite_ghrsst_ncei_avhrr_anl': {
                'SL1L2': {
                    'plot_stats_list': 'bias, rmse',
                    'interp': 'NEAREST',
                    'vx_mask_list' : [
                        'NH', 'SH', 'POLAR', 'ARCTIC', 'SEA_ICE', 
                        'SEA_ICE_FREE', 'SEA_ICE_POLAR', 'SEA_ICE_FREE_POLAR'
                    ],
                    'var_dict': {
                        'SST': {'fcst_var_name': 'TMP_Z0_mean',
                                'fcst_var_levels': ['Z0'],
                                'fcst_var_thresholds': '',
                                'fcst_var_options': '',
                                'obs_var_name': 'analysed_sst',
                                'obs_var_levels': ['Z0'],
                                'obs_var_thresholds': '',
                                'obs_var_options': '',
                                'plot_group':'sfc_upper'},
                        'ICEC': {'fcst_var_name': 'ICEC_Z0_mean',
                                 'fcst_var_levels': ['Z0'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options':  '',
                                 'obs_var_name': 'sea_ice_fraction',
                                 'obs_var_levels': ['Z0'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'}
                    }
                }
            },
            'satellite_ghrsst_ospo_geopolar_anl': {
                'SL1L2': {
                    'plot_stats_list': 'bias, rmse',
                    'interp': 'NEAREST',
                    'vx_mask_list' : [
                        'NH', 'SH', 'POLAR', 'ARCTIC', 'SEA_ICE', 
                        'SEA_ICE_FREE', 'SEA_ICE_POLAR', 'SEA_ICE_FREE_POLAR'
                    ],
                    'var_dict': {
                        'SST': {'fcst_var_name': 'TMP_Z0_mean',
                                'fcst_var_levels': ['Z0'],
                                'fcst_var_thresholds': '',
                                'fcst_var_options': '',
                                'obs_var_name': 'analysed_sst',
                                'obs_var_levels': ['Z0'],
                                'obs_var_thresholds': '',
                                'obs_var_options': '',
                                'plot_group':'sfc_upper'},
                        'ICEC': {'fcst_var_name': 'ICEC_Z0_mean',
                                 'fcst_var_levels': ['Z0'],
                                 'fcst_var_thresholds': '',
                                 'fcst_var_options': '',
                                 'obs_var_name': 'sea_ice_fraction',
                                 'obs_var_levels': ['Z0'],
                                 'obs_var_thresholds': '',
                                 'obs_var_options': '',
                                 'plot_group':'sfc_upper'}
                    }
                }
            }
        }


