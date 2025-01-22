#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

import os
import sys


class BSCheck(object):
    """
    Base class for all Beman Standard checks.
    """

    def __init__(self, repo_info, beman_standard, check_name):
        """
        Initialize the check.
        """
        # check name e.g. "LIBRARY.NAMES"
        self.name = check_name

        # unique entry in the list - [(check_name, check_type, check_full_text_body)]
        beman_standard_check = [
            entry for entry in beman_standard if entry[0] == check_name]
        assert len(beman_standard_check) <= 1

        # set type and full_text_body
        if len(beman_standard_check) == 1:
            (check_name, check_type, check_body) = beman_standard_check[0]

            self.type = check_type
            self.full_text_body = check_body
        else:
            self.type = "REQUIREMENT"
            self.full_text_body = "beman-tidy internal check."
        assert self.type in ['REQUIREMENT', 'RECOMMANDATION']

        self.log_level = 'ERROR' if self.type == 'REQUIREMENT' else 'WARNING'
        self.log_enabled = True

        self.repo_info = repo_info

        assert "name" in repo_info
        self.repo_name = repo_info["name"]
        assert "top_level" in repo_info
        self.repo_path = repo_info["top_level"]

        self.library_name = f"beman.{self.repo_name}"
        assert self.library_name is not None

    def base_check(self, log_enabled=True):
        """
        Checks if this rule is properly initialized.
        """
        self.log_enabled = log_enabled

        if self.name is None:
            self.log("The name is not set.")
            return False

        if self.repo_name is None:
            self.log(f"The repo_name is not set for check = {self.name}.")
            return False

        if self.repo_path is None:
            self.log(f"The repo_path is not set for check = {self.name}.")
            return False

        return True

    def check(self, log_enabled=True):
        """
        Checks if the Beman Standard check/rule is already applied.
        - If the standard is applied, the check should return True.
        - If the standard is not applied, the check should return False and self.fix() should be able to fix the issue.

        Base check method that should be overridden by subclasses.
        But it should be called directly on first line of the subclass check method.
        """
        self.log_enabled = log_enabled

        return self.base_check(log_enabled)

    def fix(self):
        """
        Fixes the issue if The  Beman Standard is not applied.
        - If the standard is applied, the check should return True. NOP here.
        - - Otherwise, the check should be applied inplace. If the check cannot be applied inplace, the check should return False.
        """
        self.log_enabled = False
        return False

    def log(self, message, enabled=True):
        """
        Logs a message with the check's log level.
        e.g. [WARN][REPOSITORY.NAME]: The name "${name}" should be snake_case.'
        e.g. [ERROR][TOPLEVEL.CMAKE]: Missing top level CMakeLists.txt.'
        """

        if enabled:
            print(f'[{self.log_level:<15}][{self.name:<25}]: {message}')
