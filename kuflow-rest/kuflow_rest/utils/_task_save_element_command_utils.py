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

from .._generated.models import TaskElementValue
from ..models import (
    TaskElementValueDocumentItem,
    TaskElementValuePrincipalItem,
    TaskSaveElementCommand,
)
from .element_values import (
    ElementValueSimpleType,
    ElementValueUnion,
    TaskElementValueAccessor,
    add_element_value,
    add_element_value_list,
    find_element_value_as_date,
    find_element_value_as_dict,
    find_element_value_as_document,
    find_element_value_as_float,
    find_element_value_as_principal,
    find_element_value_as_str,
    get_element_value_as_date,
    get_element_value_as_date_list,
    get_element_value_as_dict,
    get_element_value_as_dict_list,
    get_element_value_as_document,
    get_element_value_as_document_list,
    get_element_value_as_float,
    get_element_value_as_float_list,
    get_element_value_as_principal,
    get_element_value_as_principal_list,
    get_element_value_as_str,
    get_element_value_as_str_list,
    get_element_value_valid,
    get_element_value_valid_at,
    set_element_value,
    set_element_value_list,
    set_element_value_valid,
    set_element_value_valid_at,
)


class CurrentElementValueAccessor(TaskElementValueAccessor):
    def __init__(self, task_save_element_command: TaskSaveElementCommand):
        self.task_save_element_command = task_save_element_command

    def set_element_values(self, element_values: List[ElementValueUnion]):
        if len(element_values) == 0:
            self.task_save_element_command.element_values = None
        else:
            self.task_save_element_command.element_values = element_values

    def get_element_values(self) -> List[TaskElementValue]:
        if self.task_save_element_command.element_values is None:
            return []

        return self.task_save_element_command.element_values


class TaskSaveElementCommandUtils:
    @staticmethod
    def get_element_value_valid(
        task_save_element_command: TaskSaveElementCommand,
    ) -> bool:
        """
        Check if all related valid values are TRUE.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            True if all related valid values are TRUE, otherwise False.
        """
        return get_element_value_valid(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_valid_at(
        task_save_element_command: TaskSaveElementCommand,
        index: int,
    ) -> bool:
        """
        Check if the requested valid value at the given index is TRUE.

        Arguments:
            task_save_element_command: The task save element command.

            index: The element value index.

        Returns:
            The requested valid value if it exists, otherwise None.
        """
        return get_element_value_valid_at(
            CurrentElementValueAccessor(task_save_element_command), index
        )

    @staticmethod
    def set_element_value_valid(
        task_save_element_command: TaskSaveElementCommand, valid: Optional[bool]
    ) -> TaskSaveElementCommand:
        """
        Set the valid value for all element values.

        Arguments:
            task_save_element_command: The task save element command.
            valid: The valid value.

        Returns:
            The passed task.
        """
        set_element_value_valid(
            CurrentElementValueAccessor(task_save_element_command), valid
        )

        return task_save_element_command

    @staticmethod
    def set_element_value_valid_at(
        task_save_element_command: TaskSaveElementCommand,
        valid: Optional[bool],
        index: int,
    ) -> TaskSaveElementCommand:
        """
        Set the valid value for the selected element value.

        Arguments:
            task_save_element_command: The task save element command.
            valid: The valid value.
            index: The element value index.

        Returns:
            The passed task.
        """
        set_element_value_valid_at(
            CurrentElementValueAccessor(task_save_element_command), valid, index
        )

        return task_save_element_command

    @staticmethod
    def set_element_value(
        task_save_element_command: TaskSaveElementCommand,
        element_value: Optional[ElementValueSimpleType] = None,
    ) -> TaskSaveElementCommand:
        """
        Set an element value.

        Arguments:
            task_save_element_command: The task save element command.
            element_value: The element value. If the value is None, all current values are removed.

        Returns:
            The passed task.
        """
        set_element_value(
            CurrentElementValueAccessor(task_save_element_command), element_value
        )

        return task_save_element_command

    @staticmethod
    def set_element_value_list(
        task_save_element_command: TaskSaveElementCommand,
        element_values: Optional[List[ElementValueSimpleType]] = None,
    ) -> TaskSaveElementCommand:
        """
        Set an element value.

        Arguments:
            task_save_element_command: The task save element command.
            element_values: The element value. If the value is None or empty, all current values are removed.

        Returns:
            The passed task.
        """
        set_element_value_list(
            CurrentElementValueAccessor(task_save_element_command), element_values
        )

        return task_save_element_command

    @staticmethod
    def add_element_value(
        task_save_element_command: TaskSaveElementCommand,
        element_value: Optional[ElementValueSimpleType] = None,
    ) -> TaskSaveElementCommand:
        """
        Add an element value.

        Arguments:
            task_save_element_command: The task save element command.
            element_value: The element value. If the value is None, all current values are removed.

        Returns:
            The passed task.
        """
        add_element_value(
            CurrentElementValueAccessor(task_save_element_command), element_value
        )

        return task_save_element_command

    @staticmethod
    def add_element_value_list(
        task_save_element_command: TaskSaveElementCommand,
        element_values: Optional[List[ElementValueSimpleType]] = None,
    ) -> TaskSaveElementCommand:
        """
        Add element values.

        Arguments:
            task_save_element_command: The task save element command.
            element_values: The element values. If the values is None or empty, all current values are removed.

        Returns:
            The passed model related object.
        """
        add_element_value_list(
            CurrentElementValueAccessor(task_save_element_command), element_values
        )

        return task_save_element_command

    @staticmethod
    def get_element_value_as_str(
        task_save_element_command: TaskSaveElementCommand,
    ) -> str:
        """
        Get an element as a str.

        Arguments:
            task_save_element_command: The task save element command

        Returns:
            The element value as a str.
        """
        return get_element_value_as_str(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def find_element_value_as_str(
        task_save_element_command: TaskSaveElementCommand,
    ) -> Optional[str]:
        """
        Try to get an element as a str.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a str.
        """
        return find_element_value_as_str(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_str_list(
        task_save_element_command: TaskSaveElementCommand,
    ) -> List[str]:
        """
        Try to get an element as a str list.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element values as a str list.
        """
        return get_element_value_as_str_list(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_float(
        task_save_element_command: TaskSaveElementCommand,
    ) -> float:
        """
        Get an element as a float.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a float.
        """
        return get_element_value_as_float(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def find_element_value_as_float(
        task_save_element_command: TaskSaveElementCommand,
    ) -> float:
        """
        Try to get an element as a float.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a float.
        """
        return find_element_value_as_float(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_float_list(
        task_save_element_command: TaskSaveElementCommand,
    ) -> List[float]:
        """
        Get all elements as a float list.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a float.
        """
        return get_element_value_as_float_list(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_date(
        task_save_element_command: TaskSaveElementCommand,
    ) -> date:
        """
        Get an element as a date.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a date.
        """
        return get_element_value_as_date(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def find_element_value_as_date(
        task_save_element_command: TaskSaveElementCommand,
    ) -> Optional[date]:
        """
        Try to get  an element as a date.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a date.
        """
        return find_element_value_as_date(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_date_list(
        task_save_element_command: TaskSaveElementCommand,
    ) -> Optional[List[date]]:
        """
        Get all elements as date list.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element values as date list.
        """
        return get_element_value_as_date_list(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_dict(
        task_save_element_command: TaskSaveElementCommand,
    ) -> dict:
        """
        Get an element as a dict.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a dict.
        """
        return get_element_value_as_dict(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def find_element_value_as_dict(
        task_save_element_command: TaskSaveElementCommand,
    ) -> Optional[dict]:
        """
        Try to get an element as a dict.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a dict.
        """
        return find_element_value_as_dict(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_dict_list(
        task_save_element_command: TaskSaveElementCommand,
    ) -> Optional[List[dict]]:
        """
        Get all elements as dict list.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element values as dict list.
        """
        return get_element_value_as_dict_list(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_document(
        task_save_element_command: TaskSaveElementCommand,
    ) -> TaskElementValueDocumentItem:
        """
        Get an element as a TaskElementValueDocumentItem.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a TaskElementValueDocumentItem.
        """
        return get_element_value_as_document(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def find_element_value_as_document(
        task_save_element_command: TaskSaveElementCommand,
    ) -> Optional[TaskElementValueDocumentItem]:
        """
        Try to get  an element as a TaskElementValueDocumentItem.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a TaskElementValueDocumentItem.
        """
        return find_element_value_as_document(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_document_list(
        task_save_element_command: TaskSaveElementCommand,
    ) -> List[TaskElementValueDocumentItem]:
        """
        Get all elements as TaskElementValueDocumentItem list.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element values as TaskElementValueDocumentItem list.
        """
        return get_element_value_as_document_list(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_principal(
        task_save_element_command: TaskSaveElementCommand,
    ) -> TaskElementValuePrincipalItem:
        """
        Get an element as a TaskElementValuePrincipalItem.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a TaskElementValuePrincipalItem.
        """
        return get_element_value_as_principal(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def find_element_value_as_principal(
        task_save_element_command: TaskSaveElementCommand,
    ) -> Optional[TaskElementValuePrincipalItem]:
        """
        Try to get  an element as a TaskElementValuePrincipalItem.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element value as a TaskElementValuePrincipalItem.
        """
        return find_element_value_as_principal(
            CurrentElementValueAccessor(task_save_element_command)
        )

    @staticmethod
    def get_element_value_as_principal_list(
        task_save_element_command: TaskSaveElementCommand,
    ) -> List[TaskElementValuePrincipalItem]:
        """
        Get all elements as TaskElementValuePrincipalItem list.

        Arguments:
            task_save_element_command: The task save element command.

        Returns:
            The element values as TaskElementValuePrincipalItem list.
        """
        return get_element_value_as_principal_list(
            CurrentElementValueAccessor(task_save_element_command)
        )
