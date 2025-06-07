#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from .base_check import BaseCheck
import os
import sys


class DirectoryBaseCheck(BaseCheck):
    """
    Base class for checks that operate on a directory.
    """

    def __init__(self, repo_info, beman_standard_check_config, relative_path):
        super().__init__(repo_info, beman_standard_check_config)

        # set path - e.g. "src/beman/exemplar"
        self.path = os.path.join(repo_info["top_level"], relative_path)

    def default_check(self):
        pass

    # TODO: add methods to read the directory content
