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

import os
from dataclasses import dataclass, field
from typing import List, Optional

import robot
from temporalio import activity
from temporalio.exceptions import ApplicationError

from kuflow_temporal_common.activity_utils import auto_heartbeater
from kuflow_temporal_common.exceptions import KuFlowFailureType


def _default_variables() -> List[str]:
    return []


def _default_additional_options() -> dict:
    return {}


@dataclass
class ExecuteRobotRequest:
    """Data class for execute robot activity.

    Attributes:
        tests: Paths to test case files/directories to be executed similarly
            as when running the ``robot`` command on the command line.
            If the KUFLOW_ROBOT_PATH environment variable defined in the
            activity worker exists, its content is added as a prefix to the
            value of this field.
        variables: Options to configure and control execution.
            Take precedence over possible "variable" key present in :param options.
            Take precedence over default_variables in :class:`RobotFrameworkActivities`.
            Values are merged.
            Please see :func:`robot.run.run` docstring to more info
        options: Options to configure and control execution.
            Take precedence over default_options in :class:`RobotFrameworkActivities`
            Values are merged.
            Please see :func:`robot.run.run` docstring to more info
    """

    tests: str

    variables: List[str] = field(default_factory=_default_variables)

    options: dict = field(default_factory=_default_additional_options)


class RobotFrameworkActivities:
    """
    Set of Temporal.io activities to manage Robot Framework activities

    Arguments:
        default_variables (Optional[List[str]]): Variables to pass to the robot.
            Format: ["<key>:<value>"]. Example: ["key1:value1", "key2:000"]
            It is equivalent to setting the variables on the command line of 'robot'.
            Important. Take precedence over "variable" key in :arg default_options. Values are merged.
            We recommend avoiding the "variable" key in default_options and using the
            default_variables field for it.
            These variables can be overridden in activity invocations.
        default_options (Optional[dict]): Options to configure and control execution.
            These options can be overridden in activity invocations.
            Please see :func:`robot.run.run` docstring to more info.
    """

    def __init__(
        self,
        default_variables: Optional[List[str]] = None,
        default_options: Optional[dict] = None,
    ) -> None:
        if default_options is None:
            default_options = {}
        if default_variables is None:
            default_variables = []

        merge_variables = self._merge_variables(default_options.get("variable"), default_variables)
        options = {**default_options, **{"variable": merge_variables}}

        self._default_options = options
        self.activities = [self.execute_robot]

    @activity.defn(name="KuFlow_RobotFramework_ExecuteRobot")
    @auto_heartbeater
    async def execute_robot(self, request: ExecuteRobotRequest):
        # Prepare
        merge_variables_in_request = self._merge_variables(request.options.get("variable"), request.variables)
        merge_variables_in_default = self._merge_variables(
            self._default_options.get("variable"), merge_variables_in_request
        )
        options = {**self._default_options, **{"variable": merge_variables_in_default}}

        tests = self._prepend_robot_path_variable(request.tests)

        # Run
        robot_code = robot.run(tests, **options)

        if robot_code != 0:
            raise ApplicationError(
                f"Robot finished with undesired status value of ${robot_code}",
                type=KuFlowFailureType.ACTIVITIES_FAILURE,
            )

    def _merge_variables(self, variables: List = None, variables_overwrite: List = None):
        # Merge two lists of variables, giving priority to those in variables_overwrite
        if variables_overwrite is None:
            variables_overwrite = []
        if variables is None:
            variables = []

        merge_variables = variables_overwrite + variables
        # Remove duplicates
        unique_variables = list({s.split(":", 1)[0]: s for s in merge_variables}.values())

        return unique_variables

    def _prepend_robot_path_variable(self, relative_path):
        # Check if the "KUFLOW_ROBOT_PATH" environment variable is defined
        robot_path = os.getenv("KUFLOW_ROBOT_PATH")

        # If is defined, prepend it to the relative path
        if robot_path is not None:
            absolute_path = os.path.join(robot_path, relative_path)
            return absolute_path
        else:
            return relative_path
