# coding=utf-8

from setuptools import setup, find_packages


PACKAGE_NAME = "kuflow-rest"
version = "0.0.1"
setup(
    name=PACKAGE_NAME,
    version=version,
    description="KuFlowRestClient",
    author_email="",
    url="",
    keywords="azure, azure sdk",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "isodate<1.0.0,>=0.6.1",
        "azure-core<2.0.0,>=1.24.0",
        "typing-extensions>=4.3.0; python_version<'3.8.0'",
    ],
    long_description="""\
    Introduction
============

This document contains the KuFlow REST API reference. This API is a fundamental part in the integration of external
systems with KuFlow and is used, among others, by the different implementations of the Workers that connect to our
network.

API Versioning
==============

A versioning strategy allows our clients to continue using the existing REST API and migrate their applications to
the newer API when they are ready.

The scheme followed is a simplification of *Semver* where only MAJOR versions are differentiated from MINOR or PATCH
versions, i.e. a version number of only two levels is used. With this approach, you only have to migrate your
applications if you want to upgrade to a MAJOR version of the KuFlow API. In case you want to upgrade to a MINOR
version, you can do so without any incompatibility issues.

The versioning of the api is done through the URI Path, that is, the version number is included in the URI Path. The
URL structure would be as follows:

.. code-block:: bash

   https://{endpoint}/v{VERSION}/{api-path}

Idempotency
===========

The API is designed to support idempotency in order to achieve a correct resilience in the implementation of its
clients. The way to achieve this is very simple, in the methods that create resources, you simply have to specify a
UUID in the input data and the API will respond by creating or returning the resource if it previously existed. With
this mechanism, your systems can implement retry logic without worrying about performing data tradeoffs.

OpenAPI Specification
=====================

This API is documented in OpenAPI format. This file allows you to create REST clients with the technology of your
choice automatically. In our code repositories you can find an example of this automation using Feign for JAVA.
    """,
)
