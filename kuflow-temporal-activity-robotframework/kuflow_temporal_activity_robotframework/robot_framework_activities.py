from attr import dataclass
import robot

from temporalio import activity
from temporalio.exceptions import ApplicationError
from kuflow_temporal_common.activity_utils import auto_heartbeater

# from kuflow_temporal_common import activity_utils

from kuflow_temporal_common.exceptions import KuFlowFailureType

# Path to robot
# Variables


@dataclass
class ExecuteRobotRequest:
    """Data class for execute robot activity.

    :param tests: Paths to test case files/directories to be executed similarly
        as when running the ``robot`` command on the command line.
    :param options: Options to configure and control execution. Please see
        Please see :func:`robot.run.run` docstring to more info
    """

    tests: any

    options: dict


class RobotFrameworkActivities:
    def __init__(self) -> None:
        pass

    @activity.defn
    # @auto_heartbeater
    async def execute_robot(self, request: ExecuteRobotRequest):
        robot_code = robot.run(request.tests, **request.options)

        if robot_code != 0:
            raise ApplicationError(
                message=f"Robot finised with undesired status value of ${robot_code}",
                non_retryable=True,
                type=KuFlowFailureType.ACTIVITIES_VALIDATION_FAILURE,
            )
