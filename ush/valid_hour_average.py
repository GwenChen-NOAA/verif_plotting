###############################################################################
#
# Name:          valid_hour_average.py
# Contact(s):    Marcel Caron
# Developed:     Nov. 22, 2021 by Marcel Caron 
# Last Modified: Apr. 06, 2022 by Marcel Caron             
# Title:         Line plot of verification metric as a function of 
#                valid or init hour
# Abstract:      Plots METplus output (e.g., BCRMSE) as a line plot, 
#                varying by valid or init hour, which represents the x-axis. 
#                Line colors and styles are unique for each model, and several
#                models can be plotted at once.
#
###############################################################################
import os
import sys
import numpy as np
import pandas as pd
import logging
from functools import reduce
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from datetime import datetime, timedelta as td

SETTINGS_DIR = os.environ['USH_DIR']
sys.path.insert(0, os.path.abspath(SETTINGS_DIR))
from settings import Toggle, Templates, Presets, ModelSpecs, Reference
from plotter import Plotter
from prune_stat_files import prune_data
import plot_util
import df_preprocessing
from check_variables import *


# ================ GLOBALS AND CONSTANTS ================

plotter = Plotter(fig_size=(28.,14.))
plotter.set_up_plots()
toggle = Toggle()
templates = Templates()
presets = Presets()
model_colors = ModelSpecs()
reference = Reference()


# =================== FUNCTIONS =========================


def plot_valid_hour_average(df: pd.DataFrame, logger: logging.Logger, 
                      date_range: tuple, model_list: list, num: int = 0, 
                      level: str = '500', flead='all', thresh: list = ['<20'], 
                      metric1_name: str = 'BCRMSE', metric2_name: str = 'ME', 
                      y_min_limit: float = -10., y_max_limit: float = 10., 
                      y_lim_lock: bool = False,
                      xlabel: str = 'Forecast Lead Hour', 
                      date_type: str = 'VALID', date_hours: list = [0,6,12,18], 
                      anti_date_hours: list = [0,3,6,9,12,15,18,21],
                      verif_type: str = 'pres', save_dir: str = '.',
                      requested_var: str = 'HGT', line_type: str = 'SL1L2',
                      dpi: int = 300, confidence_intervals: bool = False,
                      bs_nrep: int = 5000, bs_method: str = 'MATCHED_PAIRS', 
                      ci_lev: float = .95, bs_min_samp: int = 30,
                      eval_period: str = 'TEST', save_header: str = '', 
                      display_averages: bool = True, 
                      plot_group: str = 'sfc_upper'):

    logger.info("========================================")
    logger.info(f"Creating Plot {num} ...")

    if df.empty:
        logger.warning(f"Empty Dataframe. Continuing onto next plot...")
        logger.info("========================================")
        return None
    if str(line_type).upper() == 'CTC' and np.array(thresh).size == 0:
        logger.warning(f"Empty list of thresholds. Continuing onto next"
                       + f" plot...")
        logger.info("========================================")
        return None

    fig, ax = plotter.get_plots(num)  
    variable_translator = reference.variable_translator
    domain_translator = reference.domain_translator
    model_settings = model_colors.model_settings

    # filter by level
    df = df[df['FCST_LEV'].astype(str).eq(str(level))]

    if df.empty:
        logger.warning(f"Empty Dataframe. Continuing onto next plot...")
        plt.close(num)
        logger.info("========================================")
        return None

    # filter by forecast lead times
    if isinstance(flead, list):
        if len(flead) <= 8:
            if len(flead) > 1:
                frange_phrase = 's '+', '.join([str(f) for f in flead])
            else:
                frange_phrase = ' '+', '.join([str(f) for f in flead])
            frange_save_phrase = '-'.join([str(f) for f in flead])
        else:
            frange_phrase = f's {flead[0]}'+u'\u2013'+f'{flead[-1]}'
            frange_save_phrase = f'{flead[0]}_TO_F{flead[-1]}'
        frange_string = f'Forecast Hour{frange_phrase}'
        frange_save_string = f'F{frange_save_phrase}'
        df = df[df['LEAD_HOURS'].isin(flead)]
    elif isinstance(flead, tuple):
        frange_string = (f'Forecast Hours {flead[0]:02d}'
                         + u'\u2013' + f'{flead[1]:02d}')
        frange_save_string = f'F{flead[0]:02d}-F{flead[1]:02d}'
        df = df[
            (df['LEAD_HOURS'] >= flead[0]) & (df['LEAD_HOURS'] <= flead[1])
        ]
    elif isinstance(flead, np.int):
        frange_string = f'Forecast Hour {flead:02d}'
        frange_save_string = f'F{flead:02d}'
        df = df[df['LEAD_HOURS'] == flead]
    else:
        e1 = f"Invalid forecast lead: \'{flead}\'"
        e2 = f"Please check settings for forecast leads."
        logger.error(e1)
        logger.error(e2)
        raise ValueError(e1+"\n"+e2)

    if str(date_type).upper() == 'INIT':
        anti_date_type = 'VALID'
    elif str(date_type).upper() == 'VALID':
        anti_date_type = 'INIT'

    # Filter ANTI_DATE_HOURS column based on what is in anti_date_hours
    # Remove from date_hours and anti_date_hours the init and valid hours that 
    # don't exist in the dataframe.  
    df['DATE_HOURS'] = df[str(date_type).upper()].dt.hour.astype(int)
    df['ANTI_DATE_HOURS'] = df[str(anti_date_type).upper()].dt.hour.astype(int)
    df = df[df['ANTI_DATE_HOURS'].isin([int(x) for x in anti_date_hours])]
    date_hours = np.array(date_hours)[[
        int(x) in df['DATE_HOURS'].tolist() for x in date_hours
    ]]
    anti_date_hours = np.array(anti_date_hours)[[
        int(x) in df['ANTI_DATE_HOURS'].tolist() for x in anti_date_hours
    ]]

    if thresh and '' not in thresh:
        requested_thresh_symbol, requested_thresh_letter = list(
            zip(*[plot_util.format_thresh(t) for t in thresh])
        )
        symbol_found = False
        for opt in ['>=', '>', '==', '!=', '<=', '<']:
            if any(opt in t for t in requested_thresh_symbol):
                if all(opt in t for t in requested_thresh_symbol):
                    symbol_found = True
                    opt_letter = requested_thresh_letter[0][:2]
                    break
                else:
                    e = ("Threshold operands do not match among all requested"
                         + f" thresholds.")
                    logger.error(e)
                    logger.error("Quitting ...")
                    raise ValueError(e+"\nQuitting ...")
        if not symbol_found:
            e = "None of the requested thresholds contain a valid symbol."
            logger.error(e)
            logger.error("Quitting ...")
            raise ValueError(e+"\nQuitting ...")
        df_thresh_symbol, df_thresh_letter = list(
            zip(*[plot_util.format_thresh(t) for t in df['FCST_THRESH']])
        )
        df['FCST_THRESH_SYMBOL'] = df_thresh_symbol
        df['FCST_THRESH_VALUE'] = [str(item)[2:] for item in df_thresh_letter]
        requested_thresh_value = [
            str(item)[2:] for item in requested_thresh_letter
        ]
        df = df[df['FCST_THRESH_SYMBOL'].isin(requested_thresh_symbol)]
        thresholds_removed = (
            np.array(requested_thresh_symbol)[
                ~np.isin(requested_thresh_symbol, df['FCST_THRESH_SYMBOL'])
            ]
        )
        requested_thresh_symbol = (
            np.array(requested_thresh_symbol)[
                np.isin(requested_thresh_symbol, df['FCST_THRESH_SYMBOL'])
            ]
        )
        if thresholds_removed.size > 0:
            thresholds_removed_string = ', '.join(thresholds_removed)
            if len(thresholds_removed) > 1:
                warning_string = (f"{thresholds_removed_string} thresholds"
                                  + f" were not found and will not be"
                                  + f" plotted.")
            else:
                warning_string = (f"{thresholds_removed_string} threshold was"
                                  + f" not found and will not be plotted.")
            logger.warning(warning_string)
            logger.warning("Continuing ...")

    # Remove from model_list the models that don't exist in the dataframe
    cols_to_keep = [
        str(model) 
        in df['MODEL'].tolist() 
        for model in model_list
    ]
    models_removed = [
        str(m) 
        for (m, keep) in zip(model_list, cols_to_keep) if not keep
    ]
    models_removed_string = ', '.join(models_removed)
    model_list = [
        str(m) 
        for (m, keep) in zip(model_list, cols_to_keep) if keep
    ]
    if not all(cols_to_keep):
        logger.warning(
            f"{models_removed_string} data were not found and will not be"
            + f" plotted."
        )
    if df.empty:
        logger.warning(f"Empty Dataframe. Continuing onto next plot...")
        plt.close(num)
        logger.info("========================================")
        return None
    df_groups = df.groupby(['MODEL','ANTI_DATE_HOURS'])
    # Aggregate unit statistics before calculating metrics
    if str(line_type).upper() == 'CTC':
        df_aggregated = df_groups.sum()
    else:
        df_aggregated = df_groups.mean()

    # Effective "event equalization", i.e. removing datapoints that aren't 
    # shared among all models. Otherwise plot_util.calculate_stat will throw 
    # an error
    df_split = [df_aggregated.xs(str(model)) for model in model_list]
    df_reduced = reduce(
        lambda x,y: pd.merge(
            x, y, on='ANTI_DATE_HOURS', how='inner'
        ), 
        df_split
    )
    df_aggregated = df_aggregated[
        df_aggregated.index.get_level_values('ANTI_DATE_HOURS')
        .isin(df_reduced.index)
    ]

    if df_aggregated.empty:
        logger.warning(f"Empty Dataframe. Continuing onto next plot...")
        plt.close(num)
        logger.info("========================================")
        return None

    # Calculate desired metric
    metric_long_names = []
    for stat in [metric1_name, metric2_name]:
        if stat:
            stat_output = plot_util.calculate_stat(
                logger, df_aggregated, str(stat).lower()
            )
            df_aggregated[str(stat).upper()] = stat_output[0]
            metric_long_names.append(stat_output[2])
            if confidence_intervals:
                ci_output = df_groups.apply(
                    lambda x: plot_util.calculate_bootstrap_ci(
                        logger, bs_method, x, str(stat).lower(), bs_nrep,
                        ci_lev, bs_min_samp
                    )
                )
                if any(ci_output['STATUS'] == 1):
                    logger.warning(f"Failed attempt to compute bootstrap"
                                   + f" confidence intervals.  Sample size"
                                   + f" for one or more groups is too small."
                                   + f" Minimum sample size can be changed"
                                   + f" in settings.py.")
                    logger.warning(f"Confidence intervals will not be"
                                   + f" plotted.")
                    confidence_intervals = False
                    continue
                ci_output = ci_output.reset_index(level=2, drop=True)
                ci_output = (
                    ci_output
                    .reindex(df_aggregated.index)
                    #.reindex(ci_output.index)
                )
                df_aggregated[str(stat).upper()+'_BLERR'] = ci_output[
                    'CI_LOWER'
                ].values
                df_aggregated[str(stat).upper()+'_BUERR'] = ci_output[
                    'CI_UPPER'
                ].values

    df_aggregated[str(metric1_name).upper()] = (
        df_aggregated[str(metric1_name).upper()]
    ).astype(float).tolist()
    if metric2_name is not None:
        df_aggregated[str(metric2_name).upper()] = (
            df_aggregated[str(metric2_name).upper()]
        ).astype(float).tolist()

    df_aggregated = df_aggregated[
        df_aggregated.index.isin(model_list, level='MODEL')
    ]

    pivot_metric1 = pd.pivot_table(
        df_aggregated, values=str(metric1_name).upper(), columns='MODEL', 
        index='ANTI_DATE_HOURS'
    )
    pivot_metric1 = pivot_metric1.dropna() 
    if metric2_name is not None:
        pivot_metric2 = pd.pivot_table(
            df_aggregated, values=str(metric2_name).upper(), columns='MODEL', 
            index='ANTI_DATE_HOURS'
        )
        pivot_metric2 = pivot_metric2.dropna() 
    if confidence_intervals:
        pivot_ci_lower1 = pd.pivot_table(
            df_aggregated, values=str(metric1_name).upper()+'_BLERR',
            columns='MODEL', index='ANTI_DATE_HOURS'
        )
        pivot_ci_upper1 = pd.pivot_table(
            df_aggregated, values=str(metric1_name).upper()+'_BUERR',
            columns='MODEL', index='ANTI_DATE_HOURS'
        )
        if metric2_name is not None:
            pivot_ci_lower2 = pd.pivot_table(
                df_aggregated, values=str(metric2_name).upper()+'_BLERR',
                columns='MODEL', index='ANTI_DATE_HOURS'
            )
            pivot_ci_upper2 = pd.pivot_table(
                df_aggregated, values=str(metric2_name).upper()+'_BUERR',
                columns='MODEL', index='ANTI_DATE_HOURS'
            )

    if (metric2_name and (pivot_metric1.empty or pivot_metric2.empty)):
        print_varname = df['FCST_VAR'].tolist()[0]
        logger.warning(
            f"Could not find (and cannot plot) {metric1_name} and/or"
            + f" {metric2_name} stats for {print_varname} at any level. "
            + f"Continuing ..."
        )
        plt.close(num)
        logger.info("========================================")
        print("Quitting due to missing data.  Check the log file for details.")
        return None
    elif not metric2_name and pivot_metric1.empty:
        print_varname = df['FCST_VAR'].tolist()[0]
        logger.warning(
            f"Could not find (and cannot plot) {metric1_name}"
            f" stats for {print_varname} at any level. "
            + f"Continuing ..."
        )
        plt.close(num)
        logger.info("========================================")
        print("Quitting due to missing data.  Check the log file for details.")
        return None


    models_renamed = []
    count_renamed = 1
    for requested_model in model_list:
        if requested_model in model_colors.model_alias:
            requested_model = (
                model_colors.model_alias[requested_model]['settings_key']
            )
        if requested_model in model_settings:
            models_renamed.append(requested_model)
        else:
            models_renamed.append('model'+str(count_renamed))
            count_renamed+=1
    models_renamed = np.array(models_renamed)
    # Check that there are no repeated colors
    temp_colors = [
        model_colors.get_color_dict(name)['color'] for name in models_renamed
    ]
    colors_corrected=False
    loop_count=0
    while not colors_corrected and loop_count < 10:
        unique, counts = np.unique(temp_colors, return_counts=True)
        repeated_colors = [u for i, u in enumerate(unique) if counts[i] > 1]
        if repeated_colors:
            for c in repeated_colors:
                models_sharing_colors = models_renamed[
                    np.array(temp_colors)==c
                ]
                if np.flatnonzero(np.core.defchararray.find(
                        models_sharing_colors, 'model')!=-1):
                    need_to_rename = models_sharing_colors[
                        np.flatnonzero(np.core.defchararray.find(
                            models_sharing_colors, 'model'
                        )!=-1)[0]
                    ]
                else:
                    continue
                models_renamed[models_renamed==need_to_rename] = (
                    'model'+str(count_renamed)
                )
                count_renamed+=1
            temp_colors = [
                model_colors.get_color_dict(name)['color'] 
                for name in models_renamed
            ]
            loop_count+=1
        else:
            colors_corrected = True
    mod_setting_dicts = [
        model_colors.get_color_dict(name) for name in models_renamed
    ]

    # Plot data
    logger.info("Begin plotting ...")
    f = lambda m,c,ls,lw,ms,mec: plt.plot(
        [], [], marker=m, mec=mec, mew=2., c=c, ls=ls, lw=lw, ms=ms
    )[0]
    if metric2_name is not None:
        handles = [
            f('', 'black', line_setting, 5., 0, 'white')
            for line_setting in ['solid','dashed']
        ]
        labels = [
            str(metric_name).upper()
            for metric_name in [metric1_name, metric2_name]
        ]
    else:
        handles = []
        labels = []
    incr = 1
    if confidence_intervals:
        indices_in_common1 = list(set.intersection(*map(
            set, 
            [
                pivot_metric1.index, 
                pivot_ci_lower1.index, 
                pivot_ci_upper1.index
            ]
        )))
        pivot_metric1 = pivot_metric1[pivot_metric1.index.isin(indices_in_common1)]
        pivot_ci_lower1 = pivot_ci_lower1[pivot_ci_lower1.index.isin(indices_in_common1)]
        pivot_ci_upper1 = pivot_ci_upper1[pivot_ci_upper1.index.isin(indices_in_common1)]
        if metric2_name is not None:
            indices_in_common2 = list(set.intersection(*map(
                set, 
                [
                    pivot_metric2.index, 
                    pivot_ci_lower2.index, 
                    pivot_ci_upper2.index
                ]
            )))
            pivot_metric2 = pivot_metric2[pivot_metric2.index.isin(indices_in_common2)]
            pivot_ci_lower2 = pivot_ci_lower2[pivot_ci_lower2.index.isin(indices_in_common2)]
            pivot_ci_upper2 = pivot_ci_upper2[pivot_ci_upper2.index.isin(indices_in_common2)]
    x_vals1 = pivot_metric1.index
    if metric2_name is not None:
        x_vals2 = pivot_metric2.index
    y_min = y_min_limit
    y_max = y_max_limit
    if thresh and '' not in thresh:
        thresh_labels = np.unique(df['FCST_THRESH_VALUE'])
        thresh_argsort = np.argsort(thresh_labels.astype(float))
        requested_thresh_argsort = np.argsort([
            float(item) for item in requested_thresh_value
        ])
        thresh_labels = [thresh_labels[i] for i in thresh_argsort]
        requested_thresh_labels = [
            requested_thresh_value[i] for i in requested_thresh_argsort
        ]
    for m in range(len(mod_setting_dicts)):
        if model_list[m] in model_colors.model_alias:
            model_plot_name = (
                model_colors.model_alias[model_list[m]]['plot_name']
            )
        else:
            model_plot_name = model_list[m]
        y_vals_metric1 = pivot_metric1[str(model_list[m])].values
        y_vals_metric1_mean = np.nanmean(y_vals_metric1)
        if metric2_name is not None:
            y_vals_metric2 = pivot_metric2[str(model_list[m])].values
            y_vals_metric2_mean = np.nanmean(y_vals_metric2)
        if confidence_intervals:
            y_vals_ci_lower1 = pivot_ci_lower1[
                str(model_list[m])
            ].values
            y_vals_ci_upper1 = pivot_ci_upper1[
                str(model_list[m])
            ].values
            if metric2_name is not None:
                y_vals_ci_lower2 = pivot_ci_lower2[
                    str(model_list[m])
                ].values
                y_vals_ci_upper2 = pivot_ci_upper2[
                    str(model_list[m])
                ].values
        if not y_lim_lock:
            if metric2_name is not None:
                y_vals_metric_min = np.nanmin([y_vals_metric1, y_vals_metric2])
                y_vals_metric_max = np.nanmax([y_vals_metric1, y_vals_metric2])
            else:
                y_vals_metric_min = np.nanmin(y_vals_metric1)
                y_vals_metric_max = np.nanmax(y_vals_metric1)
            if m == 0:
                y_mod_min = y_vals_metric_min
                y_mod_max = y_vals_metric_max
            else:
                y_mod_min = np.nanmin([y_mod_min, y_vals_metric_min])
                y_mod_max = np.nanmax([y_mod_max, y_vals_metric_max])
            if (y_vals_metric_min > y_min_limit 
                    and y_vals_metric_min <= y_mod_min):
                y_min = y_vals_metric_min
            if (y_vals_metric_max < y_max_limit 
                    and y_vals_metric_max >= y_mod_max):
                y_max = y_vals_metric_max
        if np.abs(y_vals_metric1_mean) < 1E4:
            metric1_mean_fmt_string = f'{y_vals_metric1_mean:.2f}'
        else:
            metric1_mean_fmt_string = f'{y_vals_metric1_mean:.2E}'
        plt.plot(
            x_vals1.tolist(), y_vals_metric1, 
            marker=mod_setting_dicts[m]['marker'], 
            c=mod_setting_dicts[m]['color'], mew=2., mec='white', 
            figure=fig, ms=mod_setting_dicts[m]['markersize'], ls='solid', 
            lw=mod_setting_dicts[m]['linewidth']
        )
        if metric2_name is not None:
            if np.abs(y_vals_metric2_mean) < 1E4:
                metric2_mean_fmt_string = f'{y_vals_metric2_mean:.2f}'
            else:
                metric2_mean_fmt_string = f'{y_vals_metric2_mean:.2E}'
            plt.plot(
                x_vals2.tolist(), y_vals_metric2, 
                marker=mod_setting_dicts[m]['marker'], 
                c=mod_setting_dicts[m]['color'], mew=2., mec='white', 
                figure=fig, ms=mod_setting_dicts[m]['markersize'], ls='dashed', 
                lw=mod_setting_dicts[m]['linewidth']
            )
        if confidence_intervals:
            plt.errorbar(
                x_vals1.tolist(), y_vals_metric1,
                yerr=[np.abs(y_vals_ci_lower1), y_vals_ci_upper1],
                fmt='none', ecolor=mod_setting_dicts[m]['color'],
                elinewidth=mod_setting_dicts[m]['linewidth'],
                capsize=10., capthick=mod_setting_dicts[m]['linewidth'],
                alpha=.70, zorder=0
            )
            if metric2_name is not None:
                plt.errorbar(
                    x_vals2.tolist(), y_vals_metric2,
                    yerr=[np.abs(y_vals_ci_lower2), y_vals_ci_upper2],
                    fmt='none', ecolor=mod_setting_dicts[m]['color'],
                    elinewidth=mod_setting_dicts[m]['linewidth'],
                    capsize=10., capthick=mod_setting_dicts[m]['linewidth'],
                    alpha=.70, zorder=0
                )
        handles+=[
            f(
                mod_setting_dicts[m]['marker'], mod_setting_dicts[m]['color'],
                'solid', mod_setting_dicts[m]['linewidth'], 
                mod_setting_dicts[m]['markersize'], 'white'
            )
        ]
        if display_averages:
            if metric2_name is not None:
                labels+=[
                    f'{model_plot_name} ({metric1_mean_fmt_string},'
                    + f'{metric2_mean_fmt_string})'
                ]
            else:
                labels+=[
                    f'{model_plot_name} ({metric1_mean_fmt_string})'
                ]
        else:
            labels+=[f'{model_plot_name}']

    # Zero line
    plt.axhline(y=0, color='black', linestyle='--', linewidth=1, zorder=0) 
    metrics_with_axline_at_1 = [
        'FBIAS','RSD'
    ]
    if (str(metric1_name).upper() in metrics_with_axline_at_1
            or str(metric2_name).upper() in metrics_with_axline_at_1):
        plt.axhline(y=1, color='black', linestyle='--', linewidth=1, zorder=0)

    # Configure axis ticks
    xticks_min = 0
    xticks_max = 23
    xticks = [
        x_val for x_val in np.arange(xticks_min, xticks_max+incr, incr)
    ] 
    xtick_labels = [str(xtick) for xtick in xticks]
    if len(xticks) < 48:
        show_xtick_every = 1
    else:
        show_xtick_every = 2
    xtick_labels_with_blanks = ['' for item in xtick_labels]
    for i, item in enumerate(xtick_labels[::int(show_xtick_every)]):
         xtick_labels_with_blanks[int(show_xtick_every)*i] = item
    x_buffer_size = .15
    ax.set_xlim(
        xticks_min-incr*x_buffer_size, xticks_max+incr*x_buffer_size
    )
    y_range_categories = np.array([
        [np.power(10.,y), 2.*np.power(10.,y)] 
        for y in [-5,-4,-3,-2,-1,0,1,2,3,4,5]
    ]).flatten()
    round_to_nearest_categories = y_range_categories/20.
    y_range = y_max-y_min
    round_to_nearest =  round_to_nearest_categories[
        np.digitize(y_range, y_range_categories[:-1])
    ]
    ylim_min = np.floor(y_min/round_to_nearest)*round_to_nearest
    ylim_max = np.ceil(y_max/round_to_nearest)*round_to_nearest
    if len(str(ylim_min)) > 5 and np.abs(ylim_min) < 1.:
        ylim_min = float(
            np.format_float_scientific(ylim_min, unique=False, precision=3)
        )
    yticks = np.arange(ylim_min, ylim_max+round_to_nearest, round_to_nearest)
    var_long_name_key = df['FCST_VAR'].tolist()[0]
    if str(var_long_name_key).upper() == 'HGT':
        if str(df['OBS_VAR'].tolist()[0]).upper() == 'CEILING':
            var_long_name_key = 'HGTCLDCEIL'
    var_long_name = variable_translator[var_long_name_key]
    units = df['FCST_UNITS'].tolist()[0]
    metrics_using_var_units = [
        'BCRMSE','RMSE','BIAS','ME','FBAR','OBAR','MAE','FBAR_OBAR',
        'SPEED_ERR','DIR_ERR','RMSVE','VDIFF_SPEED','VDIF_DIR',
        'FBAR_OBAR_SPEED','FBAR_OBAR_DIR','FBAR_SPEED','FBAR_DIR'
    ]
    if metric2_name is not None:
        metric1_string, metric2_string = metric_long_names
        if (str(metric1_name).upper() in metrics_using_var_units
                and str(metric2_name).upper() in metrics_using_var_units):
            ylabel = f'{var_long_name} ({units})'
        else:
            ylabel = f'{metric1_string} and {metric2_string}'
    else:
        metric1_string = metric_long_names[0]
        if str(metric1_name).upper() in metrics_using_var_units:
            ylabel = f'{var_long_name} ({units})'
        else:
            ylabel = f'{metric1_string}'
    ax.set_ylim(ylim_min, ylim_max)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel) 
    ax.set_xticklabels(xtick_labels_with_blanks)
    ax.set_yticks(yticks)
    ax.set_xticks(xticks)
    ax.tick_params(
        labelleft=True, labelright=False, labelbottom=True, labeltop=False
    )
    ax.tick_params(
        left=False, labelleft=False, labelright=False, labelbottom=False, 
        labeltop=False, which='minor', axis='y', pad=15
    )

    ax.legend(
        handles, labels, loc='upper center', fontsize=15, framealpha=1, 
        bbox_to_anchor=(0.5, -0.08), ncol=4, frameon=True, numpoints=2, 
        borderpad=.8, labelspacing=2., columnspacing=3., handlelength=3., 
        handletextpad=.4, borderaxespad=.5) 
    fig.subplots_adjust(bottom=.2, wspace=0, hspace=0)
    ax.grid(
        b=True, which='major', axis='both', alpha=.5, linestyle='--', 
        linewidth=.5, zorder=0
    )

    # Title
    domain = df['VX_MASK'].tolist()[0]
    var_savename = df['FCST_VAR'].tolist()[0]
    if domain in list(domain_translator.keys()):
        domain_string = domain_translator[domain]
    else:
        domain_string = domain
    date_hours_string = ' '.join([
        f'{date_hour:02d}Z,' for date_hour in date_hours
    ])
    date_start_string = date_range[0].strftime('%d %b %Y')
    date_end_string = date_range[1].strftime('%d %b %Y')
    if str(verif_type).lower() in ['pres', 'upper_air'] or 'P' in str(level):
        level_num = level.replace('P', '')
        level_string = f'{level_num} hPa '
        level_savename = f'{level_num}MB_'
    elif str(verif_type).lower() in ['sfc', 'conus_sfc', 'polar_sfc', 'mrms']:
        if 'Z' in str(level):
            if str(level).upper() == 'Z0':
                level_string = 'Surface '
                level_savename = 'SFC_'
            else:
                level_num = level.replace('Z', '')
                if var_savename in ['TSOIL', 'SOILW']:
                    level_string = f'{level_num}-cm '
                    level_savename = f'{level_num}CM_'
                else:
                    level_string = f'{level_num}-m '
                    level_savename = f'{level_num}M_'
        elif 'L' in str(level) or 'A' in str(level):
            level_string = ''
            level_savename = ''
        else:
            level_string = f'{level} '
            level_savename = f'{level}_'
    elif str(verif_type).lower() in ['ccpa']:
        if 'A' in str(level):
            level_num = level.replace('A', '')
            level_string = f'{level_num}-hour '
            level_savename = f'{level_num}H_'
        else:
            level_string = f''
            level_savename = f''
    else:
        level_string = f'{level}'
        level_savename = f'{level}_'
    if metric2_name is not None:
        title1 = f'{metric1_string} and {metric2_string}'
    else:
        title1 = f'{metric1_string}'
    if thresh and '' not in thresh:
        thresholds_phrase = ', '.join([
            f'{opt}{thresh_label}' for thresh_label in thresh_labels
        ])
        thresholds_save_phrase = ''.join([
            f'{opt_letter}{thresh_label}' 
            for thresh_label in requested_thresh_labels
        ])
        title2 = (f'{level_string}{var_long_name} ({thresholds_phrase}'
                  + f' {units}), {domain_string}')
    else:
        title2 = f'{level_string}{var_long_name} ({units}), {domain_string}'
    title3 = (f'{str(date_type).capitalize()} {date_hours_string} '
              + f'{date_start_string} to {date_end_string}, {frange_string}')
    title_center = '\n'.join([title1, title2, title3])
    ax.set_title(title_center, loc=plotter.title_loc) 
    logger.info("... Plotting complete.")

    # Saving
    models_savename = '_'.join([str(model) for model in model_list])
    if len(date_hours) <= 8: 
        date_hours_savename = '_'.join([
            f'{date_hour:02d}Z' for date_hour in date_hours
        ])
    else:
        date_hours_savename = '-'.join([
            f'{date_hour:02d}Z' 
            for date_hour in [date_hours[0], date_hours[-1]]
        ])
    date_start_savename = date_range[0].strftime('%Y%m%d')
    date_end_savename = date_range[1].strftime('%Y%m%d')
    if str(eval_period).upper() == 'TEST':
        time_period_savename = f'{date_start_savename}-{date_end_savename}'
    else:
        time_period_savename = f'{eval_period}'
    save_name = (f'valid_hour_average_regional_'
                 + f'{str(domain).lower()}_{str(date_type).lower()}_'
                 + f'{str(date_hours_savename).lower()}_'
                 + f'{str(level_savename).lower()}'
                 + f'{str(var_savename).lower()}_{str(metric1_name).lower()}')
    if metric2_name is not None:
        save_name+=f'_{str(metric2_name).lower()}'
    save_name+=f'_{str(frange_save_string).lower()}'
    if thresh and '' not in thresh:
        save_name+=f'_{str(thresholds_save_phrase).lower()}'
    if save_header:
        save_name = f'{save_header}_'+save_name
    save_subdir = os.path.join(
        save_dir, f'{str(plot_group).lower()}', 
        f'{str(time_period_savename).lower()}'
    )
    if not os.path.isdir(save_subdir):
        os.makedirs(save_subdir)
    save_path = os.path.join(save_subdir, save_name+'.png')
    fig.savefig(save_path, dpi=dpi)
    logger.info(u"\u2713"+f" plot saved successfully as {save_path}")
    plt.close(num)
    logger.info('========================================')


def main():

    # Logging
    log_metplus_dir = '/'
    for subdir in LOG_METPLUS.split('/')[:-1]:
        log_metplus_dir = os.path.join(log_metplus_dir, subdir)
    if not os.path.isdir(log_metplus_dir):
        os.makedirs(log_metplus_dir)
    logger = logging.getLogger(LOG_METPLUS)
    logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d (%(filename)s:%(lineno)d) %(levelname)s: '
        + '%(message)s',
        '%m/%d %H:%M:%S'
    )
    file_handler = logging.FileHandler(LOG_METPLUS, mode='a')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger_info = f"Log file: {LOG_METPLUS}"
    print(logger_info)
    logger.info(logger_info)

    if str(EVAL_PERIOD).upper() == 'TEST':
        valid_beg = VALID_BEG
        valid_end = VALID_END
        init_beg = INIT_BEG
        init_end = INIT_END
    else:
        valid_beg = presets.date_presets[EVAL_PERIOD]['valid_beg']
        valid_end = presets.date_presets[EVAL_PERIOD]['valid_end']
        init_beg = presets.date_presets[EVAL_PERIOD]['init_beg']
        init_end = presets.date_presets[EVAL_PERIOD]['init_end']
    if str(DATE_TYPE).upper() == 'VALID':
        e = (f"You requested a valid_hour_average plot with the DATE_TYPE "
             + f"set to 'VALID'. Valid time is already used as the independent"
             + f" variable in valid_hour_average plots, therfore please set"
             + f" the DATE_TYPE to 'INIT', to equalize data by initialization"
             + f" time.  Also, make sure neither FCST_INIT_HOUR nor"
             + f" FCST_VALID_HOUR is an empty list.")
        logger.error(e)
        raise ValueError(e)
    elif str(DATE_TYPE).upper() == 'INIT':
        date_beg = init_beg
        date_end = init_end
        date_hours = INIT_HOURS
        anti_date_hours = VALID_HOURS
        anti_date_type_string = 'Valid'
        xlabel=f'{str(anti_date_type_string).capitalize()} Hour (UTC)'
    else:
        e = (f"Invalid DATE_TYPE: {str(date_type).upper()}. Valid values are"
             + f" VALID or INIT")
        logger.error(e)
        raise ValueError(e)
    date_range = (
        datetime.strptime(date_beg, '%Y%m%d'), 
        datetime.strptime(date_end, '%Y%m%d')
    )
    if len(METRICS) == 1:
        metrics = (METRICS[0], None)
    elif len(METRICS) > 1:
        metrics = METRICS[:2]
    else:
        e = (f"Received no list of metrics.  Check that, for the METRICS"
             + f" setting, a comma-separated string of at least one metric is"
             + f" provided")
        logger.error(e)
        raise ValueError(e)
    fcst_thresh_symbol, fcst_thresh_letter = list(
        zip(*[plot_util.format_thresh(thresh) for thresh in FCST_THRESH])
    )
    obs_thresh_symbol, obs_thresh_letter = list(
        zip(*[plot_util.format_thresh(thresh) for thresh in OBS_THRESH])
    )
    num=0
    e = ''
    if str(VERIF_CASETYPE).lower() not in list(reference.case_type.keys()):
        e = (f"The requested verification case/type combination is not valid:"
             + f" {VERIF_CASETYPE}")
    elif str(LINE_TYPE).upper() not in list(
            reference.case_type[str(VERIF_CASETYPE).lower()].keys()):
        e = (f"The requested line_type is not valid for {VERIF_CASETYPE}:"
             + f" {LINE_TYPE}")
    else:
        case_specs = (
            reference.case_type
            [str(VERIF_CASETYPE).lower()]
            [str(LINE_TYPE).upper()]
        )
    if e:
        logger.error(e)
        logger.error("Quitting ...")
        raise ValueError(e+"\nQuitting ...")
    if (str(INTERP).upper() 
            not in case_specs['interp'].replace(' ','').split(',')):
        e = (f"The requested interp method is not valid for the"
             + f" requested case type ({VERIF_CASETYPE}) and"
             + f" line_type ({LINE_TYPE}): {INTERP}")
        logger.error(e)
        logger.error("Quitting ...")
        raise ValueError(e+"\nQuitting ...")
    for metric in metrics:
        if metric is not None:
            if (str(metric).lower() 
                    not in case_specs['plot_stats_list']
                    .replace(' ','').split(',')):
                e = (f"The requested metric is not valid for the"
                     + f" requested case type ({VERIF_CASETYPE}) and"
                     + f" line_type ({LINE_TYPE}): {metric}")
                logger.error(e)
                logger.error("Quitting ...")
                raise ValueError(e+"\nQuitting ...")
    for requested_var in VARIABLES:
        if requested_var in list(case_specs['var_dict'].keys()):
            var_specs = case_specs['var_dict'][requested_var]
        else:
            e = (f"The requested variable is not valid for the requested case"
                 + f" type ({VERIF_CASETYPE}) and line_type ({LINE_TYPE}):"
                 + f" {requested_var}")
            logger.warning(e)
            logger.warning("Continuing ...")
            continue
        fcst_var_name = var_specs['fcst_var_name']
        obs_var_name = var_specs['obs_var_name']
        symbol_keep = []
        letter_keep = []
        for fcst_thresh, obs_thresh in list(
                zip(*[fcst_thresh_symbol, obs_thresh_symbol])):
            if (fcst_thresh in var_specs['fcst_var_thresholds']
                    and obs_thresh in var_specs['obs_var_thresholds']):
                symbol_keep.append(True)
            else:
                symbol_keep.append(False)
        for fcst_thresh, obs_thresh in list(
                zip(*[fcst_thresh_letter, obs_thresh_letter])):
            if (fcst_thresh in var_specs['fcst_var_thresholds']
                    and obs_thresh in var_specs['obs_var_thresholds']):
                letter_keep.append(True)
            else:
                letter_keep.append(False)
        keep = np.add(letter_keep, symbol_keep)
        dropped_items = np.array(FCST_THRESH)[~keep].tolist()
        fcst_thresh = np.array(FCST_THRESH)[keep].tolist()
        obs_thresh = np.array(OBS_THRESH)[keep].tolist()
        if dropped_items:
            dropped_items_string = ', '.join(dropped_items)
            e = (f"The requested thresholds are not valid for the requested"
                 + f" case type ({VERIF_CASETYPE}) and line_type"
                 + f" ({LINE_TYPE}): {dropped_items_string}")
            logger.warning(e)
            logger.warning("Continuing ...")
        plot_group = var_specs['plot_group']
        for l, fcst_level in enumerate(FCST_LEVELS):
            if len(FCST_LEVELS) != len(OBS_LEVELS):
                e = ("FCST_LEVELS and OBS_LEVELS must be lists of the same"
                     + f" size")
                logger.error(e)
                logger.error("Quitting ...")
                raise ValueError(e+"\nQuitting ...")
            if (FCST_LEVELS[l] not in var_specs['fcst_var_levels'] 
                    or OBS_LEVELS[l] not in var_specs['obs_var_levels']):
                e = (f"The requested variable/level combination is not valid: "
                     + f"{requested_var}/{level}")
                logger.warning(e)
                continue
            for domain in DOMAINS:
                if str(domain).upper() not in case_specs['vx_mask_list']:
                    e = (f"The requested domain is not valid for the requested"
                         + f" case type ({VERIF_CASETYPE}) and line_type"
                         + f" ({LINE_TYPE}): {domain}")
                    logger.warning(e)
                    logger.warning("Continuing ...")
                    continue
                df = df_preprocessing.get_preprocessed_data(
                    logger, STATS_DIR, PRUNE_DIR, LOOKFOR_TEMPLATE, VERIF_CASE, 
                    VERIF_TYPE, LINE_TYPE, DATE_TYPE, date_range, EVAL_PERIOD, 
                    date_hours, FLEADS, requested_var, fcst_var_name, obs_var_name, 
                    MODELS, domain, INTERP, MET_VERSION
                )
                if df is None:
                    continue
                df_metric = df
                plot_valid_hour_average(
                    df_metric, logger, date_range, MODELS, num=num, 
                    flead=FLEADS, level=fcst_level, thresh=fcst_thresh, 
                    metric1_name=metrics[0], metric2_name=metrics[1], 
                    date_type=DATE_TYPE, y_min_limit=Y_MIN_LIMIT, 
                    y_max_limit=Y_MAX_LIMIT, y_lim_lock=Y_LIM_LOCK, 
                    xlabel=xlabel, line_type=LINE_TYPE, verif_type=VERIF_TYPE, 
                    date_hours=date_hours, anti_date_hours=anti_date_hours, 
                    eval_period=EVAL_PERIOD, save_dir=SAVE_DIR, 
                    display_averages=display_averages, save_header=URL_HEADER, 
                    plot_group=plot_group, 
                    confidence_intervals=CONFIDENCE_INTERVALS, bs_nrep=bs_nrep, 
                    bs_method=bs_method, ci_lev=ci_lev, 
                    bs_min_samp=bs_min_samp
                )
                num+=1


# ============ START USER CONFIGURATIONS ================
if __name__ == "__main__":
    print("\n=================== CHECKING CONFIG VARIABLES =====================\n")
    LOG_METPLUS = check_LOG_METPLUS(os.environ['LOG_METPLUS'])
    LOG_LEVEL = check_LOG_LEVEL(os.environ['LOG_LEVEL'])
    MET_VERSION = check_MET_VERSION(os.environ['MET_VERSION'])
    URL_HEADER = check_URL_HEADER(os.environ['URL_HEADER'])
    VERIF_CASE = check_VERIF_CASE(os.environ['VERIF_CASE'])
    VERIF_TYPE = check_VERIF_TYPE(os.environ['VERIF_TYPE'])
    OUTPUT_BASE_DIR = check_OUTPUT_BASE_DIR(os.environ['OUTPUT_BASE_DIR'])
    STATS_DIR = OUTPUT_BASE_DIR
    PRUNE_DIR = check_PRUNE_DIR(os.environ['PRUNE_DIR'])
    SAVE_DIR = check_SAVE_DIR(os.environ['SAVE_DIR'])
    DATE_TYPE = check_DATE_TYPE(os.environ['DATE_TYPE'])
    LINE_TYPE = check_LINE_TYPE(os.environ['LINE_TYPE'])
    INTERP = check_INTERP(os.environ['INTERP'])
    MODELS = check_MODEL(os.environ['MODEL']).replace(' ','').split(',')
    DOMAINS = check_VX_MASK_LIST(os.environ['VX_MASK_LIST']).replace(' ','').split(',')

    # valid hour (each plot will use all available valid_hours listed below)
    VALID_HOURS = check_FCST_VALID_HOUR(os.environ['FCST_VALID_HOUR'], DATE_TYPE).replace(' ','').split(',')
    INIT_HOURS = check_FCST_INIT_HOUR(os.environ['FCST_INIT_HOUR'], DATE_TYPE).replace(' ','').split(',')

    # time period to cover (inclusive)
    EVAL_PERIOD = check_EVAL_PERIOD(os.environ['EVAL_PERIOD'])
    VALID_BEG = check_VALID_BEG(os.environ['VALID_BEG'], DATE_TYPE, EVAL_PERIOD, plot_type='time_series')
    VALID_END = check_VALID_END(os.environ['VALID_END'], DATE_TYPE, EVAL_PERIOD, plot_type='time_series')
    INIT_BEG = check_INIT_BEG(os.environ['INIT_BEG'], DATE_TYPE, EVAL_PERIOD, plot_type='time_series')
    INIT_END = check_INIT_END(os.environ['INIT_END'], DATE_TYPE, EVAL_PERIOD, plot_type='time_series')

    # list of variables
    # Options: {'TMP','HGT','CAPE','RH','DPT','UGRD','VGRD','UGRD_VGRD','TCDC',
    #           'VIS'}
    VARIABLES = check_var_name(os.environ['var_name']).replace(' ','').split(',')

    # list of lead hours
    # Options: {list of lead hours; string, 'all'; tuple, start/stop flead; 
    #           string, single flead}
    FLEADS = check_FCST_LEAD(os.environ['FCST_LEAD']).replace(' ','').split(',')

    # list of levels
    FCST_LEVELS = check_FCST_LEVEL(os.environ['FCST_LEVEL']).replace(' ','').split(',')
    OBS_LEVELS = check_OBS_LEVEL(os.environ['OBS_LEVEL']).replace(' ','').split(',')

    FCST_THRESH = check_FCST_THRESH(os.environ['FCST_THRESH'], LINE_TYPE)
    OBS_THRESH = check_OBS_THRESH(os.environ['OBS_THRESH'], FCST_THRESH, LINE_TYPE).replace(' ','').split(',')
    FCST_THRESH = FCST_THRESH.replace(' ','').split(',')
    
    # requires two metrics to plot
    METRICS = list(filter(None, check_STATS(os.environ['STATS']).replace(' ','').split(',')))

    # set the lowest possible lower (and highest possible upper) axis limits. 
    # E.g.: If Y_LIM_LOCK == True, use Y_MIN_LIMIT as the definitive lower 
    # limit (ditto with Y_MAX_LIMIT)
    # If Y_LIM_LOCK == False, then allow lower and upper limits to adjust to 
    # data as long as limits don't overcome Y_MIN_LIMIT or Y_MAX_LIMIT 
    Y_MIN_LIMIT = toggle.plot_settings['y_min_limit']
    Y_MAX_LIMIT = toggle.plot_settings['y_max_limit']
    Y_LIM_LOCK = toggle.plot_settings['y_lim_lock']


    # configure CIs
    CONFIDENCE_INTERVALS = check_CONFIDENCE_INTERVALS(os.environ['CONFIDENCE_INTERVALS']).replace(' ','')
    bs_nrep = toggle.plot_settings['bs_nrep']
    bs_method = toggle.plot_settings['bs_method']
    ci_lev = toggle.plot_settings['ci_lev']
    bs_min_samp = toggle.plot_settings['bs_min_samp']

    # Whether or not to display average values beside legend labels
    display_averages = toggle.plot_settings['display_averages']

    LOOKFOR_TEMPLATE = templates.lookfor_template

    print("\n===================================================================\n")
    # ============= END USER CONFIGURATIONS =================

    LOG_METPLUS = str(LOG_METPLUS)
    LOG_LEVEL = str(LOG_LEVEL)
    MET_VERSION = float(MET_VERSION)
    VALID_HOURS = [
        int(valid_hour) if valid_hour else None for valid_hour in VALID_HOURS
    ]
    INIT_HOURS = [
        int(init_hour) if init_hour else None for init_hour in INIT_HOURS
    ]
    FLEADS = [int(flead) for flead in FLEADS]
    VERIF_CASETYPE = str(VERIF_CASE).lower() + '_' + str(VERIF_TYPE).lower()
    FCST_LEVELS = [str(level) for level in FCST_LEVELS]
    OBS_LEVELS = [str(level) for level in OBS_LEVELS]
    CONFIDENCE_INTERVALS = str(CONFIDENCE_INTERVALS).lower() in [
        'true', '1', 't', 'y', 'yes'
    ]
    main()
