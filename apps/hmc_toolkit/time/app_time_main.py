#!/usr/bin/python3
"""
HMC-SUITE - TIME APP

__date__ = '20241209'
__version__ = '1.0.0'
__author__ =
    'Fabio Delogu (fabio.delogu@cimafoundation.org),
     Andrea Libertino (andrea.libertino@cimafoundation.org)'
__library__ = 'hmc-suite'

General command line:
python app_time_main.py -settings_file configuration.json -time "YYYY-MM-DD HH:MM"

Version(s):
20241209 (1.0.0) --> Beta release for hmc-suite package
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import os
import time

from apps.generic_toolkit.lib_utils_args import get_args
from apps.generic_toolkit.lib_utils_logging import set_logging_stream

from apps.generic_toolkit.lib_default_args import logger_name, logger_format, logger_arrow
from apps.generic_toolkit.lib_default_args import collector_data

from apps.hmc_toolkit.settings.driver_hmc_settings import DrvSettings
from apps.hmc_toolkit.time.driver_hmc_time import DrvTime

# set logger
logger_stream = logging.getLogger(logger_name)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# algorithm information
project_name = 'hmc-suite'
alg_name = 'Application for hmc time'
alg_type = 'Package'
alg_version = '1.0.0'
alg_release = '2024-12-09'
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# script main
def main(collectors_data=None):

    # ------------------------------------------------------------------------------------------------------------------
    # get file settings
    alg_file_settings, alg_time_settings = get_args(settings_folder=os.path.dirname(os.path.realpath(__file__)))

    # method to initialize settings class
    driver_hmc_settings = DrvSettings(file_name=alg_file_settings, time=alg_time_settings,
                                      file_key='info_time')
    # method to configure variable settings
    alg_data_settings, alg_data_variables = driver_hmc_settings.configure_variable_settings()
    # method to organize variable settings
    driver_hmc_settings.organize_variable_settings(alg_data_settings)
    # method to view variable settings
    driver_hmc_settings.view_variable_settings(mode=False)

    # collector data
    collector_data.view()

    # set logging stream
    set_logging_stream(
        logger_name=logger_name, logger_format=logger_format,
        logger_folder=alg_data_settings['log']['folder_name'],
        logger_file=alg_data_settings['log']['file_name'])
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # info algorithm (start)
    logger_stream.info(logger_arrow.arrow_main_break)
    logger_stream.info(logger_arrow.main + alg_name + ' (Version: ' + alg_version + ' Release_Date: ' + alg_release + ')')
    logger_stream.info(logger_arrow.main + 'START ... ')
    logger_stream.info(logger_arrow.arrow_main_blank)

    # time algorithm
    start_time = time.time()
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # class to initialize the hmc time
    driver_hmc_time = DrvTime(
        obj_variables_time=alg_data_settings['variables']['hmc'])
    # configure time variables
    alg_time_obj = driver_hmc_time.configure_time_variables(time_run_cmd=alg_time_settings)
    # organize time variables
    alg_time_info = driver_hmc_time.organize_time_variables(time_obj=alg_time_obj)

    # collector data
    collector_data.view()
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # info algorithm (end)
    alg_time_elapsed = round(time.time() - start_time, 1)

    logger_stream.info(logger_arrow.arrow_main_blank)
    logger_stream.info(logger_arrow.main + alg_name + ' (Version: ' + alg_version + ' Release_Date: ' + alg_release + ')')
    logger_stream.info(logger_arrow.main + 'TIME ELAPSED: ' + str(alg_time_elapsed) + ' seconds')
    logger_stream.info(logger_arrow.main + '... END')
    logger_stream.info(logger_arrow.main + 'Bye, Bye')
    logger_stream.info(logger_arrow.arrow_main_break)
    # ------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call script from external library
if __name__ == "__main__":

    collector_obj = {
        'log': {'folder_name': 'log', 'file_name': 'log.txt'},
        'tmp': {'folder_name': 'tmp','file_name': 'tmp.txt'},
        'time_run': '202312011400'
    }

    main(collectors_data=collector_obj)
# ----------------------------------------------------------------------------------------------------------------------
