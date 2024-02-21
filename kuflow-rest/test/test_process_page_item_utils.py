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
    ProcessDefinitionSummary,
    ProcessElementValueNumber,
    ProcessElementValueString,
    ProcessPageItem,
)
from kuflow_rest.utils import ProcessPageItemUtils


class ProcessPageItemUtilsTest(unittest.TestCase):
    def test_get_element_value_valid(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.get_element_value_valid(process_page_item, "EV_STRING")
        self.assertFalse(value)

        value = ProcessPageItemUtils.get_element_value_valid(process_page_item, "EV_NUMBER")
        self.assertTrue(value)

        value = ProcessPageItemUtils.get_element_value_valid(process_page_item, "EV_DATE")
        self.assertFalse(value)

    def test_get_element_value_valid_at(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.get_element_value_valid_at(process_page_item, "EV_STRING", 0)
        self.assertTrue(value)

        value = ProcessPageItemUtils.get_element_value_valid_at(process_page_item, "EV_STRING", 1)
        self.assertFalse(value)

        with self.assertRaises(IndexError) as context:
            ProcessPageItemUtils.get_element_value_valid_at(process_page_item, "EV_STRING", 10)
        self.assertEqual(str(context.exception), "Array index out of bound: 10")

    def test_set_element_value_valid(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.set_element_value_valid(process_page_item, "EV_STRING", True)
        self.assertEqual(
            process_page_item.element_values.get("EV_STRING"),
            [
                ProcessElementValueString(value="MY TEXT 1", valid=True),
                ProcessElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        ProcessPageItemUtils.set_element_value_valid(process_page_item, "EV_STRING", False)
        self.assertEqual(
            process_page_item.element_values.get("EV_STRING"),
            [
                ProcessElementValueString(value="MY TEXT 1", valid=False),
                ProcessElementValueString(value="MY TEXT 2", valid=False),
            ],
        )

    def test_set_element_value_valid_at(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.set_element_value_valid_at(process_page_item, "EV_STRING", False, 0)
        ProcessPageItemUtils.set_element_value_valid_at(process_page_item, "EV_STRING", True, 1)
        self.assertEqual(
            process_page_item.element_values.get("EV_STRING"),
            [
                ProcessElementValueString(value="MY TEXT 1", valid=False),
                ProcessElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        with self.assertRaises(IndexError) as context:
            ProcessPageItemUtils.set_element_value_valid_at(process_page_item, "EV_STRING", False, 10)
        self.assertEqual(str(context.exception), "Array index out of bound: 10")

    def test_get_element_value_as_str(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.get_element_value_as_str(process_page_item, "EV_STRING")
        self.assertEqual(value, "MY TEXT 1")

        with self.assertRaises(ValueError) as context:
            ProcessPageItemUtils.get_element_value_as_str(process_page_item, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_str(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.find_element_value_as_str(process_page_item, "EV_STRING")
        self.assertEqual(value, "MY TEXT 1")

        value = ProcessPageItemUtils.find_element_value_as_str(process_page_item, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_str_list(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.get_element_value_as_str_list(process_page_item, "EV_STRING")
        self.assertEqual(value, ["MY TEXT 1", "MY TEXT 2"])

        value = ProcessPageItemUtils.get_element_value_as_str_list(process_page_item, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_str(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.set_element_value(process_page_item, "EV_STRING", "MY TEXT NEW")
        self.assertEqual(
            process_page_item.element_values.get("EV_STRING"),
            [
                ProcessElementValueString(value="MY TEXT NEW", valid=True),
            ],
        )

        ProcessPageItemUtils.set_element_value(process_page_item, "EV_STRING", None)
        self.assertIsNone(process_page_item.element_values.get("EV_STRING"))

    def test_set_element_value_as_str_list(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.set_element_value_list(process_page_item, "EV_STRING", ["MY TEXT NEW1", "MY TEXT NEW2"])
        self.assertEqual(
            process_page_item.element_values.get("EV_STRING"),
            [
                ProcessElementValueString(value="MY TEXT NEW1", valid=True),
                ProcessElementValueString(value="MY TEXT NEW2", valid=True),
            ],
        )

        ProcessPageItemUtils.set_element_value_list(process_page_item, "EV_STRING", [])
        self.assertIsNone(process_page_item.element_values.get("EV_STRING"))

    def test_add_element_value_as_str(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.add_element_value(process_page_item, "EV_STRING", "MY TEXT NEW1")

        expected_element_values = [
            ProcessElementValueString(value="MY TEXT 1", valid=True),
            ProcessElementValueString(value="MY TEXT 2", valid=False),
            ProcessElementValueString(value="MY TEXT NEW1", valid=True),
        ]
        self.assertEqual(process_page_item.element_values.get("EV_STRING"), expected_element_values)

        ProcessPageItemUtils.add_element_value(process_page_item, "EV_STRING", None)
        self.assertEqual(process_page_item.element_values.get("EV_STRING"), expected_element_values)

    def test_add_element_value_as_str_list(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.add_element_value_list(process_page_item, "EV_STRING", ["MY TEXT NEW1", "MY TEXT NEW2"])

        expected_element_values = [
            ProcessElementValueString(value="MY TEXT 1", valid=True),
            ProcessElementValueString(value="MY TEXT 2", valid=False),
            ProcessElementValueString(value="MY TEXT NEW1", valid=True),
            ProcessElementValueString(value="MY TEXT NEW2", valid=True),
        ]
        self.assertEqual(process_page_item.element_values.get("EV_STRING"), expected_element_values)

        ProcessPageItemUtils.add_element_value_list(process_page_item, "EV_STRING", None)
        self.assertEqual(process_page_item.element_values.get("EV_STRING"), expected_element_values)

        ProcessPageItemUtils.add_element_value_list(process_page_item, "EV_STRING", [])
        self.assertEqual(process_page_item.element_values.get("EV_STRING"), expected_element_values)

    def test_get_element_value_as_float(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.get_element_value_as_float(process_page_item, "EV_NUMBER")
        self.assertEqual(value, 500)

        with self.assertRaises(ValueError) as context:
            ProcessPageItemUtils.get_element_value_as_float(process_page_item, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_float(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.find_element_value_as_float(process_page_item, "EV_NUMBER")
        self.assertEqual(value, 500)

        value = ProcessPageItemUtils.find_element_value_as_float(process_page_item, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_float_list(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.get_element_value_as_float_list(process_page_item, "EV_NUMBER")
        self.assertEqual(value, [500, 600])

        value = ProcessPageItemUtils.get_element_value_as_float_list(process_page_item, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_float(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.set_element_value(process_page_item, "EV_NUMBER", 700)
        self.assertEqual(
            process_page_item.element_values.get("EV_NUMBER"),
            [
                ProcessElementValueNumber(value=700, valid=True),
            ],
        )

        ProcessPageItemUtils.set_element_value(process_page_item, "EV_NUMBER", None)
        self.assertIsNone(process_page_item.element_values.get("EV_NUMBER"))

    def test_set_element_value_as_float_list(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.set_element_value_list(process_page_item, "EV_NUMBER", [700, 800])
        self.assertEqual(
            process_page_item.element_values.get("EV_NUMBER"),
            [
                ProcessElementValueNumber(value=700, valid=True),
                ProcessElementValueNumber(value=800, valid=True),
            ],
        )

        ProcessPageItemUtils.set_element_value_list(process_page_item, "EV_NUMBER", [])
        self.assertIsNone(process_page_item.element_values.get("EV_NUMBER"))

    def test_add_element_value_as_float(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.add_element_value(process_page_item, "EV_NUMBER", 800)

        expected_element_values = [
            ProcessElementValueNumber(value=500, valid=True),
            ProcessElementValueNumber(value=600, valid=True),
            ProcessElementValueNumber(value=800, valid=True),
        ]
        self.assertEqual(process_page_item.element_values.get("EV_NUMBER"), expected_element_values)

        ProcessPageItemUtils.add_element_value(process_page_item, "EV_NUMBER", None)
        self.assertEqual(process_page_item.element_values.get("EV_NUMBER"), expected_element_values)

    def test_add_element_value_as_float_list(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.add_element_value_list(process_page_item, "EV_NUMBER", [800, 900])

        expected_element_values = [
            ProcessElementValueNumber(value=500, valid=True),
            ProcessElementValueNumber(value=600, valid=True),
            ProcessElementValueNumber(value=800, valid=True),
            ProcessElementValueNumber(value=900, valid=True),
        ]
        self.assertEqual(
            process_page_item.element_values.get("EV_NUMBER"),
            expected_element_values,
        )

        ProcessPageItemUtils.add_element_value_list(process_page_item, "EV_NUMBER", None)
        self.assertEqual(process_page_item.element_values.get("EV_NUMBER"), expected_element_values)

        ProcessPageItemUtils.add_element_value_list(process_page_item, "EV_NUMBER", [])
        self.assertEqual(process_page_item.element_values.get("EV_NUMBER"), expected_element_values)

    def test_get_element_value_as_date(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.get_element_value_as_date(process_page_item, "EV_DATE")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        with self.assertRaises(ValueError) as context:
            ProcessPageItemUtils.get_element_value_as_date(process_page_item, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_date(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.find_element_value_as_date(process_page_item, "EV_DATE")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        value = ProcessPageItemUtils.find_element_value_as_date(process_page_item, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_date_list(self):
        process_page_item = prepare_process_page_item()

        value = ProcessPageItemUtils.get_element_value_as_date_list(process_page_item, "EV_DATE")
        self.assertEqual(value, [date.fromisoformat("2000-01-01"), date.fromisoformat("1980-01-01")])

        value = ProcessPageItemUtils.get_element_value_as_date_list(process_page_item, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_date(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.set_element_value(process_page_item, "EV_DATE", date.fromisoformat("2020-05-05"))
        self.assertEqual(
            process_page_item.element_values.get("EV_DATE"),
            [
                ProcessElementValueString(value="2020-05-05", valid=True),
            ],
        )

        ProcessPageItemUtils.set_element_value(process_page_item, "EV_DATE", None)
        self.assertIsNone(process_page_item.element_values.get("EV_DATE"))

    def test_set_element_value_as_date_list(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.set_element_value_list(
            process_page_item,
            "EV_DATE",
            [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")],
        )
        self.assertEqual(
            process_page_item.element_values.get("EV_DATE"),
            [
                ProcessElementValueString(value="2020-05-05", valid=True),
                ProcessElementValueString(value="2020-08-08", valid=True),
            ],
        )

        ProcessPageItemUtils.set_element_value_list(process_page_item, "EV_DATE", [])
        self.assertIsNone(process_page_item.element_values.get("EV_DATE"))

    def test_add_element_value_as_date(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.add_element_value(process_page_item, "EV_DATE", date.fromisoformat("2020-08-08"))
        expected_element_values = [
            ProcessElementValueString(value="2000-01-01", valid=False),
            ProcessElementValueString(value="1980-01-01", valid=False),
            ProcessElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(process_page_item.element_values.get("EV_DATE"), expected_element_values)

        ProcessPageItemUtils.add_element_value(process_page_item, "EV_DATE", None)
        self.assertEqual(process_page_item.element_values.get("EV_DATE"), expected_element_values)

    def test_add_element_value_as_date_list(self):
        process_page_item = prepare_process_page_item()

        ProcessPageItemUtils.add_element_value_list(
            process_page_item,
            "EV_DATE",
            [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")],
        )
        expected_element_values = [
            ProcessElementValueString(value="2000-01-01", valid=False),
            ProcessElementValueString(value="1980-01-01", valid=False),
            ProcessElementValueString(value="2020-05-05", valid=True),
            ProcessElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(process_page_item.element_values.get("EV_DATE"), expected_element_values)

        ProcessPageItemUtils.add_element_value_list(process_page_item, "EV_DATE", None)
        self.assertEqual(process_page_item.element_values.get("EV_DATE"), expected_element_values)

        ProcessPageItemUtils.add_element_value_list(process_page_item, "EV_DATE", [])
        self.assertEqual(process_page_item.element_values.get("EV_DATE"), expected_element_values)


def prepare_process_page_item() -> ProcessPageItem:
    return ProcessPageItem(
        process_definition=ProcessDefinitionSummary(
            id="e68d8136-1166-455c-93d6-d106201c1856",
        ),
        process_id="3b755d5e-b64f-4ec2-a830-173f006bdf8e",
        element_values={
            "EV_STRING": [
                ProcessElementValueString(value="MY TEXT 1", valid=True),
                ProcessElementValueString(value="MY TEXT 2", valid=False),
            ],
            "EV_NUMBER": [
                ProcessElementValueNumber(value=500, valid=True),
                ProcessElementValueNumber(value=600, valid=True),
            ],
            "EV_DATE": [
                ProcessElementValueString(value="2000-01-01", valid=False),
                ProcessElementValueString(value="1980-01-01", valid=False),
            ],
        },
    )


if __name__ == "__main__":
    unittest.main()
