"""
Library Features:

Name:          lib_info_settings
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241202'
Version:       '1.0.0'
"""
# ----------------------------------------------------------------------------------------------------------------------
# libraries
import os
import json
import logging

from copy import deepcopy
from apps.generic_toolkit.lib_utils_envs import get_variable_envs, set_variable_envs
from apps.generic_toolkit.lib_utils_system import (swap_keys_values, get_dict_value,
                                                   fill_tags2string, add_dict_key, flat_dict_key)

from apps.generic_toolkit.lib_default_args import logger_name, logger_arrow, collector_data

# logging
logger_stream = logging.getLogger(logger_name)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to get data settings
def get_data_settings(file_name: str, key_reference: str = 'namelist',
                      delete_keys: list = None):

    if delete_keys is None:
        delete_keys = []

    if os.path.exists(file_name):
        with open(file_name) as file_handle:
            data_settings = json.load(file_handle)
    else:
        logger_stream.error(logger_arrow.error + ' Error in reading settings file "' + file_name + '"')
        raise IOError('File not found')

    if key_reference in list(data_settings.keys()):
        data_reference = data_settings[key_reference]
        data_settings.pop(key_reference)
        data_settings = {**data_settings, **data_reference}

    comment_keys = ['comment', 'comments', '__comments__', '__comment__', '_comment_']
    delete_keys.extend(comment_keys)

    if delete_keys is not None:
        for delete_key in delete_keys:
            if delete_key in list(data_settings.keys()):
                data_settings.pop(delete_key)

    return data_settings
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to get environment settings
def get_variables_env(data_settings: dict, key_list: list = None) -> dict:

    # get variables from settings and collector
    settings_variables = get_dict_value(data_settings, key_list)
    collector_variables = collector_data.retrieve()
    # join variables
    env_variables = {**settings_variables, **collector_variables}

    return env_variables
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to map from environment to local variables
def map_env2loc_settings(env_lut=None):

    # call method to get environment variables
    user_system_obj = swap_keys_values(env_lut)
    env_system_select, env_system_not_select = get_variable_envs(obj_variable_lut=user_system_obj)

    return env_system_select, env_system_not_select
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to map from local to environment variables
def map_loc2env_settings(env_data, env_lut):
    # call method to set environment variables
    return set_variable_envs(env_data, env_lut)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to insert data in collector
def map_loc2collector_settings(env_data):
    collector_data.collect(env_data)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to retrieve data from collector
def map_collector2loc_settings():
    return collector_data.retrieve()
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to update data settings
def update_data_settings(data_settings, env_settings):

    data_flatten = flat_dict_key(data_settings, separator=":")

    data_filled = {}
    for data_key, tmp_value in data_flatten.items():
        if isinstance(tmp_value, str):
            data_value = fill_tags2string(tmp_value, template_keys, template_values)[0]
        else:
            data_value = tmp_value
        data_filled[data_key] = data_value

    data_update = {}
    for tmp_key, data_value in data_filled.items():
        list_key = tmp_key.split(':')
        add_dict_key(data_update, list_key, data_value)

    return data_update
# ----------------------------------------------------------------------------------------------------------------------
