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
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to get data settings
def get_data_settings(file_name, key_reference='namelist'):
    if os.path.exists(file_name):
        with open(file_name) as file_handle:
            data_settings = json.load(file_handle)
    else:
        logging.error(' ===> Error in reading settings file "' + file_name + '"')
        raise IOError('File not found')

    if key_reference in list(data_settings.keys()):
        data_reference = data_settings[key_reference]
        data_settings.pop(key_reference)

        data_settings = {**data_settings, **data_reference}

    return data_settings
# ----------------------------------------------------------------------------------------------------------------------
