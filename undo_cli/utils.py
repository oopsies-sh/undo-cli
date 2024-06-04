import subprocess
from functools import wraps

commands = {
    "repository_url": ["git", "remote", "get-url", "origin"],
    "current_branch": ["git", "branch", "--show-current"],
    "repository_path": ["git", "rev-parse", "--show-toplevel"],
    "list_remotes": ["git", "remote", "-v"],
    "log": ["git", "log", "--oneline", "--all"],
    "is_git_repo": ["git", "rev-parse", "--is-inside-work-tree"],
    "clone": lambda repo_url, temp_dir: ["git", "clone", repo_url, temp_dir],
    "current_branch": ["git", "rev-parse", "--abbrev-ref", "HEAD"],
    "staged_files": ["git", "diff", "--cached", "--name-only"],
    "unstaged_files": ["git", "diff"],
    "local_modifications": ["git", "diff", "HEAD"],
    "untracked_files": ["git", "ls-files", "--others", "--exclude-standard"],
    "checkout": lambda branch: ["git", "checkout", branch],
    "remote_branch": [
        "git",
        "for-each-ref",
        "--format='%(upstream:short)'",
        "$(git symbolic-ref -q HEAD)",
    ],
}


def run_cmd(args):
    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout, stderr
    except Exception as e:
        return None, str(e)


def gather_git_state():
    state = {
        "current_branch": None,
        "local_modifications": None,
        "staged_files": None,
        "untracked_files": None,
        "remote_branch": None,
        "unstaged_files": None,
        "errors": {},
    }
    current_branch, current_branch_errors = run_cmd(commands["current_branch"])
    staged_files, staged_files_errors = run_cmd(commands["staged_files"])
    local_modifications, local_modifications_errors = run_cmd(
        commands["local_modifications"]
    )
    untracked_files, untracked_files_errors = run_cmd(commands["untracked_files"])
    remote_branch, remote_branch_errors = run_cmd(commands["remote_branch"])
    unstaged_files, unstaged_files_errors = run_cmd(commands["unstaged_files"])

    state["current_branch"] = current_branch
    state["staged_files"] = staged_files
    state["local_modifications"] = local_modifications
    state["untracked_files"] = untracked_files
    state["remote_branch"] = remote_branch
    state["unstaged_files"] = unstaged_files

    return state


def git_repo_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_git_repo = run_cmd(commands["is_git_repo"])[0]
        if is_git_repo.strip() == "true":
            return func(*args, **kwargs)
        else:
            raise EnvironmentError("Not a Git repository")

    return wrapper


if __name__ == "__main__":
    # Run the command
    stdout, stderr = run_cmd(["ls", "-l"])
    if stderr:
        print("Error: ", stderr)
    else:
        print("Output: ", stdout)
