# Beman Tidy Development Guide

Expected Development Flow:

* Find a Beman Standard check that is not implemented.
* Add a new entry to the `.beman-standard.yml` file.
* Add a new check to the `lib/checks/beman_standard/` directory (find existing checks for inspiration).
* Add tests for the new check.
* Run the tests.
* Commit the changes.

Requirements:
* `beman-tidy` must be able to run on Windows, Linux, and macOS, thus it's 100% Python.
* `beman-tidy` must NOT use internet access.  A local snapshot of the standard is used (check `.beman-standard.yml`).
* `beman-tidy` must have `verbose` and `non-verbose` modes. Default is `non-verbose`.
* `beman-tidy` must have `dry-run` and `fix-inplace` modes. Default is `dry-run`.
* `beman-tidy` must detect types of checks: failed, passed, skipped (not implemented) and print the summary/coverage.

Limitations:
* `2025-06-07`: `beman-tidy` will not support the `--fix-inplace` flag in the first iteration for most of the checks.
* `2025-06-07`: `beman-tidy` may generate small changes to the standard (e.g., for automated fixes), while the standard is not stable. Thus, the tool itself may be unstable.

## Tree structure

* `beman-tidy`: A Python script that is used to check and apply the Beman Standard to a repository.
* `.beman-standard.yml`: Stable version of the standard; the tool does not fetch the latest unstable version of the standard.
* `lib/`: The library for the beman-tidy tool (e.g, checks, utils, etc.).
   * `lib/checks/beman_standard/`: Direct implementation of the checks from the standard (e.g, `lib/checks/beman_standard/readme.py` is the implementation of the `README.md` checks).
   * `lib/checks/base/`: Base classes for the checks - not to be used directly.
   * `lib/pipeline.py`: The pipeline for the `beman-tidy` tool.
* `tests/`: The tests for the beman-tidy tool.
   * Structure is similar to the `lib/` directory.
   * `pytest` is used for testing.

## Linting

Run the linter:

```shell
# Run the linter - dry run.
$ make lint
# Run the linter - fix issues.
$ make lint-fix
```

## Testing

### Running Tests

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

### Writing Tests

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
