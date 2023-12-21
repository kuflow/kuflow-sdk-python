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

from kuflow_rest.models import TaskElementValue, TaskElementValueDocumentItem, TaskElementValuePrincipalItem
from kuflow_rest.utils import ElementValueSimpleType, ElementValueUnion, TaskElementValueAccessor
from kuflow_rest.utils.element_values import (
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

from ..models import SaveTaskElementRequest


class CurrentAccessor(TaskElementValueAccessor):
    def __init__(self, request: SaveTaskElementRequest):
        self.request = request

    def set_element_values(self, element_values: List[ElementValueUnion]):
        if len(element_values) == 0:
            self.request.element_values = None
        else:
            self.request.element_values = element_values

    def get_element_values(self) -> List[TaskElementValue]:
        if self.request.element_values is None or len(self.request.element_values) == 0:
            return []

        return self.request.element_values


class SaveTaskElementRequestUtils:
    @staticmethod
    def get_element_value_valid(request: SaveTaskElementRequest) -> bool:
        """
        Check if all related valid values are TRUE.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            True if all related valid values are TRUE, otherwise False.
        """
        return get_element_value_valid(CurrentAccessor(request))

    @staticmethod
    def get_element_value_valid_at(request: SaveTaskElementRequest, index: int) -> bool:
        """
        Check if the requested valid value at the given index is TRUE.

        Arguments:
            request: The SaveTaskElement request.
            index: The element value index.

        Returns:
            The requested valid value if it exists, otherwise None.
        """
        return get_element_value_valid_at(CurrentAccessor(request), index)

    @staticmethod
    def set_element_value_valid(request: SaveTaskElementRequest, valid: Optional[bool]) -> SaveTaskElementRequest:
        """
        Set the valid value for all element values.

        Arguments:
            request: The SaveTaskElement request.
            valid: The valid value.

        Returns:
            The passed task.
        """
        set_element_value_valid(CurrentAccessor(request), valid)

        return request

    @staticmethod
    def set_element_value_valid_at(
        request: SaveTaskElementRequest, valid: Optional[bool], index: int
    ) -> SaveTaskElementRequest:
        """
        Set the valid value for all element values.

        Arguments:
            request: The SaveTaskElement request.
            valid: The valid value.
            index: The element value index.

        Returns:
            The passed task.
        """
        set_element_value_valid_at(CurrentAccessor(request), valid, index)

        return request

    @staticmethod
    def set_element_value(
        request: SaveTaskElementRequest, element_value: Optional[ElementValueSimpleType] = None
    ) -> SaveTaskElementRequest:
        """
        Set an element value.

        Arguments:
            request: The SaveTaskElement request.
            element_value: The element value. If the value is None, all current values are removed.

        Returns:
            The passed task.
        """
        set_element_value(CurrentAccessor(request), element_value)

        return request

    @staticmethod
    def set_element_value_list(
        request: SaveTaskElementRequest, element_values: Optional[List[ElementValueSimpleType]] = None
    ) -> SaveTaskElementRequest:
        """
        Set an element value.

        Arguments:
            request: The SaveTaskElement request.
            element_values: The element value. If the value is None or empty, all current values are removed.

        Returns:
            The passed task.
        """
        set_element_value_list(CurrentAccessor(request), element_values)

        return request

    @staticmethod
    def add_element_value(
        request: SaveTaskElementRequest, element_value: Optional[ElementValueSimpleType] = None
    ) -> SaveTaskElementRequest:
        """
        Add an element value.

        Arguments:
            request: The SaveTaskElement request.
            element_value: The element value. If the value is None, all current values are removed.

        Returns:
            The passed task.
        """
        add_element_value(CurrentAccessor(request), element_value)

        return request

    @staticmethod
    def add_element_value_list(
        request: SaveTaskElementRequest, element_values: Optional[List[ElementValueSimpleType]] = None
    ) -> SaveTaskElementRequest:
        """
        Add element values.

        Arguments:
            request: The SaveTaskElement request.
            element_values: The element values. If the values is None or empty, all current values are removed.

        Returns:
            The passed model related object.
        """
        add_element_value_list(CurrentAccessor(request), element_values)

        return request

    @staticmethod
    def get_element_value_as_str(request: SaveTaskElementRequest) -> str:
        """
        Get an element as a str.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a str.
        """
        return get_element_value_as_str(CurrentAccessor(request))

    @staticmethod
    def find_element_value_as_str(request: SaveTaskElementRequest) -> Optional[str]:
        """
        Try to get an element as a str.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a str.
        """
        return find_element_value_as_str(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_str_list(request: SaveTaskElementRequest) -> List[str]:
        """
        Try to get an element as a str list.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element values as a str list.
        """
        return get_element_value_as_str_list(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_float(request: SaveTaskElementRequest) -> float:
        """
        Get an element as a float.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a float.
        """
        return get_element_value_as_float(CurrentAccessor(request))

    @staticmethod
    def find_element_value_as_float(request: SaveTaskElementRequest) -> float:
        """
        Try to get an element as a float.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a float.
        """
        return find_element_value_as_float(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_float_list(request: SaveTaskElementRequest) -> List[float]:
        """
        Get all elements as a float list.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a float.
        """
        return get_element_value_as_float_list(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_date(request: SaveTaskElementRequest) -> date:
        """
        Get an element as a date.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a date.
        """
        return get_element_value_as_date(CurrentAccessor(request))

    @staticmethod
    def find_element_value_as_date(request: SaveTaskElementRequest) -> Optional[date]:
        """
        Try to get  an element as a date.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a date.
        """
        return find_element_value_as_date(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_date_list(request: SaveTaskElementRequest) -> List[date]:
        """
        Get all elements as date list.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element values as date list.
        """
        return get_element_value_as_date_list(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_dict(request: SaveTaskElementRequest) -> dict:
        """
        Get an element as a dict.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a dict.
        """
        return get_element_value_as_dict(CurrentAccessor(request))

    @staticmethod
    def find_element_value_as_dict(request: SaveTaskElementRequest) -> Optional[dict]:
        """
        Try to get an element as a dict.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a dict.
        """
        return find_element_value_as_dict(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_dict_list(request: SaveTaskElementRequest) -> List[dict]:
        """
        Get all elements as dict list.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element values as dict list.
        """
        return get_element_value_as_dict_list(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_document(request: SaveTaskElementRequest) -> TaskElementValueDocumentItem:
        """
        Get an element as a TaskElementValueDocumentItem.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a TaskElementValueDocumentItem.
        """
        return get_element_value_as_document(CurrentAccessor(request))

    @staticmethod
    def find_element_value_as_document(request: SaveTaskElementRequest) -> Optional[TaskElementValueDocumentItem]:
        """
        Try to get  an element as a TaskElementValueDocumentItem.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a TaskElementValueDocumentItem.
        """
        return find_element_value_as_document(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_document_list(request: SaveTaskElementRequest) -> List[TaskElementValueDocumentItem]:
        """
        Get all elements as TaskElementValueDocumentItem list.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element values as TaskElementValueDocumentItem list.
        """
        return get_element_value_as_document_list(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_principal(request: SaveTaskElementRequest) -> TaskElementValuePrincipalItem:
        """
        Get an element as a TaskElementValuePrincipalItem.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a TaskElementValuePrincipalItem.
        """
        return get_element_value_as_principal(CurrentAccessor(request))

    @staticmethod
    def find_element_value_as_principal(request: SaveTaskElementRequest) -> Optional[TaskElementValuePrincipalItem]:
        """
        Try to get  an element as a TaskElementValuePrincipalItem.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element value as a TaskElementValuePrincipalItem.
        """
        return find_element_value_as_principal(CurrentAccessor(request))

    @staticmethod
    def get_element_value_as_principal_list(request: SaveTaskElementRequest) -> List[TaskElementValuePrincipalItem]:
        """
        Get all elements as TaskElementValuePrincipalItem list.

        Arguments:
            request: The SaveTaskElement request.

        Returns:
            The element values as TaskElementValuePrincipalItem list.
        """
        return get_element_value_as_principal_list(CurrentAccessor(request))
