#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

from ..base.base_check import BSCheck

import sys


class BSCheckFixInplaceIncompatibleWithUnstagedChanges(BSCheck):
    """
    Check if the fix can be applied inplace.
    """

    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard,
                         'NO_UNSTAGED_CHANGES')

    def check(self):
        """
        Check already applied if no unstaged changes are present.
        """
        return len(self.repo_info["unstaged_changes"]) == 0

    def fix(self):
        """
        Fix the issue if the fix can be applied inplace, so unstaged changes are not present!
        """
        self.log(
            "The fix cannot be applied inplace. Please commit or stash your changes. STOP.")
        sys.exit(1)
