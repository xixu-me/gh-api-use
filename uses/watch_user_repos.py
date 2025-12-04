"""
Watch All Repositories of a User

This script subscribes (watches) all repositories of a specified GitHub user.
Useful for staying updated on all activity from a particular user or organization.

Usage:
1. Replace TOKEN with your GitHub Personal Access Token
2. Replace TARGET_USER with the username whose repos you want to watch
3. Run the script: python watch_user_repos.py

Requirements:
- PAT with `repo` scope (for private repos) or no special scope (for public repos only)
"""

import time

import requests

# Configuration - replace these values
TOKEN = "YOUR_PAT"  # GitHub Personal Access Token
TARGET_USER = "target_username"  # Username whose repositories to watch

# API setup
API = "https://api.github.com"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def list_user_repos(username):
    """List all repositories of a user (public, and private if token has access)."""
    page = 1
    while True:
        resp = requests.get(
            f"{API}/users/{username}/repos",
            headers=headers,
            params={
                "per_page": 100,
                "page": page,
                "type": "all",
                "sort": "full_name",
            },
        )
        if resp.status_code != 200:
            error_msg = resp.json().get("message", "No error message provided")
            print(f"Error listing repos: {error_msg}")
            break
        repos = resp.json()
        if not repos:
            break
        yield from repos
        page += 1


def watch_repo(owner, repo_name):
    """Subscribe (watch) a single repository."""
    url = f"{API}/repos/{owner}/{repo_name}/subscription"
    payload = {
        "subscribed": True,
        "ignored": False,
    }
    resp = requests.put(url, json=payload, headers=headers)
    if resp.status_code in (200, 201):
        print(f"Watching {owner}/{repo_name}")
    else:
        error_msg = resp.json().get("message", "No error message provided")
        print(f"Failed {owner}/{repo_name}: {error_msg}")


def watch_all_repos_of_user(username):
    """Watch all repositories of a specified user."""
    print(f"Fetching repositories for user: {username}")
    count = 0
    for repo in list_user_repos(username):
        owner = repo["owner"]["login"]
        name = repo["name"]
        watch_repo(owner, name)
        count += 1
        # Sleep to avoid hitting secondary rate limits
        time.sleep(0.2)
    print(f"Finished. Watched {count} repositories.")


if __name__ == "__main__":
    watch_all_repos_of_user(TARGET_USER)
