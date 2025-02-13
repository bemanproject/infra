#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

from ..base.generic_file_check import BSGenericFileCheck


class BSGeneriChangelogCheck(BSGenericFileCheck):
    def __init__(self, repo_info, beman_standard, check_name):
        super().__init__(repo_info, beman_standard, check_name, "Changelog.md")


# TODO CHANGELOG.TITLE
class BSChangelogTitleCheck(BSGeneriChangelogCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "CHANGELOG.TITLE")

    def check(self):
        """
        The CHANGELOG.md must begin with a level 1 header with the name "Changelog".
        """
        lines = self.read_lines_strip()
        if len(lines) == 0:
            self.log(f"CHANGELOG.md is empty.")
            return False
        first_line = lines[0]

        # Match the pattern
        if not first_line.startswith("#") or not first_line[2:].startswith("Changelog"):
            self.log(
                f"CHANGELOG.md must begin with a level 1 header with the name 'Changelog'")
            return False

        return True

    def fix(self):
        default_line_title = "# Changelog"

        all_lines = self.read_lines_strip()
        if len(all_lines) > 0 and all_lines[0].startswith("#"):
            all_lines[0] = default_line_title
        else:
            all_lines.insert(0, default_line_title)

        all_lines.append("")  # Add empty line at the end of the file.
        self.write_lines(all_lines)

# TODO CHANGELOG.FORMAT


class BSChangelogLibraryStatus(BSGeneriChangelogCheck):
    def __init__(self, repo_info, beman_standard):
        super().__init__(repo_info, beman_standard, "CHANGELOG.LIBRARY_STATUS")

    def check(self):
        """
        The CHANGELOG.md must contain a line for each previous library status with respect to the Beman library maturity model.

        The line must be in the format:
        - [LIBRARY_STATUS]: Library status updated to [${LIBRARY STATUS}](${LIBRARY STATUS BADGE URL}): It was rejected from ISO standardization.

        """
        all_lines = self.read_lines_strip()
        if len(all_lines) == 0:
            self.log(f"CHANGELOG.md is empty.")
            return False

        # Extract all beman standard library status from the full_text_body.
        standard_library_status = [line for line in self.full_text_body.split(
            "\n") if line.startswith("- [LIBRARY_STATUS]")]
        # Extract all library status from the CHANGELOG.md
        changelog_library_status = [
            line for line in all_lines if line.startswith("- [LIBRARY_STATUS]")]

        if len(changelog_library_status) == 0:
            self.log(f"CHANGELOG.md must contain a line for each previous library status with respect to the Beman library maturity model. Initial library status is missing.")
            return False

        for library_status in changelog_library_status:
            # Check for common prefix until 3rd column.
            if not any(standard_status[:standard_status.index(")") + 1] in library_status for standard_status in standard_library_status):
                self.log(
                    f"Library status '{library_status}' is not in the correct format.")
                return False

        return True

    def fix(self):
        # Only if the changelog is empty, add the initial library status.
        all_lines = self.read_lines_strip()
        if len(all_lines) > 1:
            return False

        default_change_log = [
            "# Changelog",
            "",
            "<!---",
            "SPDX-License-Identifier: 2.0 license with LLVM exceptions",
            "--->",
            "",
            "## [Unreleased]",
            "",
            "### Added",
            "- [LIBRARY_STATUS]: Library status updated to [Under development and not yet ready for production use.](https://github.com/bemanproject/beman/blob/main/docs/BEMAN_LIBRARY_MATURITY_MODEL.md#under-development-and-not-yet-ready-for-production-use): It is not yet ready for production use."
            "",
            ""
        ]
        self.write_lines(default_change_log)
