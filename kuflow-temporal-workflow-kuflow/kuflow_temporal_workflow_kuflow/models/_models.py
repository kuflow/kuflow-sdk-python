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

import datetime
from typing import TYPE_CHECKING, Any, Optional

from kuflow_rest._generated import _serialization


if TYPE_CHECKING:
    from .. import models as _models

KUFLOW_ENGINE_SIGNAL_PROCESS_ITEM = "KuFlow_Engine_Signal_Process_Item"


class WorkflowRequest(_serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "request_time": {"key": "requestTime", "type": "iso-8601"},
        "request_time_zone": {"key": "requestTimeZone", "type": "str"},
    }

    def __init__(self, process_id: str, request_time: datetime.datetime, request_time_zone: str, **kwargs: Any) -> None:
        """
        Parameters:
            process_id: Identifier of the related created process
            request_time: Request time of the related created process
            request_time_zone: Request time zone of the related created process
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.request_time = request_time
        self.request_time_zone = request_time_zone


class WorkflowResponse(_serialization.Model):
    _attribute_map = {
        "message": {"key": "message", "type": "str"},
    }

    def __init__(self, message: Optional[str] = None, **kwargs: Any) -> None:
        """
        Parameters:
            message: Response message
        """
        super().__init__(**kwargs)
        self.message = message


class WorkflowUserActionRequest(_serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "user_action_definition_type": {"key": "userActionDefinitionType", "type": "WorkflowUserActionDefinitionType"},
        "user_action_definition_code": {"key": "userActionDefinitionCode", "type": "str"},
        "user_action_id": {"key": "userActionId", "type": "str"},
        "requestor_principal_id": {"key": "requestorPrincipalId", "type": "str"},
        "request_time": {"key": "requestTime", "type": "iso-8601"},
        "request_time_zone": {"key": "requestTimeZone", "type": "str"},
    }

    def __init__(
        self,
        process_id: str,
        user_action_definition_type: "_models.WorkflowUserActionDefinitionType",
        user_action_definition_code: str,
        user_action_id: str,
        requestor_principal_id: str,
        request_time: datetime.datetime,
        request_time_zone: str,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_id: Identifier of the related process
            user_action_definition_type: Type of the user action definition
            user_action_definition_code: Code of the user action definition
            user_action_id: Identifier of the user action
            requestor_principal_id: Identifier of the principal that request the user action
            request_time: The timestamp when the request was made.
            request_time_zone: The time zone associated with the request.
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.user_action_definition_type = user_action_definition_type
        self.user_action_definition_code = user_action_definition_code
        self.user_action_id = user_action_id
        self.requestor_principal_id = requestor_principal_id
        self.request_time = request_time
        self.request_time_zone = request_time_zone


class WorkflowUserActionResponse(_serialization.Model):
    _attribute_map = {
        "message": {"key": "message", "type": "str"},
    }

    def __init__(self, message: Optional[str] = None, **kwargs: Any) -> None:
        """
        Parameters:
            message: User action message response
        """
        super().__init__(**kwargs)
        self.message = message


class WorkflowRobotRequest(_serialization.Model):
    _attribute_map = {
        "process_id": {"key": "processId", "type": "str"},
        "process_item_id": {"key": "processItemId", "type": "str"},
        "robot_id": {"key": "robotId", "type": "str"},
        "robot_operation": {"key": "robotOperation", "type": "str"},
        "request_time": {"key": "requestTime", "type": "iso-8601"},
        "request_time_zone": {"key": "requestTimeZone", "type": "str"},
    }

    def __init__(
        self,
        process_id: str,
        process_item_id: str,
        robot_id: str,
        robot_operation: str,
        request_time: datetime.datetime,
        request_time_zone: str,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_id: The unique identifier of a process.
            process_item_id: The identifier of a specific process item within a workflow.
            robot_id: The unique identifier of the robot associated with the workflow process item task.
            robot_operation: The operation to be performed by the robot within the workflow process.
            request_time: The timestamp when the request was made.
            request_time_zone: The time zone associated with the request.
        """
        super().__init__(**kwargs)
        self.process_id = process_id
        self.process_item_id = process_item_id
        self.robot_id = robot_id
        self.robot_operation = robot_operation
        self.request_time = request_time
        self.request_time_zone = request_time_zone


class WorkflowRobotResponse(_serialization.Model):
    _attribute_map = {
        "message": {"key": "message", "type": "str"},
    }

    def __init__(self, message: Optional[str] = None, **kwargs: Any) -> None:
        """
        Parameters:
            message: Response message
        """
        super().__init__(**kwargs)
        self.message = message


class SignalProcessItemPayload(_serialization.Model):
    _attribute_map = {
        "process_item_definition_code": {"key": "processItemDefinitionCode", "type": "str"},
        "data_structure_data_definition_code": {"key": "dataStructureDataDefinitionCode", "type": "str"},
    }

    def __init__(
        self,
        process_item_definition_code: Optional[str],
        data_structure_data_definition_code: Optional[str],
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            process_item_definition_code: Process Item definition code
            data_structure_data_definition_code: Data structure data definition code
        """
        super().__init__(**kwargs)
        self.process_item_definition_code = process_item_definition_code
        self.data_structure_data_definition_code = data_structure_data_definition_code


class SignalProcessItem(_serialization.Model):
    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "type": {"key": "type", "type": "SignalProcessItemType"},
        "payload": {"key": "payload", "type": "SignalProcessItemPayload"},
        "request_time": {"key": "requestTime", "type": "iso-8601"},
        "request_time_zone": {"key": "requestTimeZone", "type": "str"},
    }

    def __init__(
        self,
        id: str,
        type: "_models.SignalProcessItemType",
        payload: "_models.SignalProcessItemPayload",
        request_time: datetime.datetime,
        request_time_zone: str,
        **kwargs: Any,
    ) -> None:
        """
        Parameters:
            id: Process item Id
            type: Process item type
            payload: Process item signal payload
            request_time: The timestamp when the request was made.
            request_time_zone: The time zone associated with the request.
        """
        super().__init__(**kwargs)
        self.id = id
        self.type = type
        self.payload = payload
        self.request_time = request_time
        self.request_time_zone = request_time_zone


class SignalUserAction(_serialization.Model):
    _attribute_map = {
        "user_action_definition_code": {"key": "userActionDefinitionCode", "type": "str"},
        "request_instant": {"key": "requestInstant", "type": "iso-8601"},
    }

    def __init__(self, user_action_definition_code: str, request_instant: datetime.datetime, **kwargs: Any) -> None:
        """
        Parameters:
            user_action_definition_code: Code of the user action definition
            request_instant: Instant at which the user action was requested
        """
        super().__init__(**kwargs)
        self.user_action_definition_code = user_action_definition_code
        self.request_instant = request_instant
