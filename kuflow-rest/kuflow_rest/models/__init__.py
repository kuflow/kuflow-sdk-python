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

from .._generated.models import (
    AbstractAudited,
    Authentication,
    AuthenticationCreateParams,
    AuthenticationEngineCertificate,
    AuthenticationEngineCertificateTls,
    AuthenticationEngineToken,
    AuthenticationType,
    DefaultError,
    DefaultErrorInfo,
    DocumentReference,
    JsonPatchOperation,
    JsonPatchOperationType,
    JsonValue,
    JsonValueError,
    Page,
    PageMetadata,
    Principal,
    PrincipalApplication,
    PrincipalPage,
    PrincipalPageItem,
    PrincipalType,
    PrincipalUser,
    Process,
    ProcessChangeInitiatorParams,
    ProcessCreateParams,
    ProcessDefinitionSummary,
    ProcessEntityUpdateParams,
    ProcessItem,
    ProcessItemCreateParams,
    ProcessItemMessage,
    ProcessItemMessageCreateParams,
    ProcessItemMessagePageItem,
    ProcessItemPage,
    ProcessItemPageItem,
    ProcessItemTask,
    ProcessItemTaskAppendLogParams,
    ProcessItemTaskAssignParams,
    ProcessItemTaskCreateParams,
    ProcessItemTaskDataUpdateParams,
    ProcessItemTaskLog,
    ProcessItemTaskLogLevel,
    ProcessItemTaskPageItem,
    ProcessItemTaskState,
    ProcessItemType,
    ProcessMetadataUpdateParams,
    ProcessPage,
    ProcessPageItem,
    ProcessRelated,
    ProcessState,
    Robot,
    RobotAssetArchitecture,
    RobotAssetPlatform,
    RobotAssetType,
    RobotFilterContext,
    RobotPage,
    RobotPageItem,
    RobotSourceFile,
    RobotSourceType,
    TaskDefinitionSummary,
    TenantUser,
    TenantUserPage,
    TenantUserPageItem,
    WebhookEvent,
    WebhookEventProcessCreated,
    WebhookEventProcessCreatedData,
    WebhookEventProcessItemCreated,
    WebhookEventProcessItemCreatedData,
    WebhookEventProcessItemTaskStateChanged,
    WebhookEventProcessItemTaskStateChangedData,
    WebhookEventProcessStateChanged,
    WebhookEventProcessStateChangedData,
    WebhookType,
    Worker,
    WorkerCreateParams,
)
from .._generated.models import __all__ as _all_generated_models
from ._models import (
    Document,
    KuFlowFile,
    KuFlowPrincipal,
)


__all__ = [
    # From _generated.models
    "AbstractAudited",
    "Authentication",
    "AuthenticationCreateParams",
    "AuthenticationEngineCertificate",
    "AuthenticationEngineCertificateTls",
    "AuthenticationEngineToken",
    "AuthenticationType",
    "DefaultError",
    "DefaultErrorInfo",
    "DocumentReference",
    "JsonPatchOperation",
    "JsonPatchOperationType",
    "JsonValue",
    "JsonValueError",
    "Page",
    "PageMetadata",
    "Principal",
    "PrincipalApplication",
    "PrincipalPage",
    "PrincipalPageItem",
    "PrincipalType",
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
    "ProcessItemTaskLogLevel",
    "ProcessItemTaskPageItem",
    "ProcessItemTaskState",
    "ProcessItemType",
    "ProcessMetadataUpdateParams",
    "ProcessPage",
    "ProcessPageItem",
    "ProcessRelated",
    "ProcessState",
    "Robot",
    "RobotAssetArchitecture",
    "RobotAssetPlatform",
    "RobotAssetType",
    "RobotFilterContext",
    "RobotPage",
    "RobotPageItem",
    "RobotSourceFile",
    "RobotSourceType",
    "TaskDefinitionSummary",
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
    "WebhookType",
    "Worker",
    "WorkerCreateParams",
    # From models
    "Document",
    "KuFlowFile",
    "KuFlowPrincipal",
]


# For usability, we must include in __all__, all the items of the model generated package
# So this assertion is to avoid forgetfulness.
assert all(item in __all__ for item in _all_generated_models)
