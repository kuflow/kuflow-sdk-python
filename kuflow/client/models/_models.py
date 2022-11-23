# coding=utf-8

from typing import IO


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
