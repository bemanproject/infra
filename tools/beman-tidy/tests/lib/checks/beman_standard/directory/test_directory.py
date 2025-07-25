#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import pytest
from pathlib import Path

from tests.utils.path_runners import (
    run_check_for_each_path,
)

# Actual tested checks.
from beman_tidy.lib.checks.beman_standard.directory import (
    DirectorySourcesCheck,
    DirectoryDocsCheck,
    DirectoryExamplesCheck,
)

test_data_prefix = "tests/lib/checks/beman_standard/directory/data"
valid_prefix = f"{test_data_prefix}/valid"
invalid_prefix = f"{test_data_prefix}/invalid"


def test__DIRECTORY_SOURCES__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid CMakeLists.txt.
    """
    valid_cmake_paths = [
        # exemplar/ repo with src/beman/exemplar/ - valid source tree.
        Path(f"{valid_prefix}/repo-exemplar-v1/"),
        # exemplar/ repo without src/ - no source files (header-only).
        Path(f"{valid_prefix}/repo-exemplar-v2/"),
    ]

    run_check_for_each_path(
        True,
        valid_cmake_paths,
        DirectorySourcesCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__DIRECTORY_SOURCES__invalid(repo_info, beman_standard_check_config):
    """
    Test that repositories with invalid CMakeLists.txt.
    """
    invalid_cmake_paths = [
        # Sources in src/beman/optional - wrong inner directory.
        Path(f"{invalid_prefix}/repo-exemplar-v1"),
        # Sources in src/beman/ - missing 3rd subdirectory.
        Path(f"{invalid_prefix}/repo-exemplar-v2"),
        # Sources in src/ - missing 2nd and 3rd subdirectories.
        Path(f"{invalid_prefix}/repo-exemplar-v3"),
        # Sources in sources/ - wrong prefix.
        Path(f"{invalid_prefix}/repo-exemplar-v4"),
        # Sources in source/ - wrong prefix.
        Path(f"{invalid_prefix}/repo-exemplar-v5"),
        # Sources in lib/ - wrong prefix.
        Path(f"{invalid_prefix}/repo-exemplar-v6"),
        # Sources in library/ - wrong prefix.
        Path(f"{invalid_prefix}/repo-exemplar-v7"),
    ]

    run_check_for_each_path(
        False,
        invalid_cmake_paths,
        DirectorySourcesCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__DIRECTORY_SOURCES__fix_inplace(repo_info, beman_standard_check_config):
    pass


def test__DIRECTORY_EXAMPLES__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid examples directory pass the check.
    """
    valid_examples_paths = [
        # exemplar/ repo with correct examples/ dir.
        Path(f"{valid_prefix}/repo-exemplar-v1/"),
    ]

    run_check_for_each_path(
        True,
        valid_examples_paths,
        DirectoryExamplesCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__DIRECTORY_EXAMPLES__invalid(repo_info, beman_standard_check_config):
    """
    Test that repositories with invalid examples directory fail the check.
    """
    invalid_examples_paths = [
        # Missing examples/ directory.
        Path(f"{invalid_prefix}/repo-exemplar-v1"),
        # Empty examples/ directory.
        Path(f"{invalid_prefix}/repo-exemplar-v2"),
        # examples/ directory without .cpp files.
        Path(f"{invalid_prefix}/repo-exemplar-v3"),
        # examples/ directory without CMakeLists.txt files.
        Path(f"{invalid_prefix}/repo-exemplar-v4"),
        # examples/ directory with no relevant example files.
        Path(f"{invalid_prefix}/repo-exemplar-v5"),
    ]

    run_check_for_each_path(
        False,
        invalid_examples_paths,
        DirectoryExamplesCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__DIRECTORY_EXAMPLES__fix_inplace(repo_info, beman_standard_check_config):
    pass


def test__DIRECTORY_DOCS__valid(repo_info, beman_standard_check_config):
    """
    Test that repositories with valid documentation structure pass the check.
    """
    valid_docs_paths = [
        # exemplar/ repo without docs/ dir and with root README.md.
        Path(f"{valid_prefix}/repo-exemplar-v1/"),
        # exemplar/ repo with docs/ dir and root README.md.
        Path(f"{valid_prefix}/repo-exemplar-v2/"),
        # exemplar/ repo with papers/ dir and root README.md.
        Path(f"{valid_prefix}/repo-exemplar-v3/"),
    ]

    run_check_for_each_path(
        True,
        valid_docs_paths,
        DirectoryDocsCheck,
        repo_info,
        beman_standard_check_config,
    )


def test__DIRECTORY_DOCS__invalid(repo_info, beman_standard_check_config):
    """
    Test that repositories with invalid documentation structure fail the check.
    """
    invalid_docs_paths = [
        # Misplaced MD files in root directory.
        Path(f"{invalid_prefix}/repo-exemplar-v1"),
        # Misplaced MD files in root subdirectories.
        Path(f"{invalid_prefix}/repo-exemplar-v2"),
        # Misplaced MD files in root directory and root subdirectories.
        Path(f"{invalid_prefix}/repo-exemplar-v3"),
        # Wrong name for docs/ directory.
        Path(f"{invalid_prefix}/repo-exemplar-v4"),
    ]

    run_check_for_each_path(
        False,
        invalid_docs_paths,
        DirectoryDocsCheck,
        repo_info,
        beman_standard_check_config,
    )


@pytest.mark.skip(reason="NOT implemented")
def test__DIRECTORY_DOCS__fix_inplace(repo_info, beman_standard_check_config):
    pass
