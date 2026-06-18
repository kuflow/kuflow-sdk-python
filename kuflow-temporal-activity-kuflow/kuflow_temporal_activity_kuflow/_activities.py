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

from temporalio import activity

from kuflow_rest import KuFlowRestClient
from kuflow_rest import models as models_rest
from kuflow_temporal_common import create_application_error

from . import _validation as validation
from . import models as models_temporal


class KuFlowActivities:
    def __init__(self, kuflow_client: KuFlowRestClient) -> None:
        self._kuflow_client = kuflow_client
        self.activities = [
            self.retrieve_principal,
            self.retrieve_tenant_user,
            self.find_processes,
            self.retrieve_process,
            self.update_process_entity,
            self.patch_process_entity,
            self.update_process_metadata,
            self.patch_process_metadata,
            self.change_process_initiator,
            self.find_process_items,
            self.retrieve_process_item,
            self.create_process_item,
            self.complete_process_item_task,
            self.claim_process_item_task,
            self.assign_process_item_task,
            self.update_process_item_task_data,
            self.patch_process_item_task_data,
            self.update_process_item_task_context_data,
            self.append_process_item_task_log,
            self.retrieve_process_item_ai_assistance,
            self.generate_process_item_ai_assistance,
            self.cancel_process_items,
            self.find_business_artifacts,
            self.create_business_artifact,
            self.retrieve_business_artifact,
            self.delete_business_artifact,
            self.update_business_artifact,
            self.patch_business_artifact,
            self.create_business_artifact_action,
            self.retrieve_business_artifact_action,
            self.cancel_business_artifact_action,
            self.prepare_business_artifact_create_artifact,
        ]

    @activity.defn(name="KuFlow_Engine_retrievePrincipal")
    async def retrieve_principal(
        self,
        request: models_temporal.PrincipalRetrieveRequest,
    ) -> models_temporal.PrincipalRetrieveResponse:
        try:
            validation.validate_retrieve_principal_request(request)

            principal = self._kuflow_client.principal.retrieve_principal(id=request.principal_id)

            return models_temporal.PrincipalRetrieveResponse(principal=principal)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_retrieveTenantUser")
    async def retrieve_tenant_user(
        self,
        request: models_temporal.TenantUserRetrieveRequest,
    ) -> models_temporal.TenantUserRetrieveResponse:
        try:
            validation.validate_retrieve_tenant_user_request(request)

            tenant_user = self._kuflow_client.tenant_user.retrieve_tenant_user(id=request.tenant_user_id)

            return models_temporal.TenantUserRetrieveResponse(tenant_user=tenant_user)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_findProcesses")
    async def find_processes(
        self,
        request: models_temporal.ProcessFindRequest,
    ) -> models_temporal.ProcessFindResponse:
        try:
            # Get all non-None properties of the object to avoid overwrite defaults
            non_none_props = {k: v for k, v in vars(request).items() if v is not None}
            proces_page = self._kuflow_client.process.find_processes(**non_none_props)

            return models_temporal.ProcessFindResponse(processes=proces_page)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_retrieveProcess")
    async def retrieve_process(
        self,
        request: models_temporal.ProcessRetrieveRequest,
    ) -> models_temporal.ProcessRetrieveResponse:
        try:
            validation.validate_retrieve_process_request(request)

            process = self._kuflow_client.process.retrieve_process(id=request.process_id)

            return models_temporal.ProcessRetrieveResponse(process=process)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_updateProcessEntity")
    async def update_process_entity(
        self,
        request: models_temporal.ProcessEntityUpdateRequest,
    ) -> models_temporal.ProcessEntityUpdateResponse:
        try:
            validation.validate_process_entity_update_request(request)

            params = models_rest.ProcessEntityUpdateParams(entity=request.entity)

            process = self._kuflow_client.process.update_process_entity(
                id=request.process_id, process_entity_update_params=params
            )

            return models_temporal.ProcessEntityUpdateResponse(process=process)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_patchProcessEntity")
    async def patch_process_entity(
        self,
        request: models_temporal.ProcessEntityPatchRequest,
    ) -> models_temporal.ProcessEntityPatchResponse:
        try:
            validation.validate_process_entity_patch_request(request)

            json_patch = request.json_patch

            process = self._kuflow_client.process.patch_process_entity(id=request.process_id, json_patch=json_patch)

            return models_temporal.ProcessEntityPatchResponse(process=process)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_updateProcessMetadata")
    async def update_process_metadata(
        self,
        request: models_temporal.ProcessMetadataUpdateRequest,
    ) -> models_temporal.ProcessMetadataUpdateResponse:
        try:
            validation.validate_process_metadata_update_request(request)

            params = models_rest.ProcessMetadataUpdateParams(metadata=request.metadata)

            process = self._kuflow_client.process.update_process_metadata(
                id=request.process_id, process_metadata_update_params=params
            )

            return models_temporal.ProcessMetadataUpdateResponse(process=process)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_patchProcessMetadata")
    async def patch_process_metadata(
        self,
        request: models_temporal.ProcessMetadataPatchRequest,
    ) -> models_temporal.ProcessMetadataPatchResponse:
        try:
            validation.validate_process_metadata_patch_request(request)

            process = self._kuflow_client.process.patch_process_metadata(
                id=request.process_id, json_patch=request.json_patch
            )

            return models_temporal.ProcessMetadataPatchResponse(process=process)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_changeProcessInitiator")
    async def change_process_initiator(
        self,
        request: models_temporal.ProcessInitiatorChangeRequest,
    ) -> models_temporal.ProcessInitiatorChangeResponse:
        try:
            validation.validate_process_initiator_change_request(request)

            params = models_rest.ProcessChangeInitiatorParams(
                initiator_id=request.initiator_id, initiator_email=request.initiator_email
            )

            process = self._kuflow_client.process.change_process_initiator(
                id=request.process_id, process_change_initiator_params=params
            )

            return models_temporal.ProcessInitiatorChangeResponse(process=process)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_findProcessItems")
    async def find_process_items(
        self,
        request: models_temporal.ProcessItemFindRequest,
    ) -> models_temporal.ProcessItemFindResponse:
        try:
            process_items = self._kuflow_client.process_item.find_process_items(
                size=request.size,
                page=request.page,
                sort=request.sorts,
                process_id=request.process_ids,
                type=request.types,
                task_state=request.task_states,
                process_item_definition_code=request.process_item_definition_codes,
                process_definition_id=request.process_definition_ids,
                process_definition_code=request.process_definition_codes,
                tenant_id=request.tenant_ids,
            )

            return models_temporal.ProcessItemFindResponse(process_items=process_items)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_retrieveProcessItem")
    async def retrieve_process_item(
        self,
        request: models_temporal.ProcessItemRetrieveRequest,
    ) -> models_temporal.ProcessItemRetrieveResponse:
        try:
            validation.validate_process_item_retrieve_request(request)

            process_item = self._kuflow_client.process_item.retrieve_process_item(id=request.process_item_id)

            return models_temporal.ProcessItemRetrieveResponse(process_item=process_item)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_createProcessItem")
    async def create_process_item(
        self,
        request: models_temporal.ProcessItemCreateRequest,
    ) -> models_temporal.ProcessItemCreateResponse:
        try:
            validation.validate_process_item_create_request(request)

            params = models_rest.ProcessItemCreateParams(
                id=request.id,
                type=request.type,
                process_id=request.process_id,
                owner_id=request.owner_id,
                owner_email=request.owner_email,
                process_item_definition_code=request.process_item_definition_code,
                task=request.task,
                message=request.message,
            )

            process_item = self._kuflow_client.process_item.create_process_item(process_item_create_params=params)

            return models_temporal.ProcessItemCreateResponse(process_item=process_item)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_completeProcessItemTask")
    async def complete_process_item_task(
        self,
        request: models_temporal.ProcessItemTaskCompleteRequest,
    ) -> models_temporal.ProcessItemTaskCompleteResponse:
        try:
            validation.validate_process_item_task_complete_request(request)

            process_item = self._kuflow_client.process_item.complete_process_item_task(id=request.process_item_id)

            return models_temporal.ProcessItemTaskCompleteResponse(process_item=process_item)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_claimProcessItemTask")
    async def claim_process_item_task(
        self,
        request: models_temporal.ProcessItemTaskClaimRequest,
    ) -> models_temporal.ProcessItemTaskClaimResponse:
        try:
            validation.validate_process_item_task_claim_request(request)

            process_item = self._kuflow_client.process_item.claim_process_item_task(id=request.process_item_id)

            return models_temporal.ProcessItemTaskClaimResponse(process_item=process_item)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_assignProcessItemTask")
    async def assign_process_item_task(
        self,
        request: models_temporal.ProcessItemTaskAssignRequest,
    ) -> models_temporal.ProcessItemTaskAssignResponse:
        try:
            validation.validate_process_item_task_assign_request(request)

            params = models_rest.ProcessItemTaskAssignParams(owner_id=request.owner_id, owner_email=request.owner_email)

            process_item = self._kuflow_client.process_item.assign_process_item_task(
                id=request.process_item_id, process_item_task_assign_params=params
            )

            return models_temporal.ProcessItemTaskAssignResponse(process_item=process_item)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_updateProcessItemTaskData")
    async def update_process_item_task_data(
        self,
        request: models_temporal.ProcessItemTaskDataUpdateRequest,
    ) -> models_temporal.ProcessItemTaskDataUpdateResponse:
        try:
            validation.validate_process_item_task_data_update_request(request)

            params = models_rest.ProcessItemTaskDataUpdateParams(data=request.data)

            process_item = self._kuflow_client.process_item.update_process_item_task_data(
                id=request.process_item_id, process_item_task_data_update_params=params
            )

            return models_temporal.ProcessItemTaskDataUpdateResponse(process_item=process_item)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_patchProcessItemTaskData")
    async def patch_process_item_task_data(
        self,
        request: models_temporal.ProcessItemTaskDataPatchRequest,
    ) -> models_temporal.ProcessItemTaskDataPatchResponse:
        try:
            validation.validate_process_item_task_data_patch_request(request)

            process_item = self._kuflow_client.process_item.patch_process_item_task_data(
                id=request.process_item_id, json_patch=request.json_patch
            )

            return models_temporal.ProcessItemTaskDataPatchResponse(process_item=process_item)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_appendProcessItemTaskLog")
    async def append_process_item_task_log(
        self,
        request: models_temporal.ProcessItemTaskLogAppendRequest,
    ) -> models_temporal.ProcessItemTaskLogAppendResponse:
        try:
            validation.validate_process_item_task_log_append_request(request)

            params = models_rest.ProcessItemTaskAppendLogParams(level=request.level, message=request.message)

            process_item = self._kuflow_client.process_item.append_process_item_task_log(
                id=request.process_item_id, process_item_task_append_log_params=params
            )

            return models_temporal.ProcessItemTaskLogAppendResponse(process_item=process_item)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_updateProcessItemTaskContextData")
    async def update_process_item_task_context_data(
        self,
        request: models_temporal.ProcessItemTaskContextDataUpdateRequest,
    ) -> models_temporal.ProcessItemTaskContextDataUpdateResponse:
        try:
            validation.validate_process_item_task_context_data_update_request(request)

            params = models_rest.ProcessItemTaskContextDataUpdateParams(data=request.data)

            process_item = self._kuflow_client.process_item.update_process_item_task_context_data(
                id=request.process_item_id, process_item_task_context_data_update_params=params
            )

            return models_temporal.ProcessItemTaskContextDataUpdateResponse(process_item=process_item)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_retrieveProcessItemAiAssistance")
    async def retrieve_process_item_ai_assistance(
        self,
        request: models_temporal.ProcessItemAiAssistanceRetrieveRequest,
    ) -> models_temporal.ProcessItemAiAssistanceRetrieveResponse:
        try:
            validation.validate_process_item_ai_assistance_retrieve_request(request)

            process_item_ai_assistance = self._kuflow_client.process_item.retrieve_process_item_ai_assistance(
                id=request.process_item_id
            )

            return models_temporal.ProcessItemAiAssistanceRetrieveResponse(
                process_item_ai_assistance=process_item_ai_assistance
            )
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_generateProcessItemAiAssistance")
    async def generate_process_item_ai_assistance(
        self,
        request: models_temporal.ProcessItemAiAssistanceGenerateRequest,
    ) -> models_temporal.ProcessItemAiAssistanceGenerateResponse:
        try:
            validation.validate_process_item_ai_assistance_generate_request(request)

            params = models_rest.ProcessItemAiAssistanceGenerateParams(request_id=request.request_id)

            process_item_ai_assistance = self._kuflow_client.process_item.generate_process_item_ai_assistance(
                id=request.process_item_id, process_item_ai_assistance_generate_params=params
            )

            return models_temporal.ProcessItemAiAssistanceGenerateResponse(
                process_item_ai_assistance=process_item_ai_assistance
            )
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_cancelProcessItems")
    async def cancel_process_items(
        self,
        request: models_temporal.ProcessItemsCancelRequest,
    ) -> models_temporal.ProcessItemsCancelResponse:
        try:
            validation.validate_process_items_cancel_request(request)

            process = self._kuflow_client.process.cancel_process_items(
                id=request.process_id, process_item_id=request.process_item_ids
            )

            return models_temporal.ProcessItemsCancelResponse(process=process)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_findBusinessArtifacts")
    async def find_business_artifacts(
        self,
        request: models_temporal.BusinessArtifactFindRequest,
    ) -> models_temporal.BusinessArtifactFindResponse:
        try:
            business_artifacts = self._kuflow_client.business_artifact.find_business_artifacts(
                size=request.size,
                page=request.page,
                sort=request.sorts,
                tenant_id=request.tenant_ids,
                business_artifact_definition_id=request.business_artifact_definition_ids,
                business_artifact_definition_code=request.business_artifact_definition_codes,
                value=request.values,
            )

            return models_temporal.BusinessArtifactFindResponse(business_artifacts=business_artifacts)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_createBusinessArtifact")
    async def create_business_artifact(
        self,
        request: models_temporal.BusinessArtifactCreateRequest,
    ) -> models_temporal.BusinessArtifactCreateResponse:
        try:
            validation.validate_business_artifact_create_request(request)

            params = models_rest.BusinessArtifactCreateParams(
                id=request.id,
                business_artifact_definition_id=request.business_artifact_definition_id,
                tenant_id=request.tenant_id,
                business_artifact_definition_code=request.business_artifact_definition_code,
                data=request.data,
            )

            business_artifact = self._kuflow_client.business_artifact.create_business_artifact(
                business_artifact_create_params=params
            )

            return models_temporal.BusinessArtifactCreateResponse(business_artifact=business_artifact)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_retrieveBusinessArtifact")
    async def retrieve_business_artifact(
        self,
        request: models_temporal.BusinessArtifactRetrieveRequest,
    ) -> models_temporal.BusinessArtifactRetrieveResponse:
        try:
            validation.validate_business_artifact_retrieve_request(request)

            business_artifact = self._kuflow_client.business_artifact.retrieve_business_artifact(
                id=request.business_artifact_id
            )

            return models_temporal.BusinessArtifactRetrieveResponse(business_artifact=business_artifact)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_deleteBusinessArtifact")
    async def delete_business_artifact(
        self,
        request: models_temporal.BusinessArtifactDeleteRequest,
    ) -> models_temporal.BusinessArtifactDeleteResponse:
        try:
            validation.validate_business_artifact_delete_request(request)

            self._kuflow_client.business_artifact.delete_business_artifact(id=request.business_artifact_id)

            return models_temporal.BusinessArtifactDeleteResponse()
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_updateBusinessArtifact")
    async def update_business_artifact(
        self,
        request: models_temporal.BusinessArtifactUpdateRequest,
    ) -> models_temporal.BusinessArtifactUpdateResponse:
        try:
            validation.validate_business_artifact_update_request(request)

            params = models_rest.BusinessArtifactDataUpdateParams(data=request.data)

            business_artifact = self._kuflow_client.business_artifact.update_business_artifact_data(
                id=request.business_artifact_id, business_artifact_data_update_params=params
            )

            return models_temporal.BusinessArtifactUpdateResponse(business_artifact=business_artifact)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_patchBusinessArtifact")
    async def patch_business_artifact(
        self,
        request: models_temporal.BusinessArtifactPatchRequest,
    ) -> models_temporal.BusinessArtifactPatchResponse:
        try:
            validation.validate_business_artifact_patch_request(request)

            business_artifact = self._kuflow_client.business_artifact.patch_business_artifact_data(
                id=request.business_artifact_id, json_patch=request.json_patch
            )

            return models_temporal.BusinessArtifactPatchResponse(business_artifact=business_artifact)
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_createBusinessArtifactAction")
    async def create_business_artifact_action(
        self,
        request: models_temporal.BusinessArtifactActionCreateRequest,
    ) -> models_temporal.BusinessArtifactActionCreateResponse:
        try:
            validation.validate_business_artifact_action_create_request(request)

            params = models_rest.BusinessArtifactActionCreateParams(
                business_artifact_action_definition_code=request.business_artifact_action_definition_code,
                id=request.id,
                start_workflow=request.start_workflow,
                downloadable=request.downloadable,
                start_process=request.start_process,
                create_artifact=request.create_artifact,
            )

            business_artifact_action = self._kuflow_client.business_artifact.create_business_artifact_action(
                id=request.business_artifact_id, business_artifact_action_create_params=params
            )

            return models_temporal.BusinessArtifactActionCreateResponse(
                business_artifact_action=business_artifact_action
            )
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_retrieveBusinessArtifactAction")
    async def retrieve_business_artifact_action(
        self,
        request: models_temporal.BusinessArtifactActionRetrieveRequest,
    ) -> models_temporal.BusinessArtifactActionRetrieveResponse:
        try:
            validation.validate_business_artifact_action_retrieve_request(request)

            business_artifact_action = self._kuflow_client.business_artifact.retrieve_business_artifact_action(
                id=request.business_artifact_id, action_id=request.business_artifact_action_id
            )

            return models_temporal.BusinessArtifactActionRetrieveResponse(
                business_artifact_action=business_artifact_action
            )
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_cancelBusinessArtifactAction")
    async def cancel_business_artifact_action(
        self,
        request: models_temporal.BusinessArtifactActionCancelRequest,
    ) -> models_temporal.BusinessArtifactActionCancelResponse:
        try:
            validation.validate_business_artifact_action_cancel_request(request)

            business_artifact_action = self._kuflow_client.business_artifact.cancel_business_artifact_action(
                id=request.business_artifact_id, action_id=request.business_artifact_action_id
            )

            return models_temporal.BusinessArtifactActionCancelResponse(
                business_artifact_action=business_artifact_action
            )
        except Exception as err:
            raise create_application_error(err)  # noqa: B904

    @activity.defn(name="KuFlow_Engine_prepareBusinessArtifactCreateArtifact")
    async def prepare_business_artifact_create_artifact(
        self,
        request: models_temporal.BusinessArtifactCreateArtifactPrepareRequest,
    ) -> models_temporal.BusinessArtifactCreateArtifactPrepareResponse:
        try:
            validation.validate_business_artifact_create_artifact_prepare_request(request)

            params = models_rest.BusinessArtifactCreateArtifactPrepareParams(
                business_artifact_action_definition_code=request.business_artifact_action_definition_code
            )

            business_artifact_create_artifact_prepare = (
                self._kuflow_client.business_artifact.prepare_business_artifact_create_artifact(
                    id=request.business_artifact_id,
                    business_artifact_create_artifact_prepare_params=params,
                )
            )

            return models_temporal.BusinessArtifactCreateArtifactPrepareResponse(
                business_artifact_create_artifact_prepare=business_artifact_create_artifact_prepare
            )
        except Exception as err:
            raise create_application_error(err)  # noqa: B904
