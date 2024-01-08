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

from kuflow_rest.models import JsonFormsFile, JsonFormsPrincipal, PrincipalType
from kuflow_temporal_activity_kuflow.models import SaveTaskJsonFormsValueDataRequest
from kuflow_temporal_activity_kuflow.utils import SaveTaskJsonFormsValueDataRequestUtils


class SaveTaskJsonFormsValueDataRequestUtilsTest(unittest.TestCase):
    def test_get_json_forms_property_as_str(self):
        request = prepare_save_task_json_forms_value_data_request()
        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_str(request, "key1")
        self.assertEqual(value, "value_key1")

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_str(
            request, "key2.0.key2_key1.0.key2_key1_key2"
        )
        self.assertEqual(value, "value_key2_key1_key2")

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_str(request, "key2.0.key2_key1.0.unknown")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_str(request, "key2.0.key2_key1.10")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_str(
                request, "key2.0.key2_key1.100.key2_key1_key2"
            )
        self.assertEqual(str(context.exception), "Property value doesn't exist")

    def test_find_json_forms_property_as_str(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_str(request, "key1")
        self.assertEqual(value, "value_key1")

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_str(
            request, "key2.0.key2_key1.0.key2_key1_key2"
        )
        self.assertEqual(value, "value_key2_key1_key2")

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_str(
            request, "key2.0.key2_key1.0.unknown"
        )
        self.assertIsNone(value)

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_str(request, "key2.0.key2_key1.10")
        self.assertIsNone(value)

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_str(
            request, "key2.0.key2_key1.100.key2_key1_key2"
        )
        self.assertIsNone(value)

    def test_get_json_forms_property_as_int(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_int(request, "key3.0")
        self.assertEqual(value, 500)

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_int(request, "key3.1")
        self.assertEqual(value, 1000)

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_int(request, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_int(request, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a int")

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_int(request, "key3.2")
        self.assertEqual(str(context.exception), "Property key3.2 is not a int")

    def test_find_json_forms_property_as_int(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_int(request, "key3.0")
        self.assertEqual(value, 500)

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_int(request, "key3.1")
        self.assertEqual(value, 1000)

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_int(request, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_int(request, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a int")

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_int(request, "key3.2")
        self.assertEqual(str(context.exception), "Property key3.2 is not a int")

    def test_get_json_forms_property_as_float(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_float(request, "key3.0")
        self.assertEqual(value, 500)

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_float(request, "key3.1")
        self.assertEqual(value, 1000)

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_float(request, "key3.2")
        self.assertEqual(value, 2000.1)

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_float(request, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_float(request, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a float")

    def test_find_json_forms_property_as_float(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_float(request, "key3.0")
        self.assertEqual(value, 500)

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_float(request, "key3.1")
        self.assertEqual(value, 1000)

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_float(request, "key3.2")
        self.assertEqual(value, 2000.1)

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_float(request, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as context:
            SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_float(request, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a float")

    def test_get_json_forms_property_as_date(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_date(request, "key5.0")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_date(request, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_date(request, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_find_json_forms_property_as_date(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_date(request, "key5.0")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_date(request, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_date(request, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_get_json_forms_property_as_datetime(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_datetime(request, "key5.1")
        self.assertEqual(value, datetime.fromisoformat("2000-01-01T10:10:05+01:00"))

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_datetime(request, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_datetime(request, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date-time following ISO 8601 format")

    def test_find_json_forms_property_as_datetime(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_datetime(request, "key5.1")
        self.assertEqual(value, datetime.fromisoformat("2000-01-01T10:10:05+01:00"))

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_datetime(request, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_datetime(request, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date-time following ISO 8601 format")

    def test_get_json_forms_property_as_file(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_file(request, "key6")
        self.assertEqual(value.uri, "xxx-yyy-zzz")
        self.assertEqual(value.type, "application/pdf")
        self.assertEqual(value.name, "dummy.pdf")
        self.assertEqual(value.size, 500)

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_file(request, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_file(request, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a file")

    def test_find_json_forms_property_as_file(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_file(request, "key6")
        self.assertEqual(value.uri, "xxx-yyy-zzz")
        self.assertEqual(value.type, "application/pdf")
        self.assertEqual(value.name, "dummy.pdf")
        self.assertEqual(value.size, 500)

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_file(request, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_file(request, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a file")

    def test_get_json_forms_property_as_principal(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_principal(request, "key7")
        self.assertEqual(value.id, "xxx-yyy-zzz")
        self.assertEqual(value.type, "USER")
        self.assertEqual(value.name, "Homer Simpson")

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_principal(request, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_principal(request, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a principal")

    def test_find_json_forms_property_as_principal(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_principal(request, "key7")
        self.assertEqual(value.id, "xxx-yyy-zzz")
        self.assertEqual(value.type, "USER")
        self.assertEqual(value.name, "Homer Simpson")

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_principal(request, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_principal(request, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a principal")

    def test_get_json_forms_property_as_list(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_list(request, "key3")
        self.assertEqual(value, [500, "1000", 2000.1])

        with self.assertRaises(Exception) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_list(request, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(Exception) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_list(request, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a list")

    def test_find_json_forms_property_as_list(self):
        request = prepare_save_task_json_forms_value_data_request()

        value1 = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_list(request, "key3")
        self.assertEqual(value1, [500, "1000", 2000.1])

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_list(request, "key_xxxxxxx")
        self.assertIsNone(value)

    def test_get_json_forms_property_as_dict(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_dict(request, "key2.0.key2_key1.0")
        self.assertEqual(
            value,
            {
                "key2_key1_key1": 0,
                "key2_key1_key2": "value_key2_key1_key2",
            },
        )

        with self.assertRaises(Exception) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_dict(request, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(Exception) as context:
            SaveTaskJsonFormsValueDataRequestUtils.get_json_forms_property_as_dict(request, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a dict")

    def test_find_json_forms_property_as_dict(self):
        request = prepare_save_task_json_forms_value_data_request()

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_dict(request, "key2.0.key2_key1.0")
        self.assertEqual(
            value,
            {
                "key2_key1_key1": 0,
                "key2_key1_key2": "value_key2_key1_key2",
            },
        )

        value = SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_dict(request, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(Exception) as context:
            SaveTaskJsonFormsValueDataRequestUtils.find_json_forms_property_as_dict(request, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a dict")

    def test_update_json_forms_property(self):
        request = prepare_save_task_json_forms_value_data_request()
        request.data = None

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

        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key1", "text")
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key2.0.key1", True)
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(
            request, "key2.0.key2", date.fromisoformat("2020-01-01")
        )
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key2.1.key1", False)
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(
            request, "key2.1.key2", date.fromisoformat("3030-01-01")
        )
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key2.2.key1", False)
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(
            request, "key2.2.key2", datetime.fromisoformat("3030-01-01T10:10:00+01:00")
        )
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key3", 100)
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key4", file)
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key5", principal)

        self.assertEqual(
            request.data,
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

        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key1", None)
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key2.0", None)
        SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key2.0.key1", None)

        self.assertEqual(
            request.data,
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
            SaveTaskJsonFormsValueDataRequestUtils.update_json_forms_property(request, "key2.100.key1", None)
        self.assertEqual(str(context.exception), "Property key2.100.key1 doesn't exist")


def prepare_save_task_json_forms_value_data_request() -> SaveTaskJsonFormsValueDataRequest:
    return SaveTaskJsonFormsValueDataRequest(
        task_id="xxx-yyy-zzz",
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
    )


if __name__ == "__main__":
    unittest.main()
