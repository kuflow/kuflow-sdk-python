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

from collections.abc import Iterator
from typing import Any, Optional, Union

from .. import models as _models
from .._generated import KuFlowRestClient as KuFlowRestClientGenerated


class RobotOperations:
    """
    .. warning::
        **DO NOT** instantiate this class directly.

        Instead, you should access the following operations through
        :class:`~kuflow.rest.client.KuFlowRestClient`'s
        :attr:`principal` attribute.
    """

    def __init__(self, kuflow_client: KuFlowRestClientGenerated):
        self._kuflow_client = kuflow_client

    def find_robots(
        self,
        size: int = 25,
        page: int = 0,
        sort: Optional[Union[str, list[str]]] = None,
        tenant_id: Optional[Union[str, list[str]]] = None,
        filter_context: Optional[Union[str, _models.RobotFilterContext]] = None,
        **kwargs: Any,
    ) -> _models.PrincipalPage:
        """Find all accessible Robots.

        List all the Robots that have been created and the credentials has access.

        Available sort query values: createdAt, lastModifiedAt.

        :keyword size: The number of records returned within a single API call. Default value is 25.
        :type size: int
        :keyword page: The page number of the current page in the returned records, 0 is the first
         page. Default value is 0.
        :type page: int
        :keyword sort: Sorting criteria in the format: property{,asc|desc}. Example: createdAt,desc

         Default sort order is ascending. Multiple sort criteria are supported.

         Please refer to the method description for supported properties. Default value is None.
        :type sort: Optional[Union[str, List[str]]]
        :keyword tenant_id: Filter by tenantId. Default value is None.
        :type tenant_id: Optional[Union[str, List[str]]]
        :keyword filter_context: Filter by the specified context. Known values are: "READY" and "DEFAULT".
         Default value is None.
        :type filter_context: str or ~kuflow.rest.models.RobotFilterContext
        :return: RobotPage
        :rtype: ~kuflow.rest.models.RobotPage
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        if sort is not None and isinstance(sort, str):
            sort = [sort]

        if tenant_id is not None and isinstance(tenant_id, str):
            tenant_id = [tenant_id]

        return self._kuflow_client.robot.find_robots(
            size=size, page=page, sort=sort, tenant_id=tenant_id, filter_context=filter_context, **kwargs
        )

    def retrieve_robot(self, id: str, **kwargs: Any) -> _models.Principal:
        """Get a Robot by ID.

        Returns the requested Robot when has access to do it.

        :param id: The resource ID. Required.
        :type id: str
        :return: Robot
        :rtype: ~kuflow.rest.models.Robot
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.robot.retrieve_robot(id=id, **kwargs)

    def download_robot_source_code(self, id: str, **kwargs: Any) -> Iterator[bytes]:
        """Download robot code.

        Given a robot, download the source code.

        :param id: The resource ID. Required.
        :type id: str
        :return: Iterator[bytes]
        :rtype: Iterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.robot.download_robot_source_code(id=id, **kwargs)

    def download_robot_asset(
        self,
        id: str,
        *,
        type: _models.RobotAssetType,
        version: str,
        platform: _models.RobotAssetPlatform,
        architecture: _models.RobotAssetArchitecture,
        **kwargs: Any,
    ) -> Iterator[bytes]:
        """Download robot asset.

        Given a robot, download the requested asset.

        :param id: The resource ID. Required.
        :type id: str
        :keyword type: The asset type. Known values are: "PYTHON", "PYTHON_PIP", and "NODEJS".
         Required.
        :type type: str or ~kuflow.rest.models.RobotAssetType
        :keyword version: The asset version. Required.
        :type version: str
        :keyword platform: The asset platform. Known values are: "WINDOWS", "MAC_OS", and "LINUX".
         Required.
        :type platform: str or ~kuflow.rest.models.RobotAssetPlatform
        :keyword architecture: The asset platform architecture. Known values are: "X86_32" and "X86_64". Required.
        :type architecture: str or ~kuflow.rest.models.RobotAssetArchitecture
        :return: Iterator[bytes]
        :rtype: Iterator[bytes]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        return self._kuflow_client.robot.download_robot_asset(
            id=id, type=type, version=version, platform=platform, architecture=architecture, **kwargs
        )
