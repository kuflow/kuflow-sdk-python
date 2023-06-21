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


from typing import Any, List, Optional, Union

from .._generated import KuFlowRestClient as KuFlowRestClientGenerated
from .._generated import models as _models


class PrincipalOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.client.KuFlowRestClient`'s
        :attr:`principal` attribute.
    """

    def __init__(self, kuflow_client: KuFlowRestClientGenerated):
        self._kuflow_client = kuflow_client

    def find_principals(
        self,
        size: int = 25,
        page: int = 0,
        sort: Optional[Union[str, List[str]]] = None,
        type: Optional[_models.PrincipalType] = None,
        group_id: Optional[Union[str, List[str]]] = None,
        **kwargs: Any,
    ) -> _models.PrincipalPage:
        """Find all accessible Principals.

        List all the Principals that have been created and the used credentials has access.

        Available sort query values: id, name.

        :keyword size: The number of records returned within a single API call. Default value is 25.
        :type size: int
        :keyword page: The page number of the current page in the returned records, 0 is the first page.
                       Default value is 0.
        :type page: int
        :keyword sort: Sorting criteria in the format: property{,asc|desc}. Example: createdAt,desc
                       Default sort order is ascending. Multiple sort criteria are supported.
                       Please refer to the method description for supported properties. Default value is None.
        :type sort: Optional[Union[str, List[str]]]
        :keyword type: Filter principals by type. Known values are: "USER", "APPLICATION", and
                      "SYSTEM". Default value is None.
        :type type: Optional[_models.PrincipalType]
        :keyword group_id: Filter principals that exists in one of group ids. Default value is None.
        :type group_id: Optional[Union[str, List[str]]]
        :return: PrincipalPage
        :rtype: ~kuflow.rest.models.PrincipalPage
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        if sort is not None and isinstance(sort, str):
            sort = [sort]

        if group_id is not None and isinstance(group_id, str):
            group_id = [group_id]

        return self._kuflow_client.principal.find_principals(
            size=size, page=page, sort=sort, type=type, group_id=group_id, **kwargs
        )

    def retrieve_principal(self, id: str, **kwargs: Any) -> _models.Principal:
        """Get a Principal by ID.

        Returns the requested Principal when has access to do it.

        :param id: The resource ID. Required.
        :type id: str
        :return: Principal
        :rtype: ~kuflow.rest.models.Principal
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.principal.retrieve_principal(id=id, **kwargs)
