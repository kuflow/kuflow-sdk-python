import asyncio

from kuflow_temporal_activity_robotframework import RobotFrameworkActivities
from kuflow_temporal_activity_robotframework.robot_framework_activities import ExecuteRobotRequest

my_var = "My custom variable value"


async def main():
    robot_framework_activities = RobotFrameworkActivities()

    options = {}
    options["variable"] = [
        f"my_var:{my_var}",
    ]
    execute_robot_request = ExecuteRobotRequest(
        tests="kuflow-temporal-activity-robotframework/test/test_hello.robot",
        options=options,
    )

    await robot_framework_activities.execute_robot(execute_robot_request)


if __name__ == "__main__":
    asyncio.run(main())
