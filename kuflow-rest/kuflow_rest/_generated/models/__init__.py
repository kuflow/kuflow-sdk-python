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

from ._models import AbstractAudited
from ._models import Authentication
from ._models import AuthenticationCreateParams
from ._models import AuthenticationEngineCertificate
from ._models import AuthenticationEngineCertificateTls
from ._models import AuthenticationEngineToken
from ._models import DefaultError
from ._models import DefaultErrorInfo
from ._models import DocumentReference
from ._models import JsonPatchOperation
from ._models import JsonValue
from ._models import JsonValueError
from ._models import Page
from ._models import PageMetadata
from ._models import Principal
from ._models import PrincipalApplication
from ._models import PrincipalPage
from ._models import PrincipalPageItem
from ._models import PrincipalUser
from ._models import Process
from ._models import ProcessChangeInitiatorParams
from ._models import ProcessCreateParams
from ._models import ProcessDefinitionSummary
from ._models import ProcessEntityUpdateParams
from ._models import ProcessItem
from ._models import ProcessItemCreateParams
from ._models import ProcessItemMessage
from ._models import ProcessItemMessageCreateParams
from ._models import ProcessItemMessagePageItem
from ._models import ProcessItemPage
from ._models import ProcessItemPageItem
from ._models import ProcessItemTask
from ._models import ProcessItemTaskAppendLogParams
from ._models import ProcessItemTaskAssignParams
from ._models import ProcessItemTaskCreateParams
from ._models import ProcessItemTaskDataUpdateParams
from ._models import ProcessItemTaskLog
from ._models import ProcessItemTaskPageItem
from ._models import ProcessMetadataUpdateParams
from ._models import ProcessPage
from ._models import ProcessPageItem
from ._models import ProcessRelated
from ._models import Robot
from ._models import RobotPage
from ._models import RobotPageItem
from ._models import RobotSourceFile
from ._models import TaskDefinitionSummary
from ._models import Tenant
from ._models import TenantPage
from ._models import TenantPageItem
from ._models import TenantUser
from ._models import TenantUserPage
from ._models import TenantUserPageItem
from ._models import WebhookEvent
from ._models import WebhookEventProcessCreated
from ._models import WebhookEventProcessCreatedData
from ._models import WebhookEventProcessItemCreated
from ._models import WebhookEventProcessItemCreatedData
from ._models import WebhookEventProcessItemTaskStateChanged
from ._models import WebhookEventProcessItemTaskStateChangedData
from ._models import WebhookEventProcessStateChanged
from ._models import WebhookEventProcessStateChangedData
from ._models import Worker
from ._models import WorkerCreateParams

from ._enums import AuthenticationType
from ._enums import JsonPatchOperationType
from ._enums import PrincipalType
from ._enums import ProcessItemTaskLogLevel
from ._enums import ProcessItemTaskState
from ._enums import ProcessItemType
from ._enums import ProcessState
from ._enums import RobotAssetArchitecture
from ._enums import RobotAssetPlatform
from ._enums import RobotAssetType
from ._enums import RobotFilterContext
from ._enums import RobotSourceType
from ._enums import TenantPricingPlan
from ._enums import WebhookType
from ._patch import __all__ as _patch_all
from ._patch import *  # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "AbstractAudited",
    "Authentication",
    "AuthenticationCreateParams",
    "AuthenticationEngineCertificate",
    "AuthenticationEngineCertificateTls",
    "AuthenticationEngineToken",
    "DefaultError",
    "DefaultErrorInfo",
    "DocumentReference",
    "JsonPatchOperation",
    "JsonValue",
    "JsonValueError",
    "Page",
    "PageMetadata",
    "Principal",
    "PrincipalApplication",
    "PrincipalPage",
    "PrincipalPageItem",
    "PrincipalUser",
    "Process",
    "ProcessChangeInitiatorParams",
    "ProcessCreateParams",
    "ProcessDefinitionSummary",
    "ProcessEntityUpdateParams",
    "ProcessItem",
    "ProcessItemCreateParams",
    "ProcessItemMessage",
    "ProcessItemMessageCreateParams",
    "ProcessItemMessagePageItem",
    "ProcessItemPage",
    "ProcessItemPageItem",
    "ProcessItemTask",
    "ProcessItemTaskAppendLogParams",
    "ProcessItemTaskAssignParams",
    "ProcessItemTaskCreateParams",
    "ProcessItemTaskDataUpdateParams",
    "ProcessItemTaskLog",
    "ProcessItemTaskPageItem",
    "ProcessMetadataUpdateParams",
    "ProcessPage",
    "ProcessPageItem",
    "ProcessRelated",
    "Robot",
    "RobotPage",
    "RobotPageItem",
    "RobotSourceFile",
    "TaskDefinitionSummary",
    "Tenant",
    "TenantPage",
    "TenantPageItem",
    "TenantUser",
    "TenantUserPage",
    "TenantUserPageItem",
    "WebhookEvent",
    "WebhookEventProcessCreated",
    "WebhookEventProcessCreatedData",
    "WebhookEventProcessItemCreated",
    "WebhookEventProcessItemCreatedData",
    "WebhookEventProcessItemTaskStateChanged",
    "WebhookEventProcessItemTaskStateChangedData",
    "WebhookEventProcessStateChanged",
    "WebhookEventProcessStateChangedData",
    "Worker",
    "WorkerCreateParams",
    "AuthenticationType",
    "JsonPatchOperationType",
    "PrincipalType",
    "ProcessItemTaskLogLevel",
    "ProcessItemTaskState",
    "ProcessItemType",
    "ProcessState",
    "RobotAssetArchitecture",
    "RobotAssetPlatform",
    "RobotAssetType",
    "RobotFilterContext",
    "RobotSourceType",
    "TenantPricingPlan",
    "WebhookType",
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()
