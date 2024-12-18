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

from lib_utils_namelist import select_namelist_type
from lib_utils_system import swap_keys_values, check_keys_of_dict, create_dict_from_list, fill_tags2string

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
    # global variable(s)
    class_type = 'driver_variables'
    select_namelist = {
        'hmc:3.1.4': select_namelist_type,
        'hmc:3.1.5': select_namelist_type,
        'hmc:3.1.6': select_namelist_type,
        'hmc:3.2.0': select_namelist_type,
        's3m': None
    }
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # class initialization
    def __init__(self, obj_variables_env: dict, obj_variables_hmc: dict,
                 namelist_version: str = '3.1.6', namelist_type: str = 'hmc', **kwargs) -> None:

        self.obj_variables_env_lut = obj_variables_env['lut']
        self.obj_variables_env_format = obj_variables_env['format']
        self.obj_variables_env_tmpl = obj_variables_env['template']

        self.check_variables_env = check_keys_of_dict(
            self.obj_variables_env_lut, self.obj_variables_env_format, name1='lut', name2='format')
        self.check_variables_env = check_keys_of_dict(
            self.obj_variables_env_lut, self.obj_variables_env_tmpl, name1='lut', name2='template')

        self.obj_variables_hmc_info = obj_variables_hmc['complete_by_info']
        self.obj_variables_hmc_pattern = obj_variables_hmc['complete_by_pattern']

        namelist_structure_default = self.select_namelist.get(
            namelist_type + ':' + namelist_version, self.error_variable_information)
        self.namelist_type_default, self.namelist_structure_default = namelist_structure_default()

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to select variables information
    def select_variables_information(self, **kwargs):

        # info algorithm (start)
        log_stream.info(' ---> Select variables information ... ')

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
            time_frequency = kwargs['time_frequency']

        # info parse namelist variables (start)
        log_stream.info(' ----> Parse namelist variables ... ')

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

        # info parse namelist variables (start)
        log_stream.info(' ----> Parse namelist variables ... DONE')

        # info control namelist variables (start)
        log_stream.info(' ----> Check namelist variables ... ')

        # check variable "time_now"
        if 'time_now' not in list(obj_env_select.keys()):
            obj_env_select['time_now'] = time_now
        if obj_env_select['time_now'] is None:
            log_stream.error(' ===> Variable "time_now" is not defined')
            raise RuntimeError('Variable must be defined to correctly set the variables')
        # adjust time now
        obj_env_select['time_now'] = obj_env_select['time_now'].floor(time_rounding.lower())

        # check variable "time_period"
        if obj_env_select['time_period'] is None:
            log_stream.error(' ===> Variable "time_period" is not defined')
            raise RuntimeError('Variable must be defined to correctly set the variables')
        # adjust time period
        obj_env_select['time_period'] = int(obj_env_select['time_period'])

        # check variable "time_restart"
        if 'time_restart' not in list(obj_env_select.keys()):
            obj_env_select['time_restart'] = obj_env_select['time_now'] - pd.Timedelta(1, unit=time_frequency.lower())
        if obj_env_select['time_restart'] is None:
            log_stream.error(' ===> Variable "time_restart" is not defined')
            raise RuntimeError('Variable must be defined to correctly set the variables')
        # add time restart format and template (if needed)
        if 'time_restart' not in list(tmp_variables_env_format.keys()):
            tmp_variables_env_format['time_restart'] = 'timestamp'
        if 'time_restart' not in list(tmp_variables_env_tmpl.keys()):
            tmp_variables_env_tmpl['time_restart'] = deepcopy(tmp_variables_env_tmpl['time_now'])
        # adjust time restart
        obj_env_select['time_restart'] = obj_env_select['time_restart'].floor(time_rounding.lower())

        # info control namelist variables (start)
        log_stream.info(' ----> Check namelist variables ... DONE')

        # info adjust namelist variables (start)
        log_stream.info(' ----> Adjust namelist variables ... ')

        # iterate over variable format and template
        for var_name_alg, var_value_alg in obj_env_select.items():

            var_format_alg = tmp_variables_env_format[var_name_alg]
            var_format_tmpl = tmp_variables_env_tmpl[var_name_alg]

            # convert variable to string
            if var_format_alg == 'timestamp':
                var_value_alg = var_value_alg.strftime(var_format_tmpl)
            elif var_format_alg == 'string':
                var_value_alg = str(var_value_alg)
                var_value_alg = var_value_alg.strip()
            elif var_format_alg == 'int':
                var_value_alg = int(var_value_alg)
            elif var_format_alg == 'float':
                var_value_alg = float(var_value_alg)
            else:
                log_stream.warning(' ===> Variable "' + var_name_alg +
                                   '" format is not expected. Default format the copy of the variable')
                var_value_alg = deepcopy(var_value_alg)

            # store variable
            obj_env_select[var_name_alg] = var_value_alg

        # info adjust namelist variables (end)
        log_stream.info(' ----> Adjust namelist variables ... DONE')

        # info algorithm (end)
        log_stream.info(' ---> Select variables information ... DONE')

        return obj_env_select

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to fill variable information
    def fill_variable_information(self, obj_variable_information, **kwargs):

        # info algorithm (start)
        log_stream.info(' ---> Fill variables information ... ')

        # get hmc variables object(s)
        tmp_variables_hmc = self.obj_variables_hmc_info

        # info manage mandatory variables (start)
        log_stream.info(' ----> Update mandatory variables ... ')
        # check mandatory variables (always required)
        if 'sTimeStart' not in list(tmp_variables_hmc.keys()):
            tmp_variables_hmc['sTimeStart'] = obj_variable_information['time_now']
            log_stream.warning(' ===> Variable "sTimeStart" is not defined. Default value is "time_now"')
        else:
            if isinstance(tmp_variables_hmc['sTimeStart'], pd.Timestamp):
                tmp_format = self.obj_variables_env_tmpl['time_now']
                tmp_variables_hmc['sTimeStart'] = tmp_variables_hmc['sTimeStart'].strftime(tmp_format)
            elif isinstance(tmp_variables_hmc['sTimeStart'], str):
                tmp_format = self.obj_variables_env_tmpl['time_now']
                tmp_variable = pd.Timestamp(tmp_variables_hmc['sTimeStart'])
                tmp_variables_hmc['sTimeStart'] = tmp_variable.strftime(tmp_format)
            else:
                log_stream.error(' ===> Variable "sTimeStart" format is not expected')
                raise RuntimeError('Variable format must be defined to correctly set the variables')
        if 'sTimeRestart' not in list(tmp_variables_hmc.keys()):
            tmp_variables_hmc['sTimeRestart'] = obj_variable_information['time_restart']
            log_stream.warning(' ===> Variable "sTimeRestart" is not defined. Default value is "time_restart"')
        else:
            if isinstance(tmp_variables_hmc['sTimeRestart'], pd.Timestamp):
                tmp_format = self.obj_variables_env_tmpl['time_restart']
                tmp_variables_hmc['sTimeRestart'] = tmp_variables_hmc['sTimeRestart'].strftime(tmp_format)
            elif isinstance(tmp_variables_hmc['sTimeRestart'], str):
                tmp_format = self.obj_variables_env_tmpl['time_restart']
                tmp_variable = pd.Timestamp(tmp_variables_hmc['sTimeRestart'])
                tmp_variables_hmc['sTimeRestart'] = tmp_variable.strftime(tmp_format)
            else:
                log_stream.error(' ===> Variable "sTimeRestart" format is not expected')
                raise RuntimeError('Variable format must be defined to correctly set the variables')
        if 'iSimLength' not in list(tmp_variables_hmc.keys()):
            tmp_variables_hmc['iSimLength'] = int(obj_variable_information['time_period'])
            log_stream.warning(' ===> Variable "iSimLength" is not defined. Default value is "time_period"')
        else:
            if isinstance(tmp_variables_hmc['iSimLength'], int):
                pass
            elif isinstance(tmp_variables_hmc['iSimLength'], str):
                log_stream.warning(' ===> Variable "iSimLength" format is defined by string. Convert to integer')
                tmp_variables_hmc['iSimLength'] = int(tmp_variables_hmc['iSimLength'])
            else:
                log_stream.error(' ===> Variable "iSimLength" format is not expected')
                raise RuntimeError('Variable format must be defined to correctly set the variables')
        # info manage mandatory variables (end)
        log_stream.info(' ----> Update mandatory variables ... DONE')

        # info update namelist variables (start)
        log_stream.info(' ----> Update namelist variables ... ')

        # create template values and tags (to fill the variables)
        template_keys = create_dict_from_list(list(obj_variable_information.keys()), 'string')
        template_values = deepcopy(obj_variable_information)

        # fill hmc variables using template
        obj_env_filled = {}
        for var_name, var_value_tmp in tmp_variables_hmc.items():

            if isinstance(var_value_tmp, str):
                var_value_def = fill_tags2string(var_value_tmp, tags_format=template_keys, tags_filling=template_values)[0]
                obj_env_filled[var_name] = var_value_def
            else:
                obj_env_filled[var_name] = var_value_tmp

        # info update namelist variables (end)
        log_stream.info(' ----> Update namelist variables ... DONE')

        # info update namelist structure (start)
        log_stream.info(' ----> Update namelist structure ... ')

        # iterate over groups
        obj_user_filled = deepcopy(self.namelist_structure_default)
        for var_group, var_fields in self.namelist_structure_default.items():

            # info group (start)
            log_stream.info(' -----> Group "' + var_group + '" ... ')

            if var_group in list(self.namelist_type_default.keys()):
                type_fields = self.namelist_type_default[var_group]

                # iterate over variables
                for var_name, var_value_default in var_fields.items():

                    # manage variable type
                    if var_name in list(type_fields.keys()):
                        type_value = type_fields[var_name]
                    else:
                        log_stream.error(' ===> Variable "' + var_name + '" type is available in type default obj.')
                        raise RuntimeError('Variable type must be defined to correctly set the variables')

                    # manage variable value
                    if var_name in list(obj_env_filled.keys()):
                        var_value_user = obj_env_filled[var_name]
                        obj_user_filled[var_group][var_name] = var_value_user
                    else:
                        if type_value == 'mandatory':
                            obj_user_filled[var_group][var_name] = None
                        else:
                            obj_user_filled[var_group][var_name] = var_value_default

            # info group (end)
            log_stream.info(' -----> Group "' + var_group + '" ... DONE')

        # info update namelist structure (start)
        log_stream.info(' ----> Update namelist structure ... DONE')

        # info algorithm (start)
        log_stream.info(' ---> Fill variables information ... DONE')

        return obj_user_filled
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to return error in selecting variables templates
    def error_variable_information(self):
        log_stream.error(' ===> Namelist type is not available')
        raise RuntimeError('Namelist type must be expected in the version dictionary to correctly set the variables')
    # ------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------
