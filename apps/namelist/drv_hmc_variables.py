"""
Class Features

Name:          drv_hmc_variables
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241126'
Version:       '4.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import os
import pandas as pd

from copy import deepcopy

from lib_utils_system import swap_keys_values, check_keys_of_dict, create_dict_from_list, fill_tags2string

from lib_default_namelist import structure_namelist_default, type_namelist_default
from lib_default_args import logger_name

# logging
log_stream = logging.getLogger(logger_name)

# debugging
# import matplotlib.pylab as plt
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to configure variables
class DrvVariables:

    # ------------------------------------------------------------------------------------------------------------------
    # class initialization
    def __init__(self, obj_variables_env, obj_variables_hmc, **kwargs):

        self.obj_variables_env_lut = obj_variables_env['lut']
        self.obj_variables_env_format = obj_variables_env['format']
        self.obj_variables_env_tmpl = obj_variables_env['template']

        self.check_variables_env = check_keys_of_dict(
            self.obj_variables_env_lut, self.obj_variables_env_format, name1='lut', name2='format')
        self.check_variables_env = check_keys_of_dict(
            self.obj_variables_env_lut, self.obj_variables_env_tmpl, name1='lut', name2='template')

        self.obj_variables_hmc = obj_variables_hmc

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to select variables information
    def select_variables_information(self, **kwargs):

        # get environment variables object(s)
        tmp_variables_env_lut = swap_keys_values(self.obj_variables_env_lut)
        tmp_variables_env_format = self.obj_variables_env_format
        tmp_variables_env_tmpl = self.obj_variables_env_tmpl

        # defined time now and time rounding
        time_now, time_restart, time_rounding, time_frequency = None, None, 'H', 'H'
        if 'time_now' in kwargs:
            time_now = kwargs['time_now']
        if 'time_restart' in kwargs:
            time_restart = kwargs['time_restart']
        if 'time_rounding' in kwargs:
            time_rounding = kwargs['time_rounding']
        if 'time_frequency' in kwargs:
            time_rounding = kwargs['time_frequency']

        # iterate over variable lut and template
        obj_env_system, obj_env_select = os.environ, {}
        for var_name_system, var_value_system in obj_env_system.items():

            if var_name_system in tmp_variables_env_lut.keys():

                var_name_alg = tmp_variables_env_lut[var_name_system]
                var_format_alg = tmp_variables_env_format[var_name_alg]

                if var_format_alg == 'int':
                    var_value_alg = int(var_value_system)
                elif var_format_alg == 'float':
                    var_value_alg = float(var_value_system)
                elif var_format_alg == 'string':
                    var_value_alg = str(var_value_system)
                elif var_format_alg == 'bool':
                    var_value_alg = bool(var_value_system)
                elif var_format_alg == 'timestamp':
                    var_value_alg = pd.Timestamp(var_value_system)
                else:
                    log_stream.warning(' ===> Variable "' + var_name_alg +
                                       '" format is not expected. Default format is "str"')
                    var_value_alg = str(var_value_system)

                obj_env_select[var_name_alg] = var_value_alg

        # check variable "time_now"
        if 'time_now' not in list(obj_env_select.keys()):
            obj_env_select['time_now'] = time_now
        if obj_env_select['time_now'] is None:
            log_stream.error(' ===> Variable "time_now" is not defined')
            raise RuntimeError('Variable must be defined to correctly set the variables')
        # adjust time now
        obj_env_select['time_now'] = obj_env_select['time_now'].floor(time_rounding)

        # check variable "time_period"
        if obj_env_select['time_period'] is None:
            log_stream.error(' ===> Variable "time_period" is not defined')
            raise RuntimeError('Variable must be defined to correctly set the variables')
        # adjust time period
        obj_env_select['time_period'] = int(obj_env_select['time_period'])

        # check variable "time_restart"
        if 'time_restart' not in list(obj_env_select.keys()):
            obj_env_select['time_restart'] = obj_env_select['time_now'] - pd.Timedelta(1, unit=time_frequency)

        if 'time_restart' not in list(tmp_variables_env_format.keys()):
            tmp_variables_env_format['time_restart'] = 'timestamp'
        if 'time_restart' not in list(tmp_variables_env_tmpl.keys()):
            tmp_variables_env_tmpl['time_restart'] = deepcopy(tmp_variables_env_tmpl['time_now'])

        # iterate over variable format and template
        for var_name_alg, var_value_alg in obj_env_select.items():

            var_format_alg = tmp_variables_env_format[var_name_alg]
            var_format_tmpl = tmp_variables_env_tmpl[var_name_alg]
            if var_format_alg == 'timestamp':
                var_value_alg = var_value_alg.strftime(var_format_tmpl)
            else:
                if isinstance(var_value_alg, str):
                    pass
                else:
                    var_value_alg = str(var_value_alg)
            var_value_alg = var_value_alg.strip()

            obj_env_select[var_name_alg] = var_value_alg

        return obj_env_select

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to fill variable information
    def fill_variable_information(self, obj_variable_information, **kwargs):

        tmp_variables_hmc = self.obj_variables_hmc

        if 'sTimeStart' not in list(tmp_variables_hmc.keys()):
            tmp_variables_hmc['sTimeStart'] = obj_variable_information['time_restart']
        if 'sTimeRestart' not in list(tmp_variables_hmc.keys()):
            tmp_variables_hmc['sTimeRestart'] = obj_variable_information['time_restart']
        if 'iSimLength' not in list(tmp_variables_hmc.keys()):
            tmp_variables_hmc['iSimLength'] = obj_variable_information['time_period']

        template_keys = create_dict_from_list(list(obj_variable_information.keys()), 'string')
        template_values = deepcopy(obj_variable_information)

        obj_env_filled = {}
        for var_name, var_value_tmp in tmp_variables_hmc.items():

            if isinstance(var_value_tmp, str):
                var_value_def = fill_tags2string(var_value_tmp, tags_format=template_keys, tags_filling=template_values)[0]
                obj_env_filled[var_name] = var_value_def
            else:
                obj_env_filled[var_name] = var_value_tmp

        # organize user variables
        obj_user_filled = deepcopy(structure_namelist_default)
        for var_group, var_fields in structure_namelist_default.items():

            if var_group in list(type_namelist_default.keys()):
                type_fields = type_namelist_default[var_group]

                for var_name, var_value_default in var_fields.items():

                    if var_name in list(type_fields.keys()):
                        type_value = type_fields[var_name]
                    else:
                        log_stream.error(' ===> Variable "' + var_name + '" type is available in type default obj.')
                        raise RuntimeError('Variable type must be defined to correctly set the variables')

                    if var_name in list(obj_env_filled.keys()):
                        var_value_user = obj_env_filled[var_name]
                        obj_user_filled[var_group][var_name] = var_value_user
                    else:
                        if type_value == 'mandatory':
                            obj_user_filled[var_group][var_name] = None
                        else:
                            obj_user_filled[var_group][var_name] = var_value_default

        return obj_user_filled
    # ------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------
