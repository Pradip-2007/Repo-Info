# GitHub CLI Tool

A command-line interface (CLI) tool written in Python to effortlessly fetch details about GitHub users and their public repositories using the GitHub API.

## Features

- **User Profile Information**: Retrieve comprehensive data about any GitHub user, including their username, full name, avatar URL, GitHub profile link, email (if public), bio, follower count, and following count.
- **Repository Details**: Obtain information for a particular repository, such as its public/private status, fork count, stargazers count, watchers count, associated topics, and license information.
- **Clear Output**: Presents fetched data in a readable key-value format directly in your terminal.

## Requirements

To run this tool, you will need:

- Python 3.6+
- The `requests` library for making HTTP requests to the GitHub API.

## Installation

1.  **Clone the repository** (if applicable, otherwise just ensure `main.py` is in your working directory):
    ```bash
    git clone https://github.com/Pradip-2007/Repo-Info.git
    cd Repo-Info
    ```
2.  **Install the required Python library**:
    ```bash
    pip install -r requirements.txt
    ```

## Command-Line Interface

The tool uses `argparse` for a user-friendly command-line experience.
### View Help
To view all available arguments and their description :
```bash
python main.py -h 
```
### Arguments

- `-user`, `--username` **(required)**  
  Specifies the GitHub username.This argument is mandatory and must always be provided.
- `-repo`, `--reponame` *(optional)*  
  Specifies the repository name.If provided along with `--username`, the tool fetches repository details instead of user details.
- `-h`, `--help`  
  Displays the help message with all available arguments and exits.

### Behaviour

- **Fetch User Details :**
To get details for a specific GitHub user, use the `--username` (or `-user`) flag:
```bash
python main.py --username <github_username>
```

- **Fetch Repository Details :**
To retrieve details about a specific repository owned by a user, provide both the `--username` and `--reponame` (or `-repo`) flags:
```bash
python main.py --username <github_username> --reponame <repository_name>
```

If the specified `username` or `reponame` is not found , an error message will be displayed .
 
### Examples

**Fetching User Details**

```bash
python main.py --username pradip-2007
```
**Fetch repository Details**

```bash
python main.py --username pradip-2007 --reponame Repo-Info
```
