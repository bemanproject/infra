#!/usr/bin/python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import os
import pytest
from pathlib import Path
from tests.utils.conftest import mock_repo_info, mock_beman_standard_check_config


@pytest.fixture
def test_data_dir():
    """Return the path to the test data directory"""
    return Path(__file__).parent / "data"


@pytest.fixture
def valid_readme_path(test_data_dir):
    """Return the path to a valid README.md file"""
    return test_data_dir / "valid" / "README.md"


@pytest.fixture
def invalid_readme_path(test_data_dir):
    """Return the path to an invalid README.md file"""
    return test_data_dir / "invalid" / "README.md"


@pytest.fixture(autouse=True)
def repo_info(mock_repo_info):
    return mock_repo_info


@pytest.fixture
def beman_standard_check_config(mock_beman_standard_check_config):
    return mock_beman_standard_check_config
