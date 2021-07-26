# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from distutils.version import LooseVersion

import pytorch_lightning.utilities.argparse


def get_version(checkpoint: dict) -> str:
    """Get the version of a Lightning checkpoint."""
    return checkpoint["pytorch-lightning_version"]


def set_version(checkpoint: dict, version: str):
    """Set the version of a Lightning checkpoint."""
    checkpoint["pytorch-lightning_version"] = version


def should_upgrade(checkpoint: dict, target: str) -> bool:
    """Returns whether a checkpoint qualifies for an upgrade when the version is lower than the given target."""
    return LooseVersion(get_version(checkpoint)) < LooseVersion(target)


class pl_legacy_patch:
    """
    Registers legacy artifacts (classes, methods, etc.) that were removed but still need to be
    included for unpickling old checkpoints. The following patches apply.

        1. ``pytorch_lightning.utilities.argparse._gpus_arg_default``: Applies to all checkpoints saved prior to
           version 1.2.8. See: https://github.com/PyTorchLightning/pytorch-lightning/pull/6898

    Example:

        with pl_legacy_patch():
            torch.load("path/to/legacy/checkpoint.ckpt")
    """

    def __enter__(self):
        setattr(pytorch_lightning.utilities.argparse, "_gpus_arg_default", lambda x: x)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if hasattr(pytorch_lightning.utilities.argparse, "_gpus_arg_default"):
            delattr(pytorch_lightning.utilities.argparse, "_gpus_arg_default")
