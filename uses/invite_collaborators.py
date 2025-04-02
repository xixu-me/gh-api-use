"""
Invite Collaborators to a Repository

This script invites multiple GitHub users as collaborators to a repository
with the specified permission level. Useful for onboarding new team members
or contributors to a project.

Usage:
1. Set your Personal Access Token (PAT) with 'repo' and 'admin' scope permissions
2. Configure the repository owner, repository name, collaborator usernames, and permission level
3. Run the script: python invite_collaborators.py

Permission levels:
- pull: Read-only access to code
- push: Read-write access to code
- admin: Full repository access including settings
- maintain: Read-write access + some repository settings (manages repository without admin)
- triage: Read-only access + manage issues and pull requests

Requirements:
- requests library: pip install requests
"""

import requests

# Configuration - Replace these values with your own
TOKEN = "YOUR_PAT"  # Personal Access Token with 'repo' and 'admin' scopes
OWNER = "your-username"  # GitHub username or organization name
REPO = "your-repo"  # Repository name
USERNAMES = ["user1", "user2", "user3"]  # List of GitHub usernames to invite
PERMISSION = "push"  # Permission level to grant (pull, push, admin, maintain, triage)

# Set up request headers with authentication
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

# Track invitation results
successful = []
failed = []

# Invite each user as a collaborator
for username in USERNAMES:
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/collaborators/{username}"
    payload = {"permission": PERMISSION}

    # Send the request to add the collaborator
    response = requests.put(url, headers=headers, json=payload)

    # Status code 201: invitation created
    # Status code 204: user was already a collaborator
    if response.status_code == 201:
        print(f"Invited {username} to {REPO} with {PERMISSION} permission")
        successful.append(username)
    elif response.status_code == 204:
        print(f"{username} is already a collaborator on {REPO}")
        successful.append(username)
    else:
        print(f"Failed to invite {username}: {response.status_code}")
        print(response.json().get("message", "No error message provided"))
        failed.append(username)

# Summary
print("\nSummary:")
print(f"Successfully processed {len(successful)} user(s): {', '.join(successful)}")
if failed:
    print(f"Failed to process {len(failed)} user(s): {', '.join(failed)}")
