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

from abc import ABC, abstractmethod
from datetime import date
from typing import Dict, List, Optional, Union

from ..models import (
    Process,
    ProcessElementValueNumber,
    ProcessElementValueString,
    ProcessPageItem,
    ProcessSaveElementCommand,
    Task,
    TaskElementValueDocument,
    TaskElementValueDocumentItem,
    TaskElementValueNumber,
    TaskElementValueObject,
    TaskElementValuePrincipal,
    TaskElementValuePrincipalItem,
    TaskElementValueString,
    TaskPageItem,
    TaskSaveElementCommand,
)

ProcessElementValueUnion = Union[ProcessElementValueString, ProcessElementValueNumber]
TaskElementValueUnion = Union[
    TaskElementValueString,
    TaskElementValueNumber,
    TaskElementValueObject,
    TaskElementValueDocument,
    TaskElementValuePrincipal,
]

ElementValueUnion = Union[
    ProcessElementValueString,
    ProcessElementValueNumber,
    TaskElementValueString,
    TaskElementValueNumber,
    TaskElementValueObject,
    TaskElementValueDocument,
    TaskElementValuePrincipal,
]

ElementValuesDicModels = Union[Process, ProcessPageItem, Task, TaskPageItem]
ElementValuesListModels = Union[ProcessSaveElementCommand, TaskSaveElementCommand]

ElementValueSimpleType = Union[
    str,
    int,
    float,
    bool,
    date,
    Dict[str, any],
    TaskElementValueDocumentItem,
    TaskElementValuePrincipalItem,
]


class ElementValueAccessor(ABC):
    @abstractmethod
    def get_element_values(self) -> List[ElementValueUnion]:
        raise NotImplementedError

    @abstractmethod
    def set_element_values(self, element_values: List[ElementValueUnion]):
        raise NotImplementedError

    @abstractmethod
    def to_element_value_object(
        self, element_value: Optional[ElementValueSimpleType]
    ) -> Optional[ElementValueUnion]:
        raise NotImplementedError


class ProcessElementValueAccessor(ElementValueAccessor):
    def get_element_values(self) -> List[ElementValueUnion]:
        raise NotImplementedError

    def set_element_values(self, element_values: List[ElementValueUnion]):
        raise NotImplementedError

    def to_element_value_object(
        self, element_value: Optional[ElementValueSimpleType]
    ) -> Optional[ElementValueUnion]:
        if element_value is None:
            return None
        elif isinstance(element_value, str):
            return ProcessElementValueString(
                valid=True,
                value=element_value,
            )
        elif isinstance(element_value, (float, int)):
            return ProcessElementValueNumber(
                valid=True,
                value=element_value,
            )
        else:
            raise Exception(f"Unsupported value {element_value.__class__}")


class TaskElementValueAccessor(ElementValueAccessor):
    def get_element_values(self) -> List[ElementValueUnion]:
        raise NotImplementedError

    def set_element_values(self, element_values: List[ElementValueUnion]):
        raise NotImplementedError

    def to_element_value_object(
        self, element_value: Optional[ElementValueSimpleType]
    ) -> Optional[ElementValueUnion]:
        if element_value is None:
            return None
        elif isinstance(element_value, str):
            return TaskElementValueString(
                valid=True,
                value=element_value,
            )
        elif isinstance(element_value, (float, int)):
            return TaskElementValueNumber(
                valid=True,
                value=element_value,
            )
        elif isinstance(element_value, dict):
            return TaskElementValueObject(
                valid=True,
                value=element_value,
            )
        elif isinstance(element_value, TaskElementValueDocumentItem):
            return TaskElementValueDocument(
                valid=True,
                value=element_value,
            )
        elif isinstance(element_value, TaskElementValuePrincipalItem):
            return TaskElementValuePrincipal(
                valid=True,
                value=element_value,
            )
        else:
            raise Exception(f"Unsupported value {element_value.__class__}")


def get_element_value_valid(accessor: ElementValueAccessor) -> bool:
    """
    Check if all related valid values are TRUE.

    Arguments:
        accessor: Element values accessor.

    Returns:
        True if all related valid values are TRUE, otherwise False.
    """
    return all(element_value.valid for element_value in accessor.get_element_values())


def get_element_value_valid_at(accessor: ElementValueAccessor, index: int) -> bool:
    """
    Check if the requested valid value at the given index is TRUE.

    Arguments:
        accessor: Element values accessor.
        index: The element value index.

    Returns:
        The requested valid value if it exists, otherwise None.
    """
    element_values = accessor.get_element_values()
    if len(element_values) <= index:
        raise IndexError(f"Array index out of bound: {index}")

    return element_values[index].valid


def set_element_value_valid(
    accessor: ElementValueAccessor, valid: Optional[bool]
) -> ElementValueAccessor:
    """
    Set the valid value for all element values.

    Arguments:
        accessor: Element values accessor.
        valid: The valid value.

    Returns:
        The passed accessor.
    """
    element_values = accessor.get_element_values()
    for elementValue in element_values:
        elementValue.valid = valid

    return accessor


def set_element_value_valid_at(
    accessor: ElementValueAccessor, valid: Optional[bool], index: int
) -> ElementValueAccessor:
    """
    Set the valid value for the selected element value.

    Arguments:
        accessor: Element values accessor.
        valid: The valid value.
        index: The element value index.

    Returns:
        The passed model object.
    """
    element_values = accessor.get_element_values()
    if index < 0 or index >= len(element_values):
        raise IndexError(f"Array index out of bound: {index}")

    element_values[index].valid = valid

    return accessor


def set_element_value(
    accessor: ElementValueAccessor,
    element_value: Optional[ElementValueSimpleType] = None,
) -> ElementValueAccessor:
    """
    Set an element value.

    Arguments:
        accessor: Element values accessor.
        element_value: The element value. If the value is None, all current values are removed.

    Returns:
        The passed model related object.
    """
    return set_element_value_list(
        accessor, [element_value] if element_value is not None else None
    )


def set_element_value_list(
    accessor: ElementValueAccessor,
    element_values: Optional[List[ElementValueSimpleType]] = None,
) -> ElementValueAccessor:
    """
    Set an element value.

    Arguments:
        accessor: Element values accessor.
        element_values: The element values. If the values is None, all current values are removed.

    Returns:
        The passed model related object.
    """
    element_value_objects = _to_element_value_objects(accessor, element_values)
    accessor.set_element_values(element_value_objects)

    return accessor


def add_element_value(
    accessor: ElementValueAccessor,
    element_value: Optional[ElementValueSimpleType] = None,
) -> ElementValueAccessor:
    """
    Add an element value.

    Arguments:
        accessor: Element values accessor.
        element_value: The element value. If the value is None, all current values are removed.

    Returns:
        The passed model related object.
    """
    return add_element_value_list(
        accessor, [element_value] if element_value is not None else None
    )


def add_element_value_list(
    accessor: ElementValueAccessor,
    element_values: Optional[List[ElementValueSimpleType]] = None,
) -> ElementValueAccessor:
    """
    Add element values.

    Arguments:
        accessor: Element values accessor.
        element_values: The element values. If the values is None or empty, all current values are removed.

    Returns:
        The passed model related object.
    """

    element_values_current = accessor.get_element_values()
    element_values = _to_element_value_objects(accessor, element_values)

    accessor.set_element_values(element_values_current + element_values)

    return accessor


def get_element_value_as_str(accessor: ElementValueAccessor) -> str:
    """
    Get an element as a str.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a str.

    Raises:
        ValueError: If value doesn't exist.
    """
    element_value = find_element_value_as_str(accessor)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def find_element_value_as_str(accessor: ElementValueAccessor) -> Optional[str]:
    """
    Try to get an element as a str.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a str.
    """
    element_values = get_element_value_as_str_list(accessor)
    if len(element_values) == 0:
        return None
    return element_values[0]


def get_element_value_as_str_list(accessor: ElementValueAccessor) -> List[str]:
    """
    Try to get an element as a str.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a str.
    """
    element_values = accessor.get_element_values()
    return [
        str(elementValue.value)
        for elementValue in element_values
        if elementValue.value is not None
        and (elementValue.type == "STRING" or elementValue.type == "NUMBER")
    ]


def get_element_value_as_float(accessor: ElementValueAccessor) -> float:
    """
    Get an element as a float.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a str.

    Raises:
        ValueError: If value doesn't exist.
    """
    element_value = find_element_value_as_float(accessor)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def find_element_value_as_float(accessor: ElementValueAccessor) -> Optional[float]:
    """
    Try to get element as a float.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a float.
    """
    element_values = get_element_value_as_float_list(accessor)
    if len(element_values) == 0:
        return None
    return element_values[0]


def get_element_value_as_float_list(accessor: ElementValueAccessor) -> List[float]:
    """
    Get all elements as a float list.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a float.
    """
    element_values = accessor.get_element_values()
    return [
        float(elementValue.value)
        for elementValue in element_values
        if elementValue.value is not None
        and (elementValue.type == "STRING" or elementValue.type == "NUMBER")
    ]


def get_element_value_as_date(accessor: ElementValueAccessor) -> date:
    """
    Get an element as a date.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a date.

    Raises:
        ValueError: If value doesn't exist.
    """
    element_value = find_element_value_as_date(accessor)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def find_element_value_as_date(accessor: ElementValueAccessor) -> Optional[date]:
    """
    Try to get an element as a date.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a date.
    """
    element_values = get_element_value_as_date_list(accessor)

    if len(element_values) == 0:
        return None

    return element_values[0]


def get_element_value_as_date_list(accessor: ElementValueAccessor) -> List[date]:
    """
    Get all elements as date list.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element values as date list.
    """
    element_values = accessor.get_element_values()
    return [
        date.fromisoformat(elementValue.value)
        for elementValue in element_values
        if elementValue.value is not None and (elementValue.type == "STRING")
    ]


def get_element_value_as_dict(accessor: ElementValueAccessor) -> dict:
    """
    Get an element as a dict.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a dict.

    Raises:
        ValueError: If value doesn't exist.
    """
    element_value = find_element_value_as_dict(accessor)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def find_element_value_as_dict(accessor: ElementValueAccessor) -> Optional[dict]:
    """
    Try to get an element as a dict.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a dict.
    """
    element_values = get_element_value_as_dict_list(accessor)

    if len(element_values) == 0:
        return None

    return element_values[0]


def get_element_value_as_dict_list(accessor: ElementValueAccessor) -> List[dict]:
    """
    Get all elements as dict list.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element values as dict list.
    """
    element_values = accessor.get_element_values()
    return [
        elementValue.value
        for elementValue in element_values
        if elementValue.value is not None and (elementValue.type == "OBJECT")
    ]


def get_element_value_as_document(
    accessor: ElementValueAccessor,
) -> TaskElementValueDocumentItem:
    """
    Get an element as a TaskElementValueDocumentItem.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a TaskElementValueDocumentItem.
    """
    element_value = find_element_value_as_document(accessor)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def find_element_value_as_document(
    accessor: ElementValueAccessor,
) -> Optional[TaskElementValueDocumentItem]:
    """
    Try to get an element as a TaskElementValueDocumentItem.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a TaskElementValueDocumentItem.
    """
    element_values = get_element_value_as_document_list(accessor)

    if len(element_values) == 0:
        return None

    return element_values[0]


def get_element_value_as_document_list(
    accessor: ElementValueAccessor,
) -> List[TaskElementValueDocumentItem]:
    """
    Get all elements as TaskElementValueDocumentItem list.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element values as TaskElementValueDocumentItem list.
    """
    element_values = accessor.get_element_values()
    return [
        elementValue.value
        for elementValue in element_values
        if elementValue.value is not None and (elementValue.type == "DOCUMENT")
    ]


def get_element_value_as_principal(
    accessor: ElementValueAccessor,
) -> TaskElementValuePrincipalItem:
    """
    Get an element as a TaskElementValuePrincipalItem.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a TaskElementValuePrincipalItem.
    """
    element_value = find_element_value_as_principal(accessor)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def find_element_value_as_principal(
    accessor: ElementValueAccessor,
) -> Optional[TaskElementValuePrincipalItem]:
    """
    Try to get an element as a TaskElementValuePrincipalItem.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element value as a TaskElementValuePrincipalItem.
    """
    element_values = get_element_value_as_principal_list(accessor)

    if len(element_values) == 0:
        return None

    return element_values[0]


def get_element_value_as_principal_list(
    accessor: ElementValueAccessor,
) -> List[TaskElementValuePrincipalItem]:
    """
    Get all elements as TaskElementValuePrincipalItem list.

    Arguments:
        accessor: Element values accessor.

    Returns:
        The element values as TaskElementValuePrincipalItem list.
    """
    element_values = accessor.get_element_values()
    return [
        elementValue.value
        for elementValue in element_values
        if elementValue.value is not None and (elementValue.type == "PRINCIPAL")
    ]


def _to_element_value_objects(
    accessor: ElementValueAccessor,
    element_values: Optional[List[ElementValueSimpleType]] = None,
) -> List[Union[ProcessElementValueUnion, TaskElementValueUnion]]:
    element_value_objects: List[
        Union[ProcessElementValueUnion, TaskElementValueUnion]
    ] = []
    for element_value in element_values or []:
        element_value = _transform_element_value(element_value)

        element_value_object = accessor.to_element_value_object(element_value)

        element_value_objects.append(element_value_object)

    return element_value_objects


def _transform_element_value(
    element_value: ElementValueSimpleType,
) -> ElementValueSimpleType:
    if isinstance(element_value, (str, float, int)):
        element_value = element_value
    elif isinstance(element_value, date):
        element_value = element_value.isoformat()
    elif isinstance(
        element_value,
        (dict, TaskElementValueDocumentItem, TaskElementValuePrincipalItem),
    ):
        element_value = element_value
    else:
        raise Exception(f"Unsupported value {element_value.__class__}")

    return element_value
