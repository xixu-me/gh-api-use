"""
Delete Non-Success Workflow Runs

This script deletes GitHub Actions workflow runs whose conclusion is not
"success". Useful for cleaning up failed, cancelled, timed out, skipped, or
otherwise unsuccessful runs while keeping successful history intact.

Usage:
1. Set your Personal Access Token (PAT) with 'repo' and 'workflow' scope permissions
2. Configure the repository owner and repository name
3. Run the script: python delete_unsuccessful_workflow_runs.py

Requirements:
- requests library: pip install requests
"""

import requests

# Configuration - Replace these values with your own
TOKEN = "YOUR_PAT"  # Personal Access Token with 'repo' and 'workflow' scopes
OWNER = "your-username"  # GitHub username or organization name
REPO = "your-repo"  # Repository name

# Set up request headers with authentication
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs?per_page=100"
total_seen = 0
total_deleted = 0
total_skipped = 0

while url:
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error fetching workflow runs: {response.status_code}")
        print(response.json().get("message", "No error message provided"))
        exit(1)

    runs = response.json().get("workflow_runs", [])

    for run in runs:
        total_seen += 1
        run_id = run["id"]
        conclusion = run.get("conclusion")
        workflow_name = run.get("name", "Unknown workflow")
        status = run.get("status", "unknown")

        if conclusion == "success":
            total_skipped += 1
            print(f"Kept run {run_id} from {workflow_name} (conclusion: success)")
            continue

        delete_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}"
        delete_response = requests.delete(delete_url, headers=headers)

        if delete_response.status_code == 204:
            print(
                f"Deleted run {run_id} from {workflow_name} "
                f"(status: {status}, conclusion: {conclusion})"
            )
            total_deleted += 1
        else:
            print(
                f"Failed to delete run {run_id}: {delete_response.status_code} "
                f"(status: {status}, conclusion: {conclusion})"
            )

    url = response.links.get("next", {}).get("url")

print(f"Total runs checked: {total_seen}")
print(f"Total runs deleted: {total_deleted}")
print(f"Total successful runs kept: {total_skipped}")
