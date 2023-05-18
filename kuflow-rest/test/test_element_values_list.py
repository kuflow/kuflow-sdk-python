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

import unittest
from datetime import date

from kuflow_rest.models import (
    TaskElementValueString,
    TaskElementValueNumber,
    TaskElementValueObject,
    TaskElementValuePrincipal,
    TaskElementValuePrincipalItem,
    TaskElementValueDocument,
    TaskElementValueDocumentItem,
    TaskSaveElementCommand,
)
from kuflow_rest.utils import (
    get_element_value_valid,
    get_element_value_valid_at,
    set_element_value_valid,
    set_element_value_valid_at,
    set_element_value,
    set_element_value_list,
    add_element_value,
    add_element_value_list,
    get_element_value_as_str,
    find_element_value_as_str,
    get_element_value_as_str_list,
    get_element_value_as_float,
    find_element_value_as_float,
    get_element_value_as_float_list,
    get_element_value_as_date,
    find_element_value_as_date,
    get_element_value_as_date_list,
    get_element_value_as_dict,
    find_element_value_as_dict,
    get_element_value_as_dict_list,
    get_element_value_as_document,
    find_element_value_as_document,
    get_element_value_as_document_list,
    get_element_value_as_principal,
    find_element_value_as_principal,
    get_element_value_as_principal_list,
)


class ElementValuesListUtilsTest(unittest.TestCase):
    def test_get_element_value_valid(self):
        command = prepare_command_save_element_command_str()

        value = get_element_value_valid(command)
        self.assertFalse(value)

    def test_get_element_value_valid_at(self):
        command = prepare_command_save_element_command_str()

        value = get_element_value_valid_at(command, 0)
        self.assertTrue(value)

        value = get_element_value_valid_at(command, 1)
        self.assertFalse(value)

    def test_set_element_value_valid(self):
        command = prepare_command_save_element_command_str()

        set_element_value_valid(command, True)
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueString(value="MY TEXT 1", valid=True),
                TaskElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        set_element_value_valid(command, False)
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueString(value="MY TEXT 1", valid=False),
                TaskElementValueString(value="MY TEXT 2", valid=False),
            ],
        )

    def test_set_element_value_valid_at(self):
        command = prepare_command_save_element_command_str()

        set_element_value_valid_at(command, False, 0)
        set_element_value_valid_at(command, True, 1)
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueString(value="MY TEXT 1", valid=False),
                TaskElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

    def test_get_element_value_as_str(self):
        command = prepare_command_save_element_command_str()

        value = get_element_value_as_str(command)
        self.assertEqual(value, "MY TEXT 1")

        command.element_values = []

        with self.assertRaises(ValueError) as context:
            get_element_value_as_str(command)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_str(self):
        command = prepare_command_save_element_command_str()

        value = find_element_value_as_str(command)
        self.assertEqual(value, "MY TEXT 1")

        command.element_values = []

        value = find_element_value_as_str(command)
        self.assertIsNone(value)

    def test_get_element_value_as_str_list(self):
        command = prepare_command_save_element_command_str()

        value = get_element_value_as_str_list(command)
        self.assertEqual(value, ["MY TEXT 1", "MY TEXT 2"])

        command.element_values = []

        value = get_element_value_as_str_list(command)
        self.assertEqual(value, [])

    def test_set_element_value_as_str(self):
        command = prepare_command_save_element_command_str()

        set_element_value(command, "MY TEXT NEW")
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueString(value="MY TEXT NEW", valid=True),
            ],
        )

        command.element_values = []

        set_element_value(command, None)
        self.assertIsNone(command.element_values)

    def test_set_element_value_as_str_list(self):
        command = prepare_command_save_element_command_str()

        set_element_value_list(command, ["MY TEXT NEW1", "MY TEXT NEW2"])
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueString(value="MY TEXT NEW1", valid=True),
                TaskElementValueString(value="MY TEXT NEW2", valid=True),
            ],
        )

        set_element_value_list(command, [])
        self.assertIsNone(command.element_values)

    def test_add_element_value_as_str(self):
        command = prepare_command_save_element_command_str()

        add_element_value(command, "MY TEXT NEW1")

        expected_element_values = [
            TaskElementValueString(value="MY TEXT 1", valid=True),
            TaskElementValueString(value="MY TEXT 2", valid=False),
            TaskElementValueString(value="MY TEXT NEW1", valid=True),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value(command, None)
        self.assertEqual(command.element_values, expected_element_values)

    def test_add_element_value_as_str_list(self):
        command = prepare_command_save_element_command_str()

        add_element_value_list(command, ["MY TEXT NEW1", "MY TEXT NEW2"])

        expected_element_values = [
            TaskElementValueString(value="MY TEXT 1", valid=True),
            TaskElementValueString(value="MY TEXT 2", valid=False),
            TaskElementValueString(value="MY TEXT NEW1", valid=True),
            TaskElementValueString(value="MY TEXT NEW2", valid=True),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, None)
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, [])
        self.assertEqual(command.element_values, expected_element_values)

    def test_get_element_value_as_float(self):
        command = prepare_command_save_element_command_float()

        value = get_element_value_as_float(command)
        self.assertEqual(value, 500)

        command.element_values = []

        with self.assertRaises(ValueError) as context:
            get_element_value_as_float(command)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_float(self):
        command = prepare_command_save_element_command_float()

        value = find_element_value_as_float(command)
        self.assertEqual(value, 500)

        command.element_values = []

        value = find_element_value_as_float(command)
        self.assertIsNone(value)

    def test_get_element_value_as_float_list(self):
        command = prepare_command_save_element_command_float()

        value = get_element_value_as_float_list(command)
        self.assertEqual(value, [500, 600])

        command.element_values = []

        value = get_element_value_as_float_list(command)
        self.assertEqual(value, [])

    def test_set_element_value_as_float(self):
        command = prepare_command_save_element_command_float()

        set_element_value(command, 700)
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueNumber(value=700, valid=True),
            ],
        )

        set_element_value(command, None)
        self.assertIsNone(command.element_values)

    def test_set_element_value_as_float_list(self):
        command = prepare_command_save_element_command_float()

        set_element_value_list(command, [700, 800])
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueNumber(value=700, valid=True),
                TaskElementValueNumber(value=800, valid=True),
            ],
        )

        set_element_value_list(command, [])
        self.assertIsNone(command.element_values)

    def test_add_element_value_as_float(self):
        command = prepare_command_save_element_command_float()

        add_element_value(command, 800)

        expected_element_values = [
            TaskElementValueNumber(value=500, valid=True),
            TaskElementValueNumber(value=600, valid=False),
            TaskElementValueNumber(value=800, valid=True),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value(command, None)
        self.assertEqual(command.element_values, expected_element_values)

    def test_add_element_value_as_float_list(self):
        command = prepare_command_save_element_command_float()

        add_element_value_list(command, [800, 900])

        expected_element_values = [
            TaskElementValueNumber(value=500, valid=True),
            TaskElementValueNumber(value=600, valid=False),
            TaskElementValueNumber(value=800, valid=True),
            TaskElementValueNumber(value=900, valid=True),
        ]
        self.assertEqual(
            command.element_values,
            expected_element_values,
        )

        add_element_value_list(command, None)
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, [])
        self.assertEqual(command.element_values, expected_element_values)

    def test_get_element_value_as_date(self):
        command = prepare_command_save_element_command_date()

        value = get_element_value_as_date(command)
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        command.element_values = []

        with self.assertRaises(ValueError) as context:
            get_element_value_as_date(command)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_date(self):
        command = prepare_command_save_element_command_date()

        value = find_element_value_as_date(command)
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        command.element_values = []

        value = find_element_value_as_date(command)
        self.assertIsNone(value)

    def test_get_element_value_as_date_list(self):
        command = prepare_command_save_element_command_date()

        value = get_element_value_as_date_list(command)
        self.assertEqual(value, [date.fromisoformat("2000-01-01"), date.fromisoformat("1980-01-01")])

        command.element_values = []

        value = get_element_value_as_date_list(command)
        self.assertEqual(value, [])

    def test_set_element_value_as_date(self):
        command = prepare_command_save_element_command_date()

        set_element_value(command, date.fromisoformat("2020-05-05"))
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueString(value="2020-05-05", valid=True),
            ],
        )

        set_element_value(command, None)
        self.assertIsNone(command.element_values)

    def test_set_element_value_as_date_list(self):
        command = prepare_command_save_element_command_date()

        set_element_value_list(command, [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")])
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueString(value="2020-05-05", valid=True),
                TaskElementValueString(value="2020-08-08", valid=True),
            ],
        )

        set_element_value_list(command, [])
        self.assertIsNone(command.element_values)

    def test_add_element_value_as_date(self):
        command = prepare_command_save_element_command_date()

        add_element_value(command, date.fromisoformat("2020-08-08"))
        expected_element_values = [
            TaskElementValueString(value="2000-01-01", valid=True),
            TaskElementValueString(value="1980-01-01", valid=False),
            TaskElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value(command, None)
        self.assertEqual(command.element_values, expected_element_values)

    def test_add_element_value_as_date_list(self):
        command = prepare_command_save_element_command_date()

        add_element_value_list(command, [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")])
        expected_element_values = [
            TaskElementValueString(value="2000-01-01", valid=True),
            TaskElementValueString(value="1980-01-01", valid=False),
            TaskElementValueString(value="2020-05-05", valid=True),
            TaskElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, None)
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, [])
        self.assertEqual(command.element_values, expected_element_values)

    def test_get_element_value_as_dict(self):
        command = prepare_command_save_element_command_dict()

        value = get_element_value_as_dict(command)
        self.assertEqual(value, {"key": "value 1"})

        command.element_values = []

        with self.assertRaises(ValueError) as context:
            get_element_value_as_dict(command)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_dict(self):
        command = prepare_command_save_element_command_dict()

        value = find_element_value_as_dict(command)
        self.assertEqual(value, {"key": "value 1"})

        command.element_values = []

        value = find_element_value_as_dict(command)
        self.assertIsNone(value)

    def test_get_element_value_as_dict_list(self):
        command = prepare_command_save_element_command_dict()

        value = get_element_value_as_dict_list(command)
        self.assertEqual(value, [{"key": "value 1"}, {"key": "value 2"}])

        command.element_values = []

        value = get_element_value_as_dict_list(command)
        self.assertEqual(value, [])

    def test_set_element_value_as_dict(self):
        command = prepare_command_save_element_command_dict()

        set_element_value(command, {"key": "value 3"})
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueObject(value={"key": "value 3"}, valid=True),
            ],
        )

        set_element_value(command, None)
        self.assertIsNone(command.element_values)

    def test_set_element_value_as_dict_list(self):
        command = prepare_command_save_element_command_dict()

        set_element_value_list(command, [{"key": "value 3"}, {"key": "value 4"}])
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueObject(value={"key": "value 3"}, valid=True),
                TaskElementValueObject(value={"key": "value 4"}, valid=True),
            ],
        )

        set_element_value_list(command, [])
        self.assertIsNone(command.element_values)

    def test_add_element_value_as_dict(self):
        command = prepare_command_save_element_command_dict()

        add_element_value(command, {"key": "value 3"})

        expected_element_values = [
            TaskElementValueObject(value={"key": "value 1"}, valid=True),
            TaskElementValueObject(value={"key": "value 2"}, valid=False),
            TaskElementValueObject(value={"key": "value 3"}, valid=True),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value(command, None)
        self.assertEqual(command.element_values, expected_element_values)

    def test_add_element_value_as_dict_list(self):
        command = prepare_command_save_element_command_dict()

        add_element_value_list(command, [{"key": "value 3"}, {"key": "value 4"}])

        expected_element_values = [
            TaskElementValueObject(value={"key": "value 1"}, valid=True),
            TaskElementValueObject(value={"key": "value 2"}, valid=False),
            TaskElementValueObject(value={"key": "value 3"}, valid=True),
            TaskElementValueObject(value={"key": "value 4"}, valid=True),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, None)
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, [])
        self.assertEqual(command.element_values, expected_element_values)

    def test_get_element_value_as_document(self):
        command = prepare_command_save_element_command_document()

        value = get_element_value_as_document(command)
        self.assertEqual(value, prepare_command_element_value_document_item("1"))

        command.element_values = []

        with self.assertRaises(ValueError) as context:
            get_element_value_as_document(command)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_document(self):
        command = prepare_command_save_element_command_document()

        value = find_element_value_as_document(command)
        self.assertEqual(value, prepare_command_element_value_document_item("1"))

        command.element_values = []

        value = find_element_value_as_document(command)
        self.assertIsNone(value)

    def test_get_element_value_as_document_list(self):
        command = prepare_command_save_element_command_document()

        value = get_element_value_as_document_list(command)
        self.assertEqual(
            value, [prepare_command_element_value_document_item("1"), prepare_command_element_value_document_item("2")]
        )

        command.element_values = []

        value = get_element_value_as_document_list(command)
        self.assertEqual(value, [])

    def test_set_element_value_as_document(self):
        command = prepare_command_save_element_command_document()

        set_element_value(command, prepare_command_element_value_document_item("3"))
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueDocument(value=prepare_command_element_value_document_item("3"), valid=True),
            ],
        )

        set_element_value(command, None)
        self.assertIsNone(command.element_values)

    def test_set_element_value_as_document_list(self):
        command = prepare_command_save_element_command_document()

        set_element_value_list(
            command,
            [prepare_command_element_value_document_item("3"), prepare_command_element_value_document_item("4")],
        )
        self.assertEqual(
            command.element_values,
            [
                TaskElementValueDocument(value=prepare_command_element_value_document_item("3"), valid=True),
                TaskElementValueDocument(value=prepare_command_element_value_document_item("4"), valid=True),
            ],
        )

        set_element_value_list(command, [])
        self.assertIsNone(command.element_values)

    def test_add_element_value_as_document(self):
        command = prepare_command_save_element_command_document()

        add_element_value(command, prepare_command_element_value_document_item("3"))

        expected_element_values = [
            TaskElementValueDocument(
                value=prepare_command_element_value_document_item("1"),
                valid=True,
            ),
            TaskElementValueDocument(
                value=prepare_command_element_value_document_item("2"),
                valid=False,
            ),
            TaskElementValueDocument(
                value=prepare_command_element_value_document_item("3"),
                valid=True,
            ),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value(command, None)
        self.assertEqual(command.element_values, expected_element_values)

    def test_add_element_value_as_document_list(self):
        command = prepare_command_save_element_command_document()

        add_element_value_list(
            command,
            [prepare_command_element_value_document_item("3"), prepare_command_element_value_document_item("4")],
        )

        expected_element_values = [
            TaskElementValueDocument(
                value=prepare_command_element_value_document_item("1"),
                valid=True,
            ),
            TaskElementValueDocument(
                value=prepare_command_element_value_document_item("2"),
                valid=False,
            ),
            TaskElementValueDocument(
                value=prepare_command_element_value_document_item("3"),
                valid=True,
            ),
            TaskElementValueDocument(
                value=prepare_command_element_value_document_item("4"),
                valid=True,
            ),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, None)
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, [])
        self.assertEqual(command.element_values, expected_element_values)

    def test_get_element_value_as_principal(self):
        command = prepare_command_save_element_command_principal()

        value = get_element_value_as_principal(command)
        self.assertEqual(value, prepare_command_element_value_principal_item("1"))

        command.element_values = []

        with self.assertRaises(ValueError) as context:
            get_element_value_as_principal(command)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_principal(self):
        command = prepare_command_save_element_command_principal()

        value = find_element_value_as_principal(command)
        self.assertEqual(value, prepare_command_element_value_principal_item("1"))

        command.element_values = []

        value = find_element_value_as_principal(command)
        self.assertIsNone(value)

    def test_get_element_value_as_principal_list(self):
        command = prepare_command_save_element_command_principal()

        value = get_element_value_as_principal_list(command)
        self.assertEqual(
            value,
            [prepare_command_element_value_principal_item("1"), prepare_command_element_value_principal_item("2")],
        )

        command.element_values = []

        value = get_element_value_as_principal_list(command)
        self.assertEqual(value, [])

    def test_set_element_value_as_principal(self):
        command = prepare_command_save_element_command_principal()

        set_element_value(command, prepare_command_element_value_principal_item("3"))
        self.assertEqual(
            command.element_values,
            [
                TaskElementValuePrincipal(value=prepare_command_element_value_principal_item("3"), valid=True),
            ],
        )

        set_element_value(command, None)
        self.assertIsNone(command.element_values)

    def test_set_element_value_as_principal_list(self):
        command = prepare_command_save_element_command_principal()

        set_element_value_list(
            command,
            [prepare_command_element_value_principal_item("3"), prepare_command_element_value_principal_item("4")],
        )
        self.assertEqual(
            command.element_values,
            [
                TaskElementValuePrincipal(value=prepare_command_element_value_principal_item("3"), valid=True),
                TaskElementValuePrincipal(value=prepare_command_element_value_principal_item("4"), valid=True),
            ],
        )

        set_element_value_list(command, [])
        self.assertIsNone(command.element_values)

    def test_add_element_value_as_principal(self):
        command = prepare_command_save_element_command_principal()

        add_element_value(command, prepare_command_element_value_principal_item("3"))

        expected_element_values = [
            TaskElementValuePrincipal(
                value=prepare_command_element_value_principal_item("1"),
                valid=True,
            ),
            TaskElementValuePrincipal(
                value=prepare_command_element_value_principal_item("2"),
                valid=False,
            ),
            TaskElementValuePrincipal(
                value=prepare_command_element_value_principal_item("3"),
                valid=True,
            ),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value(command, None)
        self.assertEqual(command.element_values, expected_element_values)

    def test_add_element_value_as_principal_list(self):
        command = prepare_command_save_element_command_principal()

        add_element_value_list(
            command,
            [prepare_command_element_value_principal_item("3"), prepare_command_element_value_principal_item("4")],
        )

        expected_element_values = [
            TaskElementValuePrincipal(
                value=prepare_command_element_value_principal_item("1"),
                valid=True,
            ),
            TaskElementValuePrincipal(
                value=prepare_command_element_value_principal_item("2"),
                valid=False,
            ),
            TaskElementValuePrincipal(
                value=prepare_command_element_value_principal_item("3"),
                valid=True,
            ),
            TaskElementValuePrincipal(
                value=prepare_command_element_value_principal_item("4"),
                valid=True,
            ),
        ]
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, None)
        self.assertEqual(command.element_values, expected_element_values)

        add_element_value_list(command, [])
        self.assertEqual(command.element_values, expected_element_values)


def prepare_command_save_element_command_str() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValueString(value="MY TEXT 1", valid=True),
            TaskElementValueString(value="MY TEXT 2", valid=False),
        ],
    )


def prepare_command_save_element_command_float() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValueNumber(value=500, valid=True),
            TaskElementValueNumber(value=600, valid=False),
        ],
    )


def prepare_command_save_element_command_date() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValueString(value="2000-01-01", valid=True),
            TaskElementValueString(value="1980-01-01", valid=False),
        ],
    )


def prepare_command_save_element_command_dict() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValueObject(value={"key": "value 1"}, valid=True),
            TaskElementValueObject(value={"key": "value 2"}, valid=False),
        ],
    )


def prepare_command_save_element_command_document() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValueDocument(value=prepare_command_element_value_document_item("1"), valid=True),
            TaskElementValueDocument(value=prepare_command_element_value_document_item("2"), valid=False),
        ],
    )


def prepare_command_save_element_command_principal() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValuePrincipal(value=prepare_command_element_value_principal_item("1"), valid=True),
            TaskElementValuePrincipal(value=prepare_command_element_value_principal_item("2"), valid=False),
        ],
    )


def prepare_command_element_value_document_item(suffix: str) -> TaskElementValueDocumentItem:
    return TaskElementValueDocumentItem(
        id=f"id_{suffix}",
        uri=f"uri_{suffix}",
        name=f"name_{suffix}",
        contentPath=f"contentPath_{suffix}",
        contentType=f"contentType_{suffix}",
        contentLength=600,
    )


def prepare_command_element_value_principal_item(suffix: str) -> TaskElementValuePrincipalItem:
    return TaskElementValuePrincipalItem(
        id=f"id_{suffix}",
        type="USER",
        name=f"name_{suffix}",
    )


if __name__ == "__main__":
    unittest.main()
