"""
Library Features:

Name:          lib_utils_system
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241202'
Version:       '1.0.0'
"""
# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import os
import re
import numpy as np

from datetime import datetime
from functools import reduce

from apps.generic_toolkit.lib_default_args import logger_name, logger_arrow

# logging
log_stream = logging.getLogger(logger_name)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to get dict value (using keys list)
def get_dict_value(dictionary: dict, keys: list, default=None):

    if not isinstance(keys, list):
        keys = [keys]
    dictionary = reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys, dictionary)

    return dictionary
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to add dictionary key
def add_dict_key(dictionary: dict, keys: list, value: (str, int, float)):
    if len(keys) == 1:
        dictionary[keys[0]] = value
    else:
        add_dict_key(dictionary.setdefault(keys[0], {}), keys[1:], value)
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to flat dictionary keys
def flat_dict_key(data: dict, parent_key: str = '', separator: str = ":", obj_dict: dict = {}):
    for k, v in data.items():
        key = parent_key + separator + k if parent_key else k
        if isinstance(v, dict):
            if v:
                flat_dict_key(v, key, obj_dict=obj_dict)
            else:
                obj_dict[key] = v
        else:
            obj_dict[key] = v
    return obj_dict
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to check if two dictionaries have the same keys
def check_keys_of_dict(d1, d2, name1='lut', name2='format'):
    if d1.keys() == d2.keys():
        return True
    else:

        list1, list2 = list(set(d1.keys())), list(set(d2.keys()))

        one_not_two = [x for x in list1 if x not in list2]
        two_not_one = [x for x in list2 if x not in list1]

        for key in one_not_two:
            log_stream.error(logger_arrow.error + 'Key "' + key + '" is not in the "' + name2 + '" dictionary')
        for key in two_not_one:
            log_stream.error(logger_arrow.error + 'Key "' + key + '" is not in the "' + name1 + '" dictionary')
        raise ValueError('The two dictionaries have different keys. Add the keys to the dictionaries')

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to swap keys and values in a dictionary
def swap_keys_values(d):
    return {v: k for k, v in d.items()}
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to create a dictionary from a list
def filter_dict_by_keys(dict_obj_in: dict, key_list: list = None,
                        default_value: (int, float, str, None) = None) -> dict:

    if key_list is not None:
        dict_obj_out = {}
        for key_step in key_list:
            if key_step in list(dict_obj_in.keys()):

                tmp_value = dict_obj_in[key_step]
                if isinstance(tmp_value, str):
                    to_remove = re.compile(r"[']")
                    tmp_value = to_remove.sub('', tmp_value)

                dict_obj_out[key_step] = tmp_value
            else:
                log_stream.warning(logger_arrow.warning + 'Variable "' + key_step + '" is not in the dictionary')
                dict_obj_out[key_step] = default_value
    else:
        dict_obj_out = dict_obj_in
    return dict_obj_out
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to convert list to string (given the delimiter)
def convert_list2string(list_data: list, list_delimiter: str = ',') -> str:
    string_data = list_delimiter.join(str(elem) for elem in list_data)
    return string_data
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to add format(s) string (path or filename)
def fill_tags2string(string_raw, tags_format=None, tags_filling=None, tags_template='[TMPL_TAG_{:}]'):

    apply_tags = False
    if string_raw is not None:
        for tag in list(tags_format.keys()):

            if tag in string_raw:
                apply_tags = True
                break

    if apply_tags:

        string_filled = None
        tag_dictionary = {}
        for tag_id, (tag_key, tag_value) in enumerate(tags_format.items()):
            tag_key_tmp = '{' + tag_key + '}'
            if tag_value is not None:

                tag_id = tags_template.format(tag_id)
                tag_dictionary[tag_id] = {'key': None, 'type': None}

                if tag_key_tmp in string_raw:
                    tag_dictionary[tag_id] = {'key': tag_key, 'type': tag_value}
                    string_filled = string_raw.replace(tag_key_tmp, tag_id)
                    string_raw = string_filled
                else:
                    tag_dictionary[tag_id] = {'key': tag_key, 'type': None}

        dim_max = 1
        for tags_filling_values_tmp in tags_filling.values():
            if isinstance(tags_filling_values_tmp, list):
                dim_tmp = tags_filling_values_tmp.__len__()
                if dim_tmp > dim_max:
                    dim_max = dim_tmp

        string_filled_list = [string_filled] * dim_max

        string_filled_def, string_list_key, string_list_value, string_list_type = [], [], [], []
        for string_id, string_filled_step in enumerate(string_filled_list):

            for tag_dict_template, tag_dict_fields in tag_dictionary.items():
                tag_dict_key = tag_dict_fields['key']
                tag_dict_type = tag_dict_fields['type']

                if string_filled_step is not None and tag_dict_template in string_filled_step:
                    if tag_dict_type is not None:

                        if tag_dict_key in list(tags_filling.keys()):

                            value_filling_obj = tags_filling[tag_dict_key]

                            if isinstance(value_filling_obj, list):
                                value_filling = value_filling_obj[string_id]
                            else:
                                value_filling = value_filling_obj

                            string_filled_step = string_filled_step.replace(tag_dict_template, tag_dict_key)

                            if isinstance(value_filling, datetime):
                                tag_dict_value = value_filling.strftime(tag_dict_type)
                            elif isinstance(value_filling, np.datetime64):
                                log_stream.error(logger_arrow.error + 'DateTime64 format is not expected')
                                raise ValueError('DateTime64 is non supported by the method. Use datetime instead')
                            elif isinstance(value_filling, (float, int)):
                                tag_dict_value = tag_dict_key.format(value_filling)
                            else:
                                tag_dict_value = value_filling

                            if tag_dict_value is None:
                                tag_dict_undef = '{' + tag_dict_key + '}'
                                string_filled_step = string_filled_step.replace(tag_dict_key, tag_dict_undef)

                            if tag_dict_value:
                                string_filled_step = string_filled_step.replace(tag_dict_key, tag_dict_value)
                                string_list_key.append(tag_dict_key)
                                string_list_value.append(tag_dict_value)
                                string_list_type.append(tag_dict_type)
                            else:
                                log_stream.warning(logger_arrow.warning + 'The key "' + tag_dict_key + '" for "' +
                                                   string_filled_step +
                                                   '" is not correctly filled; the value is set to NoneType')

            string_filled_def.append(string_filled_step)

        if dim_max == 1:
            if string_filled_def[0]:
                string_filled_out = string_filled_def[0].replace('//', '/')
            else:
                string_filled_out = []
        else:
            string_filled_out = []
            for string_filled_tmp in string_filled_def:
                if string_filled_tmp:
                    string_filled_out.append(string_filled_tmp.replace('//', '/'))

        if "'" in string_filled_out:
            string_filled_out = string_filled_out.replace("'", "")
        if '//' in string_filled_out:
            string_filled_out = string_filled_out.replace('// ', '/')

        return string_filled_out, string_list_key, string_list_value, string_list_type
    else:
        string_list_key, string_list_value, string_list_type = [], [], []
        return string_raw, string_list_key, string_list_value, string_list_type
# ----------------------------------------------------------------------------------------------------------------------
