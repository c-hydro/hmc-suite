"""
Class Features

Name:          handler_hmc_settings
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241212'
Version:       '1.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import os
import pandas as pd

from tabulate import tabulate
from copy import deepcopy

from apps.generic_toolkit.lib_utils_settings import get_data_settings

from apps.generic_toolkit.lib_utils_system import (swap_keys_values, filter_dict_by_keys,
                                                   fill_tags2string, add_dict_key, flat_dict_key)

from apps.generic_toolkit.lib_utils_dict import get_dict_value

from apps.generic_toolkit.lib_default_args import time_format_datasets, time_format_algorithm
from apps.generic_toolkit.lib_default_args import logger_name, logger_arrow
from apps.generic_toolkit.lib_default_args import collector_data

# logging
log_stream = logging.getLogger(logger_name)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class settings handler
class SettingsHandler:

    class_type = 'settings_handler'
    excluded_keys = ['__comment__', '_comment_', '__comment', '_comment']

    # initialize class
    def __init__(self, settings_obj: dict = None, system_obj: dict = None,
                 settings_key: (str, None) = 'info_time', **kwargs) -> None:

        self.settings_obj = settings_obj
        self.system_obj = system_obj
        self.variables_obj = {}

        if settings_key is not None:
            if settings_key in list(self.settings_obj.keys()):
                settings_tmp = self.settings_obj[settings_key]
                self.settings_obj.pop(settings_key)
                self.settings_obj = {**self.settings_obj, **settings_tmp}
            else:
                log_stream.error(logger_arrow.error + 'Key "' + settings_key + '" not found in settings object.')
                raise KeyError('Key must be defined.')
        else:
            self.settings_obj = self.settings_obj

        if self.system_obj is None:
            self.system_obj = dict(os.environ)

    @classmethod
    def from_file(cls, file_name: (str, None), file_key: (str, None) = 'info_time',
                  system_settings: dict = None, **kwargs):

        if file_name is not None:
            if os.path.exists(file_name):
                file_settings = get_data_settings(file_name)
            else:
                log_stream.error(logger_arrow.error + 'File "' + file_name + '" does not exists.')
                raise FileNotFoundError('File must be defined.')
        else:
            file_settings = None

        return cls(settings_obj=file_settings, settings_key=file_key, system_obj=system_settings)

    def select_variable_algorithm(self, tag_by_user: str = 'default'):

        if tag_by_user is not None:
            if tag_by_user not in list(self.variables_obj.keys()):
                tmp_obj = get_dict_value(self.settings_obj, tag_by_user)
                tmp_variables = {}
                for tmp_step in tmp_obj:
                    tmp_variables[tmp_step[0]] = tmp_step[1]
                self.variables_obj[tag_by_user] = tmp_variables
            else:
                log_stream.error(logger_arrow.error + 'Tag "' + tag_by_user + '" already exists in variables object.')
                raise KeyError('Tag string cannot overwrite saved keys.')
        else:
            if tag_by_user not in list(self.variables_obj.keys()):
                self.variables_obj[tag_by_user] = self.settings_obj
            else:
                log_stream.error(logger_arrow.error + 'Tag "' + tag_by_user + '" already exists in variables object.')
                raise KeyError('Tag string cannot overwrite saved keys.')

        return self.variables_obj[tag_by_user]

    def update_settings(self, lut_by_user: dict = None, format_by_user: dict = None, template_by_user: dict = None):

        if (lut_by_user is not None) and (template_by_user is not None):

            settings_flatten = flat_dict_key(self.settings_obj, separator=":", obj_dict={})

            settings_filled = {}
            for data_key, tmp_value in settings_flatten.items():
                if isinstance(tmp_value, str):
                    data_value = fill_tags2string(tmp_value, template_by_user, lut_by_user)[0]
                else:
                    data_value = tmp_value
                settings_filled[data_key] = data_value

            settings_update = {}
            for tmp_key, data_value in settings_filled.items():
                list_key = tmp_key.split(':')
                if list_key[-1] not in self.excluded_keys:
                    add_dict_key(settings_update, list_key, data_value)
                else:
                    log_stream.warning(logger_arrow.warning + 'Settings "' + str(list_key) +
                                       '" removed from settings object. Excluded key found.')

            self.settings_obj = settings_update

        return self.settings_obj

    def select_variable_system(self, lut_by_user: dict = None,
                               format_by_user: dict = None, template_by_user: dict = None,
                               lut_swap: bool = False, default_value: {int, float, bool } = None):

        lut_by_system = deepcopy(lut_by_user)
        if lut_by_user is not None:
            if lut_swap:
                lut_collection = swap_keys_values(lut_by_user)
            else:
                lut_collection = lut_by_user
            self.system_obj = filter_dict_by_keys(self.system_obj, list(lut_collection.keys()))

            lut_by_system = {}
            for lut_key, lut_value in lut_collection.items():

                if lut_swap:
                    lut_tag_user, lut_tag_sys = lut_value, lut_key
                else:
                    lut_tag_user, lut_tag_sys = lut_key, lut_value

                lut_format = None
                if lut_tag_user in list(format_by_user.keys()):
                    lut_format = format_by_user[lut_tag_user]
                lut_tmpl = None
                if lut_tag_user in list(template_by_user.keys()):
                    lut_tmpl = template_by_user[lut_tag_user]
                if lut_tag_sys in list(self.system_obj.keys()):

                    value_tmp = self.system_obj[lut_tag_sys]

                    if value_tmp is not None:
                        if lut_format is not None:
                            if lut_format == 'string':
                                value_def = str(value_tmp)
                            elif lut_format == 'int':
                                value_def = int(value_tmp)
                            elif lut_format == 'float':
                                value_def = float(value_tmp)
                            elif lut_format == 'bool':
                                value_def = bool(value_tmp)
                            elif lut_format == 'timestamp':
                                value_def = pd.Timestamp(value_tmp).strftime(lut_tmpl)
                            else:
                                log_stream.error(logger_arrow.error + 'Format "' + str(lut_format) +
                                                 '" not expected.')
                                raise NotImplementedError('Case not implemented yet.')
                        else:
                            log_stream.warning(logger_arrow.warning + 'Variable "'
                                               + lut_tag_user + '" format is not defined.')
                            value_def = value_tmp
                    else:
                        log_stream.warning(logger_arrow.warning + 'Variable "'
                                           + lut_tag_user + '" value is defined by default value "' +
                                           str(default_value) + '"')
                        value_def = default_value

                    lut_by_system[lut_tag_user] = value_def

        return lut_by_system

    # method to freeze data
    def freeze(self):
        """
        Error time data.
        """
        raise NotImplementedError

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
    def view(self, table_data: dict = None,
             table_variable='variables', table_values='values', table_format='psql') -> None:
        """
        View the time data.
        """

        if table_data is None:
            table_data = self.settings_obj

        table_dict = flat_dict_key(data=table_data, separator=":", obj_dict={})
        table_dframe = pd.DataFrame.from_dict(table_dict, orient='index', columns=['value'])

        table_obj = tabulate(
            table_dframe,
            headers=[table_variable, table_values],
            floatfmt=".5f",
            showindex=True,
            tablefmt=table_format,
            missingval='N/A'
        )

        print(table_obj)

    # method to check data
    def check(self):
        """
        Check if time data is available.
        """
        raise NotImplementedError
# ----------------------------------------------------------------------------------------------------------------------
