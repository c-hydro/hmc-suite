"""
Library Features:

Name:          lib_utils_time
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241202'
Version:       '1.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import pandas as pd

from datetime import date

from lib_default_args import logger_name

# set logger
alg_logger = logging.getLogger(logger_name)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to convert time frequency from string to seconds
def convert_time_frequency(time_frequency: str) -> int:
    time_delta = pd.Timedelta(1, unit=time_frequency)
    time_seconds = int(time_delta.total_seconds())
    return time_seconds

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to check string has the date format
def is_date(string: str, date_format: str = '%Y%m%d%H%M') -> bool:
    """
    Return whether the string can be interpreted as a date.
    :param string: str, string to check for date
    :param date_format: str, format of the date
    """
    try:
        pd.to_datetime(string, format=date_format, errors='raise')
        return True

    except ValueError:
        return False
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Method to set time info
def select_time_information(
        time_run_args=None, time_run_file=None, time_format='%Y-%m-%d %H:$M',
        time_run_file_start=None, time_run_file_end=None,
        time_period=1, time_frequency='H', time_rounding='H'):

    alg_logger.info(' ----> Select time information ... ')
    if (time_run_args is not None) or (time_run_file is not None):

        alg_logger.info(' -----> Time info defined by "time_now" argument ... ')

        if time_run_args is not None:
            time_run = time_run_args
            alg_logger.info(' ------> Time ' + time_run + ' set by argument')
        elif (time_run_args is None) and (time_run_file is not None):
            time_run = time_run_file
            alg_logger.info(' ------> Time ' + time_run + ' set by user')
        elif (time_run_args is None) and (time_run_file is None):
            time_now = date.today()
            time_run = time_now.strftime(time_format)
            alg_logger.info(' ------> Time ' + time_run + ' set by system')
        else:
            alg_logger.info(' ----> Select time information ... FAILED')
            alg_logger.error(' ===> Argument "time_now" is not correctly set')
            raise IOError('Time type or format is wrong')

        time_df = pd.DataFrame([{'time_now': pd.Timestamp(time_run)}])
        time_df['time_round'] = time_df['time_now'].dt.floor(time_rounding)

        time_now = time_df['time_round'].values[0]
        time_restart = time_now - pd.Timedelta(1, unit=time_frequency)

        alg_logger.info(' -----> Time info defined by "time_now" argument ... DONE')

    elif (time_run_file_start is not None) and (time_run_file_end is not None):

        alg_logger.info(' -----> Time info defined by "time_start" and "time_end" arguments ... ')

        time_run_file_start = pd.Timestamp(time_run_file_start)
        time_run_file_start = time_run_file_start.floor(time_rounding)
        time_run_file_end = pd.Timestamp(time_run_file_end)
        time_run_file_end = time_run_file_end.floor(time_rounding)

        time_range = pd.date_range(start=time_run_file_start, end=time_run_file_end, freq=time_frequency)

        time_now = time_range[0]
        time_period = len(time_range)

        time_restart = time_now - pd.Timedelta(1, unit=time_frequency)

        alg_logger.info(' -----> Time info defined by "time_start" and "time_end" arguments ... DONE')

    elif ( (time_run_args is None) and (time_run_file is None) ) and (
            (time_run_file_start is None) and (time_run_file_end is None) ):

        time_now, time_restart, time_period = None, None, None

    else:
        alg_logger.error(' ===> Time arguments are not supported')
        raise NotImplemented('Case not implemented yet')

    alg_logger.info(' ----> Select time information ... DONE')

    time_obj = {
        'time_now': time_now,
        'time_restart': time_restart,
        'time_period': time_period,
        'time_frequency': time_frequency,
        'time_rounding': time_rounding,
    }

    return time_obj

# ----------------------------------------------------------------------------------------------------------------------
