#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

from .checks.system.git import *
from .checks.beman_standard.changelog import *
from .checks.beman_standard.cmake import *
from .checks.beman_standard.cpp import *
from .checks.beman_standard.directory import *
from .checks.beman_standard.file import *
from .checks.beman_standard.general import *
from .checks.beman_standard.license import *
from .checks.beman_standard.readme import *
from .checks.beman_standard.toplevel import *


def get_all_implemented_checks():
    """
    Get the checks pipeline - it is a list of checks, that need to be run.
    The list may contain checks that are not from The Beman Standard.

    Returns a list of checks that need to be run.
    """
    return [
        # TOPLEVEL
        BSTopLevelChangelogCheck,
        BSTopLevelCMakeListsCheck,
        BSTopLevelLicenseCheck,
        BSTopLevelREADMECheck,

        # CHANGELOG
        BSChangelogTitleCheck,
        BSChangelogLibraryStatus,

        # README
        BSReadmeTitleCheck,
        BSReadmeBadgesCheck,
        # PURPOSE
        BSReadmeImplementsCheck,
        BSReadmeLibraryStatusCheck,
    ]


def get_beman_standard_check(beman_standard, check_name):
    """
    Get The Beman Standard check object from the Beman Standard that matches the check_name.
    """
    return next(filter(lambda bs_check: bs_check[0] == check_name, beman_standard), None)


def run_checks_pipeline(args, beman_standard):
    """
    Run the checks pipeline for The Beman Standard.
    Read-only checks if args.dry_run is True, otherwise try to fix the issues in-place.
    Verbosity is controlled by args.verbose.
    """
    def log(msg):
        if args.verbose:
            print(msg)

    def run_check(generic_check, log_enabled=args.verbose):
        bs_check = generic_check(args.repo_info, beman_standard)
        bs_check.log_enabled = log_enabled

        log(
            f"Running check [{bs_check.type}][{bs_check.name}] ... ")

        if (bs_check.base_check() and bs_check.check()) or (not args.dry_run and bs_check.fix()):
            log(f"\tcheck [{bs_check.type}][{bs_check.name}] ... {green_passed}\n")
            return True
        else:
            log(f"\tcheck [{bs_check.type}][{bs_check.name}] ... {red_failed}\n")
            return False

    red_failed = "\033[91mFAILED\033[0m"
    green_passed = "\033[92mPASSED\033[0m"

    log("beman-tidy started ...\n")

    # Internal checks
    if args.dry_run:
        run_check(BSCheckFixInplaceIncompatibleWithUnstagedChanges,
                  log_enabled=False)

    cnt_passed = 0
    cnt_failed = 0
    for generic_check in get_all_implemented_checks():
        if run_check(generic_check):
            cnt_passed += 1
        else:
            cnt_failed += 1

    log("\nbeman-tidy finished.\n")
    print(f"Summary: {cnt_passed} checks {green_passed}, {cnt_failed} checks {red_failed}, {len(beman_standard) - len(get_all_implemented_checks())} skipped (not implemented).")
    sys.stdout.flush()


def print_coverage(repo_info, beman_standard):
    """
    Print The Beman Standard coverage.
    """
    all_implemented_checks = [generic_check(
        repo_info, beman_standard) for generic_check in get_all_implemented_checks()]
    all_bs_implemented_checks = [check for check in all_implemented_checks if get_beman_standard_check(
        beman_standard, check.name) is not None]
    passed_bs_checks = [
        check for check in all_bs_implemented_checks if check.base_check() and check.check()]
    coverage = round(len(passed_bs_checks) / len(beman_standard) * 100, 2)

    print(
        f"\n\033[93mCoverage: {coverage}% ({len(passed_bs_checks)}/{len(beman_standard)} checks passed).\033[0m")
