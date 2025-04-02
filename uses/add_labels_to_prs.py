"""
Add Labels to Pull Requests

This script adds a specified label to all open pull requests in a repository.
Useful for bulk labeling of PRs that need attention or categorization.

Usage:
1. Set your Personal Access Token (PAT) with 'repo' scope permission
2. Configure the repository owner, repository name, and desired label
3. Run the script: python add_labels_to_prs.py

Requirements:
- requests library: pip install requests
"""

import requests

# Configuration - Replace these values with your own
TOKEN = "YOUR_PAT"  # Personal Access Token with 'repo' scope
OWNER = "your-username"  # GitHub username or organization name
REPO = "your-repo"  # Repository name
LABEL = "needs-review"  # Label to add to all open PRs

# Set up request headers with authentication
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

# Get all open pull requests
url = f"https://api.github.com/repos/{OWNER}/{REPO}/pulls?state=open"
response = requests.get(url, headers=headers)

# Check for successful API response
if response.status_code != 200:
    print(f"Error fetching pull requests: {response.status_code}")
    print(response.json().get("message", "No error message provided"))
    exit(1)

pulls = response.json()

# Add the label to each pull request
for pull in pulls:
    issue_number = pull["number"]
    labels_url = (
        f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}/labels"
    )
    payload = [LABEL]  # Labels are submitted as an array

    # Send the request to add the label
    label_response = requests.post(labels_url, headers=headers, json=payload)

    if label_response.status_code == 200 or label_response.status_code == 201:
        print(f"Added label '{LABEL}' to PR #{issue_number}")
    else:
        print(
            f"Failed to add label to PR #{issue_number}: {label_response.status_code}"
        )
        print(label_response.json().get("message", "No error message provided"))
