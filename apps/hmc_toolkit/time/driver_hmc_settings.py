"""
Class Features

Name:          driver_hmc_settings
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241212'
Version:       '1.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import os

from apps.hmc_toolkit.settings import handler_hmc_settings as hmc_settings

from apps.generic_toolkit.lib_utils_system import (check_keys_of_dict)

from apps.generic_toolkit.lib_default_args import logger_name, logger_arrow
from apps.generic_toolkit.lib_default_args import collector_data

# logging
logger_stream = logging.getLogger(logger_name)

# debugging
# import matplotlib.pylab as plt
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to configure settings
class DrvSettings:

    # ------------------------------------------------------------------------------------------------------------------
    # global variable(s)
    class_type = 'driver_settings'
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # class initialization
    def __init__(self,  file_name: str = None,
                 file_key: str = None, file_time: str = None, **kwargs) -> None:

        self.file_name = file_name
        self.file_key = file_key
        self.file_time = file_time

        self.tag_log, self.tag_tmp, self.time_run = 'log', 'tmp', 'time_run'

        self.driver_settings = None

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to view settings variable(s)
    def view_variable_settings(self):
        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'View "settings_variables" ... ')
        self.driver_settings.view()
        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'View "settings_variables" ... ')
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to organize settings variable(s)
    def organize_variable_settings(self, settings_obj):

        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'Organize "settings_variables" ... ')

        tag_list = [self.tag_log, self.tag_tmp, self.time_run]

        filter_obj = {}
        for tag_key in tag_list:
            if tag_key in list(settings_obj.keys()):
                filter_obj[tag_key] = settings_obj[tag_key]
            else:
                logger_stream.warning(logger_arrow.warning + 'Variable "' + tag_key + '" not found in settings object')
                filter_obj[tag_key] = None

        # map collector settings
        collector_data.collect(filter_obj)

        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'Organize "settings_variables" ... DONE')

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to configure settings variable(s)
    def configure_variable_settings(self, file_settings: dict = None) -> dict:

        # info algorithm (start)
        logging.info(logger_arrow.info(tag='info_method') + 'Configure "settings_variables" ... ')

        # get driver settings
        if (self.file_name is not None) and (file_settings is None):
            if os.path.exists(self.file_name):
                self.driver_settings = hmc_settings.SettingsHandler.from_file(
                    file_name=self.file_name, file_key=self.file_key)
            else:
                logger_stream.error(logger_arrow.error + ' Error in reading settings file "' + self.file_name + '"')
                raise ValueError('File "' + self.file_name + '" does not exists.')
        elif (self.file_name is None) and (file_settings is not None):
            self.driver_settings = hmc_settings.SettingsHandler(settings_obj=file_settings)
        else:
            logger_stream.error(logger_arrow.error + ' Error in defining driver settings')
            raise RuntimeError('Check your algorithm configuration')

        # get environment variables
        env_vars_lut = self.driver_settings.select_variable_algorithm(tag_by_user='lut')
        env_vars_format = self.driver_settings.select_variable_algorithm(tag_by_user='format')
        env_vars_tmpl = self.driver_settings.select_variable_algorithm(tag_by_user='template')
        # get system variables
        env_check_lut_format = check_keys_of_dict(
            env_vars_lut, env_vars_format, name1='lut', name2='format')
        env_check_lut_tmpl = check_keys_of_dict(
            env_vars_lut, env_vars_tmpl, name1='lut', name2='template')

        # select system variable
        env_vars_lut = self.driver_settings.select_variable_system(
            lut_by_user=env_vars_lut, format_by_user=env_vars_format, template_by_user=env_vars_tmpl,
            lut_swap=True)

        # update data settings
        file_settings = self.driver_settings.update_settings(
            lut_by_user=env_vars_lut, format_by_user=env_vars_format, template_by_user=env_vars_tmpl)

        # # info algorithm (end)
        logging.info(logger_arrow.info(tag='info_method') + 'Configure "settings_variables" ... DONE')

        return file_settings

    # ------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------
