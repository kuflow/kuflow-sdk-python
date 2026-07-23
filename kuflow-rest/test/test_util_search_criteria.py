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
import urllib.parse

from kuflow_rest.utils import encode_filter_expression


def _decode_filter_expression(expression: str):
    parts = expression.split(" ")
    code = urllib.parse.unquote(parts[0])
    operation = urllib.parse.unquote(parts[1])
    values = [urllib.parse.unquote(part) for part in parts[2:]]
    return code, operation, values


class UtilsSearchCriteriaTest(unittest.TestCase):
    def test_encode_filter_expression_ok(self):
        expression = encode_filter_expression("invoiceNumber", "eq", "INV-001")

        self.assertEqual(expression, "invoiceNumber eq INV-001")

        code, operation, values = _decode_filter_expression(expression)
        self.assertEqual(code, "invoiceNumber")
        self.assertEqual(operation, "eq")
        self.assertEqual(values, ["INV-001"])

    def test_encode_filter_expression_ok_with_embedded_space(self):
        expression = encode_filter_expression("FIELD_STRING", "eq", "Text value")

        self.assertEqual(expression, "FIELD_STRING eq Text%20value")

        code, operation, values = _decode_filter_expression(expression)
        self.assertEqual(code, "FIELD_STRING")
        self.assertEqual(operation, "eq")
        self.assertEqual(values, ["Text value"])

    def test_encode_filter_expression_ok_with_literal_plus(self):
        expression = encode_filter_expression("phoneNumber", "eq", "+1234567890")

        self.assertNotIn("%20", expression.split(" ")[2])

        code, operation, values = _decode_filter_expression(expression)
        self.assertEqual(code, "phoneNumber")
        self.assertEqual(operation, "eq")
        self.assertEqual(values, ["+1234567890"])

    def test_encode_filter_expression_ok_with_literal_percent(self):
        expression = encode_filter_expression("discount", "eq", "50%off")

        code, operation, values = _decode_filter_expression(expression)
        self.assertEqual(code, "discount")
        self.assertEqual(operation, "eq")
        self.assertEqual(values, ["50%off"])

    def test_encode_filter_expression_ok_multi_value(self):
        expression = encode_filter_expression("amount", "between", "10", "20")

        self.assertEqual(expression, "amount between 10 20")

        code, operation, values = _decode_filter_expression(expression)
        self.assertEqual(code, "amount")
        self.assertEqual(operation, "between")
        self.assertEqual(values, ["10", "20"])

    def test_encode_filter_expression_ok_multi_value_with_embedded_spaces(self):
        expression = encode_filter_expression("status", "in", "active now", "inactive later")

        code, operation, values = _decode_filter_expression(expression)
        self.assertEqual(code, "status")
        self.assertEqual(operation, "in")
        self.assertEqual(values, ["active now", "inactive later"])

    def test_encode_filter_expression_missing_values(self):
        with self.assertRaises(ValueError):
            encode_filter_expression("invoiceNumber", "eq")


if __name__ == "__main__":
    unittest.main()
