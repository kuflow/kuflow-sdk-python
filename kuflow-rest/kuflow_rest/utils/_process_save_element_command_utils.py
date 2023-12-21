# coding=utf-8
#
# MIT License
#
# Copyright (c) 2022 KuFlow
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from datetime import date
from typing import List, Optional

from .._generated.models import ProcessElementValue
from ..models import ProcessSaveElementCommand
from .element_values import (
    ElementValueSimpleType,
    ElementValueUnion,
    ProcessElementValueAccessor,
    add_element_value,
    add_element_value_list,
    find_element_value_as_date,
    find_element_value_as_float,
    find_element_value_as_str,
    get_element_value_as_date,
    get_element_value_as_date_list,
    get_element_value_as_float,
    get_element_value_as_float_list,
    get_element_value_as_str,
    get_element_value_as_str_list,
    get_element_value_valid,
    get_element_value_valid_at,
    set_element_value,
    set_element_value_list,
    set_element_value_valid,
    set_element_value_valid_at,
)


class CurrentElementValueAccessor(ProcessElementValueAccessor):
    def __init__(self, process_save_element_command: ProcessSaveElementCommand):
        self.process_save_element_command = process_save_element_command

    def set_element_values(self, element_values: List[ElementValueUnion]):
        if len(element_values) == 0:
            self.process_save_element_command.element_values = None
        else:
            self.process_save_element_command.element_values = element_values

    def get_element_values(self) -> List[ProcessElementValue]:
        if self.process_save_element_command.element_values is None:
            return []

        return self.process_save_element_command.element_values


class ProcessSaveElementCommandUtils:
    @staticmethod
    def get_element_value_valid(
        process_save_element_command: ProcessSaveElementCommand,
    ) -> bool:
        """
        Check if all related valid values are TRUE.

        Arguments:
            process_save_element_command: The process save element command.

        Returns:
            True if all related valid values are TRUE, otherwise False.
        """
        return get_element_value_valid(
            CurrentElementValueAccessor(process_save_element_command)
        )

    @staticmethod
    def get_element_value_valid_at(
        process_save_element_command: ProcessSaveElementCommand,
        index: int,
    ) -> bool:
        """
        Check if the requested valid value at the given index is TRUE.

        Arguments:
            process_save_element_command: The process save element command.
            index: The element value index.

        Returns:
            The requested valid value if it exists, otherwise None.
        """
        return get_element_value_valid_at(
            CurrentElementValueAccessor(process_save_element_command), index
        )

    @staticmethod
    def set_element_value_valid(
        process_save_element_command: ProcessSaveElementCommand, valid: Optional[bool]
    ) -> ProcessSaveElementCommand:
        """
        Set the valid value for all element values.

        Arguments:
            process_save_element_command: The process save element command.
            valid: The valid value.

        Returns:
            The passed process.
        """
        set_element_value_valid(
            CurrentElementValueAccessor(process_save_element_command), valid
        )

        return process_save_element_command

    @staticmethod
    def set_element_value_valid_at(
        process_save_element_command: ProcessSaveElementCommand,
        valid: Optional[bool],
        index: int,
    ) -> ProcessSaveElementCommand:
        """
        Set the valid value for the selected element value.

        Arguments:
            process_save_element_command: The process save element command.
            valid: The valid value.
            index: The element value index.

        Returns:
            The passed process.
        """
        set_element_value_valid_at(
            CurrentElementValueAccessor(process_save_element_command), valid, index
        )

        return process_save_element_command

    @staticmethod
    def set_element_value(
        process_save_element_command: ProcessSaveElementCommand,
        element_value: Optional[ElementValueSimpleType] = None,
    ) -> ProcessSaveElementCommand:
        """
        Set an element value.

        Arguments:
            process_save_element_command: The process save element command.
            element_value: The element value. If the value is None, all current values are removed.

        Returns:
            The passed process.
        """
        set_element_value(
            CurrentElementValueAccessor(process_save_element_command), element_value
        )

        return process_save_element_command

    @staticmethod
    def set_element_value_list(
        process_save_element_command: ProcessSaveElementCommand,
        element_values: Optional[List[ElementValueSimpleType]] = None,
    ) -> ProcessSaveElementCommand:
        """
        Set an element value.

        Arguments:
            process_save_element_command: The process save element command.
            element_values: The element value. If the value is None or empty, all current values are removed.

        Returns:
            The passed process.
        """
        set_element_value_list(
            CurrentElementValueAccessor(process_save_element_command), element_values
        )

        return process_save_element_command

    @staticmethod
    def add_element_value(
        process_save_element_command: ProcessSaveElementCommand,
        element_value: Optional[ElementValueSimpleType] = None,
    ) -> ProcessSaveElementCommand:
        """
        Add an element value.

        Arguments:
            process_save_element_command: The process save element command.
            element_value: The element value. If the value is None, all current values are removed.

        Returns:
            The passed process.
        """
        add_element_value(
            CurrentElementValueAccessor(process_save_element_command), element_value
        )

        return process_save_element_command

    @staticmethod
    def add_element_value_list(
        process_save_element_command: ProcessSaveElementCommand,
        element_values: Optional[List[ElementValueSimpleType]] = None,
    ) -> ProcessSaveElementCommand:
        """
        Add element values.

        Arguments:
            process_save_element_command: The process save element command.
            element_values: The element values. If the values is None or empty, all current values are removed.

        Returns:
            The passed model related object.
        """
        add_element_value_list(
            CurrentElementValueAccessor(process_save_element_command), element_values
        )

        return process_save_element_command

    @staticmethod
    def get_element_value_as_str(
        process_save_element_command: ProcessSaveElementCommand,
    ) -> str:
        """
        Get an element as a str.

        Arguments:
            process_save_element_command: The process save element command.

        Returns:
            The element value as a str.
        """
        return get_element_value_as_str(
            CurrentElementValueAccessor(process_save_element_command)
        )

    @staticmethod
    def find_element_value_as_str(
        process_save_element_command: ProcessSaveElementCommand,
    ) -> Optional[str]:
        """
        Try to get an element as a str.

        Arguments:
            process_save_element_command: The process save element command.

        Returns:
            The element value as a str.
        """
        return find_element_value_as_str(
            CurrentElementValueAccessor(process_save_element_command)
        )

    @staticmethod
    def get_element_value_as_str_list(
        process_save_element_command: ProcessSaveElementCommand,
    ) -> List[str]:
        """
        Try to get an element as a str list.

        Arguments:
            process_save_element_command: The process save element command.

        Returns:
            The element values as a str list.
        """
        return get_element_value_as_str_list(
            CurrentElementValueAccessor(process_save_element_command)
        )

    @staticmethod
    def get_element_value_as_float(
        process_save_element_command: ProcessSaveElementCommand,
    ) -> float:
        """
        Get an element as a float.

        Arguments:
            process_save_element_command: The process save element command.

        Returns:
            The element value as a float.
        """
        return get_element_value_as_float(
            CurrentElementValueAccessor(process_save_element_command)
        )

    @staticmethod
    def find_element_value_as_float(
        process_save_element_command: ProcessSaveElementCommand,
    ) -> float:
        """
        Try to get an element as a float.

        Arguments:
            process_save_element_command: The process save element command.

        Returns:
            The element value as a float.
        """
        return find_element_value_as_float(
            CurrentElementValueAccessor(process_save_element_command)
        )

    @staticmethod
    def get_element_value_as_float_list(
        process_save_element_command: ProcessSaveElementCommand,
    ) -> List[float]:
        """
        Get all elements as a float list.

        Arguments:
            process_save_element_command: The process save element command.

        Returns:
            The element value as a float.
        """
        return get_element_value_as_float_list(
            CurrentElementValueAccessor(process_save_element_command)
        )

    @staticmethod
    def get_element_value_as_date(
        process_save_element_command: ProcessSaveElementCommand,
    ) -> date:
        """
        Get an element as a date.

        Arguments:
            process_save_element_command: The process save element command.

        Returns:
            The element value as a date.
        """
        return get_element_value_as_date(
            CurrentElementValueAccessor(process_save_element_command)
        )

    @staticmethod
    def find_element_value_as_date(
        process_save_element_command: ProcessSaveElementCommand,
    ) -> Optional[date]:
        """
        Try to get  an element as a date.

        Arguments:
            process_save_element_command: The process save element command.

        Returns:
            The element value as a date.
        """
        return find_element_value_as_date(
            CurrentElementValueAccessor(process_save_element_command)
        )

    @staticmethod
    def get_element_value_as_date_list(
        process_save_element_command: ProcessSaveElementCommand,
    ) -> List[date]:
        """
        Get all elements as date list.

        Arguments:
            process_save_element_command: The process save element command.

        Returns:
            The element value as a date.
        """
        return get_element_value_as_date_list(
            CurrentElementValueAccessor(process_save_element_command)
        )
