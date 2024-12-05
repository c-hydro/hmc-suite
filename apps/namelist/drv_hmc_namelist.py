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

from lib_utils_time import convert_time_frequency
from lib_default_namelist import structure_namelist_default, type_namelist_default
from namelist_handler_base import NamelistHandler

#from hmc.algorithm.utils.lib_utils_time import parse_timefrequency_to_timeparts, convert_freqstr_to_freqsecs
#from hmc.algorithm.utils.lib_utils_string import fill_tags2string
#from hmc.algorithm.utils.lib_utils_dict import get_dict_value, get_dict_nested_value
#from hmc.algorithm.namelist.lib_namelist import convert_template_date

#from hmc.algorithm.default.lib_default_namelist import structure_namelist_default, link_namelist_default
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
    # Method class initialization
    def __init__(self, obj_variables_data, obj_variables_user, obj_time, **kwargs):

        self.obj_variables_data_src = obj_variables_data['source']
        self.obj_variables_data_dst = obj_variables_data['destination']

        self.obj_variables_user = obj_variables_user
        self.obj_time = obj_time

        self.tag_folder_name, self.tag_file_name = 'folder_name', 'file_name'

        folder_name_tmp = self.obj_variables_data_src[self.tag_folder_name]
        file_name_tmp = self.obj_variables_data_src[self.tag_file_name]
        self.file_path_src = os.path.join(folder_name_tmp, file_name_tmp)

        folder_name_tmp = self.obj_variables_data_dst[self.tag_folder_name]
        file_name_tmp = self.obj_variables_data_dst[self.tag_file_name]
        self.file_path_dst = os.path.join(folder_name_tmp, file_name_tmp)

        self.type_namelist_default = type_namelist_default
        self.structure_namelist_default = structure_namelist_default

        self.time_frequency_str = self.obj_time['time_frequency']
        self.time_frequency_seconds = convert_time_frequency(self.time_frequency_str)

        # autocomplete fields
        self.autocomplete_fields = {
            'iDt': self.time_frequency_seconds, 'sPathData': ''
        }

        self.autocomplete_flag = {
            'iDt': True, 'sPathData': True
        }

        self.flag_clean_data = True

        self.line_indent = 4 * ' '

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
            file_variables = self.update_namelist_default(tmp_variables, self.type_namelist_default)

            # info read template file (end)
            log_stream.info(' ----> Read template file ... DONE')

        else:

            # info read template obj (start)
            log_stream.info(' ----> Read template object ... ')

            # get namelist data (from default obj)
            tmp_variables = deepcopy(self.structure_namelist_default)
            # update namelist default
            file_variables = self.update_namelist_default(tmp_variables, self.type_namelist_default)

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
                            log_stream.warning(' ===> Namelist format value "' + format_value + '" is not expected')

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
        type_namelist_filled = self.type_namelist_default
        # get autocomplete fields and flags
        autocomplete_fields, autocomplete_flags = self.autocomplete_fields, self.autocomplete_flag

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
                                for auto_key, auto_flag in autocomplete_flags.items():
                                    if auto_key in file_key:
                                        if auto_flag:
                                            auto_value = autocomplete_fields[auto_key]
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
                        log_stream.warning(' ===> Namelist key "' + file_key + '" is not available in the default namelist')

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
    # method to search datasets frequency
    def search_dt(self, lut_dt, key_dt='hmc_file_frequency'):

        obj_datasets = self.obj_datasets

        obj_dt = {}
        for lut_key, lut_value in lut_dt.items():

            if lut_value in list(obj_datasets.keys()):
                obj_structure = obj_datasets[lut_value]

                if isinstance(obj_structure, dict):
                    collections_dt = []
                    for dataset_key, fields_structure in obj_structure.items():
                        if isinstance(fields_structure, dict):
                            list_dt = get_dict_value(fields_structure, key_dt, [])
                            if list_dt.__len__() > 0:
                                digits_dt, alpha_dt = parse_timefrequency_to_timeparts(list_dt)
                                num_dt = convert_freqstr_to_freqsecs(digits_dt, alpha_dt)
                                collections_dt.append(num_dt)

                    if collections_dt.__len__() > 0:

                        collections_dt = list(set(collections_dt))
                        if collections_dt.__len__() > 1:
                            value_dt = min(collections_dt)
                            log_stream.warning(' ===> Datasets dd for "' +
                                               lut_value +
                                               '" is not defined by unique value. To avoid exceptions '
                                               'procedure \n will detect the declared minimum dt "' + str(value_dt) +
                                               '" [seconds] and will set it in the model configuration file\n')

                        elif collections_dt.__len__() == 1:
                            value_dt = collections_dt[0]
                        else:
                            log_stream.error(' ===> Datasets dt is not defined')
                            raise NotImplementedError('Case not implemented yet')
                    else:
                        log_stream.error(' ===> Datasets dt is not correctly defined')
                        raise NotImplementedError('Case not implemented yet')

                    obj_dt[lut_key] = value_dt

        return obj_dt
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to organize namelist
    def organize_namelist(self, time_obj, template_time_ref, template_run_ref, template_run_filled):

        # Starting information
        log_stream.info(' ----> Organize namelist information ... ')

        # Define namelist filename
        filename_namelist_obj = self.set_filename_namelist(template_run_ref, template_run_filled)
        # Define namelist structure
        structure_namelist_obj = self.set_structure_namelist(
            time_obj, template_time_ref, template_run_ref, template_run_filled)

        # Starting information
        log_stream.info(' ----> Organize namelist information ... DONE')

        return filename_namelist_obj, structure_namelist_obj

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to set namelist structure
    def set_structure_namelist(self, obj_time, template_time_ref, template_run_ref, template_run_filled):

        structure_namelist_filled = {}
        for template_run_key, template_run_data in template_run_filled.items():

            obj_time_step = obj_time[template_run_key]

            structure_namelist_tmp = deepcopy(self.structure_namelist_raw)
            link_namelist_raw = self.link_namelist_raw

            link_keys_none = []
            for link_root, link_obj in link_namelist_raw.items():
                for link_key, link_dict in link_obj.items():

                    if isinstance(link_dict, dict):
                        link_type = list(link_dict.keys())[0]
                        link_tags = list(link_dict.values())[0]

                        if link_type == 'algorithm':
                            obj_tmp = self.obj_algorithm
                        elif link_type == 'datasets':
                            obj_tmp = self.obj_datasets
                        elif link_type == 'time':
                            obj_tmp = obj_time_step
                        else:
                            log_stream.error(' ===> Namelist type is not correctly defined')
                            raise ValueError('Dictionary key is wrong')

                        if link_key in list(self.defined_dt.keys()):
                            value_raw = self.defined_dt[link_key]
                        else:
                            value_raw = get_dict_nested_value(obj_tmp, link_tags)

                        if value_raw is None:
                            continue
                        elif isinstance(value_raw, str):
                            template_merge_ref = {**template_run_ref, **template_time_ref}
                            value_filled = fill_tags2string(value_raw, template_merge_ref, template_run_data)
                            value_tmp = convert_template_date(value_filled)
                        else:
                            value_tmp = value_raw
                        structure_namelist_tmp[link_root][link_key] = value_tmp

                    elif link_dict is None:
                        link_keys_none.append(link_key)

            structure_namelist_filled[template_run_key] = structure_namelist_tmp

        return structure_namelist_filled
    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # method to set namelist filename
    def set_filename_namelist(self, template_ref, template_filled):
        filename_namelist_obj = {}
        for template_key, template_data in template_filled.items():
            filename_namelist_def = fill_tags2string(self.filename_namelist_raw, template_ref, template_data)
            filename_namelist_obj[template_key] = filename_namelist_def
        return filename_namelist_obj
    # ------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
