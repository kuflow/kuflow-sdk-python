[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/kuflow/kuflow-sdk-python/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/kuflow-robotframework.svg)](https://pypi.org/project/kuflow-robotframework)
[![PyPI](https://img.shields.io/pypi/v/kuflow-robotframework.svg)](https://pypi.org/project/kuflow-robotframework)

# KuFlow Robot Framework

This library provides keywords to interact with the KuFlow API from a Robot Framework Robot. Its purpose is to facilitate interaction from the robot logic (RPA). Its use helps to keep the manipulation of robot results by Workflow decoupled as much as possible.

List of available keywords:

#### Set Client Authentication

> Configure the client authentication in order to execute keywords against Rest API

#### Append Log Message

> Add a log entry to the task

#### Claim Task

> Allow to claim a task

#### Retrieve Process

> Allow to get a process by ID

#### Retrieve Task

> Allow to get a task by ID

#### Save Element Document

> Save a element task of type document

#### Delete Element Document

> Allow to delete a specific document from an element of document type using its id.

#### Save Element

> Save a element task

#### Delete Element

> Allow to delete task element by specifying the item definition code.

#### Convert To Principal Item

> Given an Id of a Principal user, create an item that represents a reference to the Principal.

#### Convert To Document Item From Uri

> Given an Id of a Document or the URI reference of a Document, create an item that represents a reference to the Document elementand can be used.

#### Convert JSON String To Object

> Given a JSON string as argument, return new JSON object

#### Save Json Forms Value Data

> Allows a JSON Forms to be saved in the task.

#### Upload Json Forms Value Document

> Allows you to upload a document to the referenced task and then include a reference to it in the task's JSON Forms.

## Documentation

More detailed docs are available in the [documentation pages](https://docs.kuflow.com/developers/).

## Contributing

We are happy to receive your help and comments, together we will dance a wonderful KuFlow. Please review our [contribution guide](CONTRIBUTING.md).

## License

[MIT License](https://github.com/kuflow/kuflow-sdk-python/blob/master/LICENSE)
