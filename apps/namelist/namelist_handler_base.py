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

from lib_namelist_utils import filter_settings, group_settings, parse_settings, write_namelist_file
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class namelist handler
class NamelistHandler:

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

    # method to get data
    def get_data(self, **kwargs):
        """
        Get the namelist data
        """

        settings_lists, comments_lists = filter_settings(self.file_stream)
        settings_blocks = re.findall(self.group_regular_expression, "\n".join(settings_lists))

        settings_group_raw = group_settings(settings_blocks)
        settings_group_parsed = parse_settings(settings_group_raw)

        return settings_group_parsed

    def error_data(self):
        """
        Error data.
        """
        raise NotImplementedError
    
    def write_data(self, settings_group_parsed: dict) -> None:
        """
        Write the namelist data
        """
        write_namelist_file(self.file_stream, settings_group_parsed, line_indent=self.line_indent)

    @staticmethod
    def view_data(settings_dict: dict) -> None:
        """
        View the data.
        """

        settings_dframe = pd.DataFrame.from_dict(settings_dict, orient='index', columns=['value'])
        print(settings_dframe)

    def check_data(self):
        """
        Check if data is available.
        """
        raise NotImplementedError
# ----------------------------------------------------------------------------------------------------------------------
