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

from .._generated.models import __all__ as _all_generated_models

from .._generated.models import (
    AbstractAudited,
    Authentication,
    DefaultError,
    DefaultErrorInfo,
    Log,
    Page,
    PageMetadata,
    Principal,
    PrincipalApplication,
    PrincipalPage,
    PrincipalUser,
    Process,
    ProcessChangeInitiatorCommand,
    ProcessDefinitionSummary,
    ProcessDeleteElementCommand,
    ProcessElementValue,
    ProcessElementValueNumber,
    ProcessElementValueString,
    ProcessPage,
    ProcessPageItem,
    ProcessSaveElementCommand,
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
    TaskPage,
    TaskPageItem,
    TaskSaveElementCommand,
    WebhookEvent,
    WebhookEventProcessStateChanged,
    WebhookEventProcessStateChangedData,
    WebhookEventTaskStateChanged,
    WebhookEventTaskStateChangedData,
    AuditedObjectType,
    LogLevel,
    PagedObjectType,
    PrincipalType,
    ProcessElementValueType,
    ProcessState,
    TaskElementValueType,
    TaskState,
    WebhookType,
)

from ._models import Document, TaskSaveElementValueDocumentCommand, ProcessSaveUserActionValueDocumentCommand


__all__ = [
    # From _generated.models
    "AbstractAudited",
    "Authentication",
    "DefaultError",
    "DefaultErrorInfo",
    "Log",
    "Page",
    "PageMetadata",
    "Principal",
    "PrincipalApplication",
    "PrincipalPage",
    "PrincipalUser",
    "Process",
    "ProcessChangeInitiatorCommand",
    "ProcessDefinitionSummary",
    "ProcessDeleteElementCommand",
    "ProcessElementValue",
    "ProcessElementValueNumber",
    "ProcessElementValueString",
    "ProcessPage",
    "ProcessPageItem",
    "ProcessSaveElementCommand",
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
    "TaskPage",
    "TaskPageItem",
    "TaskSaveElementCommand",
    "WebhookEvent",
    "WebhookEventProcessStateChanged",
    "WebhookEventProcessStateChangedData",
    "WebhookEventTaskStateChanged",
    "WebhookEventTaskStateChangedData",
    "AuditedObjectType",
    "LogLevel",
    "PagedObjectType",
    "PrincipalType",
    "ProcessElementValueType",
    "ProcessState",
    "TaskElementValueType",
    "TaskState",
    "WebhookType",
    # From models
    "Document",
    "ProcessSaveUserActionValueDocumentCommand",
    "TaskSaveElementValueDocumentCommand",
]


# For usability, we must include in __all__, all the items of the model generated package
# So this assertion is to avoid forgetfulness.
assert all(item in __all__ for item in _all_generated_models)
