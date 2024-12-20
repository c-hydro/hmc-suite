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

from apps.generic_toolkit.lib_utils_dict import get_dict_nested_value
from apps.generic_toolkit.lib_utils_system import check_keys_of_dict, flat_dict_key, add_dict_key

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
                 file_key: str = None, file_time: str = None,
                 variables_lut_base: dict = None, variables_lut_extra: dict = None, **kwargs) -> None:

        self.file_name = file_name
        self.file_key = file_key
        self.file_time = file_time

        if variables_lut_base is None:
            variables_lut_base = {'log': 'log', 'tmp': 'tmp'}
        if variables_lut_extra is None:
            variables_lut_extra = {'time_run': 'variables:hmc:time_run'}

        self.variables_lut_base = variables_lut_base
        self.variables_lut_extra = variables_lut_extra

        self.driver_settings = None
        self.file_settings = None
        self.file_variables = None
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to view settings variable(s)
    def view_variable_settings(self, data: dict = None, mode: bool = True) -> None:
        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'View "settings_variables" ... ')
        if mode:
            self.driver_settings.view(data)
        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'View "settings_variables" ... ')
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to organize settings variable(s)
    def organize_variable_settings(self, settings_obj):

        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'Organize "settings_variables" ... ')

        filter_variables = {**self.variables_lut_base, **self.variables_lut_extra}
        filter_obj = {}
        for filter_tag, filter_keys in filter_variables.items():
            filter_list = filter_keys.split(":")
            filter_value = get_dict_nested_value(settings_obj, filter_list)
            filter_obj[filter_tag] = filter_value

        for filter_tag, filter_keys in filter_variables.items():
            if filter_tag not in list(filter_obj.keys()):
                logger_stream.warning(logger_arrow.warning + 'Variable "' + filter_tag +
                                      '" not found in settings object')
                filter_obj[filter_tag] = None

        # map collector settings
        collector_data.collect(filter_obj)

        # info algorithm (start)
        logger_stream.info(logger_arrow.info(tag='info_method') + 'Organize "settings_variables" ... DONE')

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to configure settings variable(s)
    def configure_variable_settings(self, file_settings: dict = None) -> (dict, dict):

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
        file_env_vars_lut = self.driver_settings.select_variable_algorithm(tag_by_user='lut')
        file_env_vars_format = self.driver_settings.select_variable_algorithm(tag_by_user='format')
        file_env_vars_tmpl = self.driver_settings.select_variable_algorithm(tag_by_user='template')
        # get system variables
        check_env_lut_format = check_keys_of_dict(
            file_env_vars_lut, file_env_vars_format, name1='lut', name2='format')
        check_env_lut_tmpl = check_keys_of_dict(
            file_env_vars_lut, file_env_vars_tmpl, name1='lut', name2='template')

        # select system variable
        self.file_variables = self.driver_settings.select_variable_system(
            lut_by_user=file_env_vars_lut, format_by_user=file_env_vars_format, template_by_user=file_env_vars_tmpl,
            lut_swap=True)

        # update data settings
        self.file_settings = self.driver_settings.update_settings(
            lut_by_user=self.file_variables, format_by_user=file_env_vars_format, template_by_user=file_env_vars_tmpl)

        # # info algorithm (end)
        logging.info(logger_arrow.info(tag='info_method') + 'Configure "settings_variables" ... DONE')

        return self.file_settings, self.file_variables

    # ------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------
