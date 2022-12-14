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

from kuflow.rest import KuFlowRestClient, models


def main() -> int:
    """Echo the input arguments to standard output"""

    client = KuFlowRestClient(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        endpoint="http://localhost:8080/apis/external/v2022-10-08",
        allow_insecure_connection=True,
    )
    principals = client.principal.find_principals(group_id="c16a8bbc-cdbd-4ebe-80d9-817defb7cb2f")
    print(principals)
    principals = client.principal.find_principals(group_id=["c16a8bbc-cdbd-4ebe-80d9-817defb7cb2f"])
    print(principals)
    principals = client.principal.find_principals(
        group_id=["c16a8bbc-cdbd-4ebe-80d9-817defb7cb2f", "aaeb0b1d-6c3d-4436-aace-219af8a1810d"]
    )
    print(principals)

    authentication = models.Authentication(type="ENGINE")
    authentication = client.authentication.create_authentication(authentication)
    print(authentication)

    process = models.Process(
        id="28abe67f-9462-4343-b58e-c8b3344eb865",
        process_definition=models.ProcessDefinitionSummary(id="be35212b-deb8-4719-a10d-b8550219d156"),
    )
    process = client.process.create_process(process)
    print(process)

    task = models.Task(
        id="4bbdf1ef-5350-4abf-b0c1-58a0c57aacdb",
        process_id=process.id,
        task_definition=models.TaskDefinitionSummary(code="TASK_0001"),
        element_values={
            "TEXT_001": [models.TaskElementValueString(value="texto")],
            "TEXT_002": [
                models.TaskElementValueString(value="texto 2 1"),
                models.TaskElementValueString(value="texto 2 2"),
            ],
        },
    )
    task = client.task.create_task(task)
    print(task)

    # client.task.actions_task_claim(task.id)

    file = models.Document(
        file_mame="bugs-bunny.png",
        content_type="image/png",
        file_content=open("/Users/kuflow/Downloads/bugs-bunny.png", "rb"),
    )
    command = models.TaskSaveElementValueDocumentCommand(element_definition_code="DOC_001")
    task = client.task.actions_task_save_element_value_document(id=task.id, file=file, command=command)
    print(task)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # next section explains the use of sys.exit
