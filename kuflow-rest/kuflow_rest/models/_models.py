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


class KuFlowPrincipal:
    """JsonFormsPrincipal.

    Principal class
    """

    def __init__(self, original: str, id: str, type: PrincipalType, name: str):
        """
        Parameters:
            id: Principal original value, ie: kuflow-principal:id=xxx-yyy-zzz;type=USER;name=John;
            id: Principal id
            type: Principal type
            name: Principal name
        """
        self.original = original
        self.id = id
        self.type = type
        self.name = name

    def __str__(self):
        return self.original


class KuFlowGroup:
    """JsonFormsGroup

    Group class
    """

    def __init__(self, original: str, id: str, type: str, name: str):
        """
        Parameters:
            id: Group original value, ie: kuflow-group:id=xxx-yyy-zzz;type=OTHERS;name=MyGroup;
            id: Group id
            type: Group type
            name: Group name
        """
        self.original = original
        self.id = id
        self.type = type
        self.name = name

    def __str__(self):
        return self.original


class KuFlowFile:
    """KuFlowFile.

    File class
    """

    def __init__(self, original: str, uri: str, type: str, name: str, size: int, original_name: Optional[str]):
        """
        Parameters:
            original: Original value,
              ie: kuflow-file:uri=kf:xxx/aaa;type=application/pdf;size=500;name=name-xxxx.pdf;originalName=dummy.pdf;
            uri: File uri, ie: kf:xxx-yyy-zzz/aaa-bbb-ccc
            type: File type, ie: application/pdf
            name: File name, ie: name-xxxx.pdf
            size: File size in bytes, ie: 500
            original_name: Original name, ie: dummy.pdf
        """
        self.original = original
        self.uri = uri
        self.type = type
        self.name = name
        self.size = size
        self.original_name = original_name

    def __str__(self):
        return self.original
