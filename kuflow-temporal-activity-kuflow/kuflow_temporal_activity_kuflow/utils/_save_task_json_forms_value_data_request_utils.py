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
from typing import Any, Dict, Optional

from kuflow_rest.models import JsonFormsFile, JsonFormsPrincipal
from kuflow_rest.utils.json_forms import (
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

from ..models import SaveTaskJsonFormsValueDataRequest


class CurrentJsonFormDataAccessor(JsonFormDataAccessor):
    def __init__(self, command: SaveTaskJsonFormsValueDataRequest):
        self.command = command

    def get_data(self) -> Optional[Dict[str, Any]]:
        return self.command.data

    def set_data(self, data: Optional[Dict[str, Any]]):
        self.command.data = data


class SaveTaskJsonFormsValueDataRequestUtils:
    @staticmethod
    def get_json_forms_property_as_str(command: SaveTaskJsonFormsValueDataRequest, property_path: str) -> str:
        """
        Get a json property as "str" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_str(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def find_json_forms_property_as_str(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> Optional[str]:
        """
        Try to find a json property as "str" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_str(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def get_json_forms_property_as_int(command: SaveTaskJsonFormsValueDataRequest, property_path: str) -> int:
        """
        Get a json property as "int" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_int(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def find_json_forms_property_as_int(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> Optional[int]:
        """
        Try to find a json property as "int" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_int(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def get_json_forms_property_as_float(command: SaveTaskJsonFormsValueDataRequest, property_path: str) -> float:
        """
        Get a json property as "float" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_float(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def find_json_forms_property_as_float(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> Optional[float]:
        """
        Try to find a json property as "float" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_float(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def get_json_forms_property_as_date(command: SaveTaskJsonFormsValueDataRequest, property_path: str) -> date:
        """
        Get a json property as "date" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_date(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def find_json_forms_property_as_date(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> Optional[date]:
        """
        Try to find a json property as "date" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_date(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def get_json_forms_property_as_datetime(command: SaveTaskJsonFormsValueDataRequest, property_path: str) -> datetime:
        """
        Get a json property as "datetime" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_datetime(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def find_json_forms_property_as_datetime(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> Optional[datetime]:
        """
        Try to find a json property as "datetime" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_datetime(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def get_json_forms_property_as_file(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> JsonFormsFile:
        """
        Get a json property as "JsonFormsFile" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_json_forms_file(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def find_json_forms_property_as_file(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> Optional[JsonFormsFile]:
        """
        Try to find a json property as "JsonFormsFile" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_json_forms_file(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def get_json_forms_property_as_principal(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> JsonFormsPrincipal:
        """
        Get a json property as "JsonFormsPrincipal" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_json_forms_principal(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def find_json_forms_property_as_principal(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> Optional[JsonFormsPrincipal]:
        """
        Try to find a json property as "JsonFormsPrincipal" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_json_forms_principal(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def get_json_forms_property_as_list(command: SaveTaskJsonFormsValueDataRequest, property_path: str) -> list:
        """
        Get a json property as "list" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_list(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def find_json_forms_property_as_list(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> Optional[list]:
        """
        Try to find a json property as "list" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_list(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def get_json_forms_property_as_dict(command: SaveTaskJsonFormsValueDataRequest, property_path: str) -> dict:
        """
        Get a json property as "dict" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            the property value if exists.

        Raises:
            ValueError: If property value doesn't exist or has incorrect format
        """
        return get_json_forms_property_as_dict(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def find_json_forms_property_as_dict(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str
    ) -> Optional[dict]:
        """
        Try to find a json property as "dict" following the "propertyPath" passed.

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"

        Return:
            The property value if exists.

        Raises:
            ValueError: If property value has incorrect format
        """
        return find_json_forms_property_as_dict(CurrentJsonFormDataAccessor(command), property_path)

    @staticmethod
    def update_json_forms_property(
        command: SaveTaskJsonFormsValueDataRequest, property_path: str, value: Optional[JsonFormsSimpleType]
    ) -> None:
        """
        Update a json forms data property in the task passed following the "property_path".

        Arguments:
            command: The task save json forms value data command.
            property_path: Property path to find. ie: "user.name" or "users.0.name"
            value: Value to update

        Raises:
            ValueError: If property value has incorrect format
        """
        update_json_forms_property(CurrentJsonFormDataAccessor(command), property_path, value)
