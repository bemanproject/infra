#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

from ..base.generic_file_check import BSGenericFileCheck


class BSGenericReadmeCheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard, check_name):
        super().__init__(repo_info, beman_standard, check_name, "README.md")

# TODO README.TITLE


class BSReadmeTitleCheck(BSGenericReadmeCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "README.TITLE")

    def check(self):
        """
        The README.md should begin with a level 1 header with the name of the library optionally followed with a ":" and short description.
        """
        content = self.read_lines_strip()
        if len(content) == 0:
            self.log("The root README.md file is empty.")
            return False

        # Match the pattern "# <library_name>[: <short_description>]"
        if not first_line[2:].startswith(f"{self.library_name}:"):
            return False


# TODO README.PURPOSE
# TODO README.IMPLEMENTS
# TODO README.LIBRARY_STATUS
