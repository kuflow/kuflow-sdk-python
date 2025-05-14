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

import urllib.parse
from typing import Optional, Union

from ..models import KuFlowFile, KuFlowGroup, KuFlowPrincipal, PrincipalType


def parse_kuflow_file(original: str) -> Optional[KuFlowFile]:
    if original is None or not isinstance(original, str) or not original.startswith("kuflow-file:"):
        return None

    original_transformed = original.replace("kuflow-file:", "")

    key_value_pairs = original_transformed.split(";")

    key_value_map = {}
    for pair in key_value_pairs:
        if pair.find("=") is -1:
            continue

        key, value = pair.split("=")
        if key is None or value is None:
            return None

        key_value_map[key] = urllib.parse.unquote(value)

    uri: Optional[str] = str(key_value_map["uri"]) if "uri" in key_value_map else None
    type: Optional[str] = str(key_value_map["type"]) if "type" in key_value_map else None
    name: Optional[str] = str(key_value_map["name"]) if "name" in key_value_map else None
    try:
        size: Optional[int] = int(key_value_map["size"]) if "size" in key_value_map else None
    except ValueError:
        size = None
    original_name: Optional[str] = str(key_value_map["original-name"]) if "original-name" in key_value_map else None

    if (uri is None) or (type is None) or (name is None) or (size is None):
        return None

    return KuFlowFile(original=original, uri=uri, type=type, name=name, size=size, original_name=original_name)


def parse_kuflow_principal(original: str) -> Optional[KuFlowPrincipal]:
    if original is None or not isinstance(original, str) or not original.startswith("kuflow-principal:"):
        return None

    original_transformed = original.replace("kuflow-principal:", "")

    key_value_pairs = original_transformed.split(";")

    key_value_map = {}
    for pair in key_value_pairs:
        if pair.find("=") is -1:
            continue

        key, value = pair.split("=")
        if key is None or value is None:
            return None

        key_value_map[key] = urllib.parse.unquote(value)

    id: Optional[str] = str(key_value_map["id"]) if "id" in key_value_map else None
    type: Optional[PrincipalType] = str(key_value_map["type"]) if "type" in key_value_map else None
    name: Optional[str] = str(key_value_map["name"]) if "name" in key_value_map else None

    if (id is None) or (type is None) or (name is None):
        return None

    return KuFlowPrincipal(
        original=original,
        id=id,
        type=type,
        name=name,
    )


def parse_kuflow_group(original: str) -> Optional[KuFlowGroup]:
    if original is None or not isinstance(original, str) or not original.startswith("kuflow-group:"):
        return None

    original_transformed = original.replace("kuflow-group:", "")

    key_value_pairs = original_transformed.split(";")

    key_value_map = {}
    for pair in key_value_pairs:
        if pair.find("=") is -1:
            continue

        key, value = pair.split("=")
        if key is None or value is None:
            return None

        key_value_map[key] = urllib.parse.unquote(value)

    id: Optional[str] = str(key_value_map["id"]) if "id" in key_value_map else None
    type: Optional[str] = str(key_value_map["type"]) if "type" in key_value_map else None
    name: Optional[str] = str(key_value_map["name"]) if "name" in key_value_map else None

    if (id is None) or (type is None) or (name is None):
        return None

    return KuFlowGroup(
        original=original,
        id=id,
        type=type,
        name=name,
    )


def generate_kuflow_principal_string(id: str, principal_type: Union[str, PrincipalType], name: Optional[str]) -> str:
    return f"kuflow-principal:id={encode(id)};type={encode(principal_type)};name={encode(name)};"


def generate_kuflow_group_string(id: str, group_type: Union[str, str], name: Optional[str]) -> str:
    return f"kuflow-group:id={encode(id)};type={encode(group_type)};name={encode(name)};"


def encode(value: Optional[str]) -> str:
    if value is None:
        return ""

    return urllib.parse.quote(value.strip(), safe="").replace("+", "%20")
