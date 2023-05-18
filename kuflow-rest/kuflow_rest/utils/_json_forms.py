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

from typing import Union, List, Dict, Optional
from datetime import date, datetime
import math
import re

from ..models import (
    PrincipalType,
    JsonFormsFile,
    JsonFormsPrincipal,
    JsonFormsValue,
    Task,
    TaskPageItem,
    TaskSaveJsonFormsValueDataCommand,
)

SimpleType = Union[str, int, float, bool, date, JsonFormsPrincipal, JsonFormsFile]

ContainerArrayType = List["ComplexType"]

ContainerRecordType = Dict[str, "ComplexType"]

ContainerType = Union[ContainerArrayType, ContainerRecordType]

ComplexType = Union[SimpleType, ContainerType]

JsonFormsModels = Union[Task, TaskPageItem, TaskSaveJsonFormsValueDataCommand]


class JsonFormsProperty:
    container: ContainerType
    path: str
    value: ComplexType

    def __init__(self, container: ContainerType, path: str, value: ComplexType):
        self.container = container
        self.path = path
        self.value = value


def get_json_forms_property_as_str(model: JsonFormsModels, property_path: str) -> str:
    """
    Get a json property as "str" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        the property value if exists.

    Raises:
        ValueError: If property value doesn't exist or has incorrect format
    """
    value = find_json_forms_property_as_str(model, property_path)
    if value is None:
        raise ValueError("Property value doesn't exist")
    return value


def find_json_forms_property_as_str(model: JsonFormsModels, property_path: str) -> Optional[str]:
    """
    Try to find a json property as "str" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        The property value if exists.

    Raises:
        ValueError: If property value has incorrect format
    """
    value = find_json_forms_property_value(model, property_path)
    if value is not None:
        return str(value)
    return None


def get_json_forms_property_as_int(model, property_path) -> int:
    """
    Get a json property as "int" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        the property value if exists.

    Raises:
        ValueError: If property value doesn't exist or has incorrect format
    """
    value = find_json_forms_property_as_int(model, property_path)
    if value is None:
        raise ValueError("Property value doesn't exist")
    return value


def find_json_forms_property_as_int(model, property_path) -> Optional[int]:
    """
    Try to find a json property as "int" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        The property value if exists.

    Raises:
        ValueError: If property value has incorrect format
    """
    value = find_json_forms_property_value(model, property_path)
    if value is None:
        return None

    if isinstance(value, int):
        if not math.isnan(value):
            return value

    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            pass

    raise ValueError(f"Property {property_path} is not a int")


def get_json_forms_property_as_float(model, property_path) -> float:
    """
    Get a json property as "float" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        the property value if exists.

    Raises:
        ValueError: If property value doesn't exist or has incorrect format
    """
    value = find_json_forms_property_as_float(model, property_path)
    if value is None:
        raise ValueError("Property value doesn't exist")
    return value


def find_json_forms_property_as_float(model, property_path) -> Optional[float]:
    """
    Try to find a json property as "float" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        The property value if exists.

    Raises:
        ValueError: If property value has incorrect format
    """
    value = find_json_forms_property_value(model, property_path)
    if value is None:
        return None

    if isinstance(value, int):
        if not math.isnan(value):
            return float(value)

    if isinstance(value, float):
        if not math.isnan(value):
            return value

    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            pass

    raise ValueError(f"Property {property_path} is not a float")


def get_json_forms_property_as_date(model, property_path) -> date:
    """
    Get a json property as "date" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        the property value if exists.

    Raises:
        ValueError: If property value doesn't exist or has incorrect format
    """
    value = find_json_forms_property_as_date(model, property_path)
    if value is None:
        raise ValueError("Property value doesn't exist")
    return value


def find_json_forms_property_as_date(model, property_path) -> Optional[date]:
    """
    Try to find a json property as "date" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        The property value if exists.

    Raises:
        ValueError: If property value has incorrect format
    """
    value = find_json_forms_property_value(model, property_path)
    if value is None:
        return None

    if isinstance(value, date):
        return value

    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass

    raise ValueError(f"Property {property_path} is not a date following ISO 8601 format")


def get_json_forms_property_as_datetime(model, property_path) -> datetime:
    """
    Get a json property as "datetime" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        the property value if exists.

    Raises:
        ValueError: If property value doesn't exist or has incorrect format
    """
    value = find_json_forms_property_as_datetime(model, property_path)
    if value is None:
        raise ValueError("Property value doesn't exist")
    return value


def find_json_forms_property_as_datetime(model, property_path) -> Optional[datetime]:
    """
    Try to find a json property as "datetime" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        The property value if exists.

    Raises:
        ValueError: If property value has incorrect format
    """
    value = find_json_forms_property_value(model, property_path)
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            pass

    raise ValueError(f"Property {property_path} is not a date-time following ISO 8601 format")


def get_json_forms_property_as_json_forms_file(model, property_path) -> JsonFormsFile:
    """
    Get a json property as "JsonFormsFile" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        the property value if exists.

    Raises:
        ValueError: If property value doesn't exist or has incorrect format
    """
    value = find_json_forms_property_as_json_forms_file(model, property_path)
    if value is None:
        raise ValueError("Property value doesn't exist")
    return value


def find_json_forms_property_as_json_forms_file(model, property_path) -> Optional[JsonFormsFile]:
    """
    Try to find a json property as "JsonFormsFile" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        The property value if exists.

    Raises:
        ValueError: If property value has incorrect format
    """
    value = find_json_forms_property_value(model, property_path)
    if value is None:
        return None

    json_forms_file = try_parse_json_forms_file(value)
    if json_forms_file is None:
        raise ValueError(f"Property {property_path} is not a file")

    return json_forms_file


def get_json_forms_property_as_json_forms_principal(model, property_path) -> JsonFormsPrincipal:
    """
    Get a json property as "JsonFormsPrincipal" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        the property value if exists.

    Raises:
        ValueError: If property value doesn't exist or has incorrect format
    """
    value = find_json_forms_property_as_json_forms_principal(model, property_path)
    if value is None:
        raise ValueError("Property value doesn't exist")
    return value


def find_json_forms_property_as_json_forms_principal(model, property_path) -> Optional[JsonFormsPrincipal]:
    """
    Try to find a json property as "JsonFormsPrincipal" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        The property value if exists.

    Raises:
        ValueError: If property value has incorrect format
    """
    value = find_json_forms_property_value(model, property_path)
    if value is None:
        return None

    json_forms_file = try_parse_json_forms_principal(value)
    if json_forms_file is None:
        raise ValueError(f"Property {property_path} is not a principal")

    return json_forms_file


def get_json_forms_property_as_list(model, property_path) -> list:
    """
    Get a json property as "list" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        the property value if exists.

    Raises:
        ValueError: If property value doesn't exist or has incorrect format
    """
    value = find_json_forms_property_as_list(model, property_path)
    if value is None:
        raise ValueError("Property value doesn't exist")
    return value


def find_json_forms_property_as_list(model, property_path) -> Optional[list]:
    """
    Try to find a json property as "list" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        The property value if exists.

    Raises:
        ValueError: If property value has incorrect format
    """
    value = find_json_forms_property_value(model, property_path)
    if value is None:
        return None

    if isinstance(value, list):
        return value

    raise ValueError(f"Property {property_path} is not a list")


def get_json_forms_property_as_dict(model, property_path) -> dict:
    """
    Get a json property as "dict" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        the property value if exists.

    Raises:
        ValueError: If property value doesn't exist or has incorrect format
    """
    value = find_json_forms_property_as_dict(model, property_path)
    if value is None:
        raise ValueError("Property value doesn't exist")
    return value


def find_json_forms_property_as_dict(model, property_path) -> Optional[dict]:
    """
    Try to find a json property as "dict" following the "propertyPath" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"

    Return:
        The property value if exists.

    Raises:
        ValueError: If property value has incorrect format
    """
    value = find_json_forms_property_value(model, property_path)
    if value is None:
        return None

    if isinstance(value, dict):
        return value

    raise ValueError(f"Property {property_path} is not a dict")


def find_json_forms_property_value(
    model: JsonFormsModels, property_path: str, create_missing_parents: bool = True
) -> Optional[ComplexType]:
    property = find_json_forms_property(model, property_path, create_missing_parents)
    if property is not None:
        return property.value
    return None


def update_json_forms_property(
    model: JsonFormsModels,
    property_path: str,
    value: Optional[SimpleType],
) -> None:
    """
    Update a json forms data property in the task passed following the "property_path".

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"
        value: Value to update

    Raises:
        ValueError: If property value has incorrect format
    """
    property = find_json_forms_property(model, property_path, True)

    value = transform_json_forms_property_value(value)

    if property is None:
        raise ValueError(f"Property {property_path} doesn't exist")

    json_forms_property_container = property.container
    json_forms_property_path = property.path
    if isinstance(json_forms_property_container, list):
        if not json_forms_property_path.isdigit():
            raise ValueError(f"Incorrect property path {json_forms_property_path}, parent path is not a List")

        json_forms_property_path_index = int(json_forms_property_path)
        if value is not None:
            json_forms_property_container[json_forms_property_path_index] = value
        else:
            json_forms_property_container.pop(json_forms_property_path_index)
    elif isinstance(json_forms_property_container, dict):
        if value is not None:
            json_forms_property_container[json_forms_property_path] = value
        else:
            del json_forms_property_container[json_forms_property_path]
    else:
        raise ValueError(f"Incorrect property path {json_forms_property_path}")


# flake8: noqa: C901
def find_json_forms_property(
    model: JsonFormsModels, property_path: str, create_missing_parents: bool = False
) -> Optional[JsonFormsProperty]:
    """
    Try to find a json property following the "property_path" passed.

    Arguments:
        model: Related model
        property_path: Property path to find. ie: "user.name" or "users.0.name"
        create_missing_parents: Create parent paths if are missing

    Return:
        The property value if exists.

    Raises:
        ValueError: If property value has incorrect format or a wrong path
    """
    property_data = get_json_forms_value_data(model, create_missing_parents)
    if property_data is None:
        return None

    property_container: ContainerType = property_data
    property_value_path = ""
    property_value: Optional[ComplexType] = None

    paths = property_path.split(".")
    for idx, path in enumerate(paths):
        property_value_path = path
        if property_value_path == "":
            continue

        property_value_path_as_integer = -1

        if is_json_forms_type_container_array(property_container):
            if not property_value_path.isdigit():
                raise ValueError(f"Wrong list index {property_value_path}")

            property_value_path_as_integer = int(property_value_path)
            if property_value_path_as_integer < 0 or property_value_path_as_integer > len(property_container):
                return None
            elif property_value_path_as_integer == len(property_container):
                if not create_missing_parents:
                    return None

                property_value = None
            else:
                property_value = property_container[property_value_path_as_integer]
        elif is_json_forms_type_container_record(property_container):
            if property_value_path not in property_container:
                if not create_missing_parents:
                    return None

            property_value = property_container.get(property_value_path)
        else:
            return None

        if property_value is None:
            if not create_missing_parents:
                return None

            if idx + 1 < len(paths):
                path_next = paths[idx + 1]
                if path_next.isdigit():
                    property_value = []
                else:
                    property_value = {}

                if is_json_forms_type_container_array(property_container):
                    if property_value_path_as_integer != len(property_container):
                        raise ValueError(f"Wrong list index {property_value_path}")

                    property_container.append(property_value)
                elif is_json_forms_type_container_record(property_container):
                    property_container[property_value_path] = property_value

        if property_value is not None and is_json_forms_type_container(property_value) and idx + 1 < len(paths):
            property_container = property_value
            property_value = None

    return JsonFormsProperty(container=property_container, path=property_value_path, value=property_value)


def transform_json_forms_property_value(value: Optional[SimpleType]) -> Optional[SimpleType]:
    if value is None:
        return None
    elif isinstance(value, JsonFormsPrincipal):
        return generate_value_for_json_forms_principal(value)
    elif isinstance(value, JsonFormsFile):
        return generate_value_for_json_forms_file(value)
    elif isinstance(value, date):
        return value.isoformat()
    elif isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, (int, float, bool, str)):
        return value

    raise Exception(f"Unsupported value {value}")


def generate_value_for_json_forms_principal(principal: JsonFormsPrincipal) -> str:
    return f"kuflow-principal:id={principal.id};type={principal.type};name={principal.name};"


def generate_value_for_json_forms_file(file: JsonFormsFile) -> str:
    return f"kuflow-file:uri={file.uri};type={file.type};size={file.size};name={file.name};"


def try_parse_json_forms_file(value: ComplexType) -> Optional[JsonFormsFile]:
    if value is None:
        return None

    if not isinstance(value, str):
        return None

    if not value.startswith("kuflow-file:"):
        return None

    value_transformed = value.replace("kuflow-file:", "")

    matches = re.findall(".*?=.*?;", value_transformed)
    if matches is None or len(matches) != 4:
        return None

    uri: Optional[str] = None
    type: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None

    for match in matches:
        match = match[:-1]
        key, value = match.split("=")
        if key == "uri":
            uri = str(value)
        elif key == "type":
            type = str(value)
        elif key == "name":
            name = str(value)
        elif key == "size":
            size = int(value)

    return JsonFormsFile(
        uri=uri,
        type=type,
        name=name,
        size=size,
    )


def try_parse_json_forms_principal(value: ComplexType) -> Optional[JsonFormsPrincipal]:
    if value is None:
        return None

    if not isinstance(value, str):
        return None

    if not value.startswith("kuflow-principal:"):
        return None

    value_transformed = value.replace("kuflow-principal:", "")

    matches = re.findall(".*?=.*?;", value_transformed)
    if matches is None or len(matches) != 3:
        return None

    id: Optional[str] = None
    type: Optional[PrincipalType] = None
    name: Optional[str] = None

    for match in matches:
        match = match[:-1]
        key, value = match.split("=")
        if key == "id":
            id = str(value)
        elif key == "type":
            type = PrincipalType(value)
        elif key == "name":
            name = str(value)

    return JsonFormsPrincipal(
        id=id,
        type=type,
        name=name,
    )


def is_json_forms_type_container(value: Optional[ComplexType]) -> bool:
    return is_json_forms_type_container_record(value) or is_json_forms_type_container_array(value)


def is_json_forms_type_container_record(value: Optional[ComplexType]) -> bool:
    return isinstance(value, dict)


def is_json_forms_type_container_array(value: Optional[ComplexType]) -> bool:
    return isinstance(value, list)


def get_json_forms_value_data(model: JsonFormsModels, create_missing_parents: bool) -> Optional[ContainerType]:
    data: Optional[ContainerType] = None

    if isinstance(model, Task) or isinstance(model, TaskPageItem):
        data = model.json_forms_value.data if model.json_forms_value else None
    else:
        data = model.data

    if data is None and create_missing_parents:
        data = {}
        if isinstance(model, Task) or isinstance(model, TaskPageItem):
            model.json_forms_value = model.json_forms_value or JsonFormsValue()
            model.json_forms_value.data = data
        else:
            model.data = data

    return data
