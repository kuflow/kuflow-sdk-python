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
from datetime import date, datetime

from kuflow_rest.models import (
    JsonFormsFile,
    JsonFormsPrincipal,
    JsonFormsValue,
    PrincipalType,
    Task,
    TaskDefinitionSummary,
    TaskElementValueDocument,
    TaskElementValueDocumentItem,
    TaskElementValueNumber,
    TaskElementValueObject,
    TaskElementValuePrincipal,
    TaskElementValuePrincipalItem,
    TaskElementValueString,
)
from kuflow_rest.utils import TaskUtils


class TaskUtilsTest(unittest.TestCase):
    def test_get_element_value_valid(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_valid(task, "EV_STRING")
        self.assertFalse(value)

        value = TaskUtils.get_element_value_valid(task, "EV_NUMBER")
        self.assertTrue(value)

        value = TaskUtils.get_element_value_valid(task, "EV_DATE")
        self.assertFalse(value)

    def test_get_element_value_valid_at(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_valid_at(task, "EV_STRING", 0)
        self.assertTrue(value)

        value = TaskUtils.get_element_value_valid_at(task, "EV_STRING", 1)
        self.assertFalse(value)

        with self.assertRaises(IndexError) as context:
            TaskUtils.get_element_value_valid_at(task, "EV_STRING", 10)
        self.assertEqual(str(context.exception), "Array index out of bound: 10")

    def test_set_element_value_valid(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value_valid(task, "EV_STRING", True)
        self.assertEqual(
            task.element_values.get("EV_STRING"),
            [
                TaskElementValueString(value="MY TEXT 1", valid=True),
                TaskElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        TaskUtils.set_element_value_valid(task, "EV_STRING", False)
        self.assertEqual(
            task.element_values.get("EV_STRING"),
            [
                TaskElementValueString(value="MY TEXT 1", valid=False),
                TaskElementValueString(value="MY TEXT 2", valid=False),
            ],
        )

    def test_set_element_value_valid_at(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value_valid_at(task, "EV_STRING", False, 0)
        TaskUtils.set_element_value_valid_at(task, "EV_STRING", True, 1)
        self.assertEqual(
            task.element_values.get("EV_STRING"),
            [
                TaskElementValueString(value="MY TEXT 1", valid=False),
                TaskElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        with self.assertRaises(IndexError) as context:
            TaskUtils.set_element_value_valid_at(task, "EV_STRING", False, 10)
        self.assertEqual(str(context.exception), "Array index out of bound: 10")

    def test_get_element_value_as_str(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_str(task, "EV_STRING")
        self.assertEqual(value, "MY TEXT 1")

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_element_value_as_str(task, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_str(self):
        task = prepare_task_element_values()

        value = TaskUtils.find_element_value_as_str(task, "EV_STRING")
        self.assertEqual(value, "MY TEXT 1")

        value = TaskUtils.find_element_value_as_str(task, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_str_list(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_str_list(task, "EV_STRING")
        self.assertEqual(value, ["MY TEXT 1", "MY TEXT 2"])

        value = TaskUtils.get_element_value_as_str_list(task, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_str(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value(task, "EV_STRING", "MY TEXT NEW")
        self.assertEqual(
            task.element_values.get("EV_STRING"),
            [
                TaskElementValueString(value="MY TEXT NEW", valid=True),
            ],
        )

        TaskUtils.set_element_value(task, "EV_STRING", None)
        self.assertIsNone(task.element_values.get("EV_STRING"))

    def test_set_element_value_as_str_list(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value_list(task, "EV_STRING", ["MY TEXT NEW1", "MY TEXT NEW2"])
        self.assertEqual(
            task.element_values.get("EV_STRING"),
            [
                TaskElementValueString(value="MY TEXT NEW1", valid=True),
                TaskElementValueString(value="MY TEXT NEW2", valid=True),
            ],
        )

        TaskUtils.set_element_value_list(task, "EV_STRING", [])
        self.assertIsNone(task.element_values.get("EV_STRING"))

    def test_add_element_value_as_str(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value(task, "EV_STRING", "MY TEXT NEW1")

        expected_element_values = [
            TaskElementValueString(value="MY TEXT 1", valid=True),
            TaskElementValueString(value="MY TEXT 2", valid=False),
            TaskElementValueString(value="MY TEXT NEW1", valid=True),
        ]
        self.assertEqual(task.element_values.get("EV_STRING"), expected_element_values)

        TaskUtils.add_element_value(task, "EV_STRING", None)
        self.assertEqual(task.element_values.get("EV_STRING"), expected_element_values)

    def test_add_element_value_as_str_list(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value_list(task, "EV_STRING", ["MY TEXT NEW1", "MY TEXT NEW2"])

        expected_element_values = [
            TaskElementValueString(value="MY TEXT 1", valid=True),
            TaskElementValueString(value="MY TEXT 2", valid=False),
            TaskElementValueString(value="MY TEXT NEW1", valid=True),
            TaskElementValueString(value="MY TEXT NEW2", valid=True),
        ]
        self.assertEqual(task.element_values.get("EV_STRING"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_STRING", None)
        self.assertEqual(task.element_values.get("EV_STRING"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_STRING", [])
        self.assertEqual(task.element_values.get("EV_STRING"), expected_element_values)

    def test_get_element_value_as_float(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_float(task, "EV_NUMBER")
        self.assertEqual(value, 500)

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_element_value_as_float(task, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_float(self):
        task = prepare_task_element_values()

        value = TaskUtils.find_element_value_as_float(task, "EV_NUMBER")
        self.assertEqual(value, 500)

        value = TaskUtils.find_element_value_as_float(task, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_float_list(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_float_list(task, "EV_NUMBER")
        self.assertEqual(value, [500, 600])

        value = TaskUtils.get_element_value_as_float_list(task, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_float(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value(task, "EV_NUMBER", 700)
        self.assertEqual(
            task.element_values.get("EV_NUMBER"),
            [
                TaskElementValueNumber(value=700, valid=True),
            ],
        )

        TaskUtils.set_element_value(task, "EV_NUMBER", None)
        self.assertIsNone(task.element_values.get("EV_NUMBER"))

    def test_set_element_value_as_float_list(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value_list(task, "EV_NUMBER", [700, 800])
        self.assertEqual(
            task.element_values.get("EV_NUMBER"),
            [
                TaskElementValueNumber(value=700, valid=True),
                TaskElementValueNumber(value=800, valid=True),
            ],
        )

        TaskUtils.set_element_value_list(task, "EV_NUMBER", [])
        self.assertIsNone(task.element_values.get("EV_NUMBER"))

    def test_add_element_value_as_float(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value(task, "EV_NUMBER", 800)

        expected_element_values = [
            TaskElementValueNumber(value=500, valid=True),
            TaskElementValueNumber(value=600, valid=True),
            TaskElementValueNumber(value=800, valid=True),
        ]
        self.assertEqual(task.element_values.get("EV_NUMBER"), expected_element_values)

        TaskUtils.add_element_value(task, "EV_NUMBER", None)
        self.assertEqual(task.element_values.get("EV_NUMBER"), expected_element_values)

    def test_add_element_value_as_float_list(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value_list(task, "EV_NUMBER", [800, 900])

        expected_element_values = [
            TaskElementValueNumber(value=500, valid=True),
            TaskElementValueNumber(value=600, valid=True),
            TaskElementValueNumber(value=800, valid=True),
            TaskElementValueNumber(value=900, valid=True),
        ]
        self.assertEqual(
            task.element_values.get("EV_NUMBER"),
            expected_element_values,
        )

        TaskUtils.add_element_value_list(task, "EV_NUMBER", None)
        self.assertEqual(task.element_values.get("EV_NUMBER"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_NUMBER", [])
        self.assertEqual(task.element_values.get("EV_NUMBER"), expected_element_values)

    def test_get_element_value_as_date(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_date(task, "EV_DATE")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_element_value_as_date(task, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_date(self):
        task = prepare_task_element_values()

        value = TaskUtils.find_element_value_as_date(task, "EV_DATE")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        value = TaskUtils.find_element_value_as_date(task, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_date_list(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_date_list(task, "EV_DATE")
        self.assertEqual(value, [date.fromisoformat("2000-01-01"), date.fromisoformat("1980-01-01")])

        value = TaskUtils.get_element_value_as_date_list(task, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_date(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value(task, "EV_DATE", date.fromisoformat("2020-05-05"))
        self.assertEqual(
            task.element_values.get("EV_DATE"),
            [
                TaskElementValueString(value="2020-05-05", valid=True),
            ],
        )

        TaskUtils.set_element_value(task, "EV_DATE", None)
        self.assertIsNone(task.element_values.get("EV_DATE"))

    def test_set_element_value_as_date_list(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value_list(
            task, "EV_DATE", [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")]
        )
        self.assertEqual(
            task.element_values.get("EV_DATE"),
            [
                TaskElementValueString(value="2020-05-05", valid=True),
                TaskElementValueString(value="2020-08-08", valid=True),
            ],
        )

        TaskUtils.set_element_value_list(task, "EV_DATE", [])
        self.assertIsNone(task.element_values.get("EV_DATE"))

    def test_add_element_value_as_date(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value(task, "EV_DATE", date.fromisoformat("2020-08-08"))
        expected_element_values = [
            TaskElementValueString(value="2000-01-01", valid=False),
            TaskElementValueString(value="1980-01-01", valid=False),
            TaskElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(task.element_values.get("EV_DATE"), expected_element_values)

        TaskUtils.add_element_value(task, "EV_DATE", None)
        self.assertEqual(task.element_values.get("EV_DATE"), expected_element_values)

    def test_add_element_value_as_date_list(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value_list(
            task, "EV_DATE", [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")]
        )
        expected_element_values = [
            TaskElementValueString(value="2000-01-01", valid=False),
            TaskElementValueString(value="1980-01-01", valid=False),
            TaskElementValueString(value="2020-05-05", valid=True),
            TaskElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(task.element_values.get("EV_DATE"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_DATE", None)
        self.assertEqual(task.element_values.get("EV_DATE"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_DATE", [])
        self.assertEqual(task.element_values.get("EV_DATE"), expected_element_values)

    def test_get_element_value_as_dict(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_dict(task, "EV_OBJECT")
        self.assertEqual(value, {"key": "value 1"})

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_element_value_as_dict(task, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_dict(self):
        task = prepare_task_element_values()

        value = TaskUtils.find_element_value_as_dict(task, "EV_OBJECT")
        self.assertEqual(value, {"key": "value 1"})

        value = TaskUtils.find_element_value_as_dict(task, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_dict_list(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_dict_list(task, "EV_OBJECT")
        self.assertEqual(value, [{"key": "value 1"}, {"key": "value 2"}])

        value = TaskUtils.get_element_value_as_dict_list(task, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_dict(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value(task, "EV_OBJECT", {"key": "value 3"})
        self.assertEqual(
            task.element_values.get("EV_OBJECT"),
            [
                TaskElementValueObject(value={"key": "value 3"}, valid=True),
            ],
        )

        TaskUtils.set_element_value(task, "EV_OBJECT", None)
        self.assertIsNone(task.element_values.get("EV_OBJECT"))

    def test_set_element_value_as_dict_list(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value_list(task, "EV_OBJECT", [{"key": "value 3"}, {"key": "value 4"}])
        self.assertEqual(
            task.element_values.get("EV_OBJECT"),
            [
                TaskElementValueObject(value={"key": "value 3"}, valid=True),
                TaskElementValueObject(value={"key": "value 4"}, valid=True),
            ],
        )

        TaskUtils.set_element_value_list(task, "EV_OBJECT", [])
        self.assertIsNone(task.element_values.get("EV_OBJECT"))

    def test_add_element_value_as_dict(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value(task, "EV_OBJECT", {"key": "value 3"})

        expected_element_values = [
            TaskElementValueObject(value={"key": "value 1"}, valid=True),
            TaskElementValueObject(value={"key": "value 2"}, valid=False),
            TaskElementValueObject(value={"key": "value 3"}, valid=True),
        ]
        self.assertEqual(task.element_values.get("EV_OBJECT"), expected_element_values)

        TaskUtils.add_element_value(task, "EV_OBJECT", None)
        self.assertEqual(task.element_values.get("EV_OBJECT"), expected_element_values)

    def test_add_element_value_as_dict_list(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value_list(task, "EV_OBJECT", [{"key": "value 3"}, {"key": "value 4"}])

        expected_element_values = [
            TaskElementValueObject(value={"key": "value 1"}, valid=True),
            TaskElementValueObject(value={"key": "value 2"}, valid=False),
            TaskElementValueObject(value={"key": "value 3"}, valid=True),
            TaskElementValueObject(value={"key": "value 4"}, valid=True),
        ]
        self.assertEqual(task.element_values.get("EV_OBJECT"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_OBJECT", None)
        self.assertEqual(task.element_values.get("EV_OBJECT"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_OBJECT", [])
        self.assertEqual(task.element_values.get("EV_OBJECT"), expected_element_values)

    def test_get_element_value_as_document(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_document(task, "EV_DOCUMENT")
        self.assertEqual(value, prepare_task_element_value_document_item("1"))

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_element_value_as_document(task, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_document(self):
        task = prepare_task_element_values()

        value = TaskUtils.find_element_value_as_document(task, "EV_DOCUMENT")
        self.assertEqual(value, prepare_task_element_value_document_item("1"))

        value = TaskUtils.find_element_value_as_document(task, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_document_list(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_document_list(task, "EV_DOCUMENT")
        self.assertEqual(
            value, [prepare_task_element_value_document_item("1"), prepare_task_element_value_document_item("2")]
        )

        value = TaskUtils.get_element_value_as_document_list(task, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_document(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value(task, "EV_DOCUMENT", prepare_task_element_value_document_item("3"))
        self.assertEqual(
            task.element_values.get("EV_DOCUMENT"),
            [
                TaskElementValueDocument(value=prepare_task_element_value_document_item("3"), valid=True),
            ],
        )

        TaskUtils.set_element_value(task, "EV_DOCUMENT", None)
        self.assertIsNone(task.element_values.get("EV_DOCUMENT"))

    def test_set_element_value_as_document_list(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value_list(
            task,
            "EV_DOCUMENT",
            [prepare_task_element_value_document_item("3"), prepare_task_element_value_document_item("4")],
        )
        self.assertEqual(
            task.element_values.get("EV_DOCUMENT"),
            [
                TaskElementValueDocument(value=prepare_task_element_value_document_item("3"), valid=True),
                TaskElementValueDocument(value=prepare_task_element_value_document_item("4"), valid=True),
            ],
        )

        TaskUtils.set_element_value_list(task, "EV_DOCUMENT", [])
        self.assertIsNone(task.element_values.get("EV_DOCUMENT"))

    def test_add_element_value_as_document(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value(task, "EV_DOCUMENT", prepare_task_element_value_document_item("3"))

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
        self.assertEqual(task.element_values.get("EV_DOCUMENT"), expected_element_values)

        TaskUtils.add_element_value(task, "EV_DOCUMENT", None)
        self.assertEqual(task.element_values.get("EV_DOCUMENT"), expected_element_values)

    def test_add_element_value_as_document_list(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value_list(
            task,
            "EV_DOCUMENT",
            [prepare_task_element_value_document_item("3"), prepare_task_element_value_document_item("4")],
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
        self.assertEqual(task.element_values.get("EV_DOCUMENT"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_DOCUMENT", None)
        self.assertEqual(task.element_values.get("EV_DOCUMENT"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_DOCUMENT", [])
        self.assertEqual(task.element_values.get("EV_DOCUMENT"), expected_element_values)

    def test_get_element_value_as_principal(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_principal(task, "EV_PRINCIPAL")
        self.assertEqual(value, prepare_task_element_value_principal_item("1"))

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_element_value_as_principal(task, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_principal(self):
        task = prepare_task_element_values()

        value = TaskUtils.find_element_value_as_principal(task, "EV_PRINCIPAL")
        self.assertEqual(value, prepare_task_element_value_principal_item("1"))

        value = TaskUtils.find_element_value_as_principal(task, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_principal_list(self):
        task = prepare_task_element_values()

        value = TaskUtils.get_element_value_as_principal_list(task, "EV_PRINCIPAL")
        self.assertEqual(
            value, [prepare_task_element_value_principal_item("1"), prepare_task_element_value_principal_item("2")]
        )

        value = TaskUtils.get_element_value_as_principal_list(task, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_principal(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value(task, "EV_PRINCIPAL", prepare_task_element_value_principal_item("3"))
        self.assertEqual(
            task.element_values.get("EV_PRINCIPAL"),
            [
                TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("3"), valid=True),
            ],
        )

        TaskUtils.set_element_value(task, "EV_PRINCIPAL", None)
        self.assertIsNone(task.element_values.get("EV_PRINCIPAL"))

    def test_set_element_value_as_principal_list(self):
        task = prepare_task_element_values()

        TaskUtils.set_element_value_list(
            task,
            "EV_PRINCIPAL",
            [prepare_task_element_value_principal_item("3"), prepare_task_element_value_principal_item("4")],
        )
        self.assertEqual(
            task.element_values.get("EV_PRINCIPAL"),
            [
                TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("3"), valid=True),
                TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("4"), valid=True),
            ],
        )

        TaskUtils.set_element_value_list(task, "EV_PRINCIPAL", [])
        self.assertIsNone(task.element_values.get("EV_PRINCIPAL"))

    def test_add_element_value_as_principal(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value(task, "EV_PRINCIPAL", prepare_task_element_value_principal_item("3"))

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
        self.assertEqual(task.element_values.get("EV_PRINCIPAL"), expected_element_values)

        TaskUtils.add_element_value(task, "EV_PRINCIPAL", None)
        self.assertEqual(task.element_values.get("EV_PRINCIPAL"), expected_element_values)

    def test_add_element_value_as_principal_list(self):
        task = prepare_task_element_values()

        TaskUtils.add_element_value_list(
            task,
            "EV_PRINCIPAL",
            [prepare_task_element_value_principal_item("3"), prepare_task_element_value_principal_item("4")],
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
        self.assertEqual(task.element_values.get("EV_PRINCIPAL"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_PRINCIPAL", None)
        self.assertEqual(task.element_values.get("EV_PRINCIPAL"), expected_element_values)

        TaskUtils.add_element_value_list(task, "EV_PRINCIPAL", [])
        self.assertEqual(task.element_values.get("EV_PRINCIPAL"), expected_element_values)

    def test_get_json_forms_property_as_str(self):
        task = prepare_task_json_forms()
        value = TaskUtils.get_json_forms_property_as_str(task, "key1")
        self.assertEqual(value, "value_key1")

        value = TaskUtils.get_json_forms_property_as_str(task, "key2.0.key2_key1.0.key2_key1_key2")
        self.assertEqual(value, "value_key2_key1_key2")

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_json_forms_property_as_str(task, "key2.0.key2_key1.0.unknown")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_json_forms_property_as_str(task, "key2.0.key2_key1.10")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_json_forms_property_as_str(task, "key2.0.key2_key1.100.key2_key1_key2")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

    def test_find_json_forms_property_as_str(self):
        task = prepare_task_json_forms()

        value = TaskUtils.find_json_forms_property_as_str(task, "key1")
        self.assertEqual(value, "value_key1")

        value = TaskUtils.find_json_forms_property_as_str(task, "key2.0.key2_key1.0.key2_key1_key2")
        self.assertEqual(value, "value_key2_key1_key2")

        value = TaskUtils.find_json_forms_property_as_str(task, "key2.0.key2_key1.0.unknown")
        self.assertIsNone(value)

        value = TaskUtils.find_json_forms_property_as_str(task, "key2.0.key2_key1.10")
        self.assertIsNone(value)

        value = TaskUtils.find_json_forms_property_as_str(task, "key2.0.key2_key1.100.key2_key1_key2")
        self.assertIsNone(value)

    def test_get_json_forms_property_as_int(self):
        task = prepare_task_json_forms()

        value = TaskUtils.get_json_forms_property_as_int(task, "key3.0")
        self.assertEqual(value, 500)

        value = TaskUtils.get_json_forms_property_as_int(task, "key3.1")
        self.assertEqual(value, 1000)

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_json_forms_property_as_int(task, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_json_forms_property_as_int(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a int")

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_json_forms_property_as_int(task, "key3.2")
        self.assertEqual(str(context.exception), "Property key3.2 is not a int")

    def test_find_json_forms_property_as_int(self):
        task = prepare_task_json_forms()

        value = TaskUtils.find_json_forms_property_as_int(task, "key3.0")
        self.assertEqual(value, 500)

        value = TaskUtils.find_json_forms_property_as_int(task, "key3.1")
        self.assertEqual(value, 1000)

        value = TaskUtils.find_json_forms_property_as_int(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as context:
            TaskUtils.find_json_forms_property_as_int(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a int")

        with self.assertRaises(ValueError) as context:
            TaskUtils.find_json_forms_property_as_int(task, "key3.2")
        self.assertEqual(str(context.exception), "Property key3.2 is not a int")

    def test_get_json_forms_property_as_float(self):
        task = prepare_task_json_forms()

        value = TaskUtils.get_json_forms_property_as_float(task, "key3.0")
        self.assertEqual(value, 500)

        value = TaskUtils.get_json_forms_property_as_float(task, "key3.1")
        self.assertEqual(value, 1000)

        value = TaskUtils.get_json_forms_property_as_float(task, "key3.2")
        self.assertEqual(value, 2000.1)

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_json_forms_property_as_float(task, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            TaskUtils.get_json_forms_property_as_float(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a float")

    def test_find_json_forms_property_as_float(self):
        task = prepare_task_json_forms()

        value = TaskUtils.find_json_forms_property_as_float(task, "key3.0")
        self.assertEqual(value, 500)

        value = TaskUtils.find_json_forms_property_as_float(task, "key3.1")
        self.assertEqual(value, 1000)

        value = TaskUtils.find_json_forms_property_as_float(task, "key3.2")
        self.assertEqual(value, 2000.1)

        value = TaskUtils.find_json_forms_property_as_float(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as context:
            TaskUtils.find_json_forms_property_as_float(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a float")

    def test_get_json_forms_property_as_date(self):
        task = prepare_task_json_forms()

        value = TaskUtils.get_json_forms_property_as_date(task, "key5.0")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        with self.assertRaises(ValueError) as cm:
            TaskUtils.get_json_forms_property_as_date(task, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            TaskUtils.get_json_forms_property_as_date(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_find_json_forms_property_as_date(self):
        task = prepare_task_json_forms()

        value = TaskUtils.find_json_forms_property_as_date(task, "key5.0")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        value = TaskUtils.find_json_forms_property_as_date(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            TaskUtils.find_json_forms_property_as_date(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_get_json_forms_property_as_datetime(self):
        task = prepare_task_json_forms()

        value = TaskUtils.get_json_forms_property_as_datetime(task, "key5.1")
        self.assertEqual(value, datetime.fromisoformat("2000-01-01T10:10:05+01:00"))

        with self.assertRaises(ValueError) as cm:
            TaskUtils.get_json_forms_property_as_datetime(task, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            TaskUtils.get_json_forms_property_as_datetime(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date-time following ISO 8601 format")

    def test_find_json_forms_property_as_datetime(self):
        task = prepare_task_json_forms()

        value = TaskUtils.find_json_forms_property_as_datetime(task, "key5.1")
        self.assertEqual(value, datetime.fromisoformat("2000-01-01T10:10:05+01:00"))

        value = TaskUtils.find_json_forms_property_as_datetime(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            TaskUtils.find_json_forms_property_as_datetime(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date-time following ISO 8601 format")

    def test_get_json_forms_property_as_file(self):
        task = prepare_task_json_forms()

        value = TaskUtils.get_json_forms_property_as_file(task, "key6")
        self.assertEqual(value.uri, "xxx-yyy-zzz")
        self.assertEqual(value.type, "application/pdf")
        self.assertEqual(value.name, "dummy.pdf")
        self.assertEqual(value.size, 500)

        with self.assertRaises(ValueError) as cm:
            TaskUtils.get_json_forms_property_as_file(task, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            TaskUtils.get_json_forms_property_as_file(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a file")

    def test_find_json_forms_property_as_file(self):
        task = prepare_task_json_forms()

        value = TaskUtils.find_json_forms_property_as_file(task, "key6")
        self.assertEqual(value.uri, "xxx-yyy-zzz")
        self.assertEqual(value.type, "application/pdf")
        self.assertEqual(value.name, "dummy.pdf")
        self.assertEqual(value.size, 500)

        value = TaskUtils.find_json_forms_property_as_file(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            TaskUtils.find_json_forms_property_as_file(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a file")

    def test_get_json_forms_property_as_principal(self):
        task = prepare_task_json_forms()

        value = TaskUtils.get_json_forms_property_as_principal(task, "key7")
        self.assertEqual(value.id, "xxx-yyy-zzz")
        self.assertEqual(value.type, "USER")
        self.assertEqual(value.name, "Homer Simpson")

        with self.assertRaises(ValueError) as cm:
            TaskUtils.get_json_forms_property_as_principal(task, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            TaskUtils.get_json_forms_property_as_principal(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a principal")

    def test_find_json_forms_property_as_principal(self):
        task = prepare_task_json_forms()

        value = TaskUtils.find_json_forms_property_as_principal(task, "key7")
        self.assertEqual(value.id, "xxx-yyy-zzz")
        self.assertEqual(value.type, "USER")
        self.assertEqual(value.name, "Homer Simpson")

        value = TaskUtils.find_json_forms_property_as_principal(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            TaskUtils.find_json_forms_property_as_principal(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a principal")

    def test_get_json_forms_property_as_list(self):
        task = prepare_task_json_forms()

        value = TaskUtils.get_json_forms_property_as_list(task, "key3")
        self.assertEqual(value, [500, "1000", 2000.1])

        with self.assertRaises(Exception) as context:
            TaskUtils.get_json_forms_property_as_list(task, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(Exception) as context:
            TaskUtils.get_json_forms_property_as_list(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a list")

    def test_find_json_forms_property_as_list(self):
        task = prepare_task_json_forms()

        value1 = TaskUtils.find_json_forms_property_as_list(task, "key3")
        self.assertEqual(value1, [500, "1000", 2000.1])

        value = TaskUtils.find_json_forms_property_as_list(task, "key_xxxxxxx")
        self.assertIsNone(value)

    def test_get_json_forms_property_as_dict(self):
        task = prepare_task_json_forms()

        value = TaskUtils.get_json_forms_property_as_dict(task, "key2.0.key2_key1.0")
        self.assertEqual(
            value,
            {
                "key2_key1_key1": 0,
                "key2_key1_key2": "value_key2_key1_key2",
            },
        )

        with self.assertRaises(Exception) as context:
            TaskUtils.get_json_forms_property_as_dict(task, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(Exception) as context:
            TaskUtils.get_json_forms_property_as_dict(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a dict")

    def test_find_json_forms_property_as_dict(self):
        task = prepare_task_json_forms()

        value = TaskUtils.find_json_forms_property_as_dict(task, "key2.0.key2_key1.0")
        self.assertEqual(
            value,
            {
                "key2_key1_key1": 0,
                "key2_key1_key2": "value_key2_key1_key2",
            },
        )

        value = TaskUtils.find_json_forms_property_as_dict(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(Exception) as context:
            TaskUtils.find_json_forms_property_as_dict(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a dict")

    def test_update_json_forms_property(self):
        task = prepare_task_json_forms()
        task.json_forms_value = JsonFormsValue()

        file = JsonFormsFile(
            uri="xxx-yyy-zzz",
            type="application/pdf",
            name="dummy.pdf",
            size=500,
        )

        principal = JsonFormsPrincipal(
            id="xxx-yyy-zzz",
            type=PrincipalType.USER,
            name="Homer Simpson",
        )

        TaskUtils.update_json_forms_property(task, "key1", "text")
        TaskUtils.update_json_forms_property(task, "key2.0.key1", True)
        TaskUtils.update_json_forms_property(task, "key2.0.key2", date.fromisoformat("2020-01-01"))
        TaskUtils.update_json_forms_property(task, "key2.1.key1", False)
        TaskUtils.update_json_forms_property(task, "key2.1.key2", date.fromisoformat("3030-01-01"))
        TaskUtils.update_json_forms_property(task, "key2.2.key1", False)
        TaskUtils.update_json_forms_property(task, "key2.2.key2", datetime.fromisoformat("3030-01-01T10:10:00+01:00"))
        TaskUtils.update_json_forms_property(task, "key3", 100)
        TaskUtils.update_json_forms_property(task, "key4", file)
        TaskUtils.update_json_forms_property(task, "key5", principal)

        self.assertEqual(
            task.json_forms_value.data,
            {
                "key1": "text",
                "key2": [
                    {
                        "key1": True,
                        "key2": "2020-01-01",
                    },
                    {
                        "key1": False,
                        "key2": "3030-01-01",
                    },
                    {
                        "key1": False,
                        "key2": "3030-01-01T10:10:00+01:00",
                    },
                ],
                "key3": 100,
                "key4": "kuflow-file:uri=xxx-yyy-zzz;type=application/pdf;size=500;name=dummy.pdf;",
                "key5": "kuflow-principal:id=xxx-yyy-zzz;type=USER;name=Homer Simpson;",
            },
        )

        TaskUtils.update_json_forms_property(task, "key1", None)
        TaskUtils.update_json_forms_property(task, "key2.0", None)
        TaskUtils.update_json_forms_property(task, "key2.0.key1", None)

        self.assertEqual(
            task.json_forms_value.data,
            {
                "key2": [
                    {
                        "key2": "3030-01-01",
                    },
                    {
                        "key1": False,
                        "key2": "3030-01-01T10:10:00+01:00",
                    },
                ],
                "key3": 100,
                "key4": "kuflow-file:uri=xxx-yyy-zzz;type=application/pdf;size=500;name=dummy.pdf;",
                "key5": "kuflow-principal:id=xxx-yyy-zzz;type=USER;name=Homer Simpson;",
            },
        )

        with self.assertRaises(ValueError) as context:
            TaskUtils.update_json_forms_property(task, "key2.100.key1", None)
        self.assertEqual(str(context.exception), "Property key2.100.key1 doesn't exist")


def prepare_task_element_values() -> Task:
    return Task(
        task_definition=TaskDefinitionSummary(
            id="e68d8136-1166-455c-93d6-d106201c1856",
        ),
        process_id="3b755d5e-b64f-4ec2-a830-173f006bdf8e",
        element_values={
            "EV_STRING": [
                TaskElementValueString(value="MY TEXT 1", valid=True),
                TaskElementValueString(value="MY TEXT 2", valid=False),
            ],
            "EV_NUMBER": [
                TaskElementValueNumber(value=500, valid=True),
                TaskElementValueNumber(value=600, valid=True),
            ],
            "EV_DATE": [
                TaskElementValueString(value="2000-01-01", valid=False),
                TaskElementValueString(value="1980-01-01", valid=False),
            ],
            "EV_OBJECT": [
                TaskElementValueObject(value={"key": "value 1"}, valid=True),
                TaskElementValueObject(value={"key": "value 2"}, valid=False),
            ],
            "EV_DOCUMENT": [
                TaskElementValueDocument(
                    value=prepare_task_element_value_document_item("1"),
                    valid=True,
                ),
                TaskElementValueDocument(
                    value=prepare_task_element_value_document_item("2"),
                    valid=False,
                ),
            ],
            "EV_PRINCIPAL": [
                TaskElementValuePrincipal(
                    value=prepare_task_element_value_principal_item("1"),
                    valid=True,
                ),
                TaskElementValuePrincipal(
                    value=prepare_task_element_value_principal_item("2"),
                    valid=False,
                ),
            ],
        },
    )


def prepare_task_element_value_document_item(suffix: str) -> TaskElementValueDocumentItem:
    return TaskElementValueDocumentItem(
        id=f"id_{suffix}",
        uri=f"uri_{suffix}",
        name=f"name_{suffix}",
        content_path=f"contentPath_{suffix}",
        content_type=f"contentType_{suffix}",
        content_length=600,
    )


def prepare_task_element_value_principal_item(suffix: str) -> TaskElementValuePrincipalItem:
    return TaskElementValuePrincipalItem(
        id=f"id_{suffix}",
        type="USER",
        name=f"name_{suffix}",
    )


def prepare_task_json_forms() -> Task:
    return Task(
        task_definition=TaskDefinitionSummary(id="e68d8136-1166-455c-93d6-d106201c1856"),
        process_id="3b755d5e-b64f-4ec2-a830-173f006bdf8e",
        json_forms_value=JsonFormsValue(
            valid=True,
            data={
                "key1": "value_key1",
                "key2": [
                    {
                        "key2_key1": [
                            {
                                "key2_key1_key1": 0,
                                "key2_key1_key2": "value_key2_key1_key2",
                            },
                        ],
                    }
                ],
                "key3": [500, "1000", 2000.1],
                "key4": [True, False, "true", "false"],
                "key5": ["2000-01-01", "2000-01-01T10:10:05+01:00"],
                "key6": "kuflow-file:uri=xxx-yyy-zzz;type=application/pdf;size=500;name=dummy.pdf;",
                "key7": "kuflow-principal:id=xxx-yyy-zzz;type=USER;name=Homer Simpson;",
            },
        ),
    )


if __name__ == "__main__":
    unittest.main()
