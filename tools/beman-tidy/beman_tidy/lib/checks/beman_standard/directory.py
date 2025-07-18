#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import os
from ..base.directory_base_check import DirectoryBaseCheck
from ..system.registry import register_beman_standard_check


# [DIRECTORY.*] checks category.
# All checks in this file extend the DirectoryBaseCheck class.
#
# Note: DirectoryBaseCheck is not a registered check!
class BemanTreeDirectoryCheck(DirectoryBaseCheck):
    """
    Beman tree: ${prefix_path}/beman/${short_name}.
    Available via member: self.path

    Examples for a repo named "exemplar":
    - include/beman/exemplar
    - tests/beman/exemplar
    - src/beman/exemplar

    Note: A path can be optional. Actual implementation will be in the derived's check().
    """

    def __init__(self, repo_info, beman_standard_check_config, prefix_path):
        super().__init__(
            repo_info,
            beman_standard_check_config,
            f"{prefix_path}/beman/{repo_info['name']}",
        )


@register_beman_standard_check("DIRECTORY.INTERFACE_HEADERS")
class DirectoryInterfaceHeadersCheck(DirectoryBaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config, ".")

    def check(self):
        """
        Check that all public header files reside within the include/beman/<short_name>/ directory.
        """
        # Check if the path exists.
        # Example path: "exemplar/include/beman/exemplar"
        include_path = self.path / "include" / "beman" / self.repo_info["name"]
        if (
            not os.path.exists(include_path)
            or os.path.isfile(include_path)
            or len(os.listdir(include_path)) == 0
        ):
            self.log(
                f"The path '{self.path}' does not exist, is a file or is empty."
                " All public header files must reside within include/beman/<short_name>/."
            )
            return False

        # Get all .hpp files paths, excluding certain directories.
        exclude_dirs = {"src"}
        if self.repo_info["name"] == "exemplar":
            exclude_dirs.add("cookiecutter")

        hpp_files = []
        for root, dirs, files in os.walk(self.path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for name in files:
                if name.lower().endswith(".hpp"):
                    hpp_files.append(os.path.join(root, name))

        # Check that all .hpp files are under the include/beman/<short_name>/
        for hpp_file in hpp_files:
            if not hpp_file.startswith(str(include_path)):
                self.log(
                    f"Header file '{hpp_file}' is not under include/beman/{self.repo_info['name']}/ directory."
                    " All public header files must reside within include/beman/<short_name>/."
                )
                return False

        return True

    def fix(self):
        pass


# TODO DIRECTORY.IMPLEMENTATION_HEADERS


@register_beman_standard_check("DIRECTORY.SOURCES")
class DirectorySourcesCheck(BemanTreeDirectoryCheck):
    """
    Check if the sources directory is src/beman/<short_name>.
    Note: Allow header-only libraries (missing any source files location).

    Example for a repo named "exemplar": src/beman/exemplar
    """

    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config, "src")

    def pre_check(self):
        # Need to override this, because DIRECTORY.SOURCES is conditional
        # (a repo without any source files location is still valid - header only libraries)
        return True

    def check(self):
        # TODO: This is a temporary implementation. Use CMakeLists.txt to actually get the source files location.
        # Should not allow other known source locations.
        forbidden_source_locations = ["source/", "sources/", "lib/", "library/"]
        for forbidden_prefix in forbidden_source_locations:
            forbidden_prefix = self.repo_path / forbidden_prefix
            if forbidden_prefix.exists():
                self.log(
                    f"Please move source files from {forbidden_prefix} to src/beman/{self.repo_name}. See https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md#directorysources for more information."
                )
                return False

        # If `src/` exists, src/beman/<short_name> also should exist.
        if (self.repo_path / "src/").exists() and not self.path.exists():
            self.log(
                f"Please use the required source files location: src/beman/{self.repo_name}. See https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md#directorysources for more information."
            )
            return False

        # Valid source file location or missing -> Beman Standard compliant.
        return True

    def fix(self):
        # Because we don't know which is the actually invalid source file locations,
        # we cannot do a proper implementation for fix().
        if not self.check():
            self.log(
                f"Please manually move sources to src/beman/{self.repo_name}. See https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md#directorysources for more information."
            )


# TODO DIRECTORY.TESTS


# TODO DIRECTORY.EXAMPLES


# TODO DIRECTORY.DOCS


# TODO DIRECTORY.PAPERS
