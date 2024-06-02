from .utils import run_cmd
from rich.console import Console
from rich.syntax import Syntax


"""
Supported Git Commands: https://git-scm.com/docs
"""


# Internal git state machine to do simulations for Large Language Models to do retry Mechanism
class Git:
    def __init__(self):
        self._log = None

    @property
    def log(self):
        if self._log is None:
            self._fetch_log()
        return self._log

    def _fetch_log(self):
        cmd = ["git", "log", "--oneline", "--all"]
        stdout, stderr = run_cmd(cmd)
        if stdout:
            self._log = stdout.decode("utf-8")
        else:
            self._log = "Error fetching logs" if stderr else "No logs available"


# UI for Git Class
class GitTree:
    def __init__(self, git: Git, console: Console):
        self.console = console
        self.git = git

    def display_log(self):
        log_content = self.git.log
        if log_content:
            syntax = Syntax(log_content, "bash", theme="monokai", line_numbers=True)
            self.console.print(syntax)
        else:
            self.console.print("No log available")


def main():
    console = Console()
    git = Git()
    git_tree = GitTree(git, console)
    git_tree.display_log()


if __name__ == "__main__":
    main()
