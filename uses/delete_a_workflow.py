"""
Delete All Runs for a Specific Workflow

This script deletes all runs for a specific GitHub Actions workflow.
Useful when you need to clean up a workflow's history completely.

Usage:
1. Set your Personal Access Token (PAT) with 'repo' and 'workflow' scope permissions
2. Configure the repository owner, repository name, and workflow ID
3. Run the script: python delete-workflow.py

To find your workflow ID:
curl -H "Authorization: Bearer YOUR_PAT" -H "Accept: application/vnd.github+json" \
     https://api.github.com/repos/OWNER/REPO/actions/workflows

Requirements:
- requests library: pip install requests
"""

import requests

# Configuration - Replace these values with your own
TOKEN = "YOUR_PAT"  # Personal Access Token with 'repo' and 'workflow' scopes
OWNER = "your-username"  # GitHub username or organization name
REPO = "your-repo"  # Repository name
WORKFLOW_ID = "your-workflow-id"  # ID of the workflow to delete runs for

# Set up request headers with authentication
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

# Get all runs for the specified workflow
url = (
    f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{WORKFLOW_ID}/runs"
)
response = requests.get(url, headers=headers)

# Check for successful API response
if response.status_code != 200:
    print(f"Error fetching workflow runs: {response.status_code}")
    print(response.json().get("message", "No error message provided"))
    exit(1)

runs = response.json()["workflow_runs"]
total_deleted = 0

# Delete each run in the current page
for run in runs:
    run_id = run["id"]
    delete_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}"

    # Send the request to delete the run
    delete_response = requests.delete(delete_url, headers=headers)

    if delete_response.status_code == 204:
        print(f"Deleted run {run_id}")
        total_deleted += 1
    else:
        print(f"Failed to delete run {run_id}: {delete_response.status_code}")

# Handle pagination if there are more runs
# GitHub API returns pagination links in the response headers
while "next" in response.links:
    response = requests.get(response.links["next"]["url"], headers=headers)

    if response.status_code != 200:
        print(f"Error fetching next page: {response.status_code}")
        break

    runs = response.json()["workflow_runs"]

    for run in runs:
        run_id = run["id"]
        delete_url = (
            f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}"
        )

        # Send the request to delete the run
        delete_response = requests.delete(delete_url, headers=headers)

        if delete_response.status_code == 204:
            print(f"Deleted run {run_id}")
            total_deleted += 1
        else:
            print(f"Failed to delete run {run_id}: {delete_response.status_code}")

print(f"Total runs deleted: {total_deleted}")
