"""
Class Features

Name:          drv_hmc_namelist
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241126'
Version:       '4.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import os

from copy import deepcopy

from lib_utils_namelist import select_namelist_type
from lib_utils_time import convert_time_frequency
from handler_hmc_namelist import NamelistHandler

from lib_default_args import logger_name

# logging
log_stream = logging.getLogger(logger_name)

# debugging
# import matplotlib.pylab as plt
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to configure namelist
class DrvNamelist:

    # ------------------------------------------------------------------------------------------------------------------
    # global variable(s)
    class_type = 'namelist_driver'
    select_namelist = {
        'hmc:3.1.4': select_namelist_type,
        'hmc:3.1.5': select_namelist_type,
        'hmc:3.1.6': select_namelist_type,
        'hmc:3.2.0': select_namelist_type,
        's3m': None
    }
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Method class initialization
    def __init__(self, obj_variables_data: dict, obj_variables_user: dict, obj_variables_hmc: dict, obj_time: dict,
                 namelist_version: str = '3.1.6', namelist_type: str = 'hmc',
                 flag_clean_data: bool = True, **kwargs) -> None:

        self.obj_variables_data_src = obj_variables_data['source']
        self.obj_variables_data_dst = obj_variables_data['destination']

        self.obj_variables_user = obj_variables_user

        self.obj_variables_hmc_info = obj_variables_hmc['complete_by_info']
        self.obj_variables_hmc_pattern = obj_variables_hmc['complete_by_pattern']

        self.namelist_version, self.namelist_type = namelist_version, namelist_type

        self.obj_time = obj_time

        self.tag_folder_name, self.tag_file_name = 'folder_name', 'file_name'

        folder_name_tmp = self.obj_variables_data_src[self.tag_folder_name]
        file_name_tmp = self.obj_variables_data_src[self.tag_file_name]
        self.file_path_src = os.path.join(folder_name_tmp, file_name_tmp)

        folder_name_tmp = self.obj_variables_data_dst[self.tag_folder_name]
        file_name_tmp = self.obj_variables_data_dst[self.tag_file_name]
        self.file_path_dst = os.path.join(folder_name_tmp, file_name_tmp)

        self.time_frequency_str = self.obj_time['time_frequency']
        self.time_frequency_seconds = convert_time_frequency(self.time_frequency_str)

        self.flag_clean_data = flag_clean_data
        self.line_indent = 4 * ' '

        namelist_structure_obj = self.select_namelist.get(
            namelist_type + ':' + namelist_version, self.error_variable_information)
        self.namelist_type_default, self.namelist_structure_default = namelist_structure_obj()

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to dump namelist object
    def dump_namelist_obj(self, namelist_variables):

        # info algorithm (start)
        log_stream.info(' ---> Dump namelist information ... ')

        # write namelist file path
        file_path_dst = self.file_path_dst
        if self.flag_clean_data:
            if os.path.exists(file_path_dst):
                os.remove(file_path_dst)

        # check file namelist availability
        if not os.path.exists(file_path_dst):

            # info read template file (start)
            log_stream.info(' ----> Write namelist template ... ')

            # create folder (if needed)
            folder_name, file_name = os.path.split(file_path_dst)
            os.makedirs(folder_name, exist_ok=True)

            # write namelist file
            driver_handler_namelist = NamelistHandler(file_path_dst, file_method='w')
            driver_handler_namelist.write_data(namelist_variables)

            # info algorithm (end)
            log_stream.info(' ---> Dump namelist information ... DONE')

        else:

            # info algorithm (end)
            log_stream.info(' ---> Dump namelist information ... SKIPPED. File already exists')

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to select namelist object
    def get_namelist_obj(self):

        # info algorithm (start)
        log_stream.info(' ---> Get namelist information ... ')

        # get namelist file path
        file_path_src = self.file_path_src
        # check file namelist availability
        if os.path.exists(file_path_src):

            # info read template file (start)
            log_stream.info(' ----> Read template file ... ')

            # read namelist file
            driver_handler_namelist = NamelistHandler(file_path_src, file_method='r')
            # get namelist data (from default file)
            tmp_variables = driver_handler_namelist.get_data()
            # update namelist default
            file_variables = self.update_namelist_default(tmp_variables, self.namelist_type_default)

            # info read template file (end)
            log_stream.info(' ----> Read template file ... DONE')

        else:

            # info read template obj (start)
            log_stream.info(' ----> Read template object ... ')

            # get namelist data (from default obj)
            tmp_variables = deepcopy(self.namelist_structure_default)
            # update namelist default
            file_variables = self.update_namelist_default(tmp_variables, self.namelist_type_default)

            # info read template obj (end)
            log_stream.info(' ----> Read template object ... DONE')

        # info algorithm (start)
        log_stream.info(' ---> Get namelist information ... DONE')

        return file_variables

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to update namelist default
    @staticmethod
    def update_namelist_default(namelist_variables_default, namelist_type_default):

        # iterate over namelist groups
        namelist_variables_update, namelist_variable_mandatory = {}, []
        for file_group, file_fields in namelist_variables_default.items():

            # info check group (start)
            log_stream.info(' ----> Group "' + file_group + '" ... ')

            # check group fields in the default namelist
            if file_group in list(namelist_type_default.keys()):
                # get default namelist fields
                format_fields = namelist_type_default[file_group]

                # iterate over namelist fields
                namelist_variables_update[file_group] = {}
                for file_key, file_value in file_fields.items():

                    # check key fields in the default namelist
                    if file_key in list(format_fields.keys()):
                        # get default namelist value
                        format_value = format_fields[file_key]

                        # check namelist value and type
                        namelist_variables_update[file_group][file_key] = {}
                        if format_value == 'mandatory':
                            namelist_variables_update[file_group][file_key] = None
                            namelist_variable_tag = file_group + ':' + file_key
                            namelist_variable_mandatory.append(namelist_variable_tag)
                        elif format_value == 'default' or format_value == 'ancillary':
                            namelist_variables_update[file_group][file_key] = file_value
                        else:
                            log_stream.warning(' ===> Namelist format value "' + str(format_value) + '" is not expected')

                    else:
                        # warning message
                        log_stream.warning(' ===> Namelist key "' + file_key + '" is not available in the default namelist')

            else:
                # error message
                log_stream.error(' ===> Namelist group "' + file_group + '" is not available in the default namelist')
                raise TypeError('Group "' + file_group + '" is not defined')
            # info check group (end)
            log_stream.info(' ----> Group "' + file_group + '" ... DONE')

        # info mandatory variable(s)
        log_stream.info(' ----> Variable defined by mandatory flag ... ')
        for variable_n, variable_step in enumerate(namelist_variable_mandatory):
            log_stream.info(' -----> Variable "' + variable_step + '"')
        log_stream.info(' ----> Variable defined by mandatory flag ... DONE')

        # info algorithm (end)
        log_stream.info(' ---> Check namelist information ... DONE')

        return namelist_variables_update

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to fill namelist default
    def fill_namelist_variables(self, file_variables_generic):

        # info algorithm (start)
        log_stream.info(' ---> Fill namelist information ... ')

        # get namelist user variables
        file_variables_user = self.obj_variables_user

        # get namelist generic variables
        file_variables_filled = deepcopy(file_variables_generic)

        # iterate over namelist user variables
        for file_key, file_value in file_variables_user.items():
            if file_key in file_variables_filled:
                file_variables_filled[file_key] = file_value
            else:
                log_stream.warning(' ===> Namelist key "' + file_key + '" is not correctly defined')

        # info algorithm (start)
        log_stream.info(' ---> Fill namelist information ... DONE')

        return file_variables_filled

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to check namelist variables
    def define_namelist_variables(self, file_variables_generic):

        # info algorithm (start)
        log_stream.info(' ---> Check namelist information ... ')

        # get namelist default type(s)
        type_namelist_filled = self.namelist_type_default
        # get autocomplete fields and flags
        file_variables_hmc_by_pattern = self.obj_variables_hmc_pattern

        # iterate over namelist groups
        file_variables_defined, file_variables_checked = {}, {}
        for file_group, file_fields in file_variables_generic.items():

            # info check group (start)
            log_stream.info(' ----> Group "' + file_group + '" ... ')

            # check group fields in the default namelist
            if file_group in list(type_namelist_filled.keys()):
                # get default namelist fields
                format_fields = type_namelist_filled[file_group]

                # iterate over namelist fields
                file_variables_checked[file_group], file_variables_defined[file_group] = {}, {}
                for file_key, file_value in file_fields.items():

                    # check key fields in the default namelist
                    if file_key in list(format_fields.keys()):
                        # get default namelist value
                        format_value = format_fields[file_key]

                        # check namelist value and type
                        file_variables_checked[file_group][file_key], file_variables_defined[file_group][file_key] = {}, {}
                        if format_value == 'mandatory':
                            if file_value is None:

                                auto_value = None
                                for key_pattern, fields_pattern in file_variables_hmc_by_pattern.items():

                                    pattern_active = fields_pattern['active']
                                    pattern_tmpl, pattern_value = fields_pattern['template'], fields_pattern['value']

                                    if pattern_tmpl in file_key:
                                        if pattern_active:
                                            auto_value = deepcopy(pattern_value)
                                            log_stream.warning(
                                                ' ===> Namelist variable "' + file_key +
                                                '" auto completed by value "' + str(auto_value) + '"')

                                if auto_value is None:
                                    log_stream.error(' ===> Namelist key "' + file_key + '" is not defined')
                                    raise TypeError('Field mandatory value "' + file_key +
                                                    '" is not defined or defined by NoneType')

                                file_variables_defined[file_group][file_key] = auto_value
                            else:
                                file_variables_checked[file_group][file_key] = True
                                file_variables_defined[file_group][file_key] = file_value
                        elif format_value == 'default' or format_value == 'ancillary':
                            file_variables_checked[file_group][file_key] = True
                            file_variables_defined[file_group][file_key] = file_value
                        else:
                            log_stream.warning(' ===> Namelist format value "' + format_value + '" is not expected')

                    else:
                        # warning message
                        log_stream.warning(' ===> Namelist key "' + file_key +
                                           '" is not available in the default namelist')

            else:
                # error message
                log_stream.error(' ===> Namelist group "' + file_group + '" is not available in the default namelist')
                raise TypeError('Group "' + file_group + '" is not defined')

            # info check group (end)
            log_stream.info(' ----> Group "' + file_group + '" ... DONE')

        # info algorithm (end)
        log_stream.info(' ---> Check namelist information ... DONE')

        return file_variables_defined, file_variables_checked

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to return error in selecting variables templates
    def error_variable_information(self):
        log_stream.error(' ===> Namelist type is not available')
        raise RuntimeError('Namelist type must be expected in the version dictionary to correctly set the variables')
    # ------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
