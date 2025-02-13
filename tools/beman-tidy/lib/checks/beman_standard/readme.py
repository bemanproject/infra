#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

from ..base.generic_file_check import BSGenericFileCheck
from ...utils.string import *
from ...utils.git import *


class BSGenericReadmeCheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard, check_name):
        super().__init__(repo_info, beman_standard, check_name, "README.md")


class BSReadmeTitleCheck(BSGenericReadmeCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "README.TITLE")

    def check(self):
        """
        The README.md should begin with a level 1 header with the name of the library optionally followed
        with a ":" and short description.
        """
        lines = self.read_lines_strip()
        if len(lines) == 0:
            return False
        first_line = lines[0]

        # Match the pattern "# <library_name>[: <short_description>]"
        if not first_line[2:].startswith(f"{self.library_name}:"):
            return False

        return True


class BSReadmeBadgesCheck(BSGenericReadmeCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "README.BADGES")

    def check(self):
        """
        Following the title, the `README.md` must have a one-line badge list: library status (`[README.LIBRARY_STATUS]`), CI status, code coverage.

        Badge format: ![Name with multiple words](url_no_spaces)
        Badge line format: ![Name1](url1) ![Name2](url2) ![Name3](url3) ...

        Example:
        ![Library Status](https://raw.githubusercontent.com/bemanproject/beman/refs/heads/main/images/badges/beman_badge-beman_library_under_development.svg) ![Continuous Integration Tests](https://github.com/bemanproject/exemplar/actions/workflows/ci_tests.yml/badge.svg) ![Lint Check (pre-commit)](https://github.com/bemanproject/exemplar/actions/workflows/pre-commit.yml/badge.svg)
        """
        repo_badges = self.parse_lines(self.read_lines_strip())
        if repo_badges is None:
            self.log(f"First line of README.md must contain badges.")
            return False

        standard_badges = match_badges(self.full_text_body)
        if standard_badges is None:
            self.log(
                f"No badges found in Beman Standard. Please add badge examples to the Beman Standard in section README.BADGES.")
            return False

        # Check if the badges in the README.md are the same as in the Beman Standard.
        for badge_name, badge_url in repo_badges:
            matched_badge = next(
                (standard_badge for standard_badge in standard_badges if standard_badge[0] == badge_name), None)
            if not matched_badge:
                self.log(
                    f"Badge \"{badge_name}\" not found in the Beman Standard. Standard badges: {set([badge[0] for badge in standard_badges])}.")
                return False
            beman_standard_badge_url = matched_badge[1]

            if badge_name == "Library Status":
                if not badge_url.startswith("https://raw.githubusercontent.com/bemanproject/beman/refs/heads/main/images/badges/beman_badge-beman_library_"):
                    self.log(
                        f"Badge \"{badge_name}\" URL is invalid: {badge_url}. The URL should start with \"https://raw.githubusercontent.com/bemanproject/beman/refs/heads/main/images/badges/beman_badge-beman_library_\".")
                    return False

                if badge_url not in [standard_badge[1] for standard_badge in standard_badges]:
                    self.log(
                        f"Badge \"{badge_name}\" URL is invalid: {badge_url}. The URL should be in the Beman Standard.")
                    return False

            if not validate_url(badge_url):
                self.log(
                    f"Badge \"{badge_name}\" URL is invalid: {badge_url}.")
                return False

        return True

    def parse_lines(self, lines):
        if lines is None or len(lines) == 0:
            return None

        lines = skip_lines(lines, 1)    # Skip the title.
        lines = skip_empty_lines(lines)  # Skip empty lines.
        # Skip 3 lines of "SPDX-License-Identifier"
        lines = skip_lines(lines, 3)
        lines = skip_empty_lines(lines)  # Skip empty lines.
        badge_line = lines[0] if len(lines) > 0 else None
        lines = skip_lines(lines, 1)    # Skip the badges.
        if len(lines) > 0:
            # No more badges on remaining lines.
            if any(match_badges(line) for line in lines):
                self.log(f"Only one line of badges is allowed.")
                return None

        return match_badges(badge_line)

# README.PURPOSE


class BSReadmeImplementsCheck(BSGenericReadmeCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "README.IMPLEMENTS")

    def check(self):
        """
        Following the purpose and a newline, the README.md should indicate which papers the repository implements. 

        Use the following style:

        **Implements**: [Give *std::optional* Range Support (P3168R1)](https://wg21.link/P3168R1).
        **Implements**: [`std::optional<T&>` (P2988R5)](https://wg21.link/P2988R5) and [Give *std::optional* Range Support (P3168R1)](https://wg21.link/P3168R1).
        """
        lines = self.read_lines_strip()
        if len(lines) == 0:
            return False

        # Find the line with "Implements", make sure is exactly one.
        implements_line = next(
            (line for line in lines if line.startswith("**Implements**:")), None)
        if not implements_line:
            self.log(
                f"README.md must contain a line with \"**Implements**: ...\" after the purpose and a newline.")
            return False

        # Check if the line is in the correct format.
        all_paper_md_links = re.findall(
            r"\[.*?\([PD][0-9]*R[0-9]*\)\]\(https://wg21.link/.*?\)", implements_line)
        if len(all_paper_md_links) == 0:
            self.log(
                f"The \"Implements\" line must contain at least one paper link. For example:\n\"**Implements**: [Give *std::optional* Range Support (P3168R1)](https://wg21.link/P3168R1)\"")
            return False

        return True


class BSReadmeLibraryStatusCheck(BSGenericReadmeCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "README.LIBRARY_STATUS")

    def check(self):
        """
        Following the implements section and a newline, the README.md must indicate the current library status
        with respect to the Beman library maturity model.
        """
        lines = self.read_lines_strip()
        if len(lines) == 0:
            return False

        # Find the line with "Status", make sure is exactly one.
        status_line = next(
            (line for line in lines if line.startswith("**Status**:")), None)
        if not status_line:
            self.log(
                f"README.md must contain a line with \"**Status**: ...\" after the implements section and a newline.")
            return False

        # Check if the line is in the Beman Standard (perfect content match).
        beman_standard_status_lines = [line for line in self.full_text_body.split(
            "\n") if line.startswith("**Status**:")]
        if len(beman_standard_status_lines) == 0:
            self.log(
                f"The Beman Standard must contain all possible line with format \"**Status**: ...\" in README.LIBRARY_STATUS.")
            return False
        if status_line not in beman_standard_status_lines:
            self.log(
                f"Status line \"{status_line}\" not found in the Beman Standard.")
            return False

        return True
