# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator (autorest: 3.9.3, generator: @autorest/python@6.2.9)
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._client import KuFlowClient
from ._version import VERSION

__version__ = VERSION

try:
    from ._patch import __all__ as _patch_all
    from ._patch import *  # pylint: disable=unused-wildcard-import
except ImportError:
    _patch_all = []
from ._patch import patch_sdk as _patch_sdk

__all__ = [
    "KuFlowClient",
]
__all__.extend([p for p in _patch_all if p not in __all__])

_patch_sdk()
