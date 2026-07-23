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

from ._parser import encode


def encode_filter_expression(code: str, operation: str, *values: str) -> str:
    """Build a "code operation value1 value2..." filter expression.

    Used by the KuFlow REST API's search-criteria query parameters (e.g. the ``metadata`` filter of
    ``find_processes`` or the ``value`` filter of ``find_business_artifacts``).

    The server splits each expression on spaces, then decodes each resulting token (code, operation,
    each value) individually. So code, operation and each value are percent-encoded individually here
    (space becomes ``%20``) before joining them with the literal space separator, so that a space or
    any other reserved character inside one of them doesn't collide with the separator. The HTTP client
    is responsible for percent-encoding the resulting expression as a whole when it places it on the
    wire as a query-parameter value; this function must not do that itself.

    :param code: The field code to filter/sort by.
    :type code: str
    :param operation: The operation code, e.g. "eq", "le", "ge", "between", "contains", "in".
    :type operation: str
    :param values: One or more values for the operation.
    :type values: str
    :return: The encoded filter expression, ready to be passed as a ``value``/``metadata`` query parameter.
    :rtype: str
    """
    if not values:
        raise ValueError("At least one value is required")

    tokens = [encode(code), encode(operation), *(encode(value) for value in values)]

    return " ".join(tokens)
