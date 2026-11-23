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

import warnings
from collections.abc import Iterator
from typing import Any, Optional

from .. import models as _models
from .._generated import KuFlowRestClient as KuFlowRestClientGenerated


class DocumentOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.client.KuFlowRestClient`'s
        :attr:`document` attribute.
    """

    def __init__(self, kuflow_client: KuFlowRestClientGenerated):
        self._kuflow_client = kuflow_client

    def upload_document(
        self, document: _models.Document, *, target_uri: Optional[str] = None, **kwargs: Any
    ) -> _models.DocumentReference:
        """Upload a temporal document.

        Upload a temporal document that later on must be linked with a domain resource.

        The document belongs to the credentials that upload it, and its reference has the URI
        ``ku:storage-staging/{id}``. Only those credentials can download it and link it, by sending its
        reference in the data of any resource they can update; the permission on that resource is checked
        when the data is saved.

        Documents not linked are deleted after 2 hours.

        :param document: Document to save. Required.
        :type document: ~kuflow.rest.models.Document
        :keyword target_uri: Deprecated and ignored: the document can be linked to any resource the
                             credentials can update. Still sent when given.
        :type target_uri: str
        :return: DocumentReference
        :rtype: ~kuflow.rest.models.DocumentReference
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        if target_uri is not None:
            warnings.warn(
                "target_uri is deprecated and ignored: the document can be linked to any resource the credentials "
                "can update",
                DeprecationWarning,
                stacklevel=2,
            )

        return self._kuflow_client.document.upload_document(
            file=document.file_content,
            target_uri=target_uri,
            file_content_type=document.content_type,
            file_name=document.file_name,
            **kwargs,
        )

    def download_document(self, *, document_uri: str, **kwargs: Any) -> Iterator[bytes]:
        """Download a document.

        Given a document uri, download its content. Accepts both the ``kuflow-file:`` reference returned by
        the upload operations and a plain ``ku:`` document uri.

        The credentials must be able to read the resource that owns the document; a document outside their
        reach, or a uri that does not resolve to a document, answers ``404``.

        :keyword document_uri: Document URI to download, in ``kuflow-file:`` or ``ku:`` form. Required.
        :type document_uri: str
        :return: Iterator[bytes]
        :rtype: Iterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.document.download_document(document_uri=document_uri, **kwargs)
