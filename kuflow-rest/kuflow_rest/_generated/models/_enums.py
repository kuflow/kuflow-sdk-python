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


class AuthenticationType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """AuthenticationType."""

    ENGINE_TOKEN = "ENGINE_TOKEN"
    ENGINE_CERTIFICATE = "ENGINE_CERTIFICATE"


class JsonPatchOperationType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The operation to perform."""

    ADD = "add"
    REMOVE = "remove"
    REPLACE = "replace"
    MOVE = "move"
    COPY = "copy"
    TEST = "test"


class PrincipalType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """PrincipalType."""

    USER = "USER"
    APPLICATION = "APPLICATION"
    SYSTEM = "SYSTEM"


class ProcessItemTaskLogLevel(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """ProcessItemTaskLogLevel."""

    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class ProcessItemTaskState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Process Item Task state."""

    READY = "READY"
    CLAIMED = "CLAIMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ProcessItemType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Process Item Type."""

    TASK = "TASK"
    MESSAGE = "MESSAGE"


class ProcessState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Process state."""

    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class RobotAssetArchitecture(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Robot asset platform architecture."""

    X86_BIT32 = "X86_32"
    X86_BIT64 = "X86_64"


class RobotAssetPlatform(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Robot asset platform."""

    WINDOWS = "WINDOWS"
    MAC_OS = "MAC_OS"
    LINUX = "LINUX"


class RobotAssetType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Robot asset type."""

    PYTHON = "PYTHON"
    PYTHON_PIP = "PYTHON_PIP"
    NODE_JS = "NODEJS"


class RobotFilterContext(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Robot filter context:


    * READY: filters out robots ready for execution for the current credentials
    * DEFAULT: filters out robots accessible for the current credentials (if no set this is the
    default option).
    """

    READY = "READY"
    DEFAULT = "DEFAULT"


class RobotSourceType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Robot source type."""

    PACKAGE = "PACKAGE"
    UNKNOWN = "UNKNOWN"


class TenantPricingPlan(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Tenant pricing plan."""

    FREE = "FREE"
    PREMIUM = "PREMIUM"
    UNLIMITED = "UNLIMITED"


class WebhookType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of the Event."""

    PROCESS_CREATED = "PROCESS.CREATED"
    PROCESS_STATE_CHANGED = "PROCESS.STATE_CHANGED"
    PROCESS_ITEM_CREATED = "PROCESS_ITEM.CREATED"
    PROCESS_ITEM_TASK_STATE_CHANGED = "PROCESS_ITEM.TASK_STATE_CHANGED"
