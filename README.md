# GitHub REST API Use

A collection of Python scripts demonstrating practical uses of the GitHub REST API for repository management and automation.

## Overview

This repository contains ready-to-use Python scripts for common GitHub repository management tasks that can be performed using the GitHub REST API. These scripts help automate repetitive tasks and streamline repository workflows.

## Requirements

- Python 3.6+
- `requests` library: `pip install requests`
- GitHub Personal Access Token (PAT) with appropriate permissions

## Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/username/gh-api-use.git
   cd gh-api-use
   ```

2. Install the required Python package:

   ```bash
   pip install requests
   ```

3. Create a GitHub Personal Access Token:
   - Go to GitHub > Settings > Developer settings > Personal access tokens
   - Generate a new token with the necessary permissions (usually `repo` scope)
   - Copy your token for use in the scripts

## Usage

Each script follows a similar pattern:

1. Open the script you want to use and replace the configuration variables:
   - `TOKEN`: Your GitHub Personal Access Token
   - `OWNER`: Your GitHub username or organization name
   - `REPO`: Target repository name
   - Other script-specific settings

2. Run the script:

   ```bash
   python uses/script_name.py
   ```

3. Check the console output for results

## Permissions

Different scripts require different token scopes:

- `repo` - For repository operations (all scripts)
- `workflow` - For GitHub Actions workflow operations
- `admin` - For repository administration tasks

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Copyright &copy; [Xi Xu](https://xi-xu.me). All rights reserved.

Licensed under the [GPL-3.0](LICENSE) license.
