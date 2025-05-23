# coding=utf-8
# --------------------------------------------------------------------------
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
# --------------------------------------------------------------------------
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
#
# --------------------------------------------------------------------------
# pylint: disable=wrong-import-position

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ._patch import *  # pylint: disable=unused-wildcard-import

from ._authentication_operations import AuthenticationOperations  # type: ignore
from ._kms_operations import KmsOperations  # type: ignore
from ._principal_operations import PrincipalOperations  # type: ignore
from ._group_operations import GroupOperations  # type: ignore
from ._tenant_operations import TenantOperations  # type: ignore
from ._tenant_user_operations import TenantUserOperations  # type: ignore
from ._process_operations import ProcessOperations  # type: ignore
from ._process_item_operations import ProcessItemOperations  # type: ignore
from ._worker_operations import WorkerOperations  # type: ignore
from ._robot_operations import RobotOperations  # type: ignore

from ._patch import __all__ as _patch_all
from ._patch import *
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "AuthenticationOperations",
    "KmsOperations",
    "PrincipalOperations",
    "GroupOperations",
    "TenantOperations",
    "TenantUserOperations",
    "ProcessOperations",
    "ProcessItemOperations",
    "WorkerOperations",
    "RobotOperations",
]
__all__.extend([p for p in _patch_all if p not in __all__])  # pyright: ignore
_patch_sdk()
