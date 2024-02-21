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
    Principal,
    PrincipalType,
    PrincipalUser,
    TenantUser,
    TenantUserMetadata,
)
from kuflow_rest.utils import TenantUserUtils


class TenantUserUtilsTest(unittest.TestCase):
    def test_get_metadata_property_as_str(self):
        tenant_user = prepare_tenant_user()
        value = TenantUserUtils.get_metadata_property_as_str(tenant_user, "key1")
        self.assertEqual(value, "value_key1")

        value = TenantUserUtils.get_metadata_property_as_str(tenant_user, "key2.0.key2_key1.0.key2_key1_key2")
        self.assertEqual(value, "value_key2_key1_key2")

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.get_metadata_property_as_str(tenant_user, "key2.0.key2_key1.0.unknown")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.get_metadata_property_as_str(tenant_user, "key2.0.key2_key1.10")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.get_metadata_property_as_str(tenant_user, "key2.0.key2_key1.100.key2_key1_key2")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

    def test_find_json_forms_property_as_str(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.find_metadata_property_as_str(tenant_user, "key1")
        self.assertEqual(value, "value_key1")

        value = TenantUserUtils.find_metadata_property_as_str(tenant_user, "key2.0.key2_key1.0.key2_key1_key2")
        self.assertEqual(value, "value_key2_key1_key2")

        value = TenantUserUtils.find_metadata_property_as_str(tenant_user, "key2.0.key2_key1.0.unknown")
        self.assertIsNone(value)

        value = TenantUserUtils.find_metadata_property_as_str(tenant_user, "key2.0.key2_key1.10")
        self.assertIsNone(value)

        value = TenantUserUtils.find_metadata_property_as_str(tenant_user, "key2.0.key2_key1.100.key2_key1_key2")
        self.assertIsNone(value)

    def test_get_metadata_property_as_int(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.get_metadata_property_as_int(tenant_user, "key3.0")
        self.assertEqual(value, 500)

        value = TenantUserUtils.get_metadata_property_as_int(tenant_user, "key3.1")
        self.assertEqual(value, 1000)

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.get_metadata_property_as_int(tenant_user, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.get_metadata_property_as_int(tenant_user, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a int")

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.get_metadata_property_as_int(tenant_user, "key3.2")
        self.assertEqual(str(context.exception), "Property key3.2 is not a int")

    def test_find_json_forms_property_as_int(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.find_metadata_property_as_int(tenant_user, "key3.0")
        self.assertEqual(value, 500)

        value = TenantUserUtils.find_metadata_property_as_int(tenant_user, "key3.1")
        self.assertEqual(value, 1000)

        value = TenantUserUtils.find_metadata_property_as_int(tenant_user, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.find_metadata_property_as_int(tenant_user, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a int")

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.find_metadata_property_as_int(tenant_user, "key3.2")
        self.assertEqual(str(context.exception), "Property key3.2 is not a int")

    def test_get_metadata_property_as_float(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.get_metadata_property_as_float(tenant_user, "key3.0")
        self.assertEqual(value, 500)

        value = TenantUserUtils.get_metadata_property_as_float(tenant_user, "key3.1")
        self.assertEqual(value, 1000)

        value = TenantUserUtils.get_metadata_property_as_float(tenant_user, "key3.2")
        self.assertEqual(value, 2000.1)

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.get_metadata_property_as_float(tenant_user, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.get_metadata_property_as_float(tenant_user, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a float")

    def test_find_json_forms_property_as_float(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.find_metadata_property_as_float(tenant_user, "key3.0")
        self.assertEqual(value, 500)

        value = TenantUserUtils.find_metadata_property_as_float(tenant_user, "key3.1")
        self.assertEqual(value, 1000)

        value = TenantUserUtils.find_metadata_property_as_float(tenant_user, "key3.2")
        self.assertEqual(value, 2000.1)

        value = TenantUserUtils.find_metadata_property_as_float(tenant_user, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as context:
            TenantUserUtils.find_metadata_property_as_float(tenant_user, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a float")

    def test_get_metadata_property_as_date(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.get_metadata_property_as_date(tenant_user, "key5.0")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.get_metadata_property_as_date(tenant_user, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.get_metadata_property_as_date(tenant_user, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_find_json_forms_property_as_date(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.find_metadata_property_as_date(tenant_user, "key5.0")
        self.assertEqual(value, date.fromisoformat("2000-01-01"))

        value = TenantUserUtils.find_metadata_property_as_date(tenant_user, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.find_metadata_property_as_date(tenant_user, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a date following ISO 8601 format")

    def test_get_metadata_property_as_datetime(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.get_metadata_property_as_datetime(tenant_user, "key5.1")
        self.assertEqual(value, datetime.fromisoformat("2000-01-01T10:10:05+01:00"))

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.get_metadata_property_as_datetime(tenant_user, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.get_metadata_property_as_datetime(tenant_user, "key1")
        self.assertEqual(
            str(cm.exception),
            "Property key1 is not a date-time following ISO 8601 format",
        )

    def test_find_json_forms_property_as_datetime(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.find_metadata_property_as_datetime(tenant_user, "key5.1")
        self.assertEqual(value, datetime.fromisoformat("2000-01-01T10:10:05+01:00"))

        value = TenantUserUtils.find_metadata_property_as_datetime(tenant_user, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.find_metadata_property_as_datetime(tenant_user, "key1")
        self.assertEqual(
            str(cm.exception),
            "Property key1 is not a date-time following ISO 8601 format",
        )

    def test_get_metadata_property_as_file(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.get_metadata_property_as_file(tenant_user, "key6")
        self.assertEqual(value.uri, "xxx-yyy-zzz")
        self.assertEqual(value.type, "application/pdf")
        self.assertEqual(value.name, "dummy.pdf")
        self.assertEqual(value.size, 500)

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.get_metadata_property_as_file(tenant_user, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.get_metadata_property_as_file(tenant_user, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a file")

    def test_find_json_forms_property_as_file(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.find_metadata_property_as_file(tenant_user, "key6")
        self.assertEqual(value.uri, "xxx-yyy-zzz")
        self.assertEqual(value.type, "application/pdf")
        self.assertEqual(value.name, "dummy.pdf")
        self.assertEqual(value.size, 500)

        value = TenantUserUtils.find_metadata_property_as_file(tenant_user, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.find_metadata_property_as_file(tenant_user, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a file")

    def test_get_metadata_property_as_principal(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.get_metadata_property_as_principal(tenant_user, "key7")
        self.assertEqual(value.id, "xxx-yyy-zzz")
        self.assertEqual(value.type, "USER")
        self.assertEqual(value.name, "Homer Simpson")

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.get_metadata_property_as_principal(tenant_user, "key_xxxxxxx")
        self.assertEqual(str(cm.exception), "Property value doesn't exist")

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.get_metadata_property_as_principal(tenant_user, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a principal")

    def test_find_json_forms_property_as_principal(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.find_metadata_property_as_principal(tenant_user, "key7")
        self.assertEqual(value.id, "xxx-yyy-zzz")
        self.assertEqual(value.type, "USER")
        self.assertEqual(value.name, "Homer Simpson")

        value = TenantUserUtils.find_metadata_property_as_principal(tenant_user, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(ValueError) as cm:
            TenantUserUtils.find_metadata_property_as_principal(tenant_user, "key1")
        self.assertEqual(str(cm.exception), "Property key1 is not a principal")

    def test_get_metadata_property_as_list(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.get_metadata_property_as_list(tenant_user, "key3")
        self.assertEqual(value, [500, "1000", 2000.1])

        with self.assertRaises(Exception) as context:
            TenantUserUtils.get_metadata_property_as_list(tenant_user, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(Exception) as context:
            TenantUserUtils.get_metadata_property_as_list(tenant_user, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a list")

    def test_find_json_forms_property_as_list(self):
        tenant_user = prepare_tenant_user()

        value1 = TenantUserUtils.find_metadata_property_as_list(tenant_user, "key3")
        self.assertEqual(value1, [500, "1000", 2000.1])

        value = TenantUserUtils.find_metadata_property_as_list(tenant_user, "key_xxxxxxx")
        self.assertIsNone(value)

    def test_get_metadata_property_as_dict(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.get_metadata_property_as_dict(tenant_user, "key2.0.key2_key1.0")
        self.assertEqual(
            value,
            {
                "key2_key1_key1": 0,
                "key2_key1_key2": "value_key2_key1_key2",
            },
        )

        with self.assertRaises(Exception) as context:
            TenantUserUtils.get_metadata_property_as_dict(tenant_user, "key_xxxxxxx")
        self.assertEqual(str(context.exception), "Property value doesn't exist")

        with self.assertRaises(Exception) as context:
            TenantUserUtils.get_metadata_property_as_dict(tenant_user, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a dict")

    def test_find_json_forms_property_as_dict(self):
        tenant_user = prepare_tenant_user()

        value = TenantUserUtils.find_metadata_property_as_dict(tenant_user, "key2.0.key2_key1.0")
        self.assertEqual(
            value,
            {
                "key2_key1_key1": 0,
                "key2_key1_key2": "value_key2_key1_key2",
            },
        )

        value = TenantUserUtils.find_metadata_property_as_dict(tenant_user, "key_xxxxxxx")
        self.assertIsNone(value)

        with self.assertRaises(Exception) as context:
            TenantUserUtils.find_metadata_property_as_dict(tenant_user, "key1")
        self.assertEqual(str(context.exception), "Property key1 is not a dict")

    def test_update_metadata_property(self):
        tenant_user = prepare_tenant_user()
        tenant_user.metadata = TenantUserMetadata(valid=False, value={})

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

        TenantUserUtils.update_metadata_property(tenant_user, "key1", "text")
        TenantUserUtils.update_metadata_property(tenant_user, "key2.0.key1", True)
        TenantUserUtils.update_metadata_property(tenant_user, "key2.0.key2", date.fromisoformat("2020-01-01"))
        TenantUserUtils.update_metadata_property(tenant_user, "key2.1.key1", False)
        TenantUserUtils.update_metadata_property(tenant_user, "key2.1.key2", date.fromisoformat("3030-01-01"))
        TenantUserUtils.update_metadata_property(tenant_user, "key2.2.key1", False)
        TenantUserUtils.update_metadata_property(
            tenant_user,
            "key2.2.key2",
            datetime.fromisoformat("3030-01-01T10:10:00+01:00"),
        )
        TenantUserUtils.update_metadata_property(tenant_user, "key3", 100)
        TenantUserUtils.update_metadata_property(tenant_user, "key4", file)
        TenantUserUtils.update_metadata_property(tenant_user, "key5", principal)

        self.assertEqual(
            tenant_user.metadata.value,
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

        TenantUserUtils.update_metadata_property(tenant_user, "key1", None)
        TenantUserUtils.update_metadata_property(tenant_user, "key2.0", None)
        TenantUserUtils.update_metadata_property(tenant_user, "key2.0.key1", None)

        self.assertEqual(
            tenant_user.metadata.value,
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
            TenantUserUtils.update_metadata_property(tenant_user, "key2.100.key1", None)
        self.assertEqual(str(context.exception), "Property key2.100.key1 doesn't exist")


def prepare_tenant_user() -> TenantUser:
    return TenantUser(
        id="43aff41f-e279-4865-ad6e-927feaed749f",
        principal=Principal(
            id="78efd6c5-c730-40cb-a809-a7b183ab5904",
            type=PrincipalType.USER,
            name="First name Last name",
            user=PrincipalUser(
                id="cdca37a5-5403-41d7-98da-bf8e5ce06ed0",
                email="test@test.com",
            ),
        ),
        metadata=TenantUserMetadata(
            valid=True,
            value={
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
