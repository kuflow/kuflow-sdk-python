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

import asyncio
import datetime
import logging
from typing import Mapping, Optional

from temporalio.client import Client

from kuflow_rest import models
from kuflow_temporal_common._connection_config import (
    KuFlowAuthorizationTokenProviderBackoff,
    KuFlowConfig,
    TemporalConfig,
)


logger = logging.getLogger(__name__)


class KuFlowAuthorizationTokenProvider:
    def __init__(
        self,
        kuflow_config: KuFlowConfig,
        temporal_config: TemporalConfig,
    ):
        self._temporal_client: Optional[Client] = None
        self._temporal_config = temporal_config
        self._kuflow_config = kuflow_config
        self._consecutive_failures = 0
        self._backoff = (
            kuflow_config.authorization_token_provider_backoff
            if kuflow_config.authorization_token_provider_backoff
            else KuFlowAuthorizationTokenProviderBackoff()
        )

    def initialize_rpc_auth_metadata(self, init_metadata=None) -> Mapping[str, str]:
        if init_metadata is None:
            init_metadata = {}

        authentication = self._create_authentication()
        metadata = {}
        if authentication.token:
            metadata = self._set_auth_rpc_metadata(token=authentication.token, metadata=init_metadata)
        return metadata

    def start_auto_refresh(self, temporal_client: Client):
        self._temporal_client = temporal_client
        self.schedule_authorization_token_renovation()

    def schedule_authorization_token_renovation(self) -> None:
        refresh_in_seconds = 0
        asyncio.create_task(self._delayed_schedule_authorization_token_renovation(refresh_in_seconds))

    async def _delayed_schedule_authorization_token_renovation(self, refresh_in_seconds):
        await asyncio.sleep(refresh_in_seconds)
        await self._refresh_authorization_token_renovation()

    async def _refresh_authorization_token_renovation(self):
        try:
            logger.debug("Token renewal begins...")
            authentication = self._create_authentication()
            self._consecutive_failures = 0

            if authentication.token:
                new_metadata = self._set_auth_rpc_metadata(
                    token=authentication.token, metadata=self._temporal_client.rpc_metadata
                )
                self._temporal_client.rpc_metadata = new_metadata

            refresh_in_seconds = (
                (authentication.expired_at - datetime.datetime.now(authentication.expired_at.tzinfo)).total_seconds()
                if authentication.expired_at
                else 0
            )

            logger.info(f"Token renewed. Next refresh in {refresh_in_seconds} seconds")

            asyncio.create_task(self._delayed_schedule_authorization_token_renovation(refresh_in_seconds))
        except Exception as err:
            self._consecutive_failures = self._consecutive_failures + 1

            retry_duration_in_seconds = round(
                self._backoff.sleep * self._backoff.exponential_rate**self._consecutive_failures
            )
            refresh_in_seconds = min(retry_duration_in_seconds, self._backoff.max_sleep)

            logger.error(f"Token renewal failed. Nex retry in {refresh_in_seconds} seconds", err)

            asyncio.create_task(self._delayed_schedule_authorization_token_renovation(refresh_in_seconds))

    def _set_auth_rpc_metadata(self, token: str, metadata: Mapping[str, str]):
        new_metadata = dict(metadata)
        new_metadata["authorization"] = "Bearer " + token

        return new_metadata

    def _create_authentication(self) -> models.Authentication:
        authentication = models.Authentication(
            type=models.AuthenticationType.ENGINE_TOKEN,
            tenant_id=self._kuflow_config.tenant_id,
        )

        return self._kuflow_config.rest_client.authentication.create_authentication(authentication)
