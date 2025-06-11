#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from abc import ABC, abstractmethod
import os

from .base_check import BaseCheck


class DirectoryBaseCheck(BaseCheck):
    """
    Base class for checks that operate on a directory.
    """

    def __init__(self, repo_info, beman_standard_check_config, relative_path):
        super().__init__(repo_info, beman_standard_check_config)

        # set path - e.g. "src/beman/exemplar"
        self.path = os.path.join(repo_info["top_level"], relative_path)

    def pre_check(self):
        """
        Override.
        """
        if not super().pre_check():
            return False

        # TODO: Implement the default check.
        pass

    @abstractmethod
    def check(self):
        """
        Override this method, make it abstract because this is style an abstract class.
        """
        pass

    @abstractmethod
    def fix(self):
        """
        Override this method, make it abstract because this is style an abstract class.
        """
        pass

    # TODO: add methods to read the directory content
