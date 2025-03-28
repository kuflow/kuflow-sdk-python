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

from kuflow_rest.utils import generate_kuflow_principal_string, parse_kuflow_file, parse_kuflow_principal


class UtilsParserTest(unittest.TestCase):
    def test_parse_kuflow_file_ok(self):
        kuflow_file = parse_kuflow_file(
            "kuflow-file:"
            "uri=ku:dummy/xxx-ssss-yyyy;"
            "type=application/pdf;"
            "size=11111;"
            "name=dummy.pdf;"
            "original-name=original-name.pdf;"
        )
        self.assertEqual(kuflow_file.uri, "ku:dummy/xxx-ssss-yyyy")
        self.assertEqual(kuflow_file.type, "application/pdf")
        self.assertEqual(kuflow_file.size, 11111)
        self.assertEqual(kuflow_file.name, "dummy.pdf")
        self.assertEqual(kuflow_file.original_name, "original-name.pdf")

    def test_parse_kuflow_file_ok_optional(self):
        kuflow_file = parse_kuflow_file(
            "kuflow-file:uri=ku:dummy/xxx-ssss-yyyy;type=application/pdf;size=11111;name=dummy.pdf;"
        )
        self.assertEqual(kuflow_file.uri, "ku:dummy/xxx-ssss-yyyy")
        self.assertEqual(kuflow_file.type, "application/pdf")
        self.assertEqual(kuflow_file.size, 11111)
        self.assertEqual(kuflow_file.name, "dummy.pdf")
        self.assertIsNone(kuflow_file.original_name)

    def test_parse_kuflow_file_ok_encoding(self):
        kuflow_file = parse_kuflow_file(
            "kuflow-file:"
            "uri=ku:dummy/xxx-ssss-yyyy;"
            "type=application/pdf;"
            "size=11111;"
            "name=dummy.pdf;"
            "original-name=with%20spaces.pdf;"
        )
        self.assertEqual(kuflow_file.uri, "ku:dummy/xxx-ssss-yyyy")
        self.assertEqual(kuflow_file.type, "application/pdf")
        self.assertEqual(kuflow_file.size, 11111)
        self.assertEqual(kuflow_file.name, "dummy.pdf")
        self.assertEqual(kuflow_file.original_name, "with spaces.pdf")

    def test_parse_kuflow_file_ok_unordered(self):
        kuflow_file = parse_kuflow_file(
            "kuflow-file:name=dummy.pdf;type=application/pdf;size=11111;uri=ku:dummy/xxx-ssss-yyyy;"
        )
        self.assertEqual(kuflow_file.uri, "ku:dummy/xxx-ssss-yyyy")
        self.assertEqual(kuflow_file.type, "application/pdf")
        self.assertEqual(kuflow_file.size, 11111)
        self.assertEqual(kuflow_file.name, "dummy.pdf")
        self.assertIsNone(kuflow_file.original_name)

    def test_parse_kuflow_file_ok_unknow_parts(self):
        kuflow_file = parse_kuflow_file(
            "kuflow-file:"
            "uri=ku:dummy/xxx-ssss-yyyy;"
            "type=application/pdf;"
            "size=11111;"
            "name=dummy.pdf;"
            "unknown-key1=unknown-value1;"
            "unknown-key2=unknown-value2;"
        )
        self.assertEqual(kuflow_file.uri, "ku:dummy/xxx-ssss-yyyy")
        self.assertEqual(kuflow_file.type, "application/pdf")
        self.assertEqual(kuflow_file.size, 11111)
        self.assertEqual(kuflow_file.name, "dummy.pdf")
        self.assertIsNone(kuflow_file.original_name)

    def test_parse_kuflow_file_empty(self):
        kuflow_file = parse_kuflow_file("")
        self.assertIsNone(kuflow_file)

    def test_parse_kuflow_file_missing_mandatory_part_uri(self):
        kuflow_file = parse_kuflow_file(
            "kuflow-file:type=application/pdf;size=11111;name=dummy.pdf;original-name=original-name.pdf;"
        )
        self.assertIsNone(kuflow_file)

    def test_parse_kuflow_file_incorrect_size_value(self):
        kuflow_file = parse_kuflow_file(
            "kuflow-file:"
            "uri=ku:dummy/xxx-ssss-yyyy;"
            "type=application/pdf;"
            "size=ABC;"
            "name=dummy.pdf;"
            "original-name=original-name.pdf;"
        )
        self.assertIsNone(kuflow_file)

    def test_parse_kuflow_file_incorrect_malformed(self):
        kuflow_file = parse_kuflow_file(
            "kuflow-file:uri=ku:dummy/xxx-ssss-yyyy;typeapplication/pdf;size=11111;name=dummy.pdf;"
        )
        self.assertIsNone(kuflow_file)

    def test_parse_kuflow_file_incorrect_malformed_missing_last_semicolon(self):
        kuflow_file = parse_kuflow_file(
            "kuflow-file:uri=ku:dummy/xxx-ssss-yyyy;typeapplication/pdf;size=11111;name=dummy.pdf"
        )
        self.assertIsNone(kuflow_file)

    def test_parse_kuflow_principal_ok(self):
        kuflow_principal = parse_kuflow_principal("kuflow-principal:id=xxx-ssss-yyyy;type=USER;name=Homer;")
        self.assertEqual(kuflow_principal.id, "xxx-ssss-yyyy")
        self.assertEqual(kuflow_principal.type, "USER")
        self.assertEqual(kuflow_principal.name, "Homer")

    def test_parse_kuflow_principal_ok_with_spaces(self):
        kuflow_principal = parse_kuflow_principal("kuflow-principal:id=xxx-ssss-yyyy;type=USER;name=Homer Simpson;")
        self.assertEqual(kuflow_principal.id, "xxx-ssss-yyyy")
        self.assertEqual(kuflow_principal.type, "USER")
        self.assertEqual(kuflow_principal.name, "Homer Simpson")

    def test_parse_kuflow_principal_ok_with_spaces_encoded(self):
        kuflow_principal = parse_kuflow_principal(
            "kuflow-principal:id=xxx-ssss-yyyy;type=USER;name=Homer%20Simpson%3B;"
        )
        self.assertEqual(kuflow_principal.id, "xxx-ssss-yyyy")
        self.assertEqual(kuflow_principal.type, "USER")
        self.assertEqual(kuflow_principal.name, "Homer Simpson;")

    def test_parse_kuflow_principal_missing_fields(self):
        kuflow_principal = parse_kuflow_principal("kuflow-principal:id=xxx-ssss-yyyy;type=USER;")
        self.assertIsNone(kuflow_principal)

    def test_parse_kuflow_principal_missing_fieldssss(self):
        kuflow_principal = generate_kuflow_principal_string("id=xxx-ssss-yyyy;", "USER", "Homer")
        self.assertEqual(kuflow_principal, "kuflow-principal:id=id%3Dxxx-ssss-yyyy%3B;type=USER;name=Homer;")

        kuflow_principal = generate_kuflow_principal_string("id=xxx-ssss-yyyy;", "CUSTOM", "Homer")
        self.assertEqual(kuflow_principal, "kuflow-principal:id=id%3Dxxx-ssss-yyyy%3B;type=CUSTOM;name=Homer;")

        kuflow_principal = generate_kuflow_principal_string("id=xxx-ssss-yyyy;", "USER", None)
        self.assertEqual(kuflow_principal, "kuflow-principal:id=id%3Dxxx-ssss-yyyy%3B;type=USER;name=;")


if __name__ == "__main__":
    unittest.main()
