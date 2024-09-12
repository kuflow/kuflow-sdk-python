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
import logging
from datetime import datetime
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar, cast

from temporalio import activity


logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def auto_heartbeater(fn: F) -> F:
    # We want to ensure that the type hints from the original callable are
    # available via our wrapper, so we use the functools wraps decorator
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        heartbeat_timeout = activity.info().heartbeat_timeout
        heartbeat_task = None
        if heartbeat_timeout:
            # Heartbeat twice as often as the timeout
            heartbeat_task = asyncio.create_task(heartbeat_every(heartbeat_timeout.total_seconds() / 2))
        try:
            return await fn(*args, **kwargs)
        finally:
            if heartbeat_task:
                heartbeat_task.cancel()
                # Wait for heartbeat cancellation to complete
                await asyncio.wait([heartbeat_task])

    return cast(F, wrapper)


async def heartbeat_every(delay: float, *details: Any) -> None:
    # Heartbeat every so often while not cancelled
    while True:
        await asyncio.sleep(delay)
        logger.debug(f"Heartbeating at {datetime.now()}")
        activity.heartbeat(*details)
