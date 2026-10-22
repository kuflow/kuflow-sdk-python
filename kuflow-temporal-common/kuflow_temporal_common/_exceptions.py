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

import json
from enum import Enum
from typing import Any, Optional

from azure.core.exceptions import HttpResponseError
from temporalio.exceptions import ApplicationError

from kuflow_rest import models as models_rest


class KuFlowFailureType(str, Enum):
    ACTIVITIES_FAILURE = "KuFlowActivities.Failure"

    ACTIVITIES_REST_FAILURE = "KuFlowActivities.RestFailure"

    ACTIVITIES_VALIDATION_FAILURE = "KuFlowActivities.ValidationFailure"


def create_application_error(e: Exception) -> ApplicationError:
    if isinstance(e, ApplicationError):
        return e

    # The exception is only the cause: as a detail it is not serializable and Temporal fails to encode the failure.
    error: ApplicationError
    if isinstance(e, HttpResponseError):
        default_error = _find_default_error(e)
        details = [] if default_error is None else [default_error]
        error = ApplicationError("Rest Invocation error", *details, type=KuFlowFailureType.ACTIVITIES_REST_FAILURE)
    else:
        error = ApplicationError("Invocation error", type=KuFlowFailureType.ACTIVITIES_FAILURE)
    error.__cause__ = e

    return error


def _find_default_error(e: HttpResponseError) -> Optional[dict[str, Any]]:
    """
    Find the ``DefaultError`` answered by the KuFlow API, serialized with its JSON keys (as Java and JS send it).

    azure-core only deserializes it into ``e.model`` for the unmapped status codes; for the mapped ones (401, 404,
    409, 304) it raises before deserializing, so in that case the body of ``e.response`` is parsed.
    """
    default_error = e.model if isinstance(e.model, models_rest.DefaultError) else None

    if default_error is None and e.response is not None:
        try:
            body = json.loads(e.response.text())
            if isinstance(body, dict):
                default_error = models_rest.DefaultError.deserialize(body)
        except Exception:
            default_error = None

    if default_error is None:
        return None

    serialized = default_error.serialize(keep_readonly=True)

    return serialized or None
