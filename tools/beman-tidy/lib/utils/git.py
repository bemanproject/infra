#!/usr/bin/python3
# SPDX-License-Identifier: 2.0 license with LLVM exceptions

from .terminal import run_command
import markdown
import os
import re
import requests
import sys

from git import Repo, InvalidGitRepositoryError


def get_repo_info(path):
    """
    Get information about the Git repository at the given path.
    Returns a dictionary with data about the repository.
    """

    try:
        # Initialize the repository object
        repo = Repo(os.path.abspath(path), search_parent_directories=True)

        # Get the top-level directory of the repository
        top_level_dir = repo.git.rev_parse("--show-toplevel")

        # Get the repository name (directory name of the top level)
        repo_name = os.path.basename(top_level_dir)

        # Get the remote URL (assuming 'origin' is the remote name)
        remote_url = None
        if "origin" in repo.remotes:
            remote_url = repo.remotes.origin.url

        # Get the current branch
        current_branch = repo.active_branch.name

        # Get the commit hash
        commit_hash = repo.head.commit.hexsha

        # Get the status of the repository
        status = repo.git.status()

        # Get unstaged changes
        unstaged_changes = repo.git.diff("--stat")

        return {
            "top_level": top_level_dir,
            "name": repo_name,
            "remote_url": remote_url,
            "current_branch": current_branch,
            "commit_hash": commit_hash,
            "status": status,
            "unstaged_changes": unstaged_changes,
        }
    except InvalidGitRepositoryError:
        print(f"The path '{path}' is not inside a valid Git repository.")
        sys.exit(1)
    except Exception as e:
        print(
            f"An error occurred while getting repository information. Check {path}.")
        sys.exit(1)


def parse_beman_standard(beman_standard_md_content):
    """
    Parse the Markdown content to extract checks from The Beman Standard

    Args:
        markdown_content (str): The raw Markdown content.

    Returns:
        [(check_name, check_type, check_body)]: A list of check tuples.
    """
    # Regex pattern to match checks
    pattern = r"\*\*\[([A-Z._]+)\]\*\* (REQUIREMENT|RECOMMENDATION):\s*(.*?)(?=\*\*\[|$)"
    matches = re.finditer(pattern, beman_standard_md_content, re.DOTALL)

    bs_checks = []
    for match in matches:
        check_name = match.group(1)
        check_type = match.group(2)
        check_body = match.group(3).strip()

        bs_checks.append((check_name, check_type, check_body))

    return bs_checks


def download_file(url):
    """
    Download a file from the given URL.
    """
    try:
        # Fetch the content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(
            f"An error occurred while downloading from ${raw_url}: {e}.\nSTOP.")
        sys.exit(1)


def download_beman_standard():
    """
    Download and parse The Beman Standard content from the GitHub repository.
    """
    # Raw GitHub URL for the Markdown file
    # raw_url = "https://raw.githubusercontent.com/bemanproject/beman/main/docs/BEMAN_STANDARD.md"
    raw_url = "https://raw.githubusercontent.com/bemanproject/beman/neatudarius-patch-9/docs/BEMAN_STANDARD.md"
    beman_standard_md_content = download_file(raw_url)
    bs_checks = parse_beman_standard(beman_standard_md_content)
    return bs_checks


def download_beman_default_license():
    """
    Download and parse the default Beman LICENSE content from the GitHub repository.
    """
    raw_url = "https://raw.githubusercontent.com/bemanproject/beman/refs/heads/main/LICENSE"
    licent_content = download_file(raw_url)
    return licent_content


def validate_url(url):
    """
    Validate the URL.
    """
    import requests
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        return False
