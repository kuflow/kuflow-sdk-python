*** Comments ***
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


*** Settings ***
Variables       devdata/env.py
Library         KuFlow


*** Tasks ***
Test Clear
    Clear All Elements

Test Single Claim a KuFlow Task
    Set KuFlow Credentials

    # Claim task
    Claim Task    ${KUFLOW_TASK_ID}

Test Single Add Log to KuFlow Task
    Set KuFlow Credentials

    # Add log message to the task
    Append Log Message    ${KUFLOW_TASK_ID}    I'm a message form KuFlow RobotFramework Library    level=WARN

Test Single Retrieve a KuFlow Task
    Set KuFlow Credentials

    # Get task
    ${task}=    Retrieve Task    ${KUFLOW_TASK_ID}
    Should Be Equal    ${task.id}    ${KUFLOW_TASK_ID}

Test Single Retrieve a KuFlow Process
    Set KuFlow Credentials

    # Get process
    ${process}=    Retrieve Process    ${KUFLOW_PROCESS_ID}
    Should Be Equal    ${process.id}    ${KUFLOW_PROCESS_ID}

Test Single Save document to KuFlow Task
    Set KuFlow Credentials

    # Clear previous
    Delete Element    ${KUFLOW_TASK_ID}    DOC

    # Upload a new file
    ${task}=    Save Element Document    ${KUFLOW_TASK_ID}    DOC    /files/dummy/coyote.jpg

    # Replace a existing document element with a new file
    ${taskUpdated}=    Save Element Document    ${KUFLOW_TASK_ID}    DOC    /files/dummy/robot.png
    Should Not Be Equal
    ...    ${task.element_values['DOC'][0].value.content_length}
    ...    ${taskUpdated.element_values['DOC'][0].value.content_length}

Test Multiple Save document to KuFlow Task
    Set KuFlow Credentials

    # Clear previous
    Delete Element    ${KUFLOW_TASK_ID}    DOC_MULTIPLE
    # Save multiple file in a single task element
    Save Element Document    ${KUFLOW_TASK_ID}    DOC_MULTIPLE    /files/dummy/coyote.jpg
    ${task}=    Save Element Document    ${KUFLOW_TASK_ID}    DOC_MULTIPLE    /files/dummy/piolin.gif
    ${length}=    Get length    ${task.element_values['DOC_MULTIPLE']}
    Should Be Equal As Integers    ${length}    2

    # Replace a specific file in a multivalue element with new content and marks as invalid
    ${taskUpdated}=    Save Element Document
    ...    ${KUFLOW_TASK_ID}
    ...    DOC_MULTIPLE
    ...    /files/dummy/robot.png
    ...    ${task.element_values['DOC_MULTIPLE'][1].value.id}
    ...    valid=${False}

    Should Not Be Equal
    ...    ${task.element_values['DOC_MULTIPLE'][1].value.content_length}
    ...    ${taskUpdated.element_values['DOC_MULTIPLE'][1].value.content_length}

Test Single Save Element String To KuFlow Task
    Set KuFlow Credentials

    # Save a string element
    Save Element    ${KUFLOW_TASK_ID}    FIELD_TEXT    Lorem ipsum

Test Multiple Save Element String To KuFlow Task
    Set KuFlow Credentials

    # Save a string element
    Save Element    ${KUFLOW_TASK_ID}    FIELD__TEXT_MULTIPLE    one    two    three

    # Save a multivalue string element with all elements with valid=False
    Save Element    ${KUFLOW_TASK_ID}    FIELD__TEXT_MULTIPLE    one    two    three    valid=False

Test Single Save Element Number To KuFlow Task
    Set KuFlow Credentials

    # Save a Number element (Integer)
    ${result}=    Convert To Integer    123
    Save Element    ${KUFLOW_TASK_ID}    FIELD__NUMBER    ${result}

    # Save a Number element (Float) with valid=True
    ${result}=    Convert To Number    123.123
    Save Element    ${KUFLOW_TASK_ID}    FIELD__NUMBER    ${result}    valid=${False}

Test Multiple Save Element Number To KuFlow Task
    Set KuFlow Credentials

    # Save a multivalue Number element
    ${result_one}=    Convert To Integer    123
    ${result_two}=    Convert To Number    123.123
    Save Element    ${KUFLOW_TASK_ID}    FIELD__NUMBER_MULTIPLE    ${result_one}    ${result_two}

Test Single Save Element Object To KuFlow Task
    Set KuFlow Credentials

    # Save a object element with valid=False
    &{result}=    Create Dictionary    one_key=My Example Value One    two_key=2
    Save Element    ${KUFLOW_TASK_ID}    FORM    ${result}    valid=${False}

Test Multiple Save Element Object To KuFlow Task
    Set KuFlow Credentials

    # Save a multivalue object element
    &{result_one}=    Create Dictionary    one_key=My Example Value One    two_key=2
    &{result_two}=    Create Dictionary    a_key=My Example Value A    b_key=B
    Save Element    ${KUFLOW_TASK_ID}    FORM_MULTIPLE    ${result_one}    ${result_two}

Test Single Save Element Principal To KuFlow Task
    Set KuFlow Credentials

    ${result}=    Convert To Principal Item    8934b169-c85e-4e05-9580-13ace7f267f5    USER
    Save Element    ${KUFLOW_TASK_ID}    PRINCIPAL    ${result}    valid=${False}

Test Multiple Save Element Principal To KuFlow Task
    Set KuFlow Credentials

    # Save a object element with valid=False
    ${result_one}=    Convert To Principal Item    8934b169-c85e-4e05-9580-13ace7f267f5    USER
    ${result_two}=    Convert To Principal Item    0329ae28-05b7-4f0a-984d-a0f13f2a5767    USER
    Save Element    ${KUFLOW_TASK_ID}    PRINCIPAL_MULTIPLE    ${result_one}    ${result_two}    valid=${False}

Test Single Save Element Document Reference To KuFlow Task
    Set KuFlow Credentials

    # Prepare test
    Delete Element    ${KUFLOW_TASK_ID}    DOC
    Delete Element    ${KUFLOW_TASK_ID}    DOC_MULTIPLE
    ${task}=    Save Element Document    ${KUFLOW_TASK_ID}    DOC_MULTIPLE    /files/dummy/piolin.gif

    # test
    ${result}=    Convert To Document Item From Uri
    ...    ku:task/1009b81f-f768-4c85-992b-9729c7ae6161/element-value/${task.element_values['DOC_MULTIPLE'][0].value.id}
    ${taskUpdated}=    Save Element    ${KUFLOW_TASK_ID}    DOC    ${result}

    Should Be Equal
    ...    ${task.element_values['DOC_MULTIPLE'][0].value.content_length}
    ...    ${taskUpdated.element_values['DOC'][0].value.content_length}


*** Keywords ***
Set KuFlow Credentials
    # Initialize KuFlow API client
    Set Client Authentication
    ...    ${KUFLOW_API_ENDPOINT}
    ...    ${KUFLOW_CLIENT_ID}
    ...    ${KUFLOW_CLIENT_SECRET}

Clear All Elements
    Set KuFlow Credentials

    Delete Element    ${KUFLOW_TASK_ID}    DOC
    Delete Element    ${KUFLOW_TASK_ID}    DOC_MULTIPLE

    Delete Element    ${KUFLOW_TASK_ID}    FIELD_TEXT
    Delete Element    ${KUFLOW_TASK_ID}    FIELD__TEXT_MULTIPLE

    Delete Element    ${KUFLOW_TASK_ID}    FIELD__NUMBER
    Delete Element    ${KUFLOW_TASK_ID}    FIELD__NUMBER_MULTIPLE

    Delete Element    ${KUFLOW_TASK_ID}    FORM
    Delete Element    ${KUFLOW_TASK_ID}    FORM_MULTIPLE

    Delete Element    ${KUFLOW_TASK_ID}    PRINCIPAL
    Delete Element    ${KUFLOW_TASK_ID}    PRINCIPAL_MULTIPLE

