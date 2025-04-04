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
import dataclasses
from typing import Any, NoReturn, Optional

import temporalio.client
import temporalio.worker
import temporalio.workflow

from ._kuflow_encryption_instrumentation import (
    KuFlowEncryptionState,
    KuFlowEncryptionWrapper,
    add_encryption_encoding,
    mark_objects_to_be_encrypted,
    retrieve_encryption_state,
)


class KuFlowEncryptionInterceptor(temporalio.client.Interceptor, temporalio.worker.Interceptor):
    def intercept_activity(
        self, next: temporalio.worker.ActivityInboundInterceptor
    ) -> temporalio.worker.ActivityInboundInterceptor:
        """Implementation of
        :py:meth:`temporalio.worker.Interceptor.intercept_activity`.
        """
        return KuFlowEncryptionActivityInboundInterceptor(next, self)

    def workflow_interceptor_class(
        self, input: temporalio.worker.WorkflowInterceptorClassInput
    ) -> Optional[type[temporalio.worker.WorkflowInboundInterceptor]]:
        """Implementation of
        :py:meth:`temporalio.worker.Interceptor.workflow_interceptor_class`.
        """
        return KuFlowEncryptionWorkflowInboundInterceptor


class KuFlowEncryptionActivityInboundInterceptor(temporalio.worker.ActivityInboundInterceptor):
    def __init__(
        self,
        next: temporalio.worker.ActivityInboundInterceptor,
        root: KuFlowEncryptionInterceptor,
    ) -> None:
        super().__init__(next)
        self.root = root

    async def execute_activity(self, input: temporalio.worker.ExecuteActivityInput) -> Any:
        output = await super().execute_activity(input)

        encryption_state = retrieve_encryption_state(input.headers)

        return KuFlowEncryptionWrapper(encryption_state=encryption_state, value=output)


class KuFlowEncryptionWorkflowInboundInterceptor(temporalio.worker.WorkflowInboundInterceptor):
    """Tracing interceptor for workflow calls.

    See :py:class:`TracingInterceptor` docs on why one might want to subclass
    this class.
    """

    def __init__(self, next: temporalio.worker.WorkflowInboundInterceptor) -> None:
        """Initialize a tracing workflow interceptor."""
        super().__init__(next)
        self.encryption_state = KuFlowEncryptionState(key_id=None)

    def init(self, outbound: temporalio.worker.WorkflowOutboundInterceptor) -> None:
        """Implementation of
        :py:meth:`temporalio.worker.WorkflowInboundInterceptor.init`.
        """
        super().init(KuFlowEncryptionWorkflowOutboundInterceptor(outbound, self))

    async def execute_workflow(self, input: temporalio.worker.ExecuteWorkflowInput) -> Any:
        """Implementation of
        :py:meth:`temporalio.worker.WorkflowInboundInterceptor.execute_workflow`.
        """

        encryption_state_current = retrieve_encryption_state(input.headers)

        self.encryption_state.merge(encryption_state_current)

        output = await super().execute_workflow(input)

        return KuFlowEncryptionWrapper(encryption_state=self.encryption_state, value=output)

    async def handle_query(self, input: temporalio.worker.HandleQueryInput) -> Any:
        """Implementation of
        :py:meth:`temporalio.worker.WorkflowInboundInterceptor.handle_query`.
        """
        output = await super().handle_query(input)

        return KuFlowEncryptionWrapper(encryption_state=self.encryption_state, value=output)

    async def handle_update_handler(self, input: temporalio.worker.HandleUpdateInput) -> Any:
        """Implementation of
        :py:meth:`temporalio.worker.WorkflowInboundInterceptor.handle_update_handler`.
        """
        output = await super().handle_update_handler(input)

        return KuFlowEncryptionWrapper(encryption_state=self.encryption_state, value=output)


class KuFlowEncryptionWorkflowOutboundInterceptor(temporalio.worker.WorkflowOutboundInterceptor):
    def __init__(
        self,
        next: temporalio.worker.WorkflowOutboundInterceptor,
        root: KuFlowEncryptionWorkflowInboundInterceptor,
    ) -> None:
        super().__init__(next)
        self.root = root

    def continue_as_new(self, input: temporalio.worker.ContinueAsNewInput) -> NoReturn:
        headers = input.headers
        args = input.args

        headers = add_encryption_encoding(self.root.encryption_state, headers)
        args = mark_objects_to_be_encrypted(self.root.encryption_state, args)

        return super().continue_as_new(dataclasses.replace(input, headers=headers, args=args))

    async def signal_child_workflow(self, input: temporalio.worker.SignalChildWorkflowInput) -> None:
        headers = input.headers
        args = input.args

        headers = add_encryption_encoding(self.root.encryption_state, headers)
        args = mark_objects_to_be_encrypted(self.root.encryption_state, args)

        await super().signal_child_workflow(dataclasses.replace(input, headers=headers, args=args))

    async def signal_external_workflow(self, input: temporalio.worker.SignalExternalWorkflowInput) -> None:
        headers = input.headers
        args = input.args

        headers = add_encryption_encoding(self.root.encryption_state, headers)
        args = mark_objects_to_be_encrypted(self.root.encryption_state, args)

        await super().signal_external_workflow(dataclasses.replace(input, headers=headers, args=args))

    def start_activity(self, input: temporalio.worker.StartActivityInput) -> temporalio.workflow.ActivityHandle:
        headers = input.headers
        args = input.args

        headers = add_encryption_encoding(self.root.encryption_state, headers)
        args = mark_objects_to_be_encrypted(self.root.encryption_state, args)

        return super().start_activity(dataclasses.replace(input, headers=headers, args=args))

    async def start_child_workflow(
        self, input: temporalio.worker.StartChildWorkflowInput
    ) -> temporalio.workflow.ChildWorkflowHandle:
        headers = input.headers
        args = input.args

        headers = add_encryption_encoding(self.root.encryption_state, headers)
        args = mark_objects_to_be_encrypted(self.root.encryption_state, args)

        return await super().start_child_workflow(dataclasses.replace(input, headers=headers, args=args))

    def start_local_activity(
        self, input: temporalio.worker.StartLocalActivityInput
    ) -> temporalio.workflow.ActivityHandle:
        headers = input.headers
        args = input.args

        headers = add_encryption_encoding(self.root.encryption_state, headers)
        args = mark_objects_to_be_encrypted(self.root.encryption_state, args)

        return super().start_local_activity(dataclasses.replace(input, headers=headers, args=args))
