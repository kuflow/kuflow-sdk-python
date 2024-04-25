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
    Process,
    ProcessDefinitionSummary,
    ProcessElementValueNumber,
    ProcessElementValueString,
)
from kuflow_rest.utils import ProcessUtils


class ProcessUtilsTest(unittest.TestCase):
    def test_get_element_value_valid(self):
        process = prepare_process()

        value = ProcessUtils.get_element_value_valid(process, "EV_STRING")
        self.assertFalse(value)

        value = ProcessUtils.get_element_value_valid(process, "EV_NUMBER")
        self.assertTrue(value)

        value = ProcessUtils.get_element_value_valid(process, "EV_DATE")
        self.assertFalse(value)

    def test_get_element_value_valid_at(self):
        process = prepare_process()

        value = ProcessUtils.get_element_value_valid_at(process, "EV_STRING", 0)
        self.assertTrue(value)

        value = ProcessUtils.get_element_value_valid_at(process, "EV_STRING", 1)
        self.assertFalse(value)

        with self.assertRaises(IndexError) as context:
            ProcessUtils.get_element_value_valid_at(process, "EV_STRING", 10)
        self.assertEqual(str(context.exception), "Array index out of bound: 10")

    def test_set_element_value_valid(self):
        process = prepare_process()

        ProcessUtils.set_element_value_valid(process, "EV_STRING", True)
        self.assertEqual(
            process.element_values.get("EV_STRING"),
            [
                ProcessElementValueString(value="MY TEXT 1", valid=True),
                ProcessElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        ProcessUtils.set_element_value_valid(process, "EV_STRING", False)
        self.assertEqual(
            process.element_values.get("EV_STRING"),
            [
                ProcessElementValueString(value="MY TEXT 1", valid=False),
                ProcessElementValueString(value="MY TEXT 2", valid=False),
            ],
        )

    def test_set_element_value_valid_at(self):
        process = prepare_process()

        ProcessUtils.set_element_value_valid_at(process, "EV_STRING", False, 0)
        ProcessUtils.set_element_value_valid_at(process, "EV_STRING", True, 1)
        self.assertEqual(
            process.element_values.get("EV_STRING"),
            [
                ProcessElementValueString(value="MY TEXT 1", valid=False),
                ProcessElementValueString(value="MY TEXT 2", valid=True),
            ],
        )

        with self.assertRaises(IndexError) as context:
            ProcessUtils.set_element_value_valid_at(process, "EV_STRING", False, 10)
        self.assertEqual(str(context.exception), "Array index out of bound: 10")

    def test_get_element_value_as_str(self):
        process = prepare_process()

        value = ProcessUtils.get_element_value_as_str(process, "EV_STRING")
        self.assertEqual(value, "MY TEXT 1")

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_element_value_as_str(process, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_str(self):
        process = prepare_process()

        value = ProcessUtils.find_element_value_as_str(process, "EV_STRING")
        self.assertEqual(value, "MY TEXT 1")

        value = ProcessUtils.find_element_value_as_str(process, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_str_list(self):
        process = prepare_process()

        value = ProcessUtils.get_element_value_as_str_list(process, "EV_STRING")
        self.assertEqual(value, ["MY TEXT 1", "MY TEXT 2"])

        value = ProcessUtils.get_element_value_as_str_list(process, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_str(self):
        process = prepare_process()

        ProcessUtils.set_element_value(process, "EV_STRING", "MY TEXT NEW")
        self.assertEqual(
            process.element_values.get("EV_STRING"),
            [
                ProcessElementValueString(value="MY TEXT NEW", valid=True),
            ],
        )

        ProcessUtils.set_element_value(process, "EV_STRING", None)
        self.assertIsNone(process.element_values.get("EV_STRING"))

    def test_set_element_value_as_str_list(self):
        process = prepare_process()

        ProcessUtils.set_element_value_list(process, "EV_STRING", ["MY TEXT NEW1", "MY TEXT NEW2"])
        self.assertEqual(
            process.element_values.get("EV_STRING"),
            [
                ProcessElementValueString(value="MY TEXT NEW1", valid=True),
                ProcessElementValueString(value="MY TEXT NEW2", valid=True),
            ],
        )

        ProcessUtils.set_element_value_list(process, "EV_STRING", [])
        self.assertIsNone(process.element_values.get("EV_STRING"))

    def test_add_element_value_as_str(self):
        process = prepare_process()

        ProcessUtils.add_element_value(process, "EV_STRING", "MY TEXT NEW1")

        expected_element_values = [
            ProcessElementValueString(value="MY TEXT 1", valid=True),
            ProcessElementValueString(value="MY TEXT 2", valid=False),
            ProcessElementValueString(value="MY TEXT NEW1", valid=True),
        ]
        self.assertEqual(process.element_values.get("EV_STRING"), expected_element_values)

        ProcessUtils.add_element_value(process, "EV_STRING", None)
        self.assertEqual(process.element_values.get("EV_STRING"), expected_element_values)

    def test_add_element_value_as_str_list(self):
        process = prepare_process()

        ProcessUtils.add_element_value_list(process, "EV_STRING", ["MY TEXT NEW1", "MY TEXT NEW2"])

        expected_element_values = [
            ProcessElementValueString(value="MY TEXT 1", valid=True),
            ProcessElementValueString(value="MY TEXT 2", valid=False),
            ProcessElementValueString(value="MY TEXT NEW1", valid=True),
            ProcessElementValueString(value="MY TEXT NEW2", valid=True),
        ]
        self.assertEqual(process.element_values.get("EV_STRING"), expected_element_values)

        ProcessUtils.add_element_value_list(process, "EV_STRING", None)
        self.assertEqual(process.element_values.get("EV_STRING"), expected_element_values)

        ProcessUtils.add_element_value_list(process, "EV_STRING", [])
        self.assertEqual(process.element_values.get("EV_STRING"), expected_element_values)

    def test_get_element_value_as_float(self):
        process = prepare_process()

        value = ProcessUtils.get_element_value_as_float(process, "EV_NUMBER")
        self.assertEqual(value, 500)

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_element_value_as_float(process, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_float(self):
        process = prepare_process()

        value = ProcessUtils.find_element_value_as_float(process, "EV_NUMBER")
        self.assertEqual(value, 500)

        value = ProcessUtils.find_element_value_as_float(process, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_float_list(self):
        process = prepare_process()

        value = ProcessUtils.get_element_value_as_float_list(process, "EV_NUMBER")
        self.assertEqual(value, [500, 600])

        value = ProcessUtils.get_element_value_as_float_list(process, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_float(self):
        process = prepare_process()

        ProcessUtils.set_element_value(process, "EV_NUMBER", 700)
        self.assertEqual(
            process.element_values.get("EV_NUMBER"),
            [
                ProcessElementValueNumber(value=700, valid=True),
            ],
        )

        ProcessUtils.set_element_value(process, "EV_NUMBER", None)
        self.assertIsNone(process.element_values.get("EV_NUMBER"))

    def test_set_element_value_as_float_list(self):
        process = prepare_process()

        ProcessUtils.set_element_value_list(process, "EV_NUMBER", [700, 800])
        self.assertEqual(
            process.element_values.get("EV_NUMBER"),
            [
                ProcessElementValueNumber(value=700, valid=True),
                ProcessElementValueNumber(value=800, valid=True),
            ],
        )

        ProcessUtils.set_element_value_list(process, "EV_NUMBER", [])
        self.assertIsNone(process.element_values.get("EV_NUMBER"))

    def test_add_element_value_as_float(self):
        process = prepare_process()

        ProcessUtils.add_element_value(process, "EV_NUMBER", 800)

        expected_element_values = [
            ProcessElementValueNumber(value=500, valid=True),
            ProcessElementValueNumber(value=600, valid=True),
            ProcessElementValueNumber(value=800, valid=True),
        ]
        self.assertEqual(process.element_values.get("EV_NUMBER"), expected_element_values)

        ProcessUtils.add_element_value(process, "EV_NUMBER", None)
        self.assertEqual(process.element_values.get("EV_NUMBER"), expected_element_values)

    def test_add_element_value_as_float_list(self):
        process = prepare_process()

        ProcessUtils.add_element_value_list(process, "EV_NUMBER", [800, 900])

        expected_element_values = [
            ProcessElementValueNumber(value=500, valid=True),
            ProcessElementValueNumber(value=600, valid=True),
            ProcessElementValueNumber(value=800, valid=True),
            ProcessElementValueNumber(value=900, valid=True),
        ]
        self.assertEqual(
            process.element_values.get("EV_NUMBER"),
            expected_element_values,
        )

        ProcessUtils.add_element_value_list(process, "EV_NUMBER", None)
        self.assertEqual(process.element_values.get("EV_NUMBER"), expected_element_values)

        ProcessUtils.add_element_value_list(process, "EV_NUMBER", [])
        self.assertEqual(process.element_values.get("EV_NUMBER"), expected_element_values)

    def test_get_element_value_as_date(self):
        process = prepare_process()

        value = ProcessUtils.get_element_value_as_date(process, "EV_DATE")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_element_value_as_date(process, "OTHER")
        self.assertEqual(str(context.exception), "Value is required!")

    def test_find_element_value_as_date(self):
        process = prepare_process()

        value = ProcessUtils.find_element_value_as_date(process, "EV_DATE")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        value = ProcessUtils.find_element_value_as_date(process, "OTHER")
        self.assertIsNone(value)

    def test_get_element_value_as_date_list(self):
        process = prepare_process()

        value = ProcessUtils.get_element_value_as_date_list(process, "EV_DATE")
        self.assertEqual(value, [date.fromisoformat("2000-01-01"), date.fromisoformat("1980-01-01")])

        value = ProcessUtils.get_element_value_as_date_list(process, "OTHER")
        self.assertEqual(value, [])

    def test_set_element_value_as_date(self):
        process = prepare_process()

        ProcessUtils.set_element_value(process, "EV_DATE", date.fromisoformat("2020-05-05"))
        self.assertEqual(
            process.element_values.get("EV_DATE"),
            [
                ProcessElementValueString(value="2020-05-05", valid=True),
            ],
        )

        ProcessUtils.set_element_value(process, "EV_DATE", None)
        self.assertIsNone(process.element_values.get("EV_DATE"))

    def test_set_element_value_as_date_list(self):
        process = prepare_process()

        ProcessUtils.set_element_value_list(
            process,
            "EV_DATE",
            [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")],
        )
        self.assertEqual(
            process.element_values.get("EV_DATE"),
            [
                ProcessElementValueString(value="2020-05-05", valid=True),
                ProcessElementValueString(value="2020-08-08", valid=True),
            ],
        )

        ProcessUtils.set_element_value_list(process, "EV_DATE", [])
        self.assertIsNone(process.element_values.get("EV_DATE"))

    def test_add_element_value_as_date(self):
        process = prepare_process()

        ProcessUtils.add_element_value(process, "EV_DATE", date.fromisoformat("2020-08-08"))
        expected_element_values = [
            ProcessElementValueString(value="2000-01-01", valid=False),
            ProcessElementValueString(value="1980-01-01", valid=False),
            ProcessElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(process.element_values.get("EV_DATE"), expected_element_values)

        ProcessUtils.add_element_value(process, "EV_DATE", None)
        self.assertEqual(process.element_values.get("EV_DATE"), expected_element_values)

    def test_add_element_value_as_date_list(self):
        process = prepare_process()

        ProcessUtils.add_element_value_list(
            process,
            "EV_DATE",
            [date.fromisoformat("2020-05-05"), date.fromisoformat("2020-08-08")],
        )
        expected_element_values = [
            ProcessElementValueString(value="2000-01-01", valid=False),
            ProcessElementValueString(value="1980-01-01", valid=False),
            ProcessElementValueString(value="2020-05-05", valid=True),
            ProcessElementValueString(value="2020-08-08", valid=True),
        ]
        self.assertEqual(process.element_values.get("EV_DATE"), expected_element_values)

        ProcessUtils.add_element_value_list(process, "EV_DATE", None)
        self.assertEqual(process.element_values.get("EV_DATE"), expected_element_values)

        ProcessUtils.add_element_value_list(process, "EV_DATE", [])
        self.assertEqual(process.element_values.get("EV_DATE"), expected_element_values)

    def test_get_entity_property_as_str(self):
        process = prepare_process_entity()
        value = ProcessUtils.get_entity_property_as_str(process, "key1")
        self.assertEqual(value, "value_key1")

        value = ProcessUtils.get_entity_property_as_str(process, "key2.0.key2_key1.0.key2_key1_key2")
        self.assertEqual(value, "value_key2_key1_key2")

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_entity_property_as_str(process, "key2.0.key2_key1.0.unknown")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_entity_property_as_str(process, "key2.0.key2_key1.10")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_entity_property_as_str(process, "key2.0.key2_key1.100.key2_key1_key2")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

    def test_find_entity_property_as_str(self):
        process = prepare_process_entity()

        value = ProcessUtils.find_entity_property_as_str(process, "key1")
        self.assertEqual(value, "value_key1")

        value = ProcessUtils.find_entity_property_as_str(process, "key2.0.key2_key1.0.key2_key1_key2")
        self.assertEqual(value, "value_key2_key1_key2")

        value = ProcessUtils.find_entity_property_as_str(process, "key2.0.key2_key1.0.unknown")
        self.assertIsNone(value)

        value = ProcessUtils.find_entity_property_as_str(process, "key2.0.key2_key1.10")
        self.assertIsNone(value)

        value = ProcessUtils.find_entity_property_as_str(process, "key2.0.key2_key1.100.key2_key1_key2")
        self.assertIsNone(value)

    def test_get_entity_property_as_int(self):
        process = prepare_process_entity()

        value = ProcessUtils.get_entity_property_as_int(process, "key3.0")
        self.assertEqual(value, 500)

        value = ProcessUtils.get_entity_property_as_int(process, "key3.1")
        self.assertEqual(value, 1000)

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_entity_property_as_int(process, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_entity_property_as_int(process, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a int")

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_entity_property_as_int(process, "key3.2")
        self.assertEqual(str(context.exception), "Property key3.2 is not a int")

    def test_find_entity_property_as_int(self):
        process = prepare_process_entity()

        value = ProcessUtils.find_entity_property_as_int(process, "key3.0")
        self.assertEqual(value, 500)

        value = ProcessUtils.find_entity_property_as_int(process, "key3.1")
        self.assertEqual(value, 1000)

        value = ProcessUtils.find_entity_property_as_int(process, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as context:
            ProcessUtils.find_entity_property_as_int(process, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a int")

        with self.assertRaises(ValueError) as context:
            ProcessUtils.find_entity_property_as_int(process, "key3.2")
        self.assertEqual(str(context.exception), "Property key3.2 is not a int")

    def test_get_entity_property_as_float(self):
        process = prepare_process_entity()

        value = ProcessUtils.get_entity_property_as_float(process, "key3.0")
        self.assertEqual(value, 500)

        value = ProcessUtils.get_entity_property_as_float(process, "key3.1")
        self.assertEqual(value, 1000)

        value = ProcessUtils.get_entity_property_as_float(process, "key3.2")
        self.assertEqual(value, 2000.1)

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_entity_property_as_float(process, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            ProcessUtils.get_entity_property_as_float(process, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a float")

    def test_find_entity_property_as_float(self):
        process = prepare_process_entity()

        value = ProcessUtils.find_entity_property_as_float(process, "key3.0")
        self.assertEqual(value, 500)

        value = ProcessUtils.find_entity_property_as_float(process, "key3.1")
        self.assertEqual(value, 1000)

        value = ProcessUtils.find_entity_property_as_float(process, "key3.2")
        self.assertEqual(value, 2000.1)

        value = ProcessUtils.find_entity_property_as_float(process, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as context:
            ProcessUtils.find_entity_property_as_float(process, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a float")

    def test_get_entity_property_as_date(self):
        process = prepare_process_entity()

        value = ProcessUtils.get_entity_property_as_date(process, "key5.0")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.get_entity_property_as_date(process, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.get_entity_property_as_date(process, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_find_entity_property_as_date(self):
        process = prepare_process_entity()

        value = ProcessUtils.find_entity_property_as_date(process, "key5.0")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        value = ProcessUtils.find_entity_property_as_date(process, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.find_entity_property_as_date(process, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_get_entity_property_as_datetime(self):
        process = prepare_process_entity()

        value = ProcessUtils.get_entity_property_as_datetime(process, "key5.1")
        self.assertEqual(value, datetime.fromisoformat("2000-01-01T10:10:05+01:00"))

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.get_entity_property_as_datetime(process, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.get_entity_property_as_datetime(process, "key1")
        self.assertEqual(
            str(cm.exception),
            "Property key1 is not a date-time following ISO 8601 format",
        )

    def test_find_entity_property_as_datetime(self):
        process = prepare_process_entity()

        value = ProcessUtils.find_entity_property_as_datetime(process, "key5.1")
        self.assertEqual(value, datetime.fromisoformat("2000-01-01T10:10:05+01:00"))

        value = ProcessUtils.find_entity_property_as_datetime(process, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.find_entity_property_as_datetime(process, "key1")
        self.assertEqual(
            str(cm.exception),
            "Property key1 is not a date-time following ISO 8601 format",
        )

    def test_get_entity_property_as_file(self):
        process = prepare_process_entity()

        value = ProcessUtils.get_entity_property_as_file(process, "key6")
        self.assertEqual(value.uri, "xxx-yyy-zzz")
        self.assertEqual(value.type, "application/pdf")
        self.assertEqual(value.name, "dummy.pdf")
        self.assertEqual(value.size, 500)

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.get_entity_property_as_file(process, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.get_entity_property_as_file(process, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a file")

    def test_find_entity_property_as_file(self):
        process = prepare_process_entity()

        value = ProcessUtils.find_entity_property_as_file(process, "key6")
        self.assertEqual(value.uri, "xxx-yyy-zzz")
        self.assertEqual(value.type, "application/pdf")
        self.assertEqual(value.name, "dummy.pdf")
        self.assertEqual(value.size, 500)

        value = ProcessUtils.find_entity_property_as_file(process, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.find_entity_property_as_file(process, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a file")

    def test_get_entity_property_as_principal(self):
        process = prepare_process_entity()

        value = ProcessUtils.get_entity_property_as_principal(process, "key7")
        self.assertEqual(value.id, "xxx-yyy-zzz")
        self.assertEqual(value.type, "USER")
        self.assertEqual(value.name, "Homer Simpson")

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.get_entity_property_as_principal(process, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.get_entity_property_as_principal(process, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a principal")

    def test_find_entity_property_as_principal(self):
        process = prepare_process_entity()

        value = ProcessUtils.find_entity_property_as_principal(process, "key7")
        self.assertEqual(value.id, "xxx-yyy-zzz")
        self.assertEqual(value.type, "USER")
        self.assertEqual(value.name, "Homer Simpson")

        value = ProcessUtils.find_entity_property_as_principal(process, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            ProcessUtils.find_entity_property_as_principal(process, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a principal")

    def test_get_entity_property_as_list(self):
        process = prepare_process_entity()

        value = ProcessUtils.get_entity_property_as_list(process, "key3")
        self.assertEqual(value, [500, "1000", 2000.1])

        with self.assertRaises(Exception) as context:
            ProcessUtils.get_entity_property_as_list(process, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(Exception) as context:
            ProcessUtils.get_entity_property_as_list(process, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a list")

    def test_find_entity_property_as_list(self):
        process = prepare_process_entity()

        value1 = ProcessUtils.find_entity_property_as_list(process, "key3")
        self.assertEqual(value1, [500, "1000", 2000.1])

        value = ProcessUtils.find_entity_property_as_list(process, "key_xxxxxxx")
        self.assertIsNone(value)

    def test_get_entity_property_as_dict(self):
        process = prepare_process_entity()

        value = ProcessUtils.get_entity_property_as_dict(process, "key2.0.key2_key1.0")
        self.assertEqual(
            value,
            {
                "key2_key1_key1": 0,
                "key2_key1_key2": "value_key2_key1_key2",
            },
        )

        with self.assertRaises(Exception) as context:
            ProcessUtils.get_entity_property_as_dict(process, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(Exception) as context:
            ProcessUtils.get_entity_property_as_dict(process, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a dict")

    def test_find_entity_property_as_dict(self):
        process = prepare_process_entity()

        value = ProcessUtils.find_entity_property_as_dict(process, "key2.0.key2_key1.0")
        self.assertEqual(
            value,
            {
                "key2_key1_key1": 0,
                "key2_key1_key2": "value_key2_key1_key2",
            },
        )

        value = ProcessUtils.find_entity_property_as_dict(process, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(Exception) as context:
            ProcessUtils.find_entity_property_as_dict(process, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a dict")


def prepare_process() -> Process:
    return Process(
        id="3b755d5e-b64f-4ec2-a830-173f006bdf8e",
        process_definition=ProcessDefinitionSummary(
            id="e68d8136-1166-455c-93d6-d106201c1856",
        ),
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


def prepare_process_entity() -> Process:
    return Process(
        id="3b755d5e-b64f-4ec2-a830-173f006bdf8e",
        process_definition=ProcessDefinitionSummary(
            id="e68d8136-1166-455c-93d6-d106201c1856",
        ),
        entity=JsonFormsValue(
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
