#!/usr/bin/python3

"""
HMC-SUITE - TIME APP

__date__ = '20241202'
__version__ = '1.0.0'
__author__ =
    'Fabio Delogu (fabio.delogu@cimafoundation.org),
     Andrea Libertino (andrea.libertino@cimafoundation.org)'
__library__ = 'hmc-suite'

General command line:
python app_settings_main.py -settings_file configuration.json -time "YYYY-MM-DD HH:MM"

Version(s):
20241209 (1.0.0) --> Beta release for hmc-suite package
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import os.path

from apps.generic_toolkit.lib_utils_args import get_args
from apps.generic_toolkit.lib_utils_logging import set_logging_stream

from apps.generic_toolkit.lib_default_args import logger_name, logger_format, logger_arrow
from apps.generic_toolkit.lib_default_args import collector_data

from apps.hmc_toolkit.time.driver_hmc_settings import DrvSettings

# set logger
logger_stream = logging.getLogger(logger_name)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# algorithm information
project_name = 'hmc-suite'
alg_name = 'Application for model time settings'
alg_type = 'Package'
alg_version = '1.0.0'
alg_release = '2024-12-09'
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# script main
def main():

    # ------------------------------------------------------------------------------------------------------------------
    # get file settings
    alg_file_settings, alg_time_settings = get_args(settings_folder=os.path.dirname(os.path.realpath(__file__)))

    # method to initialize settings class
    driver_hmc_settings = DrvSettings(file_name=alg_file_settings, time=alg_time_settings,
                                      file_key='info_time')
    # method to configure variable settings
    alg_data_settings = driver_hmc_settings.configure_variable_settings()
    # method to organize variable settings
    driver_hmc_settings.organize_variable_settings(alg_data_settings)
    # method to view variable settings
    driver_hmc_settings.view_variable_settings()

    # collector data
    collector_data.view_data()

    # set logging stream
    set_logging_stream(
        logger_name=logger_name, logger_format=logger_format,
        logger_folder=alg_data_settings['log']['folder_name'],
        logger_file=alg_data_settings['log']['file_name'])
    # ------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call script from external library
if __name__ == "__main__":
    main()
# ----------------------------------------------------------------------------------------------------------------------
