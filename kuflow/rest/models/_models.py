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


class Document:
    """File document.

    :ivar file_mame: File name
    :vartype file_mame: str
    :ivar content_type: File content type
    :vartype content_type: str
    :ivar file_content: File content.
    :vartype file_content: IO
    """

    def __init__(self, file_mame: str, content_type: str, file_content: IO):
        """
        :keyword file_mame:
        :paramtype file_mame: File name
        :keyword content_type: File content type
        :paramtype content_type: str
        :keyword file_content: File content.
        :paramtype File content.: IO
        """
        self.file_mame = file_mame
        self.content_type = content_type
        self.file_content = file_content


class TaskSaveElementValueDocumentCommand:
    """TaskSaveElementValueDocumentCommand.

    All required parameters must be populated in order to send to Azure.

    :ivar element_definition_code: Required.
    :vartype element_definition_code: str
    :ivar element_value_id:
    :vartype element_value_id: str
    :ivar element_value_valid:
    :vartype element_value_valid: bool
    """

    def __init__(
        self,
        element_definition_code: str,
        element_value_id: Optional[str] = None,
        element_value_valid: bool = True,
    ):
        """
        :keyword element_definition_code: Required.
        :paramtype element_definition_code: str
        :keyword element_value_id:
        :paramtype element_value_id: str
        :keyword element_value_valid:
        :paramtype element_value_valid: bool
        """
        self.element_definition_code = element_definition_code
        self.element_value_id = element_value_id
        self.element_value_valid = element_value_valid


class ProcessSaveUserActionValueDocumentCommand:
    """ProcessSaveUserActionValueDocumentCommand.

    All required parameters must be populated in order to send to Azure.

    :ivar user_action_value_id: Required.
    :vartype user_action_value_id: str
    """

    def __init__(
        self,
        user_action_value_id: str,
    ):
        """
        :keyword user_action_value_id: Required.
        :paramtype user_action_value_id: str
        """
        self.user_action_value_id = user_action_value_id
