"""
Close Old Issues

This script automatically closes issues that have been open for longer than
a specified number of days. It ignores pull requests even if they appear in
the issues list.

Usage:
1. Set your Personal Access Token (PAT) with 'repo' scope permission
2. Configure the repository owner, repository name, and age threshold
3. Run the script: python close_old_issues.py

Requirements:
- requests library: pip install requests
"""

from datetime import datetime, timedelta

import requests

# Configuration - Replace these values with your own
TOKEN = "YOUR_PAT"  # Personal Access Token with 'repo' scope
OWNER = "your-username"  # GitHub username or organization name
REPO = "your-repo"  # Repository name
DAYS_OLD = 90  # Close issues older than this many days

# Set up request headers with authentication
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

# Get all open issues
url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues?state=open"
response = requests.get(url, headers=headers)

# Check for successful API response
if response.status_code != 200:
    print(f"Error fetching issues: {response.status_code}")
    print(response.json().get("message", "No error message provided"))
    exit(1)

issues = response.json()

# Calculate the cutoff date for closing issues
cutoff_date = datetime.now() - timedelta(days=DAYS_OLD)

# Process each issue
for issue in issues:
    # Skip pull requests which appear in the issues list but should not be auto-closed
    if "pull_request" not in issue:
        issue_date = datetime.strptime(issue["created_at"], "%Y-%m-%dT%H:%M:%SZ")

        # Check if the issue is older than the cutoff date
        if issue_date < cutoff_date:
            issue_number = issue["number"]
            close_url = (
                f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{issue_number}"
            )
            payload = {"state": "closed"}

            # Send the request to close the issue
            close_response = requests.patch(close_url, headers=headers, json=payload)

            if close_response.status_code == 200:
                print(
                    f"Closed issue #{issue_number} (Created: {issue_date.strftime('%Y-%m-%d')})"
                )
            else:
                print(
                    f"Failed to close issue #{issue_number}: {close_response.status_code}"
                )
                print(close_response.json().get("message", "No error message provided"))
