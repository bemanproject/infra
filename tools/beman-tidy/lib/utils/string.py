#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

from .git import download_beman_default_license


def is_snake_case(name):
    return re.match("(^[a-z0-9]+$)|(^[a-z0-9][a-z0-9_.]+[a-z0-9]$)", name)


def is_beman_snake_case(name):
    """
    Has prefix "beman." and continues with snake_case.
    It must NOT end with a C++ target standard version - e.g. 17, 20, 23, 26, 32, etc.
    """

    return name[:6] == "beman." and is_snake_case(name[6:]) and not re.match(".*[0-9]+$", name[6:])
