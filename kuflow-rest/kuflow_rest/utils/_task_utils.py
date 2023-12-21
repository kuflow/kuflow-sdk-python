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

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from .._generated.models import TaskElementValue
from ..models import (
    JsonFormsFile,
    JsonFormsPrincipal,
    JsonFormsValue,
    Task,
    TaskElementValueDocumentItem,
    TaskElementValuePrincipalItem,
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
from .json_forms import (
    JsonFormDataAccessor,
    JsonFormsSimpleType,
    find_json_forms_property_as_date,
    find_json_forms_property_as_datetime,
    find_json_forms_property_as_dict,
    find_json_forms_property_as_float,
    find_json_forms_property_as_int,
    find_json_forms_property_as_json_forms_file,
    find_json_forms_property_as_json_forms_principal,
    find_json_forms_property_as_list,
    find_json_forms_property_as_str,
    get_json_forms_property_as_date,
    get_json_forms_property_as_datetime,
    get_json_forms_property_as_dict,
    get_json_forms_property_as_float,
    get_json_forms_property_as_int,
    get_json_forms_property_as_json_forms_file,
    get_json_forms_property_as_json_forms_principal,
    get_json_forms_property_as_list,
    get_json_forms_property_as_str,
    update_json_forms_property,
)


class CurrentElementValueAccessor(TaskElementValueAccessor):
    def __init__(self, task: Task, element_definition_code: str):
        self.task = task
        self.element_definition_code = element_definition_code

    def set_element_values(self, element_values: List[ElementValueUnion]):
        if self.task.element_values is None:
            self.task.element_values = {}

        if len(element_values) == 0:
            self.task.element_values.pop(self.element_definition_code, None)
        else:
            self.task.element_values[self.element_definition_code] = element_values

    def get_element_values(self) -> List[TaskElementValue]:
        if self.task.element_values is None:
            return []

        element_values_by_code = self.task.element_values.get(
            self.element_definition_code
        )
        if element_values_by_code is None or len(element_values_by_code) == 0:
            return []

        return element_values_by_code


class CurrentJsonFormDataAccessor(JsonFormDataAccessor):
    def __init__(self, task: Task):
        self.task = task

    def get_data(self) -> Optional[Dict[str, Any]]:
        if self.task.json_forms_value is None:
            return None

        return self.task.json_forms_value.data

    def set_data(self, data: Optional[Dict[str, Any]]):
        if self.task.json_forms_value is None:
            self.task.json_forms_value = JsonFormsValue()

        self.task.json_forms_value.data = data


class TaskUtils:
    @staticmethod
    def get_element_value_valid(task: Task, element_definition_code: str) -> bool:
        """
        Check if all related valid values are TRUE.

        Arguments:
            task: The task.
            element_definition_code: Element Definition Code.

        Returns:
            True if all related valid values are TRUE, otherwise False.
        """
        return get_element_value_valid(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_valid_at(
        task: Task,
        element_definition_code: str,
        index: int,
    ) -> bool:
        """
        Check if the requested valid value at the given index is TRUE.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.
            index: The element value index.

        Returns:
            The requested valid value if it exists, otherwise None.
        """
        return get_element_value_valid_at(
            CurrentElementValueAccessor(task, element_definition_code), index
        )

    @staticmethod
    def set_element_value_valid(
        task: Task, element_definition_code: str, valid: Optional[bool]
    ) -> Task:
        """
        Set the valid value for all element values.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.
            valid: The valid value.

        Returns:
            The passed task.
        """
        set_element_value_valid(
            CurrentElementValueAccessor(task, element_definition_code), valid
        )

        return task

    @staticmethod
    def set_element_value_valid_at(
        task: Task, element_definition_code: str, valid: Optional[bool], index: int
    ) -> Task:
        """
        Set the valid value for the selected element value.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.
            valid: The valid value.
            index: The element value index.

        Returns:
            The passed task.
        """
        set_element_value_valid_at(
            CurrentElementValueAccessor(task, element_definition_code), valid, index
        )

        return task

    @staticmethod
    def set_element_value(
        task: Task,
        element_definition_code: str,
        element_value: Optional[ElementValueSimpleType] = None,
    ) -> Task:
        """
        Set an element value.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.
            element_value: The element value. If the value is None, all current values are removed.

        Returns:
            The passed task.
        """
        set_element_value(
            CurrentElementValueAccessor(task, element_definition_code), element_value
        )

        return task

    @staticmethod
    def set_element_value_list(
        task: Task,
        element_definition_code: str,
        element_values: Optional[List[ElementValueSimpleType]] = None,
    ) -> Task:
        """
        Set an element value.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.
            element_values: The element value. If the value is None or empty, all current values are removed.

        Returns:
            The passed task.
        """
        set_element_value_list(
            CurrentElementValueAccessor(task, element_definition_code), element_values
        )

        return task

    @staticmethod
    def add_element_value(
        task: Task,
        element_definition_code: str,
        element_value: Optional[ElementValueSimpleType] = None,
    ) -> Task:
        """
        Add an element value.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.
            element_value: The element value. If the value is None, all current values are removed.

        Returns:
            The passed task.
        """
        add_element_value(
            CurrentElementValueAccessor(task, element_definition_code), element_value
        )

        return task

    @staticmethod
    def add_element_value_list(
        task: Task,
        element_definition_code: str,
        element_values: Optional[List[ElementValueSimpleType]] = None,
    ) -> Task:
        """
        Add element values.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.
            element_values: The element values. If the values is None or empty, all current values are removed.

        Returns:
            The passed model related object.
        """
        add_element_value_list(
            CurrentElementValueAccessor(task, element_definition_code), element_values
        )

        return task

    @staticmethod
    def get_element_value_as_str(task: Task, element_definition_code: str) -> str:
        """
        Get an element as a str.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a str.
        """
        return get_element_value_as_str(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def find_element_value_as_str(
        task: Task, element_definition_code: str
    ) -> Optional[str]:
        """
        Try to get an element as a str.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a str.
        """
        return find_element_value_as_str(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_str_list(
        task: Task, element_definition_code: str
    ) -> List[str]:
        """
        Try to get an element as a str list.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element values as a str list.
        """
        return get_element_value_as_str_list(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_float(task: Task, element_definition_code: str) -> float:
        """
        Get an element as a float.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a float.
        """
        return get_element_value_as_float(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def find_element_value_as_float(task: Task, element_definition_code: str) -> float:
        """
        Try to get an element as a float.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a float.
        """
        return find_element_value_as_float(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_float_list(
        task: Task, element_definition_code: str
    ) -> List[float]:
        """
        Get all elements as a float list.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a float.
        """
        return get_element_value_as_float_list(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_date(task: Task, element_definition_code: str) -> date:
        """
        Get an element as a date.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a date.
        """
        return get_element_value_as_date(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def find_element_value_as_date(
        task: Task, element_definition_code: str
    ) -> Optional[date]:
        """
        Try to get  an element as a date.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a date.
        """
        return find_element_value_as_date(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_date_list(
        task: Task, element_definition_code: str
    ) -> Optional[List[date]]:
        """
        Get all elements as date list.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element values as date list.
        """
        return get_element_value_as_date_list(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_dict(task: Task, element_definition_code: str) -> dict:
        """
        Get an element as a dict.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a dict.
        """
        return get_element_value_as_dict(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def find_element_value_as_dict(
        task: Task, element_definition_code: str
    ) -> Optional[dict]:
        """
        Try to get an element as a dict.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a dict.
        """
        return find_element_value_as_dict(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_dict_list(
        task: Task, element_definition_code: str
    ) -> Optional[List[dict]]:
        """
        Get all elements as dict list.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element values as dict list.
        """
        return get_element_value_as_dict_list(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_document(
        task: Task, element_definition_code: str
    ) -> TaskElementValueDocumentItem:
        """
        Get an element as a TaskElementValueDocumentItem.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a TaskElementValueDocumentItem.
        """
        return get_element_value_as_document(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def find_element_value_as_document(
        task: Task, element_definition_code: str
    ) -> Optional[TaskElementValueDocumentItem]:
        """
        Try to get  an element as a TaskElementValueDocumentItem.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a TaskElementValueDocumentItem.
        """
        return find_element_value_as_document(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_document_list(
        task: Task, element_definition_code: str
    ) -> List[TaskElementValueDocumentItem]:
        """
        Get all elements as TaskElementValueDocumentItem list.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element values as TaskElementValueDocumentItem list.
        """
        return get_element_value_as_document_list(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_principal(
        task: Task, element_definition_code: str
    ) -> TaskElementValuePrincipalItem:
        """
        Get an element as a TaskElementValuePrincipalItem.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a TaskElementValuePrincipalItem.
        """
        return get_element_value_as_principal(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def find_element_value_as_principal(
        task: Task, element_definition_code: str
    ) -> Optional[TaskElementValuePrincipalItem]:
        """
        Try to get  an element as a TaskElementValuePrincipalItem.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element value as a TaskElementValuePrincipalItem.
        """
        return find_element_value_as_principal(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_element_value_as_principal_list(
        task: Task, element_definition_code: str
    ) -> List[TaskElementValuePrincipalItem]:
        """
        Get all elements as TaskElementValuePrincipalItem list.

        Arguments:
            task: The task.
            element_definition_code: The element definition code.

        Returns:
            The element values as TaskElementValuePrincipalItem list.
        """
        return get_element_value_as_principal_list(
            CurrentElementValueAccessor(task, element_definition_code)
        )

    @staticmethod
    def get_json_forms_property_as_str(task: Task, property_path: str) -> str:
        """
        Get a json property as "str" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_str(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def find_json_forms_property_as_str(
        task: Task, property_path: str
    ) -> Optional[str]:
        """
        Try to find a json property as "str" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_str(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def get_json_forms_property_as_int(task: Task, property_path: str) -> int:
        """
        Get a json property as "int" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_int(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def find_json_forms_property_as_int(
        task: Task, property_path: str
    ) -> Optional[int]:
        """
        Try to find a json property as "int" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_int(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def get_json_forms_property_as_float(task: Task, property_path: str) -> float:
        """
        Get a json property as "float" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_float(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def find_json_forms_property_as_float(
        task: Task, property_path: str
    ) -> Optional[float]:
        """
        Try to find a json property as "float" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_float(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def get_json_forms_property_as_date(task: Task, property_path: str) -> date:
        """
        Get a json property as "date" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_date(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def find_json_forms_property_as_date(
        task: Task, property_path: str
    ) -> Optional[date]:
        """
        Try to find a json property as "date" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_date(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def get_json_forms_property_as_datetime(task: Task, property_path: str) -> datetime:
        """
        Get a json property as "datetime" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_datetime(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def find_json_forms_property_as_datetime(
        task: Task, property_path: str
    ) -> Optional[datetime]:
        """
        Try to find a json property as "datetime" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_datetime(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def get_json_forms_property_as_file(
        task: Task, property_path: str
    ) -> JsonFormsFile:
        """
        Get a json property as "JsonFormsFile" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_json_forms_file(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def find_json_forms_property_as_file(
        task: Task, property_path: str
    ) -> Optional[JsonFormsFile]:
        """
        Try to find a json property as "JsonFormsFile" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_json_forms_file(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def get_json_forms_property_as_principal(
        task: Task, property_path: str
    ) -> JsonFormsPrincipal:
        """
        Get a json property as "JsonFormsPrincipal" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_json_forms_principal(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def find_json_forms_property_as_principal(
        task: Task, property_path: str
    ) -> Optional[JsonFormsPrincipal]:
        """
        Try to find a json property as "JsonFormsPrincipal" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_json_forms_principal(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def get_json_forms_property_as_list(task: Task, property_path: str) -> list:
        """
        Get a json property as "list" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_list(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def find_json_forms_property_as_list(
        task: Task, property_path: str
    ) -> Optional[list]:
        """
        Try to find a json property as "list" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_list(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def get_json_forms_property_as_dict(task: Task, property_path: str) -> dict:
        """
        Get a json property as "dict" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_dict(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def find_json_forms_property_as_dict(
        task: Task, property_path: str
    ) -> Optional[dict]:
        """
        Try to find a json property as "dict" following the "propertyPath" passed.

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_dict(
            CurrentJsonFormDataAccessor(task), property_path
        )

    @staticmethod
    def update_json_forms_property(
        task: Task, property_path: str, value: Optional[JsonFormsSimpleType]
    ) -> None:
        """
        Update a json forms data property in the task passed following the "property_path".

        Arguments:
            task: The task.
            property_path: Property path to find. ie: "user.name" or "users.0.name"
            value: Value to update

        Raises:
            ValueError: If property value has incorrect format
        """
        update_json_forms_property(
            CurrentJsonFormDataAccessor(task), property_path, value
        )
