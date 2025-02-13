# beman-tidy: Codebase Bemanification Tool

<!--
SPDX-License-Identifier: 2.0 license with LLVM exceptions
-->

## Description

`beman-tidy` is a tool used to check and apply [The Beman Standard](https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md).

## Installation

```shell
$ pip3 install -r requirements.txt
```

## Usage

```shell
# Display help.
$ ./tools/beman-tidy/beman-tidy --help
usage: beman-tidy [-h] --repo-path REPO_PATH [--dry-run | --no-dry-run] [--verbose | --no-verbose]

optional arguments:
  -h, --help            show this help message and exit
  --repo-path REPO_PATH
                        path to the repository to check
  --dry-run, --no-dry-run
                        DO NOT try to automatically fix found issues (default: False)
  --verbose, --no-verbose
                        print verbose output for each check (default: False)

# Run beman-tidy on the exemplar repository (automatically fix issues).
$ ./tools/beman-tidy/beman-tidy --repo-path ../exemplar
Summary: 8 checks PASSED, 2 checks FAILED, 35 skipped (not implemented).

Coverage: 17.78% (8/45 checks passed).

# Run beman-tidy on the exemplar repository (automatically fix issues, verbose output).
$ ./tools/beman-tidy/beman-tidy --repo-path ../exemplar --verbose
beman-tidy started ...

Running check [REQUIREMENT][TOPLEVEL.CHANGELOG] ...
    check [REQUIREMENT][TOPLEVEL.CHANGELOG] ... PASSED

Running check [REQUIREMENT][TOPLEVEL.CMAKE] ...
    check [REQUIREMENT][TOPLEVEL.CMAKE] ... PASSED

Running check [REQUIREMENT][TOPLEVEL.LICENSE] ...
    check [REQUIREMENT][TOPLEVEL.LICENSE] ... PASSED

Running check [REQUIREMENT][TOPLEVEL.README] ...
    check [REQUIREMENT][TOPLEVEL.README] ... PASSED

Running check [REQUIREMENT][CHANGELOG.TITLE] ...
    check [REQUIREMENT][CHANGELOG.TITLE] ... PASSED

Running check [REQUIREMENT][CHANGELOG.LIBRARY_STATUS] ...
    check [REQUIREMENT][CHANGELOG.LIBRARY_STATUS] ... PASSED

Running check [RECOMMENDATION][README.TITLE] ...
    check [RECOMMENDATION][README.TITLE] ... FAILED

Running check [REQUIREMENT][README.BADGES] ...
[ERROR          ][README.BADGES            ]: Only one line of badges is allowed.
[ERROR          ][README.BADGES            ]: First line of README.md must contain badges.
    check [REQUIREMENT][README.BADGES] ... FAILED

Running check [RECOMMENDATION][README.IMPLEMENTS] ...
    check [RECOMMENDATION][README.IMPLEMENTS] ... PASSED

Running check [REQUIREMENT][README.LIBRARY_STATUS] ...
    check [REQUIREMENT][README.LIBRARY_STATUS] ... PASSED


beman-tidy finished.

Summary: 8 checks PASSED, 2 checks FAILED, 35 skipped (not implemented).

Coverage: 17.78% (8/45 checks passed).
```
