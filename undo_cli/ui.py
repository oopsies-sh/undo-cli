from rich.console import Console
from rich.syntax import Syntax
from undo_cli.git_sim import GitSim


class Ui:
    def __init__(self, git: GitSim, console: Console):
        self.console = console
        self.git = git

    def pretty_print(self, message: str):
        if message:
            syntax = Syntax(message, "bash", theme="monokai", line_numbers=True)
            self.console.print(syntax)

    def display_log(self):
        self.pretty_print(self.git.sim())  # testing
        # log_content = self.git.log
        # if log_content:
        #     self.pretty_print(log_content)
        # else:
        #     self.pretty_print("No logs available")
