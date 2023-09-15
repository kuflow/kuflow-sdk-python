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

from .._generated.models import (
    AbstractAudited,
    AuditedObjectType,
    Authentication,
    AuthenticationEngineCertificate,
    AuthenticationEngineCertificateTls,
    AuthenticationEngineToken,
    AuthenticationType,
    DefaultError,
    DefaultErrorInfo,
    JsonFormsValue,
    Log,
    LogLevel,
    Page,
    PagedObjectType,
    PageMetadata,
    Principal,
    PrincipalApplication,
    PrincipalPage,
    PrincipalType,
    PrincipalUser,
    Process,
    ProcessChangeInitiatorCommand,
    ProcessDefinitionSummary,
    ProcessDeleteElementCommand,
    ProcessElementValue,
    ProcessElementValueNumber,
    ProcessElementValueString,
    ProcessElementValueType,
    ProcessPage,
    ProcessPageItem,
    ProcessSaveElementCommand,
    ProcessState,
    RelatedProcess,
    Task,
    TaskAssignCommand,
    TaskDefinitionSummary,
    TaskDeleteElementCommand,
    TaskDeleteElementValueDocumentCommand,
    TaskElementValue,
    TaskElementValueDocument,
    TaskElementValueDocumentItem,
    TaskElementValueNumber,
    TaskElementValueObject,
    TaskElementValuePrincipal,
    TaskElementValuePrincipalItem,
    TaskElementValueString,
    TaskElementValueType,
    TaskPage,
    TaskPageItem,
    TaskSaveElementCommand,
    TaskSaveJsonFormsValueDataCommand,
    TaskSaveJsonFormsValueDocumentResponseCommand,
    TaskState,
    WebhookEvent,
    WebhookEventProcessStateChanged,
    WebhookEventProcessStateChangedData,
    WebhookEventTaskStateChanged,
    WebhookEventTaskStateChangedData,
    WebhookType,
    Worker,
)
from .._generated.models import __all__ as _all_generated_models
from ._models import (
    Document,
    JsonFormsFile,
    JsonFormsPrincipal,
    ProcessSaveUserActionValueDocumentCommand,
    TaskSaveElementValueDocumentCommand,
    TaskSaveJsonFormsValueDocumentRequestCommand,
)

__all__ = [
    # From _generated.models
    "AbstractAudited",
    "AuditedObjectType",
    "Authentication",
    "AuthenticationEngineCertificate",
    "AuthenticationEngineCertificateTls",
    "AuthenticationEngineToken",
    "AuthenticationType",
    "DefaultError",
    "DefaultErrorInfo",
    "JsonFormsValue",
    "Log",
    "LogLevel",
    "Page",
    "PagedObjectType",
    "PageMetadata",
    "Principal",
    "PrincipalApplication",
    "PrincipalPage",
    "PrincipalType",
    "PrincipalUser",
    "Process",
    "ProcessChangeInitiatorCommand",
    "ProcessDefinitionSummary",
    "ProcessDeleteElementCommand",
    "ProcessElementValue",
    "ProcessElementValueNumber",
    "ProcessElementValueString",
    "ProcessElementValueType",
    "ProcessPage",
    "ProcessPageItem",
    "ProcessSaveElementCommand",
    "ProcessState",
    "RelatedProcess",
    "Task",
    "TaskAssignCommand",
    "TaskDefinitionSummary",
    "TaskDeleteElementCommand",
    "TaskDeleteElementValueDocumentCommand",
    "TaskElementValue",
    "TaskElementValueDocument",
    "TaskElementValueDocumentItem",
    "TaskElementValueNumber",
    "TaskElementValueObject",
    "TaskElementValuePrincipal",
    "TaskElementValuePrincipalItem",
    "TaskElementValueString",
    "TaskElementValueType",
    "TaskPage",
    "TaskPageItem",
    "TaskSaveElementCommand",
    "TaskSaveJsonFormsValueDataCommand",
    "TaskSaveJsonFormsValueDocumentResponseCommand",
    "TaskState",
    "WebhookEvent",
    "WebhookEventProcessStateChanged",
    "WebhookEventProcessStateChangedData",
    "WebhookEventTaskStateChanged",
    "WebhookEventTaskStateChangedData",
    "WebhookType",
    "Worker",
    # From models
    "Document",
    "JsonFormsFile",
    "JsonFormsPrincipal",
    "ProcessSaveUserActionValueDocumentCommand",
    "TaskSaveElementValueDocumentCommand",
    "TaskSaveJsonFormsValueDocumentRequestCommand",
]


# For usability, we must include in __all__, all the items of the model generated package
# So this assertion is to avoid forgetfulness.
assert all(item in __all__ for item in _all_generated_models)
