"""
Create Releases

This script creates a new release with the specified tag, name, and release notes
across multiple repositories. Useful for projects with multiple related repositories
that should have synchronized releases.

Usage:
1. Set your Personal Access Token (PAT) with 'repo' scope permission
2. Configure the repository owner, repository list, and release details
3. Run the script: python create_releases.py

Requirements:
- requests library: pip install requests
"""

import requests

# Configuration - Replace these values with your own
TOKEN = "YOUR_PAT"  # Personal Access Token with 'repo' scope
OWNER = "your-username"  # GitHub username or organization name
REPOS = ["repo1", "repo2", "repo3"]  # List of repositories to create releases for
TAG_NAME = "v1.0.0"  # Git tag for the release
RELEASE_NAME = "Version 1.0.0"  # Human-readable release title
BODY = "Release notes for v1.0.0"  # Description/notes for the release

# Set up request headers with authentication
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

# Create a release for each repository in the list
for repo in REPOS:
    url = f"https://api.github.com/repos/{OWNER}/{repo}/releases"

    # Prepare the release data
    payload = {
        "tag_name": TAG_NAME,
        "name": RELEASE_NAME,
        "body": BODY,
        "draft": False,  # Set to True to create a draft release
        "prerelease": False,  # Set to True for prereleases/beta versions
    }

    # Send the request to create the release
    response = requests.post(url, headers=headers, json=payload)

    # Check the response and print results
    if response.status_code == 201:
        release_data = response.json()
        print(f"Created release for {repo}: {release_data.get('html_url')}")
    else:
        print(f"Failed to create release for {repo}: {response.status_code}")
        print(response.json().get("message", "No error message provided"))
