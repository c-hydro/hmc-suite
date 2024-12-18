"""
Library Features:

Name:          lib_default_method
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20241211'
Version:       '1.0.0'
"""
# ----------------------------------------------------------------------------------------------------------------------
# libraries
import warnings
import pandas as pd

from apps.generic_toolkit.lib_utils_system import flat_dict_key
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to configure data collector
class DataCollector(object):

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataCollector, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def __init__(self, var_name: str = None, var_data: (dict, int, float, list, pd.Timestamp) = None) -> None:

        self.collector_data = {}
        if var_name is not None:
            self.collector_data[var_name] = var_data

    def collect(self, dict_variable: dict = None):

        for key, value in dict_variable.items():
            self.insert_data(info=value, tag=key)

    def retrieve(self):

        collector_data = {}
        for key in list(self.collector_data.keys()):
            data = self.get_data(tag=key)
            collector_data[key] = data
        return collector_data

    def get_data(self, tag: str = None) -> (float, int, list, dict, pd.Timestamp):
        if tag is not None:
            if tag in list(self.collector_data.keys()):
                data = self.collector_data[tag]
            else:
                warnings.warn('Tag is not defined. Data will be not retrieved from a dictionary')
                data = None
        else:
            warnings.warn('Tag is not defined. Data will be not retrieved from a dictionary')
            data = None
        return data

    def insert_data(self, info: (float, int, list, dict, pd.Timestamp) = None, tag: str = None) -> None:
        if tag not in list(self.collector_data.keys()):
            if tag is not None:
                self.collector_data[tag] = info
            else:
                warnings.warn('Tag is not defined. Data will be not stored in a dictionary')
        else:
            warnings.warn('Tag is already defined. Data will be not stored in a dictionary')

    def view_data(self):
        """
        View the data.
        """
        collector_flatten = flat_dict_key(self.collector_data, separator=":")
        collector_dframe = pd.DataFrame.from_dict(collector_flatten, orient='index', columns=['value'])
        print(collector_dframe)

# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# class to configure arrow printer
class ArrowPrinter(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ArrowPrinter, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def __init__(self, arrow_root: str = '--->', arrow_error: str = '===>', arrow_warning: str = '===>',
                 arrow_main: str = '==>',
                 arrow_prefix: str = '-', arrow_suffix: str = '>') -> None:
        self.root = self.__format_arrow(arrow_root)
        self.error = self.__format_arrow(arrow_error)
        self.warning = self.__format_arrow(arrow_warning)

        self.main = self.__format_arrow(arrow_main)
        self.arrow_main_break = ' ============================================================================ '
        self.arrow_main_blank = ' '

        self.arrow_prefix = arrow_prefix
        self.arrow_suffix = arrow_suffix

        self.arrow_dict_tag = {}

    @classmethod
    def reset(cls, arrow_root: str = '--->'):
        class_instance = cls(arrow_root=arrow_root)
        return class_instance

    @staticmethod
    def __format_arrow(arrow_string: str, arrow_pad_start: str = ' ', arrow_pad_end: str = ' ') -> str:
        arrow_string = arrow_string.strip()
        arrow_string = arrow_pad_start + arrow_string + arrow_pad_end
        return arrow_string

    @staticmethod
    def __clean_arrow(arrow_string: str) -> str:
        arrow_string = arrow_string.strip()
        return arrow_string

    def add_prefix(self):
        self.root = self.__clean_arrow(self.root)
        self.root = self.__format_arrow(self.arrow_prefix + self.root)
        return self.root

    def remove_prefix(self):
        self.root = self.__clean_arrow(self.root)
        self.root = self.__format_arrow(self.root[1:])
        return self.root

    def add_suffix(self):
        self.root = self.__clean_arrow(self.root)
        self.root = self.__format_arrow(self.root + self.arrow_suffix)
        return self.root

    def remove_suffix(self):
        self.root = self.__clean_arrow(self.root)
        self.root = self.__format_arrow(self.root[:-1])
        return self.root

    def info(self, mode: int = 1, tag: str = None) -> str:

        if tag not in list(self.arrow_dict_tag.keys()):

            if mode == 1:
                self.root = self.add_prefix()
            elif mode == -1:
                self.root = self.remove_suffix()
            elif mode == 0:
                pass
            else:
                raise NotImplementedError(
                    'Arrow mode must be [1, 0, -1]. Set arrow mode to "' + str(mode) + '" is not expected')

            if tag is not None:
                self.arrow_dict_tag[tag] = self.root

        else:
            self.root = self.arrow_dict_tag[tag]

        return self.root

# ----------------------------------------------------------------------------------------------------------------------
