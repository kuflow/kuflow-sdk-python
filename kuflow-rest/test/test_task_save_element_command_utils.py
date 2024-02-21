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
    TaskElementValueDocument,
    TaskElementValueDocumentItem,
    TaskElementValueNumber,
    TaskElementValueObject,
    TaskElementValuePrincipal,
    TaskElementValuePrincipalItem,
    TaskElementValueString,
    TaskSaveElementCommand,
)
from kuflow_rest.utils import TaskSaveElementCommandUtils


class SaveTaskElementUtilsTest(unittest.TestCase):
    def test_get_element_value_valid(self):
        request = prepare_task_save_element_command_str()

        value = TaskSaveElementCommandUtils.get_element_value_valid(request)
        self.assertFalse(value)

    def test_get_element_value_valid_at(self):
        request = prepare_task_save_element_command_str()

        value = TaskSaveElementCommandUtils.get_element_value_valid_at(request, 0)
        self.assertTrue(value)

        value = TaskSaveElementCommandUtils.get_element_value_valid_at(request, 1)
        self.assertFalse(value)

    def test_set_element_value_valid(self):
        request = prepare_task_save_element_command_str()

        TaskSaveElementCommandUtils.set_element_value_valid(request, True)
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueString(value="MY TEXT 1", valid=True),
                TaskElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value_valid(request, False)
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueString(value="MY TEXT 1", valid=False),
                TaskElementValueString(value="MY TEXT 2", valid=False),
            ],
        )

    def test_set_element_value_valid_at(self):
        request = prepare_task_save_element_command_str()

        TaskSaveElementCommandUtils.set_element_value_valid_at(request, False, 0)
        TaskSaveElementCommandUtils.set_element_value_valid_at(request, True, 1)
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueString(value="MY TEXT 1", valid=False),
                TaskElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

    def test_get_element_value_as_str(self):
        request = prepare_task_save_element_command_str()

        value = TaskSaveElementCommandUtils.get_element_value_as_str(request)
        self.assertEqual(value, "MY TEXT 1")

        request.element_values = []

        with self.assertRaises(ValueError) as context:
            TaskSaveElementCommandUtils.get_element_value_as_str(request)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_str(self):
        request = prepare_task_save_element_command_str()

        value = TaskSaveElementCommandUtils.find_element_value_as_str(request)
        self.assertEqual(value, "MY TEXT 1")

        request.element_values = []

        value = TaskSaveElementCommandUtils.find_element_value_as_str(request)
        self.assertIsNone(value)

    def test_get_element_value_as_str_list(self):
        request = prepare_task_save_element_command_str()

        value = TaskSaveElementCommandUtils.get_element_value_as_str_list(request)
        self.assertEqual(value, ["MY TEXT 1", "MY TEXT 2"])

        request.element_values = []

        value = TaskSaveElementCommandUtils.get_element_value_as_str_list(request)
        self.assertEqual(value, [])

    def test_set_element_value_as_str(self):
        request = prepare_task_save_element_command_str()

        TaskSaveElementCommandUtils.set_element_value(request, "MY TEXT NEW")
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueString(value="MY TEXT NEW", valid=True),
            ],
        )

        request.element_values = []

        TaskSaveElementCommandUtils.set_element_value(request, None)
        self.assertIsNone(request.element_values)

    def test_set_element_value_as_str_list(self):
        request = prepare_task_save_element_command_str()

        TaskSaveElementCommandUtils.set_element_value_list(request, ["MY TEXT NEW1", "MY TEXT NEW2"])
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueString(value="MY TEXT NEW1", valid=True),
                TaskElementValueString(value="MY TEXT NEW2", valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value_list(request, [])
        self.assertIsNone(request.element_values)

    def test_add_element_value_as_str(self):
        request = prepare_task_save_element_command_str()

        TaskSaveElementCommandUtils.add_element_value(request, "MY TEXT NEW1")

        expected_element_values = [
            TaskElementValueString(value="MY TEXT 1", valid=True),
            TaskElementValueString(value="MY TEXT 2", valid=False),
            TaskElementValueString(value="MY TEXT NEW1", valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value(request, None)
        self.assertEqual(request.element_values, expected_element_values)

    def test_add_element_value_as_str_list(self):
        request = prepare_task_save_element_command_str()

        TaskSaveElementCommandUtils.add_element_value_list(request, ["MY TEXT NEW1", "MY TEXT NEW2"])

        expected_element_values = [
            TaskElementValueString(value="MY TEXT 1", valid=True),
            TaskElementValueString(value="MY TEXT 2", valid=False),
            TaskElementValueString(value="MY TEXT NEW1", valid=True),
            TaskElementValueString(value="MY TEXT NEW2", valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, None)
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, [])
        self.assertEqual(request.element_values, expected_element_values)

    def test_get_element_value_as_float(self):
        request = prepare_task_save_element_command_float()

        value = TaskSaveElementCommandUtils.get_element_value_as_float(request)
        self.assertEqual(value, 500)

        request.element_values = []

        with self.assertRaises(ValueError) as context:
            TaskSaveElementCommandUtils.get_element_value_as_float(request)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_float(self):
        request = prepare_task_save_element_command_float()

        value = TaskSaveElementCommandUtils.find_element_value_as_float(request)
        self.assertEqual(value, 500)

        request.element_values = []

        value = TaskSaveElementCommandUtils.find_element_value_as_float(request)
        self.assertIsNone(value)

    def test_get_element_value_as_float_list(self):
        request = prepare_task_save_element_command_float()

        value = TaskSaveElementCommandUtils.get_element_value_as_float_list(request)
        self.assertEqual(value, [500, 600])

        request.element_values = []

        value = TaskSaveElementCommandUtils.get_element_value_as_float_list(request)
        self.assertEqual(value, [])

    def test_set_element_value_as_float(self):
        request = prepare_task_save_element_command_float()

        TaskSaveElementCommandUtils.set_element_value(request, 700)
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueNumber(value=700, valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value(request, None)
        self.assertIsNone(request.element_values)

    def test_set_element_value_as_float_list(self):
        request = prepare_task_save_element_command_float()

        TaskSaveElementCommandUtils.set_element_value_list(request, [700, 800])
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueNumber(value=700, valid=True),
                TaskElementValueNumber(value=800, valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value_list(request, [])
        self.assertIsNone(request.element_values)

    def test_add_element_value_as_float(self):
        request = prepare_task_save_element_command_float()

        TaskSaveElementCommandUtils.add_element_value(request, 800)

        expected_element_values = [
            TaskElementValueNumber(value=500, valid=True),
            TaskElementValueNumber(value=600, valid=False),
            TaskElementValueNumber(value=800, valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value(request, None)
        self.assertEqual(request.element_values, expected_element_values)

    def test_add_element_value_as_float_list(self):
        request = prepare_task_save_element_command_float()

        TaskSaveElementCommandUtils.add_element_value_list(request, [800, 900])

        expected_element_values = [
            TaskElementValueNumber(value=500, valid=True),
            TaskElementValueNumber(value=600, valid=False),
            TaskElementValueNumber(value=800, valid=True),
            TaskElementValueNumber(value=900, valid=True),
        ]
        self.assertEqual(
            request.element_values,
            expected_element_values,
        )

        TaskSaveElementCommandUtils.add_element_value_list(request, None)
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, [])
        self.assertEqual(request.element_values, expected_element_values)

    def test_get_element_value_as_date(self):
        request = prepare_task_save_element_command_date()

        value = TaskSaveElementCommandUtils.get_element_value_as_date(request)
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        request.element_values = []

        with self.assertRaises(ValueError) as context:
            TaskSaveElementCommandUtils.get_element_value_as_date(request)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_date(self):
        request = prepare_task_save_element_command_date()

        value = TaskSaveElementCommandUtils.find_element_value_as_date(request)
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        request.element_values = []

        value = TaskSaveElementCommandUtils.find_element_value_as_date(request)
        self.assertIsNone(value)

    def test_get_element_value_as_date_list(self):
        request = prepare_task_save_element_command_date()

        value = TaskSaveElementCommandUtils.get_element_value_as_date_list(request)
        self.assertEqual(value, [date.fromisoformat("2000-01-01"), date.fromisoformat("1980-01-01")])

        request.element_values = []

        value = TaskSaveElementCommandUtils.get_element_value_as_date_list(request)
        self.assertEqual(value, [])

    def test_set_element_value_as_date(self):
        request = prepare_task_save_element_command_date()

        TaskSaveElementCommandUtils.set_element_value(request, date.fromisoformat("2020-05-05"))
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueString(value="2020-05-05", valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value(request, None)
        self.assertIsNone(request.element_values)

    def test_set_element_value_as_date_list(self):
        request = prepare_task_save_element_command_date()

        TaskSaveElementCommandUtils.set_element_value_list(
            request,
            [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")],
        )
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueString(value="2020-05-05", valid=True),
                TaskElementValueString(value="2020-08-08", valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value_list(request, [])
        self.assertIsNone(request.element_values)

    def test_add_element_value_as_date(self):
        request = prepare_task_save_element_command_date()

        TaskSaveElementCommandUtils.add_element_value(request, date.fromisoformat("2020-08-08"))
        expected_element_values = [
            TaskElementValueString(value="2000-01-01", valid=True),
            TaskElementValueString(value="1980-01-01", valid=False),
            TaskElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value(request, None)
        self.assertEqual(request.element_values, expected_element_values)

    def test_add_element_value_as_date_list(self):
        request = prepare_task_save_element_command_date()

        TaskSaveElementCommandUtils.add_element_value_list(
            request,
            [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")],
        )
        expected_element_values = [
            TaskElementValueString(value="2000-01-01", valid=True),
            TaskElementValueString(value="1980-01-01", valid=False),
            TaskElementValueString(value="2020-05-05", valid=True),
            TaskElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, None)
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, [])
        self.assertEqual(request.element_values, expected_element_values)

    def test_get_element_value_as_dict(self):
        request = prepare_task_save_element_command_dict()

        value = TaskSaveElementCommandUtils.get_element_value_as_dict(request)
        self.assertEqual(value, {"key": "value 1"})

        request.element_values = []

        with self.assertRaises(ValueError) as context:
            TaskSaveElementCommandUtils.get_element_value_as_dict(request)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_dict(self):
        request = prepare_task_save_element_command_dict()

        value = TaskSaveElementCommandUtils.find_element_value_as_dict(request)
        self.assertEqual(value, {"key": "value 1"})

        request.element_values = []

        value = TaskSaveElementCommandUtils.find_element_value_as_dict(request)
        self.assertIsNone(value)

    def test_get_element_value_as_dict_list(self):
        request = prepare_task_save_element_command_dict()

        value = TaskSaveElementCommandUtils.get_element_value_as_dict_list(request)
        self.assertEqual(value, [{"key": "value 1"}, {"key": "value 2"}])

        request.element_values = []

        value = TaskSaveElementCommandUtils.get_element_value_as_dict_list(request)
        self.assertEqual(value, [])

    def test_set_element_value_as_dict(self):
        request = prepare_task_save_element_command_dict()

        TaskSaveElementCommandUtils.set_element_value(request, {"key": "value 3"})
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueObject(value={"key": "value 3"}, valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value(request, None)
        self.assertIsNone(request.element_values)

    def test_set_element_value_as_dict_list(self):
        request = prepare_task_save_element_command_dict()

        TaskSaveElementCommandUtils.set_element_value_list(request, [{"key": "value 3"}, {"key": "value 4"}])
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueObject(value={"key": "value 3"}, valid=True),
                TaskElementValueObject(value={"key": "value 4"}, valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value_list(request, [])
        self.assertIsNone(request.element_values)

    def test_add_element_value_as_dict(self):
        request = prepare_task_save_element_command_dict()

        TaskSaveElementCommandUtils.add_element_value(request, {"key": "value 3"})

        expected_element_values = [
            TaskElementValueObject(value={"key": "value 1"}, valid=True),
            TaskElementValueObject(value={"key": "value 2"}, valid=False),
            TaskElementValueObject(value={"key": "value 3"}, valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value(request, None)
        self.assertEqual(request.element_values, expected_element_values)

    def test_add_element_value_as_dict_list(self):
        request = prepare_task_save_element_command_dict()

        TaskSaveElementCommandUtils.add_element_value_list(request, [{"key": "value 3"}, {"key": "value 4"}])

        expected_element_values = [
            TaskElementValueObject(value={"key": "value 1"}, valid=True),
            TaskElementValueObject(value={"key": "value 2"}, valid=False),
            TaskElementValueObject(value={"key": "value 3"}, valid=True),
            TaskElementValueObject(value={"key": "value 4"}, valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, None)
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, [])
        self.assertEqual(request.element_values, expected_element_values)

    def test_get_element_value_as_document(self):
        request = prepare_task_save_element_command_document()

        value = TaskSaveElementCommandUtils.get_element_value_as_document(request)
        self.assertEqual(value, prepare_task_element_value_document_item("1"))

        request.element_values = []

        with self.assertRaises(ValueError) as context:
            TaskSaveElementCommandUtils.get_element_value_as_document(request)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_document(self):
        request = prepare_task_save_element_command_document()

        value = TaskSaveElementCommandUtils.find_element_value_as_document(request)
        self.assertEqual(value, prepare_task_element_value_document_item("1"))

        request.element_values = []

        value = TaskSaveElementCommandUtils.find_element_value_as_document(request)
        self.assertIsNone(value)

    def test_get_element_value_as_document_list(self):
        request = prepare_task_save_element_command_document()

        value = TaskSaveElementCommandUtils.get_element_value_as_document_list(request)
        self.assertEqual(
            value,
            [
                prepare_task_element_value_document_item("1"),
                prepare_task_element_value_document_item("2"),
            ],
        )

        request.element_values = []

        value = TaskSaveElementCommandUtils.get_element_value_as_document_list(request)
        self.assertEqual(value, [])

    def test_set_element_value_as_document(self):
        request = prepare_task_save_element_command_document()

        TaskSaveElementCommandUtils.set_element_value(request, prepare_task_element_value_document_item("3"))
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueDocument(value=prepare_task_element_value_document_item("3"), valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value(request, None)
        self.assertIsNone(request.element_values)

    def test_set_element_value_as_document_list(self):
        request = prepare_task_save_element_command_document()

        TaskSaveElementCommandUtils.set_element_value_list(
            request,
            [
                prepare_task_element_value_document_item("3"),
                prepare_task_element_value_document_item("4"),
            ],
        )
        self.assertEqual(
            request.element_values,
            [
                TaskElementValueDocument(value=prepare_task_element_value_document_item("3"), valid=True),
                TaskElementValueDocument(value=prepare_task_element_value_document_item("4"), valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value_list(request, [])
        self.assertIsNone(request.element_values)

    def test_add_element_value_as_document(self):
        request = prepare_task_save_element_command_document()

        TaskSaveElementCommandUtils.add_element_value(request, prepare_task_element_value_document_item("3"))

        expected_element_values = [
            TaskElementValueDocument(
                value=prepare_task_element_value_document_item("1"),
                valid=True,
            ),
            TaskElementValueDocument(
                value=prepare_task_element_value_document_item("2"),
                valid=False,
            ),
            TaskElementValueDocument(
                value=prepare_task_element_value_document_item("3"),
                valid=True,
            ),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value(request, None)
        self.assertEqual(request.element_values, expected_element_values)

    def test_add_element_value_as_document_list(self):
        request = prepare_task_save_element_command_document()

        TaskSaveElementCommandUtils.add_element_value_list(
            request,
            [
                prepare_task_element_value_document_item("3"),
                prepare_task_element_value_document_item("4"),
            ],
        )

        expected_element_values = [
            TaskElementValueDocument(
                value=prepare_task_element_value_document_item("1"),
                valid=True,
            ),
            TaskElementValueDocument(
                value=prepare_task_element_value_document_item("2"),
                valid=False,
            ),
            TaskElementValueDocument(
                value=prepare_task_element_value_document_item("3"),
                valid=True,
            ),
            TaskElementValueDocument(
                value=prepare_task_element_value_document_item("4"),
                valid=True,
            ),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, None)
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, [])
        self.assertEqual(request.element_values, expected_element_values)

    def test_get_element_value_as_principal(self):
        request = prepare_task_save_element_command_principal()

        value = TaskSaveElementCommandUtils.get_element_value_as_principal(request)
        self.assertEqual(value, prepare_task_element_value_principal_item("1"))

        request.element_values = []

        with self.assertRaises(ValueError) as context:
            TaskSaveElementCommandUtils.get_element_value_as_principal(request)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_principal(self):
        request = prepare_task_save_element_command_principal()

        value = TaskSaveElementCommandUtils.find_element_value_as_principal(request)
        self.assertEqual(value, prepare_task_element_value_principal_item("1"))

        request.element_values = []

        value = TaskSaveElementCommandUtils.find_element_value_as_principal(request)
        self.assertIsNone(value)

    def test_get_element_value_as_principal_list(self):
        request = prepare_task_save_element_command_principal()

        value = TaskSaveElementCommandUtils.get_element_value_as_principal_list(request)
        self.assertEqual(
            value,
            [
                prepare_task_element_value_principal_item("1"),
                prepare_task_element_value_principal_item("2"),
            ],
        )

        request.element_values = []

        value = TaskSaveElementCommandUtils.get_element_value_as_principal_list(request)
        self.assertEqual(value, [])

    def test_set_element_value_as_principal(self):
        request = prepare_task_save_element_command_principal()

        TaskSaveElementCommandUtils.set_element_value(request, prepare_task_element_value_principal_item("3"))
        self.assertEqual(
            request.element_values,
            [
                TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("3"), valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value(request, None)
        self.assertIsNone(request.element_values)

    def test_set_element_value_as_principal_list(self):
        request = prepare_task_save_element_command_principal()

        TaskSaveElementCommandUtils.set_element_value_list(
            request,
            [
                prepare_task_element_value_principal_item("3"),
                prepare_task_element_value_principal_item("4"),
            ],
        )
        self.assertEqual(
            request.element_values,
            [
                TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("3"), valid=True),
                TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("4"), valid=True),
            ],
        )

        TaskSaveElementCommandUtils.set_element_value_list(request, [])
        self.assertIsNone(request.element_values)

    def test_add_element_value_as_principal(self):
        request = prepare_task_save_element_command_principal()

        TaskSaveElementCommandUtils.add_element_value(request, prepare_task_element_value_principal_item("3"))

        expected_element_values = [
            TaskElementValuePrincipal(
                value=prepare_task_element_value_principal_item("1"),
                valid=True,
            ),
            TaskElementValuePrincipal(
                value=prepare_task_element_value_principal_item("2"),
                valid=False,
            ),
            TaskElementValuePrincipal(
                value=prepare_task_element_value_principal_item("3"),
                valid=True,
            ),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value(request, None)
        self.assertEqual(request.element_values, expected_element_values)

    def test_add_element_value_as_principal_list(self):
        request = prepare_task_save_element_command_principal()

        TaskSaveElementCommandUtils.add_element_value_list(
            request,
            [
                prepare_task_element_value_principal_item("3"),
                prepare_task_element_value_principal_item("4"),
            ],
        )

        expected_element_values = [
            TaskElementValuePrincipal(
                value=prepare_task_element_value_principal_item("1"),
                valid=True,
            ),
            TaskElementValuePrincipal(
                value=prepare_task_element_value_principal_item("2"),
                valid=False,
            ),
            TaskElementValuePrincipal(
                value=prepare_task_element_value_principal_item("3"),
                valid=True,
            ),
            TaskElementValuePrincipal(
                value=prepare_task_element_value_principal_item("4"),
                valid=True,
            ),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, None)
        self.assertEqual(request.element_values, expected_element_values)

        TaskSaveElementCommandUtils.add_element_value_list(request, [])
        self.assertEqual(request.element_values, expected_element_values)


def prepare_task_save_element_command_str() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValueString(value="MY TEXT 1", valid=True),
            TaskElementValueString(value="MY TEXT 2", valid=False),
        ],
    )


def prepare_task_save_element_command_float() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValueNumber(value=500, valid=True),
            TaskElementValueNumber(value=600, valid=False),
        ],
    )


def prepare_task_save_element_command_date() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValueString(value="2000-01-01", valid=True),
            TaskElementValueString(value="1980-01-01", valid=False),
        ],
    )


def prepare_task_save_element_command_dict() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValueObject(value={"key": "value 1"}, valid=True),
            TaskElementValueObject(value={"key": "value 2"}, valid=False),
        ],
    )


def prepare_task_save_element_command_document() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValueDocument(value=prepare_task_element_value_document_item("1"), valid=True),
            TaskElementValueDocument(value=prepare_task_element_value_document_item("2"), valid=False),
        ],
    )


def prepare_task_save_element_command_principal() -> TaskSaveElementCommand:
    return TaskSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("1"), valid=True),
            TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("2"), valid=False),
        ],
    )


def prepare_task_element_value_document_item(
    suffix: str,
) -> TaskElementValueDocumentItem:
    return TaskElementValueDocumentItem(
        id=f"id_{suffix}",
        uri=f"uri_{suffix}",
        name=f"name_{suffix}",
        content_path=f"contentPath_{suffix}",
        content_type=f"contentType_{suffix}",
        content_length=600,
    )


def prepare_task_element_value_principal_item(
    suffix: str,
) -> TaskElementValuePrincipalItem:
    return TaskElementValuePrincipalItem(
        id=f"id_{suffix}",
        type="USER",
        name=f"name_{suffix}",
    )


if __name__ == "__main__":
    unittest.main()
