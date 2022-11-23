# KuFlow Rest API client

> see https://aka.ms/autorest

This is the AutoRest configuration file for KuFlow.

---

## Getting Started

To build the SDK for KuFlow, simply do the following in this folder:

```bash
$> npm ci
$> npm run generate
```

---

## Configuration

### Basic Information

```yaml
v3: true
python: true
title: KuFlow
override-client-name: KuFlowClient

input-file: /Users/kuflow/Projects/kuflow-openapi/specs/api.kuflow.com/v2022-10-08/openapi.yaml
output-folder: ../../kuflow/client/_generated

openapi-type: data-plane
add-credential: true
package-name: kuflow-rest-client
namespace: kuflow.client
package-version: '0.0.1'
no-namespace-folders: true
combine-operation-files: false
models-mode: msrest
black: false

# basic-setup-py: true
# generate-metadata: true
# generate-test: false
# generate-sample: false
# hide-clients: true

use-extension:
  '@autorest/python': '6.2.9'
  '@autorest/modelerfour': '4.25.0'

modelerfour:
  seal-single-value-enum-by-default: false
```

### Group operations using tag

```yaml
directive:
  - from: openapi-document
    where: $.paths[*][*]
    transform: |
      if ($.operationId.indexOf($.tags[1] + '_') === -1) {
        $.operationId = $.tags[1] + '_' + $.operationId;
      }
```
