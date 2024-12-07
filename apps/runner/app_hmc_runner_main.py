#!/usr/bin/python3

"""
HMC-SUITE - RUNNER APP

__date__ = '20241202'
__version__ = '1.0.0'
__author__ =
    'Fabio Delogu (fabio.delogu@cimafoundation.org),
     Andrea Libertino (andrea.libertino@cimafoundation.org)'
__library__ = 'hmc-suite'

General command line:
python app_hmc_runner_main.py -settings_file configuration.json -time "YYYY-MM-DD HH:MM"

Version(s):
20241206 (1.0.0) --> Beta release for hmc-suite package
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import time
import argparse

from lib_utils_logging import set_logging_stream
from lib_utils_time import select_time_information

from lib_default_args import logger_name, logger_format, time_format_algorithm
from lib_utils_settings import get_data_settings

from drv_hmc_variables import DrvVariables
from drv_hmc_namelist import DrvNamelist

# set logger
alg_logger = logging.getLogger(logger_name)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# algorithm information
project_name = 'hmc-suite'
alg_name = 'Application for hmc runner'
alg_type = 'Package'
alg_version = '1.0.0'
alg_release = '2024-12-16'
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# script main
def main():

    # ------------------------------------------------------------------------------------------------------------------
    # get file settings
    alg_file_settings, alg_time_settings = get_args()
    # read data settings
    alg_data_settings = get_data_settings(alg_file_settings, key_reference='namelist')
    # set logging
    set_logging_stream(
        logger_name=logger_name, logger_format=logger_format,
        logger_folder=alg_data_settings['log']['folder_name'],
        logger_file=alg_data_settings['log']['file_name'])
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # info algorithm (start)
    alg_logger.info(' ============================================================================ ')
    alg_logger.info(' ==> ' + alg_name + ' (Version: ' + alg_version + ' Release_Date: ' + alg_release + ')')
    alg_logger.info(' ==> START ... ')
    alg_logger.info(' ')

    # time algorithm
    start_time = time.time()
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # organize time information
    alg_time = select_time_information(
        time_run_args=alg_time_settings, time_run_file=alg_data_settings['time']['time_now'],
        time_format=time_format_algorithm,
        time_frequency=alg_data_settings['time']['time_frequency'],
        time_rounding=alg_data_settings['time']['time_rounding'])
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # driver environment variables
    driver_hmc_variables = DrvVariables(
        namelist_version=alg_data_settings['version'],
        namelist_type=alg_data_settings['type'],
        obj_variables_env=alg_data_settings['variables']['environment'],
        obj_variables_hmc=alg_data_settings['variables']['hmc'])
    # organize environment variables information
    alg_variables_env = driver_hmc_variables.select_variables_information(**alg_time)
    # fill environment variables information
    alg_variables_user = driver_hmc_variables.fill_variable_information(alg_variables_env)
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # driver namelist variable(s)
    driver_namelist = DrvNamelist(
        namelist_version=alg_data_settings['version'],
        namelist_type=alg_data_settings['type'],
        obj_variables_data=alg_data_settings['data'],
        obj_variables_user=alg_variables_user,
        obj_variables_hmc=alg_data_settings['variables']['hmc'],
        obj_time=alg_time,
        flag_clean_data=alg_data_settings['flags']['clean_data'])
    # get namelist object
    alg_variables_default = driver_namelist.get_namelist_obj()
    # fill namelist variable(s)
    alg_variables_tmp = driver_namelist.fill_namelist_variables(alg_variables_default)
    # check namelist variable(s)
    alg_variables_defined, alg_variables_checked = driver_namelist.define_namelist_variables(alg_variables_tmp)
    # dump namelist object
    driver_namelist.dump_namelist_obj(alg_variables_defined)
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # info algorithm (end)
    alg_time_elapsed = round(time.time() - start_time, 1)

    alg_logger.info(' ')
    alg_logger.info(' ==> ' + alg_name + ' (Version: ' + alg_version + ' Release_Date: ' + alg_release + ')')
    alg_logger.info(' ==> TIME ELAPSED: ' + str(alg_time_elapsed) + ' seconds')
     alg_logger.info(' ==> ... END')
    alg_logger.info(' ==> Bye, Bye')
    alg_logger.info(' ============================================================================ ')
    # ------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# method to get script argument(s)
def get_args():

    # parser algorithm arg(s)
    parser_obj = argparse.ArgumentParser()
    parser_obj.add_argument('-settings_file', action="store", dest="settings_file")
    parser_obj.add_argument('-time', action="store", dest="settings_time")
    parser_value = parser_obj.parse_args()

    # set algorithm arg(s)
    settings_file, settings_time = 'configuration.json', None
    if parser_value.settings_file:
        settings_file = parser_value.settings_file
    if parser_value.settings_time:
        settings_time = parser_value.settings_time

    return settings_file, settings_time

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# call script from external library
if __name__ == "__main__":
    main()
# ----------------------------------------------------------------------------------------------------------------------
