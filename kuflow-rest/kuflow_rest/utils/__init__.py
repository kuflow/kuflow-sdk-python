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

from ._json_forms import (
    find_json_forms_property,
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

from ._element_values import (
    get_element_value_valid,
    get_element_value_valid_with_code,
    get_element_value_valid_at,
    get_element_value_valid_at_with_code,
    set_element_value_valid,
    set_element_value_valid_with_code,
    set_element_value_valid_at,
    set_element_value_valid_at_with_code,
    set_element_value,
    set_element_value_with_code,
    set_element_value_list,
    set_element_value_list_with_code,
    add_element_value,
    add_element_value_with_code,
    add_element_value_list,
    add_element_value_list_with_code,
    get_element_value_as_str,
    get_element_value_as_str_with_code,
    find_element_value_as_str,
    find_element_value_as_str_with_code,
    get_element_value_as_str_list,
    get_element_value_as_str_list_with_code,
    get_element_value_as_float,
    get_element_value_as_float_with_code,
    find_element_value_as_float,
    find_element_value_as_float_with_code,
    get_element_value_as_float_list,
    get_element_value_as_float_list_with_code,
    get_element_value_as_date,
    get_element_value_as_date_with_code,
    find_element_value_as_date,
    find_element_value_as_date_with_code,
    get_element_value_as_date_list,
    get_element_value_as_date_list_with_code,
    get_element_value_as_dict,
    get_element_value_as_dict_with_code,
    find_element_value_as_dict,
    find_element_value_as_dict_with_code,
    get_element_value_as_dict_list,
    get_element_value_as_dict_list_with_code,
    get_element_value_as_document,
    get_element_value_as_document_with_code,
    find_element_value_as_document,
    find_element_value_as_document_with_code,
    get_element_value_as_document_list,
    get_element_value_as_document_list_with_code,
    get_element_value_as_principal,
    get_element_value_as_principal_with_code,
    find_element_value_as_principal,
    find_element_value_as_principal_with_code,
    get_element_value_as_principal_list,
    get_element_value_as_principal_list_with_code,
)

__all__ = [
    "find_json_forms_property",
    "get_json_forms_property_as_str",
    "find_json_forms_property_as_str",
    "get_json_forms_property_as_int",
    "find_json_forms_property_as_int",
    "get_json_forms_property_as_float",
    "find_json_forms_property_as_float",
    "get_json_forms_property_as_date",
    "find_json_forms_property_as_date",
    "get_json_forms_property_as_datetime",
    "find_json_forms_property_as_datetime",
    "get_json_forms_property_as_json_forms_file",
    "find_json_forms_property_as_json_forms_file",
    "get_json_forms_property_as_json_forms_principal",
    "find_json_forms_property_as_json_forms_principal",
    "get_json_forms_property_as_list",
    "find_json_forms_property_as_list",
    "get_json_forms_property_as_dict",
    "find_json_forms_property_as_dict",
    "update_json_forms_property",
    "get_element_value_valid",
    "get_element_value_valid_with_code",
    "get_element_value_valid_at",
    "get_element_value_valid_at_with_code",
    "set_element_value_valid",
    "set_element_value_valid_with_code",
    "set_element_value_valid_at",
    "set_element_value_valid_at_with_code",
    "set_element_value",
    "set_element_value_with_code",
    "set_element_value_list",
    "set_element_value_list_with_code",
    "add_element_value",
    "add_element_value_with_code",
    "add_element_value_list",
    "add_element_value_list_with_code",
    "get_element_value_as_str",
    "get_element_value_as_str_with_code",
    "find_element_value_as_str",
    "find_element_value_as_str_with_code",
    "get_element_value_as_str_list",
    "get_element_value_as_str_list_with_code",
    "get_element_value_as_float",
    "get_element_value_as_float_with_code",
    "find_element_value_as_float",
    "find_element_value_as_float_with_code",
    "get_element_value_as_float_list",
    "get_element_value_as_float_list_with_code",
    "get_element_value_as_date",
    "get_element_value_as_date_with_code",
    "find_element_value_as_date",
    "find_element_value_as_date_with_code",
    "get_element_value_as_date_list",
    "get_element_value_as_date_list_with_code",
    "get_element_value_as_dict",
    "get_element_value_as_dict_with_code",
    "find_element_value_as_dict",
    "find_element_value_as_dict_with_code",
    "get_element_value_as_dict_list",
    "get_element_value_as_dict_list_with_code",
    "get_element_value_as_document",
    "get_element_value_as_document_with_code",
    "find_element_value_as_document",
    "find_element_value_as_document_with_code",
    "get_element_value_as_document_list",
    "get_element_value_as_document_list_with_code",
    "get_element_value_as_principal",
    "get_element_value_as_principal_with_code",
    "find_element_value_as_principal",
    "find_element_value_as_principal_with_code",
    "get_element_value_as_principal_list",
    "get_element_value_as_principal_list_with_code",
]