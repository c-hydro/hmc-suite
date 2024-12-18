"""
Class Features

Name:          namelist_handler_base
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241126'
Version:       '4.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import re
import pandas as pd

from lib_utils_namelist import (filter_namelist_settings, read_namelist_group, parse_namelist_settings,
                                write_namelist_group, select_namelist_type)

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class namelist handler
class NamelistHandler:

    class_type = 'namelist_handler'
    select_namelist = {
        'hmc:3.1.5': select_namelist_type,
        'hmc:3.1.6': select_namelist_type,
        'hmc:3.2.0': select_namelist_type,
        's3m': None
    }

    # initialize class
    def __init__(self, file_name: str, file_method: str = 'r', file_line_indent: str = 4 * ' ') -> None:

        self.file_name = file_name
        if file_method == 'r':
            self.file_stream = open(self.file_name, 'r').read()
        elif file_method == 'w':
            self.file_stream = open(self.file_name, 'w')
        else:
            raise ValueError('File method not recognized.')

        self.group_regular_expression = re.compile(r'&([^&]+)/', re.DOTALL)
        self.line_indent = file_line_indent

    # method to select template
    def select_template(self, namelist_type='hmc', namelist_version='3.1.6'):

        namelist_key = namelist_type + ':' + namelist_version
        namelist_obj = self.select_namelist.get(namelist_key, self.error_data)
        namelist_type, namelist_structure = namelist_obj()

        return namelist_structure, namelist_type

    # method to get data
    def get_data(self, **kwargs):
        """
        Get the namelist data
        """

        settings_lists, comments_lists = filter_namelist_settings(self.file_stream)
        settings_blocks = re.findall(self.group_regular_expression, "\n".join(settings_lists))

        settings_group_raw = read_namelist_group(settings_blocks)
        settings_group_parsed = parse_namelist_settings(settings_group_raw)

        return settings_group_parsed

    # method to error data
    def error_data(self):
        """
        Error data.
        """
        raise NotImplementedError

    # method to write data
    def write_data(self, settings_group: dict) -> None:
        """
        Write the namelist data.
        """

        try:
            for group_name, group_vars in settings_group.items():
                if isinstance(group_vars, list):
                    for variables in group_vars:
                        write_namelist_group(self.file_stream , group_name, variables, self.line_indent)
                else:
                    write_namelist_group(self.file_stream, group_name, group_vars, self.line_indent)
        finally:
            self.file_stream.close()

    # method to view data
    @staticmethod
    def view_data(settings_dict: dict) -> None:
        """
        View the namelist data.
        """

        settings_dframe = pd.DataFrame.from_dict(settings_dict, orient='index', columns=['value'])
        print(settings_dframe)

    # method to check data
    def check_data(self):
        """
        Check if namelist data is available.
        """
        raise NotImplementedError
# ----------------------------------------------------------------------------------------------------------------------
