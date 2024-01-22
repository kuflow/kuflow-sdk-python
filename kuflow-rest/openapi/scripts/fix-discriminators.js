#!/usr/bin/env node

const fs = require('fs')

function removeUnnecessaryUnionOptions() {

  {
    // _models
    const file = `${process.cwd()}/../kuflow_rest/_generated/models/_models.py`

    const fileData = fs.readFileSync(file)
    let fileAsStr = fileData.toString('utf8')

    // _models::_subtype_map
    fileAsStr = fileAsStr.replace(/"Authentication": "Authentication"/, '"AUTHENTICATION": "Authentication"')
    fileAsStr = fileAsStr.replace(/"Process": "Process"/, '"PROCESS": "Process"')
    fileAsStr = fileAsStr.replace(/"Task": "Task"/, '"TASK": "Task"')
    fileAsStr = fileAsStr.replace(/"Worker": "Worker"/, '"WORKER": "Worker"')

    // _models::_subtype_map
    fileAsStr = fileAsStr.replace(/self.object_type: str = "Authentication"/, 'self.object_type: str = "AUTHENTICATION"')
    fileAsStr = fileAsStr.replace(/self.object_type: str = "Process"/, 'self.object_type: str = "PROCESS"')
    fileAsStr = fileAsStr.replace(/self.object_type: str = "Task"/, 'self.object_type: str = "TASK"')
    fileAsStr = fileAsStr.replace(/self.object_type: str = "Worker"/, 'self.object_type: str = "WORKER"')


    fs.writeFileSync(file, fileAsStr, 'utf8')
  }


}

removeUnnecessaryUnionOptions()
