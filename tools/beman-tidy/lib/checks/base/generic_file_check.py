#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

from .base_check import BSCheck
import os
import sys


class BSGenericFileCheck(BSCheck):
    """
    Base class for all Beman Standard checks.
    """

    def __init__(self, repo_info, beman_standard, check_name, relative_path):
        super().__init__(repo_info, beman_standard, check_name)

        self.path = os.path.join(repo_info["top_level"], relative_path)

    def base_check(self, log_enabled=True):
        """
        Checks if this rule is properly initialized.
        """
        self.log_enabled = log_enabled

        if not super().base_check(log_enabled):
            return False

        if self.path is None:
            self.log("The path is not set.")
            return False

        if not os.path.exists(self.path):
            self.log(f"The file '{self.path}' does not exist.")
            return False

        if len(self.read_lines()) == 0:
            self.log(f"The file '{self.path}' is empty.")
            return False

        return True

    def read(self):
        """
        Read the file content.
        """
        with open(self.path, 'r') as file:
            return file.read()

    def read_lines(self):
        """
        Read the file content as lines.
        """
        with open(self.path, 'r') as file:
            return file.readlines()

    def read_lines_strip(self):
        """
        Read the file content as lines and strip them.
        """
        with open(self.path, 'r') as file:
            return [line.strip() for line in file.readlines()]

    def write(self, content):
        """
        Write the content to the file.
        """
        with open(self.path, 'w') as file:
            file.write(content)

    def write_lines(self, lines):
        """
        Write the lines to the file.
        """
        with open(self.path, 'w') as file:
            file.writelines(lines)
