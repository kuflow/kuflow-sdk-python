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

from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


class AuditedObjectType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Audited object Types.
    """

    PROCESS = "PROCESS"
    PROCESS_PAGE_ITEM = "PROCESS_PAGE_ITEM"
    TASK = "TASK"
    TASK_PAGE_ITEM = "TASK_PAGE_ITEM"
    AUTHENTICATION = "AUTHENTICATION"

class LogLevel(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """LogLevel.
    """

    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"

class PagedObjectType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Paged Model types.
    """

    PRINCIPAL_PAGE = "PRINCIPAL_PAGE"
    PROCESS_PAGE = "PROCESS_PAGE"
    TASK_PAGE = "TASK_PAGE"

class PrincipalType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """PrincipalType.
    """

    USER = "USER"
    APPLICATION = "APPLICATION"
    SYSTEM = "SYSTEM"

class ProcessElementValueType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Process element value types.
    """

    STRING = "STRING"
    NUMBER = "NUMBER"

class ProcessState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Process state.
    """

    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class TaskElementValueType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """TaskElementValueType.
    """

    STRING = "STRING"
    NUMBER = "NUMBER"
    OBJECT = "OBJECT"
    DOCUMENT = "DOCUMENT"
    PRINCIPAL = "PRINCIPAL"

class TaskState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Task state.
    """

    READY = "READY"
    CLAIMED = "CLAIMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class WebhookType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of the Event.
    """

    PROCESS_STATE_CHANGED = "PROCESS.STATE_CHANGED"
    TASK_STATE_CHANGED = "TASK.STATE_CHANGED"
