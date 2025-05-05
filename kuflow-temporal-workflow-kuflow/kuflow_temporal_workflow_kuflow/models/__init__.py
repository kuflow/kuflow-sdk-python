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

from ._enums import SignalProcessItemType, WorkflowUserActionDefinitionType
from ._models import (
    KUFLOW_ENGINE_SIGNAL_PROCESS_ITEM,
    SignalProcessItem,
    SignalProcessItemPayload,
    SignalUserAction,
    WorkflowRequest,
    WorkflowResponse,
    WorkflowRobotRequest,
    WorkflowRobotResponse,
    WorkflowUserActionRequest,
    WorkflowUserActionResponse,
)


__all__ = [
    "KUFLOW_ENGINE_SIGNAL_PROCESS_ITEM",
    "SignalProcessItem",
    "SignalProcessItemPayload",
    "SignalProcessItemType",
    "SignalUserAction",
    "WorkflowRequest",
    "WorkflowResponse",
    "WorkflowRobotRequest",
    "WorkflowRobotResponse",
    "WorkflowUserActionDefinitionType",
    "WorkflowUserActionRequest",
    "WorkflowUserActionResponse",
]

from kuflow_rest import models as models_rest
from kuflow_temporal_common import register_serializable_models

from .. import models as models_workflow


register_serializable_models(models_rest.__dict__)
register_serializable_models(models_workflow.__dict__)
