#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

from .cmake import CMakeBaseCheck
from ..system.registry import register_beman_standard_check

# [TOPLEVEL.*] checks category.
# All checks in this file extend the ToplevelBaseCheck class.
#
# Note: ToplevelBaseCheck is not a registered check!


@register_beman_standard_check(check="TOPLEVEL.CMAKE")
class ToplevelCmakeCheck(CMakeBaseCheck):
    def __init__(self, repo_info, beman_standard_check_config):
        super().__init__(repo_info, beman_standard_check_config)

    def check(self):
        return super().pre_check()

    def fix(self):
        # TODO: Implement the fix.
        pass


# TODO TOPLEVEL.LICENSE - use FileBaseCheck

# TODO TOPLEVEL.README - use ReadmeBaseCheck
