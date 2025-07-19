#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import re

from ..base.file_base_check import FileBaseCheck
from ..base.base_check import BaseCheck
from ..system.registry import register_beman_standard_check

# [REPOSITORY.*] checks category.
# All checks in this file extend the FileBaseCheck class.
#
# Note: FileBaseCheck is not a registered check!


@register_beman_standard_check("REPOSITORY.NAME")
class RepositoryNameCheck(BaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def check(self):
        def is_snake_case(name):
            return re.match("(^[a-z0-9]+$)|(^[a-z0-9][a-z0-9_.]+[a-z0-9]$)", name)

        def is_beman_snake_case(name):
            """
            Has prefix "beman." and continues with snake_case.
            It must NOT end with a C++ target standard version - e.g. 17, 20, 23, 26, 32, etc.
            """
            return (
                name[:6] != "beman."
                and is_snake_case(name)
                and not re.match(".*[0-9]+$", name)
            )

        name = self.repo_info["name"]

        if not is_beman_snake_case(name):
            self.log(
                "The repository should be named after the library name excluding the 'beman.' prefix. It should not contain a target C++ version. "
                "See https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md#repositoryname for more information."
            )
            return False

        return True

    def fix(self):
        self.log(
            "beman-tidy can't automatically fix the repository name since that would require GitHub API calls and administrative permissions. "
            "Please see https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md#repositoryname for more information."
        )
        pass


@register_beman_standard_check("REPOSITORY.CODEOWNERS")
class RepositoryCodeownersCheck(FileBaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config, ".github/CODEOWNERS")

    def check(self):
        # Since this class simply checks for the existence of a CODEOWNERS file,
        # there's nothing more to do than the default pre-check.
        return super().pre_check()

    def fix(self):
        self.log(
            "Please add a CODEOWNERS file to the repository. See https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md#repositorycodeowners for more information."
        )


@register_beman_standard_check("REPOSITORY.DEFAULT_BRANCH")
class RepositoryDefaultBranchCheck(BaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def check(self):
        default_branch = self.repo_info["default_branch"]
        if default_branch != "main":
            self.log(f"Invalid default branch in repo: {default_branch} vs 'main'.")
            return False

        return True

    def fix(self):
        self.log(
            "Please set `main` as default branch in the repository. See https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md#repositorydefault_branch for more information."
        )


# TODO REPOSITORY.DISALLOW_GIT_SUBMODULES
