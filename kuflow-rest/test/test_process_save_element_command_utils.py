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

from kuflow_rest.models import ProcessElementValueNumber, ProcessElementValueString, ProcessSaveElementCommand
from kuflow_rest.utils import ProcessSaveElementCommandUtils


class SaveProcessElementUtilsTest(unittest.TestCase):
    def test_get_element_value_valid(self):
        request = prepare_process_save_element_command_str()

        value = ProcessSaveElementCommandUtils.get_element_value_valid(request)
        self.assertFalse(value)

    def test_get_element_value_valid_at(self):
        request = prepare_process_save_element_command_str()

        value = ProcessSaveElementCommandUtils.get_element_value_valid_at(request, 0)
        self.assertTrue(value)

        value = ProcessSaveElementCommandUtils.get_element_value_valid_at(request, 1)
        self.assertFalse(value)

    def test_set_element_value_valid(self):
        request = prepare_process_save_element_command_str()

        ProcessSaveElementCommandUtils.set_element_value_valid(request, True)
        self.assertEqual(
            request.element_values,
            [
                ProcessElementValueString(value="MY TEXT 1", valid=True),
                ProcessElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        ProcessSaveElementCommandUtils.set_element_value_valid(request, False)
        self.assertEqual(
            request.element_values,
            [
                ProcessElementValueString(value="MY TEXT 1", valid=False),
                ProcessElementValueString(value="MY TEXT 2", valid=False),
            ],
        )

    def test_set_element_value_valid_at(self):
        request = prepare_process_save_element_command_str()

        ProcessSaveElementCommandUtils.set_element_value_valid_at(request, False, 0)
        ProcessSaveElementCommandUtils.set_element_value_valid_at(request, True, 1)
        self.assertEqual(
            request.element_values,
            [
                ProcessElementValueString(value="MY TEXT 1", valid=False),
                ProcessElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

    def test_get_element_value_as_str(self):
        request = prepare_process_save_element_command_str()

        value = ProcessSaveElementCommandUtils.get_element_value_as_str(request)
        self.assertEqual(value, "MY TEXT 1")

        request.element_values = []

        with self.assertRaises(ValueError) as context:
            ProcessSaveElementCommandUtils.get_element_value_as_str(request)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_str(self):
        request = prepare_process_save_element_command_str()

        value = ProcessSaveElementCommandUtils.find_element_value_as_str(request)
        self.assertEqual(value, "MY TEXT 1")

        request.element_values = []

        value = ProcessSaveElementCommandUtils.find_element_value_as_str(request)
        self.assertIsNone(value)

    def test_get_element_value_as_str_list(self):
        request = prepare_process_save_element_command_str()

        value = ProcessSaveElementCommandUtils.get_element_value_as_str_list(request)
        self.assertEqual(value, ["MY TEXT 1", "MY TEXT 2"])

        request.element_values = []

        value = ProcessSaveElementCommandUtils.get_element_value_as_str_list(request)
        self.assertEqual(value, [])

    def test_set_element_value_as_str(self):
        request = prepare_process_save_element_command_str()

        ProcessSaveElementCommandUtils.set_element_value(request, "MY TEXT NEW")
        self.assertEqual(
            request.element_values,
            [
                ProcessElementValueString(value="MY TEXT NEW", valid=True),
            ],
        )

        request.element_values = []

        ProcessSaveElementCommandUtils.set_element_value(request, None)
        self.assertIsNone(request.element_values)

    def test_set_element_value_as_str_list(self):
        request = prepare_process_save_element_command_str()

        ProcessSaveElementCommandUtils.set_element_value_list(request, ["MY TEXT NEW1", "MY TEXT NEW2"])
        self.assertEqual(
            request.element_values,
            [
                ProcessElementValueString(value="MY TEXT NEW1", valid=True),
                ProcessElementValueString(value="MY TEXT NEW2", valid=True),
            ],
        )

        ProcessSaveElementCommandUtils.set_element_value_list(request, [])
        self.assertIsNone(request.element_values)

    def test_add_element_value_as_str(self):
        request = prepare_process_save_element_command_str()

        ProcessSaveElementCommandUtils.add_element_value(request, "MY TEXT NEW1")

        expected_element_values = [
            ProcessElementValueString(value="MY TEXT 1", valid=True),
            ProcessElementValueString(value="MY TEXT 2", valid=False),
            ProcessElementValueString(value="MY TEXT NEW1", valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        ProcessSaveElementCommandUtils.add_element_value(request, None)
        self.assertEqual(request.element_values, expected_element_values)

    def test_add_element_value_as_str_list(self):
        request = prepare_process_save_element_command_str()

        ProcessSaveElementCommandUtils.add_element_value_list(request, ["MY TEXT NEW1", "MY TEXT NEW2"])

        expected_element_values = [
            ProcessElementValueString(value="MY TEXT 1", valid=True),
            ProcessElementValueString(value="MY TEXT 2", valid=False),
            ProcessElementValueString(value="MY TEXT NEW1", valid=True),
            ProcessElementValueString(value="MY TEXT NEW2", valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        ProcessSaveElementCommandUtils.add_element_value_list(request, None)
        self.assertEqual(request.element_values, expected_element_values)

        ProcessSaveElementCommandUtils.add_element_value_list(request, [])
        self.assertEqual(request.element_values, expected_element_values)

    def test_get_element_value_as_float(self):
        request = prepare_process_save_element_command_float()

        value = ProcessSaveElementCommandUtils.get_element_value_as_float(request)
        self.assertEqual(value, 500)

        request.element_values = []

        with self.assertRaises(ValueError) as context:
            ProcessSaveElementCommandUtils.get_element_value_as_float(request)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_float(self):
        request = prepare_process_save_element_command_float()

        value = ProcessSaveElementCommandUtils.find_element_value_as_float(request)
        self.assertEqual(value, 500)

        request.element_values = []

        value = ProcessSaveElementCommandUtils.find_element_value_as_float(request)
        self.assertIsNone(value)

    def test_get_element_value_as_float_list(self):
        request = prepare_process_save_element_command_float()

        value = ProcessSaveElementCommandUtils.get_element_value_as_float_list(request)
        self.assertEqual(value, [500, 600])

        request.element_values = []

        value = ProcessSaveElementCommandUtils.get_element_value_as_float_list(request)
        self.assertEqual(value, [])

    def test_set_element_value_as_float(self):
        request = prepare_process_save_element_command_float()

        ProcessSaveElementCommandUtils.set_element_value(request, 700)
        self.assertEqual(
            request.element_values,
            [
                ProcessElementValueNumber(value=700, valid=True),
            ],
        )

        ProcessSaveElementCommandUtils.set_element_value(request, None)
        self.assertIsNone(request.element_values)

    def test_set_element_value_as_float_list(self):
        request = prepare_process_save_element_command_float()

        ProcessSaveElementCommandUtils.set_element_value_list(request, [700, 800])
        self.assertEqual(
            request.element_values,
            [
                ProcessElementValueNumber(value=700, valid=True),
                ProcessElementValueNumber(value=800, valid=True),
            ],
        )

        ProcessSaveElementCommandUtils.set_element_value_list(request, [])
        self.assertIsNone(request.element_values)

    def test_add_element_value_as_float(self):
        request = prepare_process_save_element_command_float()

        ProcessSaveElementCommandUtils.add_element_value(request, 800)

        expected_element_values = [
            ProcessElementValueNumber(value=500, valid=True),
            ProcessElementValueNumber(value=600, valid=False),
            ProcessElementValueNumber(value=800, valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        ProcessSaveElementCommandUtils.add_element_value(request, None)
        self.assertEqual(request.element_values, expected_element_values)

    def test_add_element_value_as_float_list(self):
        request = prepare_process_save_element_command_float()

        ProcessSaveElementCommandUtils.add_element_value_list(request, [800, 900])

        expected_element_values = [
            ProcessElementValueNumber(value=500, valid=True),
            ProcessElementValueNumber(value=600, valid=False),
            ProcessElementValueNumber(value=800, valid=True),
            ProcessElementValueNumber(value=900, valid=True),
        ]
        self.assertEqual(
            request.element_values,
            expected_element_values,
        )

        ProcessSaveElementCommandUtils.add_element_value_list(request, None)
        self.assertEqual(request.element_values, expected_element_values)

        ProcessSaveElementCommandUtils.add_element_value_list(request, [])
        self.assertEqual(request.element_values, expected_element_values)

    def test_get_element_value_as_date(self):
        request = prepare_process_save_element_command_date()

        value = ProcessSaveElementCommandUtils.get_element_value_as_date(request)
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        request.element_values = []

        with self.assertRaises(ValueError) as context:
            ProcessSaveElementCommandUtils.get_element_value_as_date(request)
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_date(self):
        request = prepare_process_save_element_command_date()

        value = ProcessSaveElementCommandUtils.find_element_value_as_date(request)
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        request.element_values = []

        value = ProcessSaveElementCommandUtils.find_element_value_as_date(request)
        self.assertIsNone(value)

    def test_get_element_value_as_date_list(self):
        request = prepare_process_save_element_command_date()

        value = ProcessSaveElementCommandUtils.get_element_value_as_date_list(request)
        self.assertEqual(value, [date.fromisoformat("2000-01-01"), date.fromisoformat("1980-01-01")])

        request.element_values = []

        value = ProcessSaveElementCommandUtils.get_element_value_as_date_list(request)
        self.assertEqual(value, [])

    def test_set_element_value_as_date(self):
        request = prepare_process_save_element_command_date()

        ProcessSaveElementCommandUtils.set_element_value(request, date.fromisoformat("2020-05-05"))
        self.assertEqual(
            request.element_values,
            [
                ProcessElementValueString(value="2020-05-05", valid=True),
            ],
        )

        ProcessSaveElementCommandUtils.set_element_value(request, None)
        self.assertIsNone(request.element_values)

    def test_set_element_value_as_date_list(self):
        request = prepare_process_save_element_command_date()

        ProcessSaveElementCommandUtils.set_element_value_list(
            request, [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")]
        )
        self.assertEqual(
            request.element_values,
            [
                ProcessElementValueString(value="2020-05-05", valid=True),
                ProcessElementValueString(value="2020-08-08", valid=True),
            ],
        )

        ProcessSaveElementCommandUtils.set_element_value_list(request, [])
        self.assertIsNone(request.element_values)

    def test_add_element_value_as_date(self):
        request = prepare_process_save_element_command_date()

        ProcessSaveElementCommandUtils.add_element_value(request, date.fromisoformat("2020-08-08"))
        expected_element_values = [
            ProcessElementValueString(value="2000-01-01", valid=True),
            ProcessElementValueString(value="1980-01-01", valid=False),
            ProcessElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        ProcessSaveElementCommandUtils.add_element_value(request, None)
        self.assertEqual(request.element_values, expected_element_values)

    def test_add_element_value_as_date_list(self):
        request = prepare_process_save_element_command_date()

        ProcessSaveElementCommandUtils.add_element_value_list(
            request, [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")]
        )
        expected_element_values = [
            ProcessElementValueString(value="2000-01-01", valid=True),
            ProcessElementValueString(value="1980-01-01", valid=False),
            ProcessElementValueString(value="2020-05-05", valid=True),
            ProcessElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(request.element_values, expected_element_values)

        ProcessSaveElementCommandUtils.add_element_value_list(request, None)
        self.assertEqual(request.element_values, expected_element_values)

        ProcessSaveElementCommandUtils.add_element_value_list(request, [])
        self.assertEqual(request.element_values, expected_element_values)


def prepare_process_save_element_command_str() -> ProcessSaveElementCommand:
    return ProcessSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            ProcessElementValueString(value="MY TEXT 1", valid=True),
            ProcessElementValueString(value="MY TEXT 2", valid=False),
        ],
    )


def prepare_process_save_element_command_float() -> ProcessSaveElementCommand:
    return ProcessSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            ProcessElementValueNumber(value=500, valid=True),
            ProcessElementValueNumber(value=600, valid=False),
        ],
    )


def prepare_process_save_element_command_date() -> ProcessSaveElementCommand:
    return ProcessSaveElementCommand(
        element_definition_code="CODE",
        element_values=[
            ProcessElementValueString(value="2000-01-01", valid=True),
            ProcessElementValueString(value="1980-01-01", valid=False),
        ],
    )


if __name__ == "__main__":
    unittest.main()
