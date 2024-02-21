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
    TaskDefinitionSummary,
    TaskElementValueDocument,
    TaskElementValueDocumentItem,
    TaskElementValueNumber,
    TaskElementValueObject,
    TaskElementValuePrincipal,
    TaskElementValuePrincipalItem,
    TaskElementValueString,
    TaskPageItem,
)
from kuflow_rest.utils import TaskPageItemUtils


class TaskPageItemsUtilsTest(unittest.TestCase):
    def test_get_element_value_valid(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_valid(task_page_item, "EV_STRING")
        self.assertFalse(value)

        value = TaskPageItemUtils.get_element_value_valid(task_page_item, "EV_NUMBER")
        self.assertTrue(value)

        value = TaskPageItemUtils.get_element_value_valid(task_page_item, "EV_DATE")
        self.assertFalse(value)

    def test_get_element_value_valid_at(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_valid_at(task_page_item, "EV_STRING", 0)
        self.assertTrue(value)

        value = TaskPageItemUtils.get_element_value_valid_at(task_page_item, "EV_STRING", 1)
        self.assertFalse(value)

        with self.assertRaises(IndexError) as context:
            TaskPageItemUtils.get_element_value_valid_at(task_page_item, "EV_STRING", 10)
        self.assertEqual(str(context.exception), "Array index out of bound: 10")

    def test_set_element_value_valid(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value_valid(task_page_item, "EV_STRING", True)
        self.assertEqual(
            task_page_item.element_values.get("EV_STRING"),
            [
                TaskElementValueString(value="MY TEXT 1", valid=True),
                TaskElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value_valid(task_page_item, "EV_STRING", False)
        self.assertEqual(
            task_page_item.element_values.get("EV_STRING"),
            [
                TaskElementValueString(value="MY TEXT 1", valid=False),
                TaskElementValueString(value="MY TEXT 2", valid=False),
            ],
        )

    def test_set_element_value_valid_at(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value_valid_at(task_page_item, "EV_STRING", False, 0)
        TaskPageItemUtils.set_element_value_valid_at(task_page_item, "EV_STRING", True, 1)
        self.assertEqual(
            task_page_item.element_values.get("EV_STRING"),
            [
                TaskElementValueString(value="MY TEXT 1", valid=False),
                TaskElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        with self.assertRaises(IndexError) as context:
            TaskPageItemUtils.set_element_value_valid_at(task_page_item, "EV_STRING", False, 10)
        self.assertEqual(str(context.exception), "Array index out of bound: 10")

    def test_get_element_value_as_str(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_str(task_page_item, "EV_STRING")
        self.assertEqual(value, "MY TEXT 1")

        with self.assertRaises(ValueError) as context:
            TaskPageItemUtils.get_element_value_as_str(task_page_item, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_str(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.find_element_value_as_str(task_page_item, "EV_STRING")
        self.assertEqual(value, "MY TEXT 1")

        value = TaskPageItemUtils.find_element_value_as_str(task_page_item, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_str_list(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_str_list(task_page_item, "EV_STRING")
        self.assertEqual(value, ["MY TEXT 1", "MY TEXT 2"])

        value = TaskPageItemUtils.get_element_value_as_str_list(task_page_item, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_str(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value(task_page_item, "EV_STRING", "MY TEXT NEW")
        self.assertEqual(
            task_page_item.element_values.get("EV_STRING"),
            [
                TaskElementValueString(value="MY TEXT NEW", valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value(task_page_item, "EV_STRING", None)
        self.assertIsNone(task_page_item.element_values.get("EV_STRING"))

    def test_set_element_value_as_str_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value_list(task_page_item, "EV_STRING", ["MY TEXT NEW1", "MY TEXT NEW2"])
        self.assertEqual(
            task_page_item.element_values.get("EV_STRING"),
            [
                TaskElementValueString(value="MY TEXT NEW1", valid=True),
                TaskElementValueString(value="MY TEXT NEW2", valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value_list(task_page_item, "EV_STRING", [])
        self.assertIsNone(task_page_item.element_values.get("EV_STRING"))

    def test_add_element_value_as_str(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value(task_page_item, "EV_STRING", "MY TEXT NEW1")

        expected_element_values = [
            TaskElementValueString(value="MY TEXT 1", valid=True),
            TaskElementValueString(value="MY TEXT 2", valid=False),
            TaskElementValueString(value="MY TEXT NEW1", valid=True),
        ]
        self.assertEqual(task_page_item.element_values.get("EV_STRING"), expected_element_values)

        TaskPageItemUtils.add_element_value(task_page_item, "EV_STRING", None)
        self.assertEqual(task_page_item.element_values.get("EV_STRING"), expected_element_values)

    def test_add_element_value_as_str_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_STRING", ["MY TEXT NEW1", "MY TEXT NEW2"])

        expected_element_values = [
            TaskElementValueString(value="MY TEXT 1", valid=True),
            TaskElementValueString(value="MY TEXT 2", valid=False),
            TaskElementValueString(value="MY TEXT NEW1", valid=True),
            TaskElementValueString(value="MY TEXT NEW2", valid=True),
        ]
        self.assertEqual(task_page_item.element_values.get("EV_STRING"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_STRING", None)
        self.assertEqual(task_page_item.element_values.get("EV_STRING"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_STRING", [])
        self.assertEqual(task_page_item.element_values.get("EV_STRING"), expected_element_values)

    def test_get_element_value_as_float(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_float(task_page_item, "EV_NUMBER")
        self.assertEqual(value, 500)

        with self.assertRaises(ValueError) as context:
            TaskPageItemUtils.get_element_value_as_float(task_page_item, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_float(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.find_element_value_as_float(task_page_item, "EV_NUMBER")
        self.assertEqual(value, 500)

        value = TaskPageItemUtils.find_element_value_as_float(task_page_item, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_float_list(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_float_list(task_page_item, "EV_NUMBER")
        self.assertEqual(value, [500, 600])

        value = TaskPageItemUtils.get_element_value_as_float_list(task_page_item, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_float(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value(task_page_item, "EV_NUMBER", 700)
        self.assertEqual(
            task_page_item.element_values.get("EV_NUMBER"),
            [
                TaskElementValueNumber(value=700, valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value(task_page_item, "EV_NUMBER", None)
        self.assertIsNone(task_page_item.element_values.get("EV_NUMBER"))

    def test_set_element_value_as_float_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value_list(task_page_item, "EV_NUMBER", [700, 800])
        self.assertEqual(
            task_page_item.element_values.get("EV_NUMBER"),
            [
                TaskElementValueNumber(value=700, valid=True),
                TaskElementValueNumber(value=800, valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value_list(task_page_item, "EV_NUMBER", [])
        self.assertIsNone(task_page_item.element_values.get("EV_NUMBER"))

    def test_add_element_value_as_float(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value(task_page_item, "EV_NUMBER", 800)

        expected_element_values = [
            TaskElementValueNumber(value=500, valid=True),
            TaskElementValueNumber(value=600, valid=True),
            TaskElementValueNumber(value=800, valid=True),
        ]
        self.assertEqual(task_page_item.element_values.get("EV_NUMBER"), expected_element_values)

        TaskPageItemUtils.add_element_value(task_page_item, "EV_NUMBER", None)
        self.assertEqual(task_page_item.element_values.get("EV_NUMBER"), expected_element_values)

    def test_add_element_value_as_float_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_NUMBER", [800, 900])

        expected_element_values = [
            TaskElementValueNumber(value=500, valid=True),
            TaskElementValueNumber(value=600, valid=True),
            TaskElementValueNumber(value=800, valid=True),
            TaskElementValueNumber(value=900, valid=True),
        ]
        self.assertEqual(
            task_page_item.element_values.get("EV_NUMBER"),
            expected_element_values,
        )

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_NUMBER", None)
        self.assertEqual(task_page_item.element_values.get("EV_NUMBER"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_NUMBER", [])
        self.assertEqual(task_page_item.element_values.get("EV_NUMBER"), expected_element_values)

    def test_get_element_value_as_date(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_date(task_page_item, "EV_DATE")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        with self.assertRaises(ValueError) as context:
            TaskPageItemUtils.get_element_value_as_date(task_page_item, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_date(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.find_element_value_as_date(task_page_item, "EV_DATE")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        value = TaskPageItemUtils.find_element_value_as_date(task_page_item, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_date_list(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_date_list(task_page_item, "EV_DATE")
        self.assertEqual(value, [date.fromisoformat("2000-01-01"), date.fromisoformat("1980-01-01")])

        value = TaskPageItemUtils.get_element_value_as_date_list(task_page_item, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_date(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value(task_page_item, "EV_DATE", date.fromisoformat("2020-05-05"))
        self.assertEqual(
            task_page_item.element_values.get("EV_DATE"),
            [
                TaskElementValueString(value="2020-05-05", valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value(task_page_item, "EV_DATE", None)
        self.assertIsNone(task_page_item.element_values.get("EV_DATE"))

    def test_set_element_value_as_date_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value_list(
            task_page_item,
            "EV_DATE",
            [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")],
        )
        self.assertEqual(
            task_page_item.element_values.get("EV_DATE"),
            [
                TaskElementValueString(value="2020-05-05", valid=True),
                TaskElementValueString(value="2020-08-08", valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value_list(task_page_item, "EV_DATE", [])
        self.assertIsNone(task_page_item.element_values.get("EV_DATE"))

    def test_add_element_value_as_date(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value(task_page_item, "EV_DATE", date.fromisoformat("2020-08-08"))
        expected_element_values = [
            TaskElementValueString(value="2000-01-01", valid=False),
            TaskElementValueString(value="1980-01-01", valid=False),
            TaskElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(task_page_item.element_values.get("EV_DATE"), expected_element_values)

        TaskPageItemUtils.add_element_value(task_page_item, "EV_DATE", None)
        self.assertEqual(task_page_item.element_values.get("EV_DATE"), expected_element_values)

    def test_add_element_value_as_date_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value_list(
            task_page_item,
            "EV_DATE",
            [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")],
        )
        expected_element_values = [
            TaskElementValueString(value="2000-01-01", valid=False),
            TaskElementValueString(value="1980-01-01", valid=False),
            TaskElementValueString(value="2020-05-05", valid=True),
            TaskElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(task_page_item.element_values.get("EV_DATE"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_DATE", None)
        self.assertEqual(task_page_item.element_values.get("EV_DATE"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_DATE", [])
        self.assertEqual(task_page_item.element_values.get("EV_DATE"), expected_element_values)

    def test_get_element_value_as_dict(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_dict(task_page_item, "EV_OBJECT")
        self.assertEqual(value, {"key": "value 1"})

        with self.assertRaises(ValueError) as context:
            TaskPageItemUtils.get_element_value_as_dict(task_page_item, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_dict(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.find_element_value_as_dict(task_page_item, "EV_OBJECT")
        self.assertEqual(value, {"key": "value 1"})

        value = TaskPageItemUtils.find_element_value_as_dict(task_page_item, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_dict_list(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_dict_list(task_page_item, "EV_OBJECT")
        self.assertEqual(value, [{"key": "value 1"}, {"key": "value 2"}])

        value = TaskPageItemUtils.get_element_value_as_dict_list(task_page_item, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_dict(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value(task_page_item, "EV_OBJECT", {"key": "value 3"})
        self.assertEqual(
            task_page_item.element_values.get("EV_OBJECT"),
            [
                TaskElementValueObject(value={"key": "value 3"}, valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value(task_page_item, "EV_OBJECT", None)
        self.assertIsNone(task_page_item.element_values.get("EV_OBJECT"))

    def test_set_element_value_as_dict_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value_list(task_page_item, "EV_OBJECT", [{"key": "value 3"}, {"key": "value 4"}])
        self.assertEqual(
            task_page_item.element_values.get("EV_OBJECT"),
            [
                TaskElementValueObject(value={"key": "value 3"}, valid=True),
                TaskElementValueObject(value={"key": "value 4"}, valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value_list(task_page_item, "EV_OBJECT", [])
        self.assertIsNone(task_page_item.element_values.get("EV_OBJECT"))

    def test_add_element_value_as_dict(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value(task_page_item, "EV_OBJECT", {"key": "value 3"})

        expected_element_values = [
            TaskElementValueObject(value={"key": "value 1"}, valid=True),
            TaskElementValueObject(value={"key": "value 2"}, valid=False),
            TaskElementValueObject(value={"key": "value 3"}, valid=True),
        ]
        self.assertEqual(task_page_item.element_values.get("EV_OBJECT"), expected_element_values)

        TaskPageItemUtils.add_element_value(task_page_item, "EV_OBJECT", None)
        self.assertEqual(task_page_item.element_values.get("EV_OBJECT"), expected_element_values)

    def test_add_element_value_as_dict_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_OBJECT", [{"key": "value 3"}, {"key": "value 4"}])

        expected_element_values = [
            TaskElementValueObject(value={"key": "value 1"}, valid=True),
            TaskElementValueObject(value={"key": "value 2"}, valid=False),
            TaskElementValueObject(value={"key": "value 3"}, valid=True),
            TaskElementValueObject(value={"key": "value 4"}, valid=True),
        ]
        self.assertEqual(task_page_item.element_values.get("EV_OBJECT"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_OBJECT", None)
        self.assertEqual(task_page_item.element_values.get("EV_OBJECT"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_OBJECT", [])
        self.assertEqual(task_page_item.element_values.get("EV_OBJECT"), expected_element_values)

    def test_get_element_value_as_document(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_document(task_page_item, "EV_DOCUMENT")
        self.assertEqual(value, prepare_task_element_value_document_item("1"))

        with self.assertRaises(ValueError) as context:
            TaskPageItemUtils.get_element_value_as_document(task_page_item, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_document(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.find_element_value_as_document(task_page_item, "EV_DOCUMENT")
        self.assertEqual(value, prepare_task_element_value_document_item("1"))

        value = TaskPageItemUtils.find_element_value_as_document(task_page_item, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_document_list(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_document_list(task_page_item, "EV_DOCUMENT")
        self.assertEqual(
            value,
            [
                prepare_task_element_value_document_item("1"),
                prepare_task_element_value_document_item("2"),
            ],
        )

        value = TaskPageItemUtils.get_element_value_as_document_list(task_page_item, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_document(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value(
            task_page_item, "EV_DOCUMENT", prepare_task_element_value_document_item("3")
        )
        self.assertEqual(
            task_page_item.element_values.get("EV_DOCUMENT"),
            [
                TaskElementValueDocument(value=prepare_task_element_value_document_item("3"), valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value(task_page_item, "EV_DOCUMENT", None)
        self.assertIsNone(task_page_item.element_values.get("EV_DOCUMENT"))

    def test_set_element_value_as_document_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value_list(
            task_page_item,
            "EV_DOCUMENT",
            [
                prepare_task_element_value_document_item("3"),
                prepare_task_element_value_document_item("4"),
            ],
        )
        self.assertEqual(
            task_page_item.element_values.get("EV_DOCUMENT"),
            [
                TaskElementValueDocument(value=prepare_task_element_value_document_item("3"), valid=True),
                TaskElementValueDocument(value=prepare_task_element_value_document_item("4"), valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value_list(task_page_item, "EV_DOCUMENT", [])
        self.assertIsNone(task_page_item.element_values.get("EV_DOCUMENT"))

    def test_add_element_value_as_document(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value(
            task_page_item, "EV_DOCUMENT", prepare_task_element_value_document_item("3")
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
        ]
        self.assertEqual(task_page_item.element_values.get("EV_DOCUMENT"), expected_element_values)

        TaskPageItemUtils.add_element_value(task_page_item, "EV_DOCUMENT", None)
        self.assertEqual(task_page_item.element_values.get("EV_DOCUMENT"), expected_element_values)

    def test_add_element_value_as_document_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value_list(
            task_page_item,
            "EV_DOCUMENT",
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
        self.assertEqual(task_page_item.element_values.get("EV_DOCUMENT"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_DOCUMENT", None)
        self.assertEqual(task_page_item.element_values.get("EV_DOCUMENT"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_DOCUMENT", [])
        self.assertEqual(task_page_item.element_values.get("EV_DOCUMENT"), expected_element_values)

    def test_get_element_value_as_principal(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_principal(task_page_item, "EV_PRINCIPAL")
        self.assertEqual(value, prepare_task_element_value_principal_item("1"))

        with self.assertRaises(ValueError) as context:
            TaskPageItemUtils.get_element_value_as_principal(task_page_item, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_principal(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.find_element_value_as_principal(task_page_item, "EV_PRINCIPAL")
        self.assertEqual(value, prepare_task_element_value_principal_item("1"))

        value = TaskPageItemUtils.find_element_value_as_principal(task_page_item, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_principal_list(self):
        task_page_item = prepare_task_page_item()

        value = TaskPageItemUtils.get_element_value_as_principal_list(task_page_item, "EV_PRINCIPAL")
        self.assertEqual(
            value,
            [
                prepare_task_element_value_principal_item("1"),
                prepare_task_element_value_principal_item("2"),
            ],
        )

        value = TaskPageItemUtils.get_element_value_as_principal_list(task_page_item, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_principal(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value(
            task_page_item,
            "EV_PRINCIPAL",
            prepare_task_element_value_principal_item("3"),
        )
        self.assertEqual(
            task_page_item.element_values.get("EV_PRINCIPAL"),
            [
                TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("3"), valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value(task_page_item, "EV_PRINCIPAL", None)
        self.assertIsNone(task_page_item.element_values.get("EV_PRINCIPAL"))

    def test_set_element_value_as_principal_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.set_element_value_list(
            task_page_item,
            "EV_PRINCIPAL",
            [
                prepare_task_element_value_principal_item("3"),
                prepare_task_element_value_principal_item("4"),
            ],
        )
        self.assertEqual(
            task_page_item.element_values.get("EV_PRINCIPAL"),
            [
                TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("3"), valid=True),
                TaskElementValuePrincipal(value=prepare_task_element_value_principal_item("4"), valid=True),
            ],
        )

        TaskPageItemUtils.set_element_value_list(task_page_item, "EV_PRINCIPAL", [])
        self.assertIsNone(task_page_item.element_values.get("EV_PRINCIPAL"))

    def test_add_element_value_as_principal(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value(
            task_page_item,
            "EV_PRINCIPAL",
            prepare_task_element_value_principal_item("3"),
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
        ]
        self.assertEqual(task_page_item.element_values.get("EV_PRINCIPAL"), expected_element_values)

        TaskPageItemUtils.add_element_value(task_page_item, "EV_PRINCIPAL", None)
        self.assertEqual(task_page_item.element_values.get("EV_PRINCIPAL"), expected_element_values)

    def test_add_element_value_as_principal_list(self):
        task_page_item = prepare_task_page_item()

        TaskPageItemUtils.add_element_value_list(
            task_page_item,
            "EV_PRINCIPAL",
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
        self.assertEqual(task_page_item.element_values.get("EV_PRINCIPAL"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_PRINCIPAL", None)
        self.assertEqual(task_page_item.element_values.get("EV_PRINCIPAL"), expected_element_values)

        TaskPageItemUtils.add_element_value_list(task_page_item, "EV_PRINCIPAL", [])
        self.assertEqual(task_page_item.element_values.get("EV_PRINCIPAL"), expected_element_values)


def prepare_task_page_item() -> TaskPageItem:
    return TaskPageItem(
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
