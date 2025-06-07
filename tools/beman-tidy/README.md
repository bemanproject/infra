# beman-tidy: The Codebase Bemanification Tool

<!--
SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
-->

## Description

`beman-tidy` is a tool used to check and apply [The Beman Standard](https://github.com/bemanproject/beman/blob/main/docs/BEMAN_STANDARD.md).

Purpose: The tool is used to `check` (`--dry-run`) and `apply` (`--fix-inplace`) the Beman Standard to a repository.
Note: `07.06.2025`: In order to make the best and quickly use of the tool in the entire organization, most of the checks will not support the `--fix-inplace` flag in the first iteration.

## Installation

```shell
$ make install
# or
$ pip3 install -r requirements.txt
```

## Usage

![beman-tidy usage example](./images/usage-example.png)

* Display help:
```shell
$ ./beman-tidy --help
usage: beman-tidy [-h] [--fix-inplace | --no-fix-inplace] [--verbose | --no-verbose] [--checks CHECKS] repo_path

positional arguments:
  repo_path             path to the repository to check

optional arguments:
  -h, --help            show this help message and exit
  --fix-inplace, --no-fix-inplace
                        Try to automatically fix found issues (default: False)
  --verbose, --no-verbose
                        print verbose output for each check (default: False)
  --checks CHECKS       array of checks to run
```

* Run beman-tidy on the exemplar repository (default: dry-run mode)

```shell
# non-verbose mode
$ ./beman-tidy ../../../exemplar
Summary:  3 checks PASSED, 0 checks FAILED, 40 skipped (NOT implemented).

Coverage: 6.98% (3/43 checks passed).

# verbose mode - no errors
$ ./beman-tidy ../../../exemplar --verbose
beman-tidy pipeline started ...

Running check [RECOMMENDATION][README.TITLE] ...
	check [RECOMMENDATION][README.TITLE] ... PASSED

Running check [RECOMMENDATION][README.BADGES] ...
	check [RECOMMENDATION][README.BADGES] ... PASSED

Running check [RECOMMENDATION][README.LIBRARY_STATUS] ...
	check [RECOMMENDATION][README.LIBRARY_STATUS] ... PASSED


beman-tidy pipeline finished.

Summary:  3 checks PASSED, 0 checks FAILED, 40 skipped (NOT implemented).

Coverage: 6.98% (3/43 checks passed).

# verbose mode - with errors
$ ./beman-tidy ../../../exemplar --verbose
beman-tidy pipeline started ...

Running check [RECOMMENDATION][README.TITLE] ...
[WARNING        ][README.TITLE             ]: The first line of the file '/Users/dariusn/dev/dn/git/Beman/exemplar/README.md' is invalid. It should start with '# beman.exemplar: <short_description>'.
	check [RECOMMENDATION][README.TITLE] ... FAILED

Running check [RECOMMENDATION][README.BADGES] ...
	check [RECOMMENDATION][README.BADGES] ... PASSED

Running check [RECOMMENDATION][README.LIBRARY_STATUS] ...
	check [RECOMMENDATION][README.LIBRARY_STATUS] ... PASSED


beman-tidy pipeline finished.

Summary:  2 checks PASSED, 1 checks FAILED, 40 skipped (NOT implemented).

Coverage: 4.65% (2/43 checks passed).
```

* Run beman-tidy on the exemplar repository (fix issues in-place):

```shell
$ ./beman-tidy ../exemplar --fix-inplace --verbose
```

## beman-tidy Development

Expected Development Flow:

* Find a Beman Standard check that is not implemented.
* Add a new entry to the `.beman-standard.yml` file.
* Add a new check to the `lib/checks/beman_standard/` directory (find existing checks for inspiration).
* Add tests for the new check.
* Run the tests.
* Commit the changes.

Requirements:
* `beman-tidy` must be able to run on Windows, Linux, and macOS, thus it's 100% Python.
* `beman-tidy` must NOT used internet access.  A local snapshot of the standard is used (check `.beman-standard.yml`).
* `beman-tidy` must have `verbose` and `non-verbose` modes. Default is `non-verbose`.
* `beman-tidy` must have `dry-run` and `fix-inplace` modes. Default is `dry-run`.
* `beman-tidy` must detect types of checks: failed, passed, skipped (not implemented) and print the summary/coverage.

Limitations:
* `07.06.2025`: `beman-tidy` will not support the `--fix-inplace` flag in the first iteration for most of the checks.
* `07.06.2025`: `beman-tidy` may generate small changes to the standard (e.g., for automated fixes), while the standard is not stable. Thus, the tool itself may be unstable.

### Tree structure

```shell
 $ tree .
.
├── beman-tidy                             # The beman-tidy tool entry point (Python script).
├── .beman-standard.yml                    # The Beman Standard configuration file.
├── __init__.py                            # Allows recursive Python packages imports.
├── README.md                              # Root README / docs.
├── Makefile                               # Makefile for the beman-tidy tool.
├── requirements.txt                       # Production requirements.
├── requirements-dev.txt                   # Development requirements.
├── lib                                    # The library for the beman-tidy tool (e.g, checks, utils, etc.).
│   ├── __init__.py                        # Recursive Python packages imports
│   ├── checks                             # The checks for the beman-tidy tool.
│   │   ├── __init__.py
│   │   ├── base                           # Base classes for the checks - not to be used directly.
│   │   │   ├── __init__.py
│   │   │   ├── base_check.py              # Base class for all checks.
│   │   │   ├── directory_base_check.py    # Base class for directory checks.
│   │   │   └── file_base_check.py         # Base class for file checks.
│   │   ├── beman_standard                 # The ACTUAL checks for the beman standard.
│   │   │   ├── __init__.py
│   │   │   ├── cmake.py                   # CMake related checks.
│   │   │   ├── cpp.py                     # C++ related checks.
│   │   │   ├── directory.py               # Directory related checks.
│   │   │   ├── file.py                    # File related checks.
│   │   │   ├── general.py                 # General checks.
│   │   │   ├── license.py                 # License related checks.
│   │   │   ├── readme.py                  # README.md related checks.
│   │   │   ├── release.py                 # Release related checks.
│   │   │   └── toplevel.py                # Top-level checks.
│   │   └── system                         # System related checks.
│   │       ├── __init__.py
│   │       ├── git.py                     # Git related checks (internal use only).
│   │       └── registry.py                # Registry related checks (internal use only).
│   ├── pipeline.py                        # The pipeline for the beman-tidy tool.
│   └── utils                              # Utility functions for the beman-tidy tool.
│       ├── __init__.py
│       ├── git.py
│       ├── string.py
│       └── terminal.py
└── tests                                  # The tests for the beman-tidy tool.
    ├── __init__.py
    ├── beman_standard
    │   ├── __init__.py
    │   └── readme                         # The tests for the README.md check.
    │       ├── __init__.py
    │       ├── conftest.py                # The conftest for the pytest tests.
    │       ├── data                       # The data for the tests (e.g., file, directory, etc.).
    │       │   ├── invalid
    │       │   │   ├── README.md
    │       │   │   └── README.md.delete_me
    │       │   └── valid
    │       │       └── README.md
    │       └── test_readme.py
    ├── conftest.py
    └── utils
        ├── __init__.py
        └── conftest.py

24 directories, 62 files
```

Notes:

* `beman-tidy`: A Python script that is used to check and apply the Beman Standard to a repository.
* `.beman-standard.yml`: Stable version of the standard; the tool does not fetch the latest unstable version of the standard.
* `lib/`: The library for the beman-tidy tool (e.g, checks, utils, etc.).
   * `lib/checks/beman_standard/`: Direct implementation of the checks from the standard (e.g, `lib/checks/beman_standard/readme.py` is the implementation of the `README.md` checks).
   * `lib/checks/base/`: Base classes for the checks - not to be used directly.
   * `lib/pipeline.py`: The pipeline for the `beman-tidy` tool.
* `tests/`: The tests for the beman-tidy tool.
   * Structure is similar to the `lib/` directory.
   * `pytest` is used for testing.

### Linting

Run the linter:

```shell
# Run the linter - dry run.
$ make lint
# Run the linter - fix issues.
$ make lint-fix
```

### Testing

#### Running Tests

Run the tests:

```shell
$ make install-dev
pip3 install -r requirements-dev.txt
...q
$ make test
Running tests...
python3 -m pytest tests/ -v
========================================================================================================= test session starts =========================================================================================================
platform darwin -- Python 3.9.6, pytest-8.4.0, pluggy-1.6.0 -- /Library/Developer/CommandLineTools/usr/bin/python3
cachedir: .pytest_cache
rootdir: /Users/dariusn/dev/dn/git/Beman/infra/tools/beman-tidy
collected 3 items

tests/beman_standard/readme/test_readme.py::test__README_TITLE__valid PASSED                                                                                                                                                    [ 33%]
tests/beman_standard/readme/test_readme.py::test__README_TITLE__invalid PASSED                                                                                                                                                  [ 66%]
tests/beman_standard/readme/test_readme.py::test__README_TITLE__fix_invalid PASSED                                                                                                                                              [100%]

========================================================================================================== 3 passed in 0.08s ==========================================================================================================


```

#### Writing Tests

* `tests/beman_standard/<check_category>/test_<check_category>.py`: The test file for the `<check_category>` check.
  * e.g., for `check_category = "readme"` the test file is `tests/beman_standard/readme/test_readme.py`.
* `test__<check_category>__<test_case_name>()` function inside the test file.
  * e.g., for `check_category = "readme"` and `test_case_name = "valid"` the function is `test__README_TITLE__valid()`.
  * e.g., for `check_category = "readme"` and `test_case_name = "invalid"` the function is `test__README_TITLE__invalid()`.
* `tests/beman_standard/<check_category>/data/`: The data for the tests (e.g., files, directories, etc.).
  * e.g., for `check_category = "readme"` and `test_case_name = "valid"` the data is in `tests/beman_standard/readme/data/valid/`.
  * e.g., for `check_category = "readme"` and `test_case_name = "invalid"` the data is in `tests/beman_standard/readme/data/invalid/`.
  * e.g., for `check_category = "readme"` and `test_case_name = "fix_invalid"` the data may use both `valid` and `invalid` files. It is recommended to not change these files and use temporary copies having suffix `.delete_me` (which are not tracked by git).
* Default setup / mocks:
  * `repo_info`: The repository information (e.g., path, name, etc.). Mocked with hardcoded values of `beman.exemplar`.
  * `beman_standard_check_config`: The Beman Standard configuration file. Actual load of the `.beman-standard.yml` file.
* Always add at least 3 test cases for each check.
  * `valid`: The test case for the valid case.
  * `invalid`: The test case for the invalid case.
  * `fix_invalid`: The test case for the fix invalid case. If the fix is not (yet) implementable, add a `@pytest.mark.skip(reason="NOT implemented")` decorator to track the progress.
