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
