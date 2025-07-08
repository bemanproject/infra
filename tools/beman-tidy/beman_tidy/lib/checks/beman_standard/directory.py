#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from ..base.directory_base_check import DirectoryBaseCheck
from ..system.registry import register_beman_standard_check


# [DIRECTORY.*] checks category.
# All checks in this file extend the DirectoryBaseCheck class.
#
# Note: DirectoryBaseCheck is not a registered check!
class BemanTreeDirectoryCheck(DirectoryBaseCheck):
    """
    Check if the directory tree is a Beman tree: ${prefix_path}/beman/${short_name}.
    Examples for a repo named "exemplar":
    - include/beman/exemplar
    - src/beman/exemplar
    - tests/beman/exemplar
    - examples/beman/exemplar
    - docs/beman/exemplar
    - papers/beman/exemplar
    """

    def __init__(self, repo_info, beman_standard_check_config, prefix_path):
        super().__init__(
            repo_info,
            beman_standard_check_config,
            f"{prefix_path}/beman/{repo_info['name']}",
        )


# TODO DIRECTORY.INTERFACE_HEADERS


# TODO DIRECTORY.IMPLEMENTATION_HEADERS


@register_beman_standard_check("DIRECTORY.SOURCES")
class DirectorySourcesCheck(BemanTreeDirectoryCheck):
    """
    Check if the sources directory is src/beman/<short_name>.

    Example for a repo named "exemplar": src/beman/exemplar
    """

    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config, "src")

    def check(self):
        return self.pre_check()  # Check if the directory exists and is not empty.

    def fix(self):
        self.log(
            f"Please move sources to src/beman/{self.repo_name}. See https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md#directorysources for more information."
        )


# TODO DIRECTORY.TESTS


# TODO DIRECTORY.EXAMPLES


# TODO DIRECTORY.DOCS


# TODO DIRECTORY.PAPERS
