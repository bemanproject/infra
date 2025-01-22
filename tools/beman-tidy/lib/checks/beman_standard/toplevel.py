#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

from ..base.generic_file_check import BSGenericFileCheck


class BSTopLevelChangelogCheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "TOPLEVEL.CHANGELOG", "CHANGELOG.md")

    # check() already implemented in the base class.

    def fix(self):
        # TODO import from beman_standard.
        pass


class BSTopLevelCMakeListsCheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "TOPLEVEL.CMAKE", "CMakeLists.txt")

    # check() already implemented in the base class.

    def fix(self):
        # TODO import from beman_standard.
        pass


class BSTopLevelLicenseCheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "TOPLEVEL.LICENSE", "LICENSE")

    # check() already implemented in the base class.

    def fix(self):
        # TODO import from beman_standard.
        self.write(download_beman_default_license())
        pass


class BSTopLevelREADMECheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "TOPLEVEL.README", "README.md")

    # check() already implemented in the base class.

    def fix(self):
        # TODO import from beman_standard.
        pass
