import asyncio

from kuflow_temporal_activity_robotframework import RobotFrameworkActivities
from kuflow_temporal_activity_robotframework.robot_framework_activities import ExecuteRobotRequest

my_var = "My custom variable value"

my_nested_dict = {}
my_nested_dict["key1"] = {}
my_nested_dict["key2"] = {}

my_nested_dict["key1"]["nested_key1"] = "value1"
my_nested_dict["key1"]["nested_key2"] = "value2"
my_nested_dict["key2"]["nested_key3"] = "value3"
my_nested_dict["key2"]["nested_key4"] = "value4"

my_list = [my_nested_dict]


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
