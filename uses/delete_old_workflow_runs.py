"""
Delete Old Workflow Runs

This script deletes GitHub Actions workflow runs that are older than a specified
number of days. Useful for cleaning up repositories with many workflow runs to
save storage space and improve workflow run list readability.

Usage:
1. Set your Personal Access Token (PAT) with 'repo' and 'workflow' scope permissions
2. Configure the repository owner, repository name, and retention period
3. Run the script: python delete_old_workflow_runs.py

Requirements:
- requests library: pip install requests
"""

from datetime import datetime, timedelta

import requests

# Configuration - Replace these values with your own
TOKEN = "YOUR_PAT"  # Personal Access Token with 'repo' and 'workflow' scopes
OWNER = "your-username"  # GitHub username or organization name
REPO = "your-repo"  # Repository name
DAYS_TO_KEEP = 30  # Delete workflow runs older than this many days

# Set up request headers with authentication
headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

# Get all workflows in the repository
url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows"
response = requests.get(url, headers=headers)

# Check for successful API response
if response.status_code != 200:
    print(f"Error fetching workflows: {response.status_code}")
    print(response.json().get("message", "No error message provided"))
    exit(1)

workflows = response.json()["workflows"]

# Calculate the cutoff date for deleting runs
cutoff_date = datetime.now() - timedelta(days=DAYS_TO_KEEP)

# Process each workflow
for workflow in workflows:
    workflow_id = workflow["id"]
    workflow_name = workflow["name"]
    print(f"Processing workflow: {workflow_name} (ID: {workflow_id})")

    # Get all runs for this workflow
    runs_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{workflow_id}/runs"
    runs_response = requests.get(runs_url, headers=headers)

    if runs_response.status_code != 200:
        print(
            f"Error fetching runs for workflow {workflow_name}: {runs_response.status_code}"
        )
        continue

    runs = runs_response.json()["workflow_runs"]

    # Check each run against the cutoff date
    for run in runs:
        run_date = datetime.strptime(run["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        if run_date < cutoff_date:
            run_id = run["id"]
            delete_url = (
                f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{run_id}"
            )

            # Send the request to delete the run
            delete_response = requests.delete(delete_url, headers=headers)

            if delete_response.status_code == 204:
                print(
                    f"Deleted run {run_id} from workflow {workflow_name} (Created: {run_date.strftime('%Y-%m-%d')})"
                )
            else:
                print(f"Failed to delete run {run_id}: {delete_response.status_code}")
