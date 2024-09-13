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

from enum import Enum

from azure.core.exceptions import HttpResponseError
from temporalio.exceptions import ApplicationError


class KuFlowFailureType(str, Enum):
    ACTIVITIES_FAILURE = "KuFlowActivities.Failure"

    ACTIVITIES_REST_FAILURE = "KuFlowActivities.RestFailure"

    ACTIVITIES_VALIDATION_FAILURE = "KuFlowActivities.ValidationFailure"


def create_application_error(e: Exception) -> ApplicationError:
    if isinstance(e, ApplicationError):
        return e

    if isinstance(e, HttpResponseError):
        return ApplicationError("Rest Invocation error", e, type=KuFlowFailureType.ACTIVITIES_REST_FAILURE)

    return ApplicationError("Invocation error", e, type=KuFlowFailureType.ACTIVITIES_FAILURE)
