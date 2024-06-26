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

from .._generated.models import ProcessElementValue
from ..models import JsonFormsFile, JsonFormsPrincipal, JsonFormsValue, Process
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
from .json_forms import (
    JsonFormDataAccessor,
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
)


class ProcessUtils:
    @staticmethod
    def get_element_value_valid(process: Process, element_definition_code: str) -> bool:
        """
        Check if all related valid values are TRUE.

        Arguments:
            process: The process.
            element_definition_code: Element Definition Code.

        Returns:
            True if all related valid values are TRUE, otherwise False.
        """
        return get_element_value_valid(CurrentElementValueAccessor(process, element_definition_code))

    @staticmethod
    def get_element_value_valid_at(
        process: Process,
        element_definition_code: str,
        index: int,
    ) -> bool:
        """
        Check if the requested valid value at the given index is TRUE.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.
            index: The element value index.

        Returns:
            The requested valid value if it exists, otherwise None.
        """
        return get_element_value_valid_at(CurrentElementValueAccessor(process, element_definition_code), index)

    @staticmethod
    def set_element_value_valid(process: Process, element_definition_code: str, valid: Optional[bool]) -> Process:
        """
        Set the valid value for all element values.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.
            valid: The valid value.

        Returns:
            The passed process.
        """
        set_element_value_valid(CurrentElementValueAccessor(process, element_definition_code), valid)

        return process

    @staticmethod
    def set_element_value_valid_at(
        process: Process,
        element_definition_code: str,
        valid: Optional[bool],
        index: int,
    ) -> Process:
        """
        Set the valid value for the selected element value.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.
            valid: The valid value.
            index: The element value index.

        Returns:
            The passed process.
        """
        set_element_value_valid_at(CurrentElementValueAccessor(process, element_definition_code), valid, index)

        return process

    @staticmethod
    def set_element_value(
        process: Process,
        element_definition_code: str,
        element_value: Optional[ElementValueSimpleType] = None,
    ) -> Process:
        """
        Set an element value.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.
            element_value: The element value. If the value is None, all current values are removed.

        Returns:
            The passed process.
        """
        set_element_value(CurrentElementValueAccessor(process, element_definition_code), element_value)

        return process

    @staticmethod
    def set_element_value_list(
        process: Process,
        element_definition_code: str,
        element_values: Optional[List[ElementValueSimpleType]] = None,
    ) -> Process:
        """
        Set an element value.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.
            element_values: The element value. If the value is None or empty, all current values are removed.

        Returns:
            The passed process.
        """
        set_element_value_list(
            CurrentElementValueAccessor(process, element_definition_code),
            element_values,
        )

        return process

    @staticmethod
    def add_element_value(
        process: Process,
        element_definition_code: str,
        element_value: Optional[ElementValueSimpleType] = None,
    ) -> Process:
        """
        Add an element value.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.
            element_value: The element value. If the value is None, all current values are removed.

        Returns:
            The passed process.
        """
        add_element_value(CurrentElementValueAccessor(process, element_definition_code), element_value)

        return process

    @staticmethod
    def add_element_value_list(
        process: Process,
        element_definition_code: str,
        element_values: Optional[List[ElementValueSimpleType]] = None,
    ) -> Process:
        """
        Add element values.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.
            element_values: The element values. If the values is None or empty, all current values are removed.

        Returns:
            The passed model related object.
        """
        add_element_value_list(
            CurrentElementValueAccessor(process, element_definition_code),
            element_values,
        )

        return process

    @staticmethod
    def get_element_value_as_str(process: Process, element_definition_code: str) -> str:
        """
        Get an element as a str.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.

        Returns:
            The element value as a str.
        """
        return get_element_value_as_str(CurrentElementValueAccessor(process, element_definition_code))

    @staticmethod
    def find_element_value_as_str(process: Process, element_definition_code: str) -> Optional[str]:
        """
        Try to get an element as a str.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.

        Returns:
            The element value as a str.
        """
        return find_element_value_as_str(CurrentElementValueAccessor(process, element_definition_code))

    @staticmethod
    def get_element_value_as_str_list(process: Process, element_definition_code: str) -> List[str]:
        """
        Try to get an element as a str list.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.

        Returns:
            The element values as a str list.
        """
        return get_element_value_as_str_list(CurrentElementValueAccessor(process, element_definition_code))

    @staticmethod
    def get_element_value_as_float(process: Process, element_definition_code: str) -> float:
        """
        Get an element as a float.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.

        Returns:
            The element value as a float.
        """
        return get_element_value_as_float(CurrentElementValueAccessor(process, element_definition_code))

    @staticmethod
    def find_element_value_as_float(process: Process, element_definition_code: str) -> float:
        """
        Try to get an element as a float.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.

        Returns:
            The element value as a float.
        """
        return find_element_value_as_float(CurrentElementValueAccessor(process, element_definition_code))

    @staticmethod
    def get_element_value_as_float_list(process: Process, element_definition_code: str) -> List[float]:
        """
        Get all elements as a float list.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.

        Returns:
            The element value as a float.
        """
        return get_element_value_as_float_list(CurrentElementValueAccessor(process, element_definition_code))

    @staticmethod
    def get_element_value_as_date(process: Process, element_definition_code: str) -> date:
        """
        Get an element as a date.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.

        Returns:
            The element value as a date.
        """
        return get_element_value_as_date(CurrentElementValueAccessor(process, element_definition_code))

    @staticmethod
    def find_element_value_as_date(process: Process, element_definition_code: str) -> Optional[date]:
        """
        Try to get  an element as a date.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.

        Returns:
            The element value as a date.
        """
        return find_element_value_as_date(CurrentElementValueAccessor(process, element_definition_code))

    @staticmethod
    def get_element_value_as_date_list(process: Process, element_definition_code: str) -> List[date]:
        """
        Get all elements as date list.

        Arguments:
            process: The process.
            element_definition_code: The element definition code.

        Returns:
            The element value as a date.
        """
        return get_element_value_as_date_list(CurrentElementValueAccessor(process, element_definition_code))

    @staticmethod
    def get_entity_property_as_str(process: Process, property_path: str) -> str:
        """
        Get a json property as "str" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_str(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def find_entity_property_as_str(process: Process, property_path: str) -> Optional[str]:
        """
        Try to find a json property as "str" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_str(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def get_entity_property_as_int(process: Process, property_path: str) -> int:
        """
        Get a json property as "int" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_int(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def find_entity_property_as_int(process: Process, property_path: str) -> Optional[int]:
        """
        Try to find a json property as "int" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_int(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def get_entity_property_as_float(process: Process, property_path: str) -> float:
        """
        Get a json property as "float" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_float(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def find_entity_property_as_float(process: Process, property_path: str) -> Optional[float]:
        """
        Try to find a json property as "float" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_float(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def get_entity_property_as_date(process: Process, property_path: str) -> date:
        """
        Get a json property as "date" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_date(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def find_entity_property_as_date(process: Process, property_path: str) -> Optional[date]:
        """
        Try to find a json property as "date" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_date(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def get_entity_property_as_datetime(process: Process, property_path: str) -> datetime:
        """
        Get a json property as "datetime" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_datetime(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def find_entity_property_as_datetime(process: Process, property_path: str) -> Optional[datetime]:
        """
        Try to find a json property as "datetime" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_datetime(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def get_entity_property_as_file(process: Process, property_path: str) -> JsonFormsFile:
        """
        Get a json property as "JsonFormsFile" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_json_forms_file(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def find_entity_property_as_file(process: Process, property_path: str) -> Optional[JsonFormsFile]:
        """
        Try to find a json property as "JsonFormsFile" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_json_forms_file(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def get_entity_property_as_principal(process: Process, property_path: str) -> JsonFormsPrincipal:
        """
        Get a json property as "JsonFormsPrincipal" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_json_forms_principal(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def find_entity_property_as_principal(process: Process, property_path: str) -> Optional[JsonFormsPrincipal]:
        """
        Try to find a json property as "JsonFormsPrincipal" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_json_forms_principal(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def get_entity_property_as_list(process: Process, property_path: str) -> list:
        """
        Get a json property as "list" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_list(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def find_entity_property_as_list(process: Process, property_path: str) -> Optional[list]:
        """
        Try to find a json property as "list" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_list(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def get_entity_property_as_dict(process: Process, property_path: str) -> dict:
        """
        Get a json property as "dict" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_dict(CurrentJsonFormDataAccessor(process), property_path)

    @staticmethod
    def find_entity_property_as_dict(process: Process, property_path: str) -> Optional[dict]:
        """
        Try to find a json property as "dict" following the "propertyPath" passed.

        Arguments:
            process: The process.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_dict(CurrentJsonFormDataAccessor(process), property_path)


class CurrentElementValueAccessor(ProcessElementValueAccessor):
    def __init__(self, process: Process, element_definition_code: str):
        self.process = process
        self.element_definition_code = element_definition_code

    def set_element_values(self, element_values: List[ElementValueUnion]):
        if self.process.element_values is None:
            self.process.element_values = {}

        if len(element_values) == 0:
            self.process.element_values.pop(self.element_definition_code, None)
        else:
            self.process.element_values[self.element_definition_code] = element_values

    def get_element_values(self) -> List[ProcessElementValue]:
        if self.process.element_values is None:
            return []

        element_values_by_code = self.process.element_values.get(self.element_definition_code)
        if element_values_by_code is None or len(element_values_by_code) == 0:
            return []

        return element_values_by_code


class CurrentJsonFormDataAccessor(JsonFormDataAccessor):
    def __init__(self, process: Process):
        self.process = process

    def get_data(self) -> Optional[Dict[str, Any]]:
        if self.process.entity is None:
            return None

        return self.process.entity.data

    def set_data(self, data: Optional[Dict[str, Any]]):
        if self.process.entity is None:
            self.process.entity = JsonFormsValue()

        self.process.entity.data = data
