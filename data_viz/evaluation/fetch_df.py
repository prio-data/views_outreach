#!/usr/bin/env python
# coding: utf-8

#Basics
import numpy as np
import pandas as pd

# Views 3
from viewser.operations import fetch
from viewser import Queryset, Column
import views_runs
from views_partitioning import data_partitioner, legacy
from stepshift import views
from views_runs import storage, ModelMetadata
from views_runs.storage import store, retrieve, fetch_metadata
from views_forecasts.extensions import *

# "calib_partitioner_dict = {\"train\":(121,420),\"predict\":(421,468)}\n",
# "test_partitioner_dict = {\"train\":(121,468),\"predict\":(469,516)}\n",
#  "future_partitioner_dict = {\"train\":(121,516),\"predict\":(517,528)}\n",

def sc_all():
    calib_run_id = 46
    test = pd.DataFrame.forecasts.read_store(run=calib_run_id, name='cm_ensemble_genetic_test')
    df = test
    last_in_calib = 468 # used to be 456
    last_in_test = 516 # used to be 504
    t_range = range(0, 48)  # t_range specifies the duration of the step-combined series to construct
    step_range = range(1, 36)
    sc_all = pd.DataFrame(df['ln_ged_sb_dep'])

    for month in t_range:
        col = 'sc_' + str(last_in_calib + month)
        sc_all[col] = np.NaN
        for step in step_range:
            if (last_in_calib + month + step) <= last_in_test:
                predcol = 'step_pred_' + str(step)
                sc_all[col].loc[[last_in_calib + month + step], :] = df[predcol].loc[
                    last_in_calib + step + month, :].values

    sc_all = pd.DataFrame(sc_all)

    return sc_all  # Add this line to return the generated DataFrame

def sc_2021():
    calib_run_id = 46
    test = pd.DataFrame.forecasts.read_store(run=calib_run_id, name='cm_ensemble_genetic_test')
    df = test
    last_in_calib = 492
    last_in_test = 504
    t_range = range(0, 12)  # t_range specifies the duration of the step-combined series to construct
    step_range = range(1, 36)
    sc_2021 = pd.DataFrame(df['ln_ged_sb_dep'])

    for month in t_range:
        col = 'sc_' + str(last_in_calib + month)
        sc_2021[col] = np.NaN
        for step in step_range:
            if (last_in_calib + month + step) <= last_in_test:
                predcol = 'step_pred_' + str(step)
                sc_2021[col].loc[[last_in_calib + month + step], :] = df[predcol].loc[
                last_in_calib + step + month, :].values

    sc_2021 = pd.DataFrame(sc_2021)
    return sc_2021
