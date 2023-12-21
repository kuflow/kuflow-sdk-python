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


from typing import IO, Optional

from .._generated.models import PrincipalType


class Document:
    """File document."""

    def __init__(self, file_mame: str, content_type: str, file_content: IO) -> None:
        """
        Parameters:
            file_mame: File name
            content_type: File content type
            file_content: File content.
        """
        self.file_mame = file_mame
        self.content_type = content_type
        self.file_content = file_content


class TaskSaveElementValueDocumentCommand:
    """TaskSaveElementValueDocumentCommand.

    All required parameters must be populated in order to send to KuFlow.
    """

    def __init__(
        self,
        element_definition_code: str,
        element_value_id: Optional[str] = None,
        element_value_valid: bool = True,
    ) -> None:
        """
        Parameters:
            element_definition_code: Element definition code. Required.
            element_value_id: Element value id
            element_value_valid: Valid
        """
        self.element_definition_code = element_definition_code
        self.element_value_id = element_value_id
        self.element_value_valid = element_value_valid


class TaskSaveJsonFormsValueDocumentRequestCommand:
    """TaskSaveJsonFormsValueDocumentCommand.

    All required parameters must be populated in order to send to KuFlow.
    """

    def __init__(self, schema_path: str) -> None:
        """
        Parameters:
            schema_path: Document schema path. Required.
        """
        self.schema_path = schema_path


class ProcessSaveUserActionValueDocumentCommand:
    """ProcessSaveUserActionValueDocumentCommand.

    All required parameters must be populated in order to send to KuFlow.

    Attributes:
        user_action_value_id: User action value id
    """

    def __init__(self, user_action_value_id: str) -> None:
        """
        Parameters:
            user_action_value_id: User action value id
        """
        self.user_action_value_id = user_action_value_id


class JsonFormsPrincipal:
    """JsonFormsPrincipal.

    Principal class
    """

    def __init__(self, id: str, type: PrincipalType, name: str):
        """
        Parameters:
            id: Principal id
            type: Principal type
            name: Principal name
        """
        self.id = id
        self.type = type
        self.name = name


class JsonFormsFile:
    """JsonFormsFile.

    File class
    """

    def __init__(self, uri: str, type: str, name: str, size: int):
        """
        Parameters:
            uri: File uri, ie: kf:xxx-yyy-zzz/aaa-bbb-ccc
            type: File type, ie: application/pdf
            name: File name, ie: dummy.pdf
            size: File size in bytes, ie: 500
        """
        self.uri = uri
        self.type = type
        self.name = name
        self.size = size
