import tempfile
import subprocess
from undo_cli.utils import run_cmd, commands, git_repo_required
from rich.console import Console
from rich.syntax import Syntax


"""
Supported Git Commands: https://git-scm.com/docs
"""


"""
Pre-req: Has to be in the same repo as the user
Internal git state machine using a temp dir to do simulations for Large Language Models to do retries 
"""


class GitSim:
    def __init__(self):
        self._log = None

    @property
    def log(self):
        if self._log is None:
            self._fetch_log()
        return self._log

    @git_repo_required
    def _fetch_log(self):
        cmd = ["git", "log", "--oneline", "--all"]
        stdout, stderr = run_cmd(cmd)
        if stdout:
            self._log = stdout.decode("utf-8")
        else:
            self._log = "Error fetching logs" if stderr else "No logs available"

    @git_repo_required
    def sim(self):
        try:
            # temp_dir = tempfile.mkdtemp()
            print(subprocess.run(commands["repository_path"], check=True))

        except Exception as e:
            return f"Error creating temp dir: {e}"


# UI for Git Class
class GitTree:
    def __init__(self, git: GitSim, console: Console):
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
    git = GitSim()
    git_tree = GitTree(git, console)
    git_tree.display_log()


if __name__ == "__main__":
    main()
