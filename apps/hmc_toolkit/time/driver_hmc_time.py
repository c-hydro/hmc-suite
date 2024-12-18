"""
Class Features

Name:          driver_hmc_time
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241126'
Version:       '4.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import os
import pandas as pd

from apps.hmc_toolkit.time import handler_hmc_time as hmc_time
from apps.generic_toolkit.lib_utils_time import select_time_run, select_time_range, select_time_restart, convert_time_frequency
from apps.generic_toolkit.lib_default_args import time_format_datasets, time_format_algorithm
from apps.generic_toolkit.lib_default_args import logger_name, logger_arrow
from apps.generic_toolkit.lib_default_args import collector_data

# logging
logger_stream = logging.getLogger(logger_name)

# debugging
# import matplotlib.pylab as plt
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to configure time
class DrvTime:

    # ------------------------------------------------------------------------------------------------------------------
    # global variable(s)
    class_type = 'driver_time'
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # class initialization
    def __init__(self, obj_variables_time: dict,
                 flag_clean_data: bool = True, **kwargs) -> None:

        self.time_run_file = obj_variables_time['time_run']
        self.time_period = obj_variables_time['time_period']
        self.time_frequency = obj_variables_time['time_frequency']
        self.time_rounding = obj_variables_time['time_rounding']

        self.time_start = obj_variables_time['time_start']
        if self.time_start is not None:
            self.time_start = pd.Timestamp(self.time_start)
        self.time_end = obj_variables_time['time_end']
        if self.time_end is not None:
            self.time_end = pd.Timestamp(self.time_end)

        self.flag_clean_data = flag_clean_data

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # configure time variable(s)
    def configure_time_variables(self, time_run_cmd=None) -> dict:

        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'Configure "time_variables" ... ')

        # define time handler class
        if time_run_cmd is not None or self.time_run_file is not None:
            time_handler = hmc_time.TimeHandler.from_time_run(
                time_run_cmd=time_run_cmd, time_run_file=self.time_run_file,
                time_period=self.time_period, time_frequency=self.time_frequency, time_rounding=self.time_rounding)
        elif (self.time_start is not None) or (self.time_end is not None):
            time_handler = hmc_time.TimeHandler.from_time_period(
                time_start=time_run_cmd, time_end=self.time_run_file,
                time_frequency=self.time_frequency, time_rounding=self.time_rounding)
        else:
            logger_stream.error(logger_arrow.error + 'Time run is not correctly defined')
            raise RuntimeError('Time run must be defined')

        # compute time restart
        time_handler.compute_time_restart(defined_by_user=None)

        # freeze time object
        time_obj = time_handler.freeze()

        # # info algorithm (end)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'Configure "time_variables" ... DONE')

        return time_obj

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to organize time variables
    def organize_time_variables(self, time_obj):

        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'Organize "time_variables" ... ')

        # map collector settings
        collector_data.collect(time_obj)

        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'Organize "time_variables" ... DONE')

    # ------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
