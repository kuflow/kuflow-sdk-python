# coding=utf-8
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


import sys
import uuid

from kuflow_rest import KuFlowRestClient, models


def main() -> int:
    """Echo the input arguments to standard output"""

    client = KuFlowRestClient(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        endpoint="http://localhost:8080/apis/external",
        allow_insecure_connection=True,
    )

    # Variables
    group_id_users = "7bed4109-c867-4f25-869b-071881a82a2b"
    group_id_owners = "f0565aee-7a90-463f-9a24-65f5e9da0210"

    # Test group operations
    principals = client.principal.find_principals(group_id=group_id_users)
    print(principals)
    principals = client.principal.find_principals(group_id=[group_id_users])
    print(principals)
    principals = client.principal.find_principals(
        group_id=[group_id_users, group_id_owners]
    )
    print(principals)

    # Test authentication tokens operations
    authentication = models.Authentication(type="ENGINE")
    authentication = client.authentication.create_authentication(authentication)
    print(authentication)

    # Test process operations
    process_id = uuid.uuid1()
    process_definition_id = "2536b747-d436-48eb-af9a-21989a74f95f"

    task_id = uuid.uuid1()
    task_definition_code = "TASK"

    process = models.Process(
        id=process_id,
        process_definition=models.ProcessDefinitionSummary(id=process_definition_id),
    )
    process = client.process.create_process(process)
    print(process)

    # Test task operations
    task = models.Task(
        id=task_id,
        process_id=process.id,
        task_definition=models.TaskDefinitionSummary(code=task_definition_code),
        element_values={
            "FIELD_TEXT": [models.TaskElementValueString(value="texto")],
            "FIELD__TEXT_MULTIPLE": [
                models.TaskElementValueString(value="texto 2 1"),
                models.TaskElementValueString(value="texto 2 2"),
            ],
        },
    )
    task = client.task.create_task(task)
    print(task)


    # Claim task
    client.task.actions_task_claim(task_id)

    file = models.Document(
        file_mame="bugs-bunny.png",
        content_type="image/png",
        file_content=open("/home/zeben/dummy/robot.png", "rb"),
    )
    command = models.TaskSaveElementValueDocumentCommand(element_definition_code="DOC")
    task = client.task.actions_task_save_element_value_document(id=task.id, file=file, command=command)
    print(task)

    # Complete task
    client.task.actions_task_complete(task_id)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # next section explains the use of sys.exit
