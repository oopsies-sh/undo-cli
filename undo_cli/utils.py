import subprocess
from functools import wraps

commands = {
    "repository_url": ["git", "remote", "get-url", "origin"],
    "current_branch": ["git", "branch", "--show-current"],
    "repository_path": ["git", "rev-parse", "--show-toplevel"],
    "list_remotes": ["git", "remote", "-v"],
    "log": ["git", "log", "--oneline", "--all"],
    "is_git_repo": ["git", "rev-parse", "--is-inside-work-tree"],
}


def run_cmd(args):
    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout, stderr
    except Exception as e:
        return None, str(e)


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
