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

    :param tests: Paths to test case files/directories to be executed similarly
        as when running the ``robot`` command on the command line.
    :param variables: Options to configure and control execution.
        Take precedence over "variable" key in :param options. Values are merged.
        Take precedence over default_variables in :class:`RobotFrameworkActivities`.
        Values are merged.
        Please see :func:`robot.run.run` docstring to more info
    :param options: Options to configure and control execution. Please see
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

       Args:
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
        default_variables: Optional[List[str]] = [],
        default_options: Optional[dict] = {},
    ) -> None:
        merge_variables = self._merge_variables(default_options.get("variable"), default_variables)
        options = {**default_options, **{"variable": merge_variables}}

        self._default_options = options
        self.activities = [self.execute_robot]

    @activity.defn
    @auto_heartbeater
    async def execute_robot(self, request: ExecuteRobotRequest):
        # Prepare
        merge_variables_in_request = self._merge_variables(request.options.get("variable"), request.variables)
        merge_variables_in_default = self._merge_variables(
            self._default_options.get("variable"), merge_variables_in_request
        )
        options = {**self._default_options, **{"variable": merge_variables_in_default}}

        # Run
        robot_code = robot.run(request.tests, **options)

        if robot_code != 0:
            raise ApplicationError(
                message=f"Robot finised with undesired status value of ${robot_code}",
                non_retryable=True,
                type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            )

    def _merge_variables(self, variables=[], variables_overwrite=[]):
        # First variables defined take priority
        variables = [] if variables is None else variables
        variables_overwrite = [] if variables_overwrite is None else variables_overwrite
        merge_variables = variables_overwrite + variables
        unique_variables = list({s.split(":")[0]: s for s in merge_variables}.values())

        return unique_variables
