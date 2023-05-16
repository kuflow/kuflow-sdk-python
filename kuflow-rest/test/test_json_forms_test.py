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
)
from kuflow_rest.utils import (
    get_json_forms_property_as_str,
    find_json_forms_property_as_str,
    get_json_forms_property_as_int,
    find_json_forms_property_as_int,
    get_json_forms_property_as_float,
    find_json_forms_property_as_float,
    get_json_forms_property_as_date,
    find_json_forms_property_as_date,
    get_json_forms_property_as_datetime,
    find_json_forms_property_as_datetime,
    get_json_forms_property_as_json_forms_file,
    find_json_forms_property_as_json_forms_file,
    get_json_forms_property_as_json_forms_principal,
    find_json_forms_property_as_json_forms_principal,
    get_json_forms_property_as_list,
    find_json_forms_property_as_list,
    get_json_forms_property_as_dict,
    find_json_forms_property_as_dict,
    update_json_forms_property,
)


class JsonFormsValueUtils(unittest.TestCase):
    def test_get_json_forms_property_as_str(self):
        task = prepare_task()
        value = get_json_forms_property_as_str(task, "key1")
        self.assertEqual(value, "value_key1")

        value = get_json_forms_property_as_str(task, "key2.key2_key1.0.key2_key1_key2")
        self.assertEqual(value, "value_key2_key1_key2")

        with self.assertRaises(ValueError) as context:
            get_json_forms_property_as_str(task, "key2.key2_key1.0.unknown")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            get_json_forms_property_as_str(task, "key2.key2_key1.10")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            get_json_forms_property_as_str(task, "key2.key2_key1.100.key2_key1_key2")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

    def test_find_json_forms_property_as_str(self):
        task = prepare_task()

        value = find_json_forms_property_as_str(task, "key1")
        self.assertEqual(value, "value_key1")

        value = find_json_forms_property_as_str(task, "key2.key2_key1.0.key2_key1_key2")
        self.assertEqual(value, "value_key2_key1_key2")

        value = find_json_forms_property_as_str(task, "key2.key2_key1.0.unknown")
        self.assertIsNone(value)

        value = find_json_forms_property_as_str(task, "key2.key2_key1.10")
        self.assertIsNone(value)

        value = find_json_forms_property_as_str(task, "key2.key2_key1.100.key2_key1_key2")
        self.assertIsNone(value)

    def test_get_json_forms_property_as_int(self):
        task = prepare_task()

        value = get_json_forms_property_as_int(task, "key3.0")
        self.assertEqual(value, 500)

        value = get_json_forms_property_as_int(task, "key3.1")
        self.assertEqual(value, 1000)

        with self.assertRaises(ValueError) as context:
            get_json_forms_property_as_int(task, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            get_json_forms_property_as_int(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a int")

        with self.assertRaises(ValueError) as context:
            get_json_forms_property_as_int(task, "key3.2")
        self.assertEqual(str(context.exception), "Property key3.2 is not a int")

    def test_find_json_forms_property_as_int(self):
        task = prepare_task()

        value = find_json_forms_property_as_int(task, "key3.0")
        self.assertEqual(value, 500)

        value = find_json_forms_property_as_int(task, "key3.1")
        self.assertEqual(value, 1000)

        value = find_json_forms_property_as_int(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as context:
            find_json_forms_property_as_int(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a int")

        with self.assertRaises(ValueError) as context:
            find_json_forms_property_as_int(task, "key3.2")
        self.assertEqual(str(context.exception), "Property key3.2 is not a int")

    def test_get_json_forms_property_as_float(self):
        task = prepare_task()

        value = get_json_forms_property_as_float(task, "key3.0")
        self.assertEqual(value, 500)

        value = get_json_forms_property_as_float(task, "key3.1")
        self.assertEqual(value, 1000)

        value = get_json_forms_property_as_float(task, "key3.2")
        self.assertEqual(value, 2000.1)

        with self.assertRaises(ValueError) as context:
            get_json_forms_property_as_float(task, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            get_json_forms_property_as_float(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a float")

    def test_find_json_forms_property_as_float(self):
        task = prepare_task()

        value = find_json_forms_property_as_float(task, "key3.0")
        self.assertEqual(value, 500)

        value = find_json_forms_property_as_float(task, "key3.1")
        self.assertEqual(value, 1000)

        value = find_json_forms_property_as_float(task, "key3.2")
        self.assertEqual(value, 2000.1)

        value = find_json_forms_property_as_float(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as context:
            find_json_forms_property_as_float(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a float")

    def test_get_json_forms_property_as_date(self):
        task = prepare_task()

        value = get_json_forms_property_as_date(task, "key5.0")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        with self.assertRaises(ValueError) as cm:
            get_json_forms_property_as_date(task, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            get_json_forms_property_as_date(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_find_json_forms_property_as_date(self):
        task = prepare_task()

        value = find_json_forms_property_as_date(task, "key5.0")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        value = find_json_forms_property_as_date(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            find_json_forms_property_as_date(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_get_json_forms_property_as_datetime(self):
        task = prepare_task()

        value = get_json_forms_property_as_datetime(task, "key5.1")
        self.assertEqual(value, datetime.fromisoformat("2000-01-01T10:10:05+01:00"))

        with self.assertRaises(ValueError) as cm:
            get_json_forms_property_as_datetime(task, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            get_json_forms_property_as_datetime(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date-time following ISO 8601 format")

    def test_find_json_forms_property_as_datetime(self):
        task = prepare_task()

        value = find_json_forms_property_as_datetime(task, "key5.1")
        self.assertEqual(value, date.fromisoformat("2000-01-01T10:10:05+01:00"))

        value = find_json_forms_property_as_datetime(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            find_json_forms_property_as_datetime(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_get_json_forms_property_as_json_forms_file(self):
        task = prepare_task()

        value = get_json_forms_property_as_json_forms_file(task, "key6")
        self.assertEqual(value.uri, "xxx-yyy-zzz")
        self.assertEqual(value.type, "application/pdf")
        self.assertEqual(value.name, "dummy.pdf")
        self.assertEqual(value.size, 500)

        with self.assertRaises(ValueError) as cm:
            get_json_forms_property_as_json_forms_file(task, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            get_json_forms_property_as_json_forms_file(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a file")

    def test_find_json_forms_property_as_json_forms_file(self):
        task = prepare_task()

        value = find_json_forms_property_as_json_forms_file(task, "key6")
        self.assertEqual(value.uri, "xxx-yyy-zzz")
        self.assertEqual(value.type, "application/pdf")
        self.assertEqual(value.name, "dummy.pdf")
        self.assertEqual(value.size, 500)

        value = find_json_forms_property_as_json_forms_file(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            find_json_forms_property_as_json_forms_file(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a file")

    def test_get_json_forms_property_as_json_forms_principal(self):
        task = prepare_task()

        value = get_json_forms_property_as_json_forms_principal(task, "key7")
        self.assertEqual(value.id, "xxx-yyy-zzz")
        self.assertEqual(value.type, "USER")
        self.assertEqual(value.name, "Homer Simpson")

        with self.assertRaises(ValueError) as cm:
            get_json_forms_property_as_json_forms_principal(task, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            get_json_forms_property_as_json_forms_principal(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a principal")

    def test_find_json_forms_property_as_json_forms_principal(self):
        task = prepare_task()

        value = find_json_forms_property_as_json_forms_principal(task, "key7")
        self.assertEqual(value.id, "xxx-yyy-zzz")
        self.assertEqual(value.type, "USER")
        self.assertEqual(value.name, "Homer Simpson")

        value = find_json_forms_property_as_json_forms_principal(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            find_json_forms_property_as_json_forms_principal(task, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a principal")

    def test_get_json_forms_property_as_list(self):
        task = prepare_task()

        value = get_json_forms_property_as_list(task, "key3")
        self.assertEqual(value, [500, "1000", 2000.1])

        with self.assertRaises(Exception) as context:
            get_json_forms_property_as_list(task, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(Exception) as context:
            get_json_forms_property_as_list(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a list")

    def test_find_json_forms_property_as_list(self):
        task = prepare_task()

        value1 = find_json_forms_property_as_list(task, "key3")
        self.assertEqual(value1, [500, "1000", 2000.1])

        value = find_json_forms_property_as_list(task, "key_xxxxxxx")
        self.assertIsNone(value)

    def test_get_json_forms_property_as_dict(self):
        task = prepare_task()

        value = get_json_forms_property_as_dict(task, "key2.key2_key1.0")
        self.assertEqual(
            value,
            {
                "key2_key1_key1": 0,
                "key2_key1_key2": "value_key2_key1_key2",
            },
        )

        with self.assertRaises(Exception) as context:
            get_json_forms_property_as_dict(task, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(Exception) as context:
            get_json_forms_property_as_dict(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a dict")

    def test_find_json_forms_property_as_dict(self):
        task = prepare_task()

        value = find_json_forms_property_as_dict(task, "key2.key2_key1.0")
        self.assertEqual(
            value,
            {
                "key2_key1_key1": 0,
                "key2_key1_key2": "value_key2_key1_key2",
            },
        )

        value = find_json_forms_property_as_dict(task, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(Exception) as context:
            find_json_forms_property_as_dict(task, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a dict")

    def test_update_json_forms_property(self):
        task = prepare_task()
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

        update_json_forms_property(task, "key1", "text")
        update_json_forms_property(task, "key2.0.key1", True)
        update_json_forms_property(task, "key2.0.key2", date.fromisoformat("2020-01-01"))
        update_json_forms_property(task, "key2.1.key1", False)
        update_json_forms_property(task, "key2.1.key2", date.fromisoformat("3030-01-01"))
        update_json_forms_property(task, "key2.2.key1", False)
        update_json_forms_property(task, "key2.2.key2", datetime.fromisoformat("3030-01-01T10:10:00+01:00"))
        update_json_forms_property(task, "key3", 100)
        update_json_forms_property(task, "key4", file)
        update_json_forms_property(task, "key5", principal)

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

        update_json_forms_property(task, "key1", None)
        update_json_forms_property(task, "key2.0", None)
        update_json_forms_property(task, "key2.0.key1", None)

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
            update_json_forms_property(task, "key2.100.key1", None)
        self.assertEqual(str(context.exception), "Property key2.100.key1 doesn't exist")


def prepare_task() -> Task:
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
