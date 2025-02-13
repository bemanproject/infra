#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

from ..base.generic_file_check import BSGenericFileCheck
from ...utils.git import *


class BSTopLevelChangelogCheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "TOPLEVEL.CHANGELOG", "CHANGELOG.md")

    def check(self):
        return super().base_check()  # Non-empty file check.

    def fix(self):
        # TODO import from beman_standard.
        pass


class BSTopLevelCMakeListsCheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "TOPLEVEL.CMAKE", "CMakeLists.txt")

    def check(self):
        return super().base_check()  # Non-empty file check.

    def fix(self):
        # TODO import from beman_standard.
        pass


class BSTopLevelLicenseCheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "TOPLEVEL.LICENSE", "LICENSE")

    def check(self):
        return super().base_check()  # Non-empty file check.

    def fix(self):
        # TODO import from beman_standard.
        self.write(download_beman_default_license())
        pass


class BSTopLevelREADMECheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "TOPLEVEL.README", "README.md")

    def check(self):
        return super().base_check()  # Non-empty file check.

    def fix(self):
        # TODO import from beman_standard.
        pass
