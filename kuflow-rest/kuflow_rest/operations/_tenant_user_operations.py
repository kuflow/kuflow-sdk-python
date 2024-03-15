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


class TenantUserOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.client.KuFlowRestClient`'s
        :attr:`principal` attribute.
    """

    def __init__(self, kuflow_client: KuFlowRestClientGenerated):
        self._kuflow_client = kuflow_client

    def find_tenant_users(
        self,
        size: int = 25,
        page: int = 0,
        sort: Optional[Union[str, List[str]]] = None,
        type: Optional[_models.PrincipalType] = None,
        group_id: Optional[Union[str, List[str]]] = None,
        email: Optional[Union[str, List[str]]] = None,
        tenant_id: Optional[Union[str, List[str]]] = None,
        **kwargs: Any,
    ) -> _models.TenantUserPage:
        """Find all accessible Tenant Users.

        List all the Tenant Users that have been created and the used credentials has access.

        Available sort query values: id, name.

        :keyword size: The number of records returned within a single API call. Default value is 25.
        :paramtype size: int
        :keyword page: The page number of the current page in the returned records, 0 is the first
         page. Default value is 0.
        :paramtype page: int
        :keyword sort: Sorting criteria in the format: property{,asc|desc}. Example: createdAt,desc

         Default sort order is ascending. Multiple sort criteria are supported.

         Please refer to the method description for supported properties. Default value is None.
        :paramtype sort: list[str]
        :keyword group_id: Filter tenant users that exists in one of the group ids. Default value is
         None.
        :paramtype group_id: list[str]
        :keyword email: Filter tenant users that have one of the emails. Default value is None.
        :paramtype email: list[str]
        :return: TenantUserPage
        :rtype: ~kuflow.rest.models.TenantUserPage
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        if sort is not None and isinstance(sort, str):
            sort = [sort]

        if group_id is not None and isinstance(group_id, str):
            group_id = [group_id]

        if email is not None and isinstance(email, str):
            email = [email]

        if tenant_id is not None and isinstance(tenant_id, str):
            tenant_id = [tenant_id]

        return self._kuflow_client.tenant_user.find_tenant_users(
            size=size,
            page=page,
            sort=sort,
            group_id=group_id,
            email=email,
            tenant_id=tenant_id,
            **kwargs,
        )

    def retrieve_tenant_user(self, id: str, **kwargs: Any) -> _models.TenantUser:
        """Get a Principal by ID.

        Returns the requested Principal when has access to do it.

        :param id: The resource ID. Required.
        :type id: str
        :return: Principal
        :rtype: ~kuflow.rest.models.Principal
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.tenant_user.retrieve_tenant_user(id=id, **kwargs)
