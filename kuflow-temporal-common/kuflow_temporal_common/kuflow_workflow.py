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

import uuid

from temporalio import workflow


def uuid7() -> uuid.UUID:
    """Get a new, determinism-safe v7 UUID based on :py:func:`random`.

    Note, this UUID is not cryptographically safe and should not be used for
    security purposes.

    Returns:
        A deterministically-seeded v7 UUID.
    """
    # random bytes
    random_bytes = workflow.random().getrandbits(16 * 8).to_bytes(16, "big")
    value = bytearray(random_bytes)

    # current timestamp in ms
    timestamp = int(workflow.time_ns() / 1_000_000)

    # timestamp
    value[0] = (timestamp >> 40) & 0xFF
    value[1] = (timestamp >> 32) & 0xFF
    value[2] = (timestamp >> 24) & 0xFF
    value[3] = (timestamp >> 16) & 0xFF
    value[4] = (timestamp >> 8) & 0xFF
    value[5] = timestamp & 0xFF

    # version and variant
    value[6] = (value[6] & 0x0F) | 0x70
    value[8] = (value[8] & 0x3F) | 0x80

    return uuid.UUID(bytes=bytes(value))
