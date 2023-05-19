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
from datetime import date

from ..models import (
    Process,
    ProcessElementValueString,
    ProcessElementValueNumber,
    ProcessPageItem,
    ProcessSaveElementCommand,
    Task,
    TaskElementValueString,
    TaskElementValueNumber,
    TaskElementValueObject,
    TaskElementValueDocument,
    TaskElementValueDocumentItem,
    TaskElementValuePrincipal,
    TaskElementValuePrincipalItem,
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

ElementValuesDicModels = Union[Process, ProcessPageItem, Task, TaskPageItem]
ElementValuesListModels = Union[ProcessSaveElementCommand, TaskSaveElementCommand]

SimpleType = Union[str, int, bool, date, Dict[str, any], TaskElementValueDocumentItem, TaskElementValuePrincipalItem]


def get_element_value_valid(model: ElementValuesListModels) -> bool:
    """
    Check if all related valid values are TRUE.

    :param model: Related model.
    :return: True if all related valid values are TRUE, otherwise False.
    """
    return _get_element_value_valid(model)


def get_element_value_valid_with_code(model: ElementValuesDicModels, element_definition_code: str) -> bool:
    """
    Check if all related valid values are TRUE.

    :param model: Related model.
    :param element_definition_code: Element Definition Code.
    :return: True if all related valid values are TRUE, otherwise False.
    """
    return _get_element_value_valid(model, element_definition_code)


def get_element_value_valid_at(model: ElementValuesListModels, index: int) -> bool:
    """
    Check if the requested valid value at the given index is TRUE.

    Arguments:
        model: The related model.
        index: The element value index.

    Returns:
        The requested valid value if it exists, otherwise None.
    """
    return _get_element_value_valid_at(model, GetElementValueValidAtOptions(index=index))


def get_element_value_valid_at_with_code(
    model: ElementValuesDicModels,
    element_definition_code: str,
    index: int,
) -> bool:
    """
    Check if the requested valid value at the given index is TRUE.

    Arguments:
        model: The related model.
        element_definition_code: The element definition code.
        index: The element value index.

    Returns:
        The requested valid value if it exists, otherwise None.
    """
    return _get_element_value_valid_at(
        model, GetElementValueValidAtOptions(element_definition_code=element_definition_code, index=index)
    )


def set_element_value_valid(model: ElementValuesListModels, valid: Optional[bool]) -> ElementValuesDicModels:
    """
    Set the valid value for all element values.

    Arguments:
        model: The related model.
        valid: The valid value.

    Returns:
        The passed model related object.
    """
    return _set_element_value_valid(model, SetElementValueValidOptions(valid=valid))


def set_element_value_valid_with_code(
    model: ElementValuesDicModels, element_definition_code: str, valid: Optional[bool]
) -> ElementValuesDicModels:
    """
    Set the valid value for all element values.

    Arguments:
        model: The related model.
        element_definition_code: The element definition code.
        valid: The valid value.

    Returns:
        The passed model related object.
    """
    return _set_element_value_valid(
        model, SetElementValueValidOptions(element_definition_code=element_definition_code, valid=valid)
    )


def set_element_value_valid_at(
    model: ElementValuesListModels,
    valid: Optional[bool],
    index: int,
) -> ElementValuesListModels:
    """
    Set the valid value for the selected element value.

    Arguments:
        model: The related model.
        valid: The valid value.
        index: The element value index.

    Returns:
        The passed model object.
    """
    return _set_element_value_valid_at(model, SetElementValueValidAtOptions(valid=valid, index=index))


def set_element_value_valid_at_with_code(
    model: ElementValuesDicModels,
    element_definition_code: str,
    valid: Optional[bool],
    index: int,
) -> ElementValuesDicModels:
    """
    Set the valid value for the selected element value.

    Arguments:
        model: The related model.
        element_definition_code: The element definition code.
        valid: The valid value.
        index: The element value index.

    Returns:
        The passed model object.
    """
    return _set_element_value_valid_at(
        model, SetElementValueValidAtOptions(element_definition_code=element_definition_code, valid=valid, index=index)
    )


def set_element_value(
    model: ElementValuesListModels,
    element_value: Optional[SimpleType] = None,
) -> ElementValuesListModels:
    """
    Set an element value.

    Args:
        model: The related model.
        element_value: The element value. If the value is None, all current values are removed.

    Returns:
        The passed model related object.
    """
    return _set_element_values(
        model,
        SetElementValuesOptions(
            element_values=[element_value] if element_value is not None else None,
        ),
    )


def set_element_value_with_code(
    model: ElementValuesDicModels,
    element_definition_code: str,
    element_value: Optional[SimpleType] = None,
) -> ElementValuesDicModels:
    """
    Set an element value.

    Args:
        model: The related model.
        element_definition_code: The element definition code.
        element_value: The element value. If the value is None, all current values are removed.

    Returns:
        The passed model related object.
    """
    return _set_element_values(
        model,
        SetElementValuesOptions(
            element_definition_code=element_definition_code,
            element_values=[element_value] if element_value is not None else None,
        ),
    )


def set_element_value_list(
    model: ElementValuesListModels,
    element_values: Optional[List[SimpleType]] = None,
) -> ElementValuesListModels:
    """
    Set an element value.

    Args:
        model: The related model.
        element_values: The element values. If the values is None, all current values are removed.

    Returns:
        The passed model related object.
    """
    return _set_element_values(model, SetElementValuesOptions(element_values=element_values))


def set_element_value_list_with_code(
    model: ElementValuesDicModels,
    element_definition_code: str,
    element_values: Optional[List[SimpleType]] = None,
) -> ElementValuesDicModels:
    """
    Set an element value.

    Args:
        model: The related model.
        element_definition_code: The element definition code.
        element_values: The element value. If the value is None or empty, all current values are removed.

    Returns:
        The passed model related object.
    """
    return _set_element_values(
        model, SetElementValuesOptions(element_definition_code=element_definition_code, element_values=element_values)
    )


def add_element_value(
    model: ElementValuesListModels,
    element_value: Optional[SimpleType] = None,
) -> ElementValuesListModels:
    """
    Add an element value.

    Args:
        model: The related model.
        element_value: The element value. If the value is None, all current values are removed.

    Returns:
        The passed model related object.
    """
    return _add_element_values(
        model,
        AddElementValuesOptions(
            element_values=[element_value] if element_value is not None else None,
        ),
    )


def add_element_value_with_code(
    model: ElementValuesDicModels,
    element_definition_code: str,
    element_value: Optional[SimpleType] = None,
) -> ElementValuesDicModels:
    """
    Set an element value.

    Args:
        model: The related model.
        element_definition_code: The element definition code.
        element_value: The element value. If the value is None, all current values are removed.

    Returns:
        The passed model related object.
    """
    return _add_element_values(
        model,
        AddElementValuesOptions(
            element_definition_code=element_definition_code,
            element_values=[element_value] if element_value is not None else None,
        ),
    )


def add_element_value_list(
    model: ElementValuesListModels,
    element_values: Optional[List[SimpleType]] = None,
) -> ElementValuesDicModels:
    """
    Set an element value.

    Args:
        model: The related model.
        element_values: The element values. If the values is None or empty, all current values are removed.

    Returns:
        The passed model related object.
    """
    return _add_element_values(model, AddElementValuesOptions(element_values=element_values))


def add_element_value_list_with_code(
    model: ElementValuesDicModels,
    element_definition_code: str,
    element_values: Optional[List[SimpleType]] = None,
) -> ElementValuesDicModels:
    """
    Set an element value.

    Args:
        model: The related model.
        element_definition_code: The element definition code.
        element_values: The element values. If the values is None or empty, all current values are removed.

    Returns:
        The passed model related object.
    """
    return _add_element_values(
        model, AddElementValuesOptions(element_definition_code=element_definition_code, element_values=element_values)
    )


def get_element_value_as_str(model: ElementValuesListModels) -> str:
    """
    Get an element as a str.

    Args:
        model: The related model.

    Returns:
        The element value as a str.
    """
    return _get_element_value_as_str(model)


def get_element_value_as_str_with_code(model: ElementValuesDicModels, element_definition_code: str) -> str:
    """
    Get an element as a str.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a str.
    """
    return _get_element_value_as_str(model, element_definition_code)


def find_element_value_as_str(model: ElementValuesListModels) -> Optional[str]:
    """
    Try to get an element as a str.

    Args:
        model: The related model.

    Returns:
        The element value as a str.
    """
    return _find_element_value_as_str(model)


def find_element_value_as_str_with_code(model: ElementValuesDicModels, element_definition_code: str) -> Optional[str]:
    """
    Try to get an element as a str.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a str.
    """
    return _find_element_value_as_str(model, element_definition_code)


def get_element_value_as_str_list(model: ElementValuesListModels) -> List[str]:
    """
    Try to get an element as a str.

    Args:
        model: The related model.

    Returns:
        The element value as a str.
    """
    return _get_element_value_as_str_list(model)


def get_element_value_as_str_list_with_code(model: ElementValuesDicModels, element_definition_code: str) -> List[str]:
    """
    Try to get an element as a str.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a str.
    """
    return _get_element_value_as_str_list(model, element_definition_code)


def get_element_value_as_float(model: ElementValuesListModels) -> float:
    """
    Get an element as a float.

    Args:
        model: The related model.

    Returns:
        The element value as a float.
    """
    return _get_element_value_as_float(model)


def get_element_value_as_float_with_code(model: ElementValuesDicModels, element_definition_code: str) -> float:
    """
    Get an element as a float.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a float.
    """
    return _get_element_value_as_float(model, element_definition_code)


def find_element_value_as_float(model: ElementValuesListModels) -> float:
    """
    Try to get element as a float.

    Args:
        model: The related model.

    Returns:
        The element value as a float.
    """
    return _find_element_value_as_float(model)


def find_element_value_as_float_with_code(model: ElementValuesDicModels, element_definition_code: str) -> float:
    """
    Try to get an element as a float.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a float.
    """
    return _find_element_value_as_float(model, element_definition_code)


def get_element_value_as_float_list(model: ElementValuesListModels) -> List[float]:
    """
    Get all elements as a float list.

    Args:
        model: The related model.

    Returns:
        The element value as a float.
    """
    return _get_element_value_as_float_list(model)


def get_element_value_as_float_list_with_code(
    model: ElementValuesDicModels, element_definition_code: str
) -> List[float]:
    """
    Get all elements as a float list.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a float.
    """
    return _get_element_value_as_float_list(model, element_definition_code)


def get_element_value_as_date(model: ElementValuesListModels) -> date:
    """
    Get an element as a date.

    Args:
        model: The related model.

    Returns:
        The element value as a date.
    """
    return _get_element_value_as_date(model)


def get_element_value_as_date_with_code(model: ElementValuesDicModels, element_definition_code: str) -> date:
    """
    Get an element as a date.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a date.
    """
    return _get_element_value_as_date(model, element_definition_code)


def find_element_value_as_date(model: ElementValuesListModels) -> Optional[date]:
    """
    Try to get an element as a date.

    Args:
        model: The related model.

    Returns:
        The element value as a date.
    """
    return _find_element_value_as_date(model)


def find_element_value_as_date_with_code(model: ElementValuesDicModels, element_definition_code: str) -> Optional[date]:
    """
    Try to get  an element as a date.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a date.
    """
    return _find_element_value_as_date(model, element_definition_code)


def get_element_value_as_date_list(model: ElementValuesListModels) -> Optional[List[date]]:
    """
    Get all elements as date list.

    Args:
        model: The related model.

    Returns:
        The element values as date list.
    """
    return _get_element_value_as_date_list(model)


def get_element_value_as_date_list_with_code(
    model: ElementValuesDicModels, element_definition_code: str
) -> Optional[List[date]]:
    """
    Get all elements as date list.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element values as date list.
    """
    return _get_element_value_as_date_list(model, element_definition_code)


def get_element_value_as_dict(model: ElementValuesListModels) -> dict:
    """
    Get an element as a dict.

    Args:
        model: The related model.

    Returns:
        The element value as a dict.
    """
    return _get_element_value_as_dict(model)


def get_element_value_as_dict_with_code(model: ElementValuesDicModels, element_definition_code: str) -> dict:
    """
    Get an element as a dict.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a dict.
    """
    return _get_element_value_as_dict(model, element_definition_code)


def find_element_value_as_dict(model: ElementValuesListModels) -> Optional[dict]:
    """
    Try to get an element as a dict.

    Args:
        model: The related model.

    Returns:
        The element value as a dict.
    """
    return _find_element_value_as_dict(model)


def find_element_value_as_dict_with_code(model: ElementValuesDicModels, element_definition_code: str) -> Optional[dict]:
    """
    Try to get  an element as a dict.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a dict.
    """
    return _find_element_value_as_dict(model, element_definition_code)


def get_element_value_as_dict_list(model: ElementValuesListModels) -> Optional[List[dict]]:
    """
    Get all elements as dict list.

    Args:
        model: The related model.

    Returns:
        The element values as dict list.
    """
    return _get_element_value_as_dict_list(model)


def get_element_value_as_dict_list_with_code(
    model: ElementValuesDicModels, element_definition_code: str
) -> Optional[List[dict]]:
    """
    Get all elements as dict list.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element values as dict list.
    """
    return _get_element_value_as_dict_list(model, element_definition_code)


def get_element_value_as_document(model: TaskSaveElementCommand) -> TaskElementValueDocumentItem:
    """
    Get an element as a TaskElementValueDocumentItem.

    Args:
        model: The related model.

    Returns:
        The element value as a TaskElementValueDocumentItem.
    """
    return _get_element_value_as_document(model)


def get_element_value_as_document_with_code(
    model: Union[Task, TaskPageItem], element_definition_code: str
) -> TaskElementValueDocumentItem:
    """
    Get an element as a TaskElementValueDocumentItem.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a TaskElementValueDocumentItem.
    """
    return _get_element_value_as_document(model, element_definition_code)


def find_element_value_as_document(model: ElementValuesListModels) -> Optional[TaskElementValueDocumentItem]:
    """
    Try to get an element as a TaskElementValueDocumentItem.

    Args:
        model: The related model.

    Returns:
        The element value as a TaskElementValueDocumentItem.
    """
    return _find_element_value_as_document(model)


def find_element_value_as_document_with_code(
    model: ElementValuesDicModels, element_definition_code: str
) -> Optional[TaskElementValueDocumentItem]:
    """
    Try to get  an element as a TaskElementValueDocumentItem.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a TaskElementValueDocumentItem.
    """
    return _find_element_value_as_document(model, element_definition_code)


def get_element_value_as_document_list(model: ElementValuesListModels) -> Optional[List[TaskElementValueDocumentItem]]:
    """
    Get all elements as TaskElementValueDocumentItem list.

    Args:
        model: The related model.

    Returns:
        The element values as TaskElementValueDocumentItem list.
    """
    return _get_element_value_as_document_list(model)


def get_element_value_as_document_list_with_code(
    model: ElementValuesDicModels, element_definition_code: str
) -> Optional[List[TaskElementValueDocumentItem]]:
    """
    Get all elements as TaskElementValueDocumentItem list.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element values as TaskElementValueDocumentItem list.
    """
    return _get_element_value_as_document_list(model, element_definition_code)


def get_element_value_as_principal(model: TaskSaveElementCommand) -> TaskElementValuePrincipalItem:
    """
    Get an element as a TaskElementValuePrincipalItem.

    Args:
        model: The related model.

    Returns:
        The element value as a TaskElementValuePrincipalItem.
    """
    return _get_element_value_as_principal(model)


def get_element_value_as_principal_with_code(
    model: Union[Task, TaskPageItem], element_definition_code: str
) -> TaskElementValuePrincipalItem:
    """
    Get an element as a TaskElementValuePrincipalItem.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a TaskElementValuePrincipalItem.
    """
    return _get_element_value_as_principal(model, element_definition_code)


def find_element_value_as_principal(model: ElementValuesListModels) -> Optional[TaskElementValuePrincipalItem]:
    """
    Try to get an element as a TaskElementValuePrincipalItem.

    Args:
        model: The related model.

    Returns:
        The element value as a TaskElementValuePrincipalItem.
    """
    return _find_element_value_as_principal(model)


def find_element_value_as_principal_with_code(
    model: ElementValuesDicModels, element_definition_code: str
) -> Optional[TaskElementValuePrincipalItem]:
    """
    Try to get  an element as a TaskElementValuePrincipalItem.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element value as a TaskElementValuePrincipalItem.
    """
    return _find_element_value_as_principal(model, element_definition_code)


def get_element_value_as_principal_list(
    model: ElementValuesListModels,
) -> Optional[List[TaskElementValuePrincipalItem]]:
    """
    Get all elements as TaskElementValuePrincipalItem list.

    Args:
        model: The related model.

    Returns:
        The element values as TaskElementValuePrincipalItem list.
    """
    return _get_element_value_as_principal_list(model)


def get_element_value_as_principal_list_with_code(
    model: ElementValuesDicModels, element_definition_code: str
) -> Optional[List[TaskElementValuePrincipalItem]]:
    """
    Get all elements as TaskElementValuePrincipalItem list.

    Args:
        model: The related model.
        element_definition_code: The element definition code.

    Returns:
        The element values as TaskElementValuePrincipalItem list.
    """
    return _get_element_value_as_principal_list(model, element_definition_code)


# =======================================
# =======================================
# =======================================


def _get_element_value_valid(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> bool:
    """
    Check if all related valid values are TRUE.

    :param model: Related model.
    :param element_definition_code: Element Definition Code.
    :return: True if all related valid values are TRUE, otherwise False.
    """
    return all(element_value.valid for element_value in _get_element_values(model, element_definition_code))


class GetElementValueValidAtOptions:
    element_definition_code: Optional[str]
    index: Optional[int]

    def __init__(self, element_definition_code: Optional[str] = None, index: Optional[int] = None):
        self.element_definition_code = element_definition_code
        self.index = index


def _get_element_value_valid_at(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    options: GetElementValueValidAtOptions,
) -> bool:
    """
    Get the requested valid value at the given index.

    Arguments:
        model: The related model.
        options: The options specifying the element definition code and index.

    Returns:
        The requested valid value if it exists, otherwise None.

    Raises:
        IndexError: If the index is not found in the element values.
    """
    element_values = _get_element_values(model, options.element_definition_code)
    if len(element_values) <= options.index:
        raise IndexError(f"Array index out of bound: {options.index}")

    return element_values[options.index].valid


class SetElementValueValidOptions:
    element_definition_code: Optional[str]
    valid: Optional[bool]

    def __init__(self, element_definition_code: Optional[str] = None, valid: Optional[bool] = None):
        self.element_definition_code = element_definition_code
        self.valid = valid


def _set_element_value_valid(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    options: SetElementValueValidOptions,
) -> Union[ElementValuesDicModels, ElementValuesListModels]:
    """
    Set the valid value for all element values.

    Arguments:
        model: The related model.
        options: The options specifying the element definition code and valid value.

    Returns:
        The passed model related object.
    """
    element_values = _get_element_values(model, options.element_definition_code)
    for elementValue in element_values:
        elementValue.valid = options.valid

    return model


class SetElementValueValidAtOptions:
    element_definition_code: Optional[str]
    valid: Optional[bool]
    index: Optional[int]

    def __init__(
        self, element_definition_code: Optional[str] = None, valid: Optional[bool] = None, index: Optional[int] = None
    ):
        self.element_definition_code = element_definition_code
        self.valid = valid
        self.index = index


def _set_element_value_valid_at(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    options: SetElementValueValidAtOptions,
) -> Union[ElementValuesDicModels, ElementValuesListModels]:
    """
    Set the valid value for the selected element value.

    Arguments:
        model: The related model.
        options: The options specifying the element definition code, valid value, and index.

    Returns:
        The passed model object.
    """
    element_values = _get_element_values(model, options.element_definition_code)
    if options.index < 0 or options.index >= len(element_values):
        raise IndexError(f"Array index out of bound: {options.index}")

    element_values[options.index].valid = options.valid

    return model


def _get_element_value_as_str(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> str:
    element_value = _find_element_value_as_str(model, element_definition_code)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def _find_element_value_as_str(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> Optional[str]:
    element_values = _get_element_value_as_str_list(model, element_definition_code)
    if len(element_values) == 0:
        return None
    return element_values[0]


def _get_element_value_as_str_list(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> List[str]:
    element_values = _get_element_values(model, element_definition_code)
    return [
        str(elementValue.value)
        for elementValue in element_values
        if elementValue.value is not None and (elementValue.type == "STRING" or elementValue.type == "NUMBER")
    ]


class SetElementValuesOptions:
    element_definition_code: Optional[str]
    element_values: List[SimpleType]

    def __init__(
        self,
        element_definition_code: Optional[str] = None,
        element_values: Optional[List[str]] = None,
    ) -> None:
        self.element_definition_code = element_definition_code
        self.element_values = element_values or []


def _set_element_values(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    options: SetElementValuesOptions,
) -> Union[ElementValuesDicModels, ElementValuesListModels]:
    return _update_element_values(
        model,
        element_definition_code=options.element_definition_code,
        element_values=_to_element_values_object(model, options.element_values),
    )


class AddElementValuesOptions:
    element_definition_code: Optional[str]
    element_values: List[SimpleType]

    def __init__(
        self,
        element_definition_code: Optional[str] = None,
        element_values: Optional[List[SimpleType]] = None,
    ) -> None:
        self.element_definition_code = element_definition_code
        self.element_values = element_values or []


def _add_element_values(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    options: AddElementValuesOptions,
) -> Union[ElementValuesDicModels, ElementValuesListModels]:
    element_values_current = _get_element_values(model, options.element_definition_code)
    element_values = _to_element_values_object(model, options.element_values)

    return _update_element_values(
        model,
        options.element_definition_code,
        element_values_current + element_values,
    )


def _to_element_values_object(
    model: Union[ElementValuesDicModels, ElementValuesListModels], element_values: List[SimpleType]
) -> List[Union[ProcessElementValueUnion, TaskElementValueUnion]]:
    element_values_object: List[Union[ProcessElementValueUnion, TaskElementValueUnion]] = []
    for element_value in element_values:
        element_value = _transform_element_value(element_value)

        element_value_object = _to_element_value_object(model, element_value)

        element_values_object.append(element_value_object)

    return element_values_object


def _transform_element_value(element_value: SimpleType) -> SimpleType:
    if isinstance(element_value, (str, float, int)):
        element_value = element_value
    elif isinstance(element_value, date):
        element_value = element_value.isoformat()
    elif isinstance(element_value, (dict, TaskElementValueDocumentItem, TaskElementValuePrincipalItem)):
        element_value = element_value
    else:
        raise Exception(f"Unsupported value {element_value.__class__}")

    return element_value


def _to_element_value_object(
    model: Union[ElementValuesDicModels, ElementValuesListModels], element_value: SimpleType
) -> Union[ProcessElementValueUnion, TaskElementValueUnion]:
    element_value_object: Optional[Union[ProcessElementValueUnion, TaskElementValueUnion]] = None
    if isinstance(model, (Process, ProcessPageItem, ProcessSaveElementCommand)):
        element_value_object = _to_element_value_object_process(element_value, element_value_object)
    elif isinstance(model, (Task, TaskPageItem, TaskSaveElementCommand)):
        element_value_object = _to_element_value_object_task(element_value, element_value_object)
    else:
        raise Exception(f"Unsupported model {model.__class__}")

    return element_value_object


def _to_element_value_object_process(element_value, element_value_object):
    if isinstance(element_value, str):
        element_value_object = ProcessElementValueString(
            valid=True,
            value=element_value,
        )
    elif isinstance(element_value, (float, int)):
        element_value_object = ProcessElementValueNumber(
            valid=True,
            value=element_value,
        )
    else:
        raise Exception(f"Unsupported value {element_value.__class__}")
    return element_value_object


def _to_element_value_object_task(element_value, element_value_object):
    if isinstance(element_value, str):
        element_value_object = TaskElementValueString(
            valid=True,
            value=element_value,
        )
    elif isinstance(element_value, (float, int)):
        element_value_object = TaskElementValueNumber(
            valid=True,
            value=element_value,
        )
    elif isinstance(element_value, dict):
        element_value_object = TaskElementValueObject(
            valid=True,
            value=element_value,
        )
    elif isinstance(element_value, TaskElementValueDocumentItem):
        element_value_object = TaskElementValueDocument(
            valid=True,
            value=element_value,
        )
    elif isinstance(element_value, TaskElementValuePrincipalItem):
        element_value_object = TaskElementValuePrincipal(
            valid=True,
            value=element_value,
        )
    else:
        raise Exception(f"Unsupported value {element_value.__class__}")
    return element_value_object


def _get_element_value_as_float(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> float:
    element_value = _find_element_value_as_float(model, element_definition_code)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def _find_element_value_as_float(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> Optional[float]:
    element_values = _get_element_value_as_float_list(model, element_definition_code)
    if len(element_values) == 0:
        return None
    return element_values[0]


def _get_element_value_as_float_list(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> List[float]:
    element_values = _get_element_values(model, element_definition_code)
    return [
        float(elementValue.value)
        for elementValue in element_values
        if elementValue.value is not None and (elementValue.type == "STRING" or elementValue.type == "NUMBER")
    ]


def _get_element_value_as_date(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> date:
    element_value = _find_element_value_as_date(model, element_definition_code)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def _find_element_value_as_date(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> Optional[date]:
    element_values = _get_element_value_as_date_list(model, element_definition_code)
    if len(element_values) == 0:
        return None
    return element_values[0]


def _get_element_value_as_date_list(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> List[date]:
    element_values = _get_element_values(model, element_definition_code)
    return [
        date.fromisoformat(elementValue.value)
        for elementValue in element_values
        if elementValue.value is not None and (elementValue.type == "STRING")
    ]


def _get_element_value_as_dict(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> dict:
    element_value = _find_element_value_as_dict(model, element_definition_code)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def _find_element_value_as_dict(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> Optional[dict]:
    element_values = _get_element_value_as_dict_list(model, element_definition_code)
    if len(element_values) == 0:
        return None
    return element_values[0]


def _get_element_value_as_dict_list(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> List[dict]:
    element_values = _get_element_values(model, element_definition_code)
    return [
        elementValue.value
        for elementValue in element_values
        if elementValue.value is not None and (elementValue.type == "OBJECT")
    ]


def _get_element_value_as_document(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> TaskElementValueDocumentItem:
    element_value = _find_element_value_as_document(model, element_definition_code)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def _find_element_value_as_document(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> Optional[TaskElementValueDocumentItem]:
    element_values = _get_element_value_as_document_list(model, element_definition_code)
    if len(element_values) == 0:
        return None
    return element_values[0]


def _get_element_value_as_document_list(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> List[TaskElementValueDocumentItem]:
    element_values = _get_element_values(model, element_definition_code)
    return [
        elementValue.value
        for elementValue in element_values
        if elementValue.value is not None and (elementValue.type == "DOCUMENT")
    ]


def _get_element_value_as_principal(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> TaskElementValuePrincipalItem:
    element_value = _find_element_value_as_principal(model, element_definition_code)

    if element_value is None:
        raise ValueError("Value is required!")

    return element_value


def _find_element_value_as_principal(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> Optional[TaskElementValuePrincipalItem]:
    element_values = _get_element_value_as_principal_list(model, element_definition_code)
    if len(element_values) == 0:
        return None
    return element_values[0]


def _get_element_value_as_principal_list(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> List[TaskElementValuePrincipalItem]:
    element_values = _get_element_values(model, element_definition_code)
    return [
        elementValue.value
        for elementValue in element_values
        if elementValue.value is not None and (elementValue.type == "PRINCIPAL")
    ]


def _update_element_values(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
    element_values: Optional[List[Union[ProcessElementValueUnion, TaskElementValueUnion]]] = None,
) -> Union[ElementValuesDicModels, ElementValuesListModels]:
    if element_values is None or len(element_values) == 0:
        if model.element_values is not None:
            if element_definition_code is not None and isinstance(model.element_values, dict):
                model.element_values.pop(element_definition_code)
            elif element_definition_code is None and isinstance(model.element_values, list):
                model.element_values = None
    else:
        if element_definition_code is not None:
            if model.element_values is None:
                model.element_values = {}
            model.element_values[element_definition_code] = element_values.copy()
        elif element_definition_code is None:
            model.element_values = element_values.copy()

    return model


def _get_element_values(
    model: Union[ElementValuesDicModels, ElementValuesListModels],
    element_definition_code: Optional[str] = None,
) -> List[Union[ProcessElementValueUnion, TaskElementValueUnion]]:
    if model.element_values is None:
        return []

    if isinstance(model.element_values, list):
        return model.element_values

    if element_definition_code is None:
        return []

    element_values_by_code = model.element_values.get(element_definition_code)
    if element_values_by_code is None or len(element_values_by_code) == 0:
        return []

    return element_values_by_code
