"""
Class Features

Name:          handler_hmc_time
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241212'
Version:       '1.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import pandas as pd

from apps.generic_toolkit.lib_utils_time import (select_time_run, select_time_range, select_time_restart,
                                                 convert_time_frequency, convert_time_format)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class time handler
class TimeHandler:

    class_type = 'time_handler'

    # initialize class
    def __init__(self, time_run: (str, pd.Timestamp) = None, time_restart: (str, pd.Timestamp) = None,
                 time_rounding: str = 'h', time_period: (int, None) = 1, time_shift: (int, None) = 1,
                 time_frequency: str = 'h', **kwargs) -> None:

        self.time_run = convert_time_format(time_run)
        self.time_period = time_period
        self.time_frequency = time_frequency
        self.time_rounding = time_rounding
        self.time_shift = time_shift
        self.time_restart = time_restart

    @classmethod
    def from_time_run(cls, time_run_cmd: (str, pd.Timestamp), time_run_file: (str, pd.Timestamp) = None,
                      time_period: (int, None) = 1, time_frequency: str = 'h', time_rounding: str = 'h'):

        time_run_cmd, time_run_file = convert_time_format(time_run_cmd), convert_time_format(time_run_file)
        time_run_select = select_time_run(time_run_cmd, time_run_file, time_rounding=time_rounding)

        return cls(time_run=time_run_select,
                   time_rounding=time_rounding, time_period=time_period, time_frequency=time_frequency)

    @classmethod
    def from_time_period(cls, time_start: (str, pd.Timestamp), time_end: (str, pd.Timestamp),
                         time_rounding: str = 'h', time_frequency: str = 'h'):

        time_start, time_end = convert_time_format(time_start), convert_time_format(time_end)

        time_start, time_end = time_start.round(time_rounding), time_end.round(time_rounding)
        time_range = select_time_range(time_start=time_start, time_end=time_end, time_frequency=time_frequency)

        time_run, time_period = time_range[0], time_range.size

        return cls(time_run=time_run,
                   time_rounding=time_rounding, time_period=time_period, time_frequency=time_frequency)

    # compute time restart
    def compute_time_restart(self, defined_by_user=None):

        if defined_by_user is None:
            self.time_restart = select_time_restart(
                time_run=self.time_run, time_frequency=self.time_frequency, time_shift=self.time_shift)
        else:
            time_tmp = self.time_run
            time_tmp = time_tmp.replace(**defined_by_user)
            self.time_restart = time_tmp

        return self.time_restart

    # method to freeze data
    def freeze(self):

        self.time_frequency = convert_time_frequency(self.time_frequency)
        self.time_run = convert_time_format(self.time_run, time_conversion="stamp_to_str")
        self.time_restart = convert_time_format(self.time_restart, time_conversion="stamp_to_str")
        self.time_rounding = self.time_rounding.lower()

        return self.__dict__

    # method to error data
    def error(self):
        """
        Error time data.
        """
        raise NotImplementedError

    # method to write data
    def write(self):
        """
        Write the time data.
        """

        raise NotImplementedError

    # method to view data
    def view(self) -> None:
        """
        View the time data.
        """
        settings_dframe = pd.DataFrame.from_dict(self.__dict__, orient='index', columns=['value'])
        print(settings_dframe)

    # method to check data
    def check(self):
        """
        Check if time data is available.
        """
        raise NotImplementedError
# ----------------------------------------------------------------------------------------------------------------------
