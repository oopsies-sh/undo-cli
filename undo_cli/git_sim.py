import os
import tempfile
import subprocess
from undo_cli.utils import run_cmd, commands, git_repo_required, gather_git_state
import shutil

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
        stdout, stderr = run_cmd(commands["log"])
        if stdout:
            self._log = stdout.decode("utf-8")
        else:
            self._log = "Error fetching logs" if stderr else "No logs available"

    @git_repo_required
    def sim(self):
        git_state = gather_git_state()

        if git_state["errors"]:
            raise Exception(f"Error fetching git state: {git_state['errors']}")

        try:
            orig_repo_dir = os.getcwd()
            print(orig_repo_dir)
            with tempfile.TemporaryDirectory() as temp_dir:
                print(f"Temporary directory created at: {temp_dir}")
                repo_url, repo_url_error = run_cmd(commands["repository_url"])
                if repo_url_error:
                    raise Exception(f"Error fetching repo url: {repo_url_error}")

                # Clone the repo to the temp dir
                clone, _ = run_cmd(commands["clone"](repo_url, temp_dir))

                # Replicate user actions i.e. what branch they are on and what they are doing
                repo_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
                os.chdir(repo_dir)

                run_cmd(commands["checkout"](git_state["current_branch"]))

                if git_state["staged_files"]:
                    staged_files = git_state["staged_files"].split("\n")
                    for file in staged_files:
                        shutil.copy2(
                            os.path.join(orig_repo_dir, file),
                            os.path.join(repo_dir, file),
                        )
                        run_cmd(["git", "add"] + staged_files)

                if git_state["unstaged_files"]:
                    with open(
                        os.path.join(temp_dir, "unstaged.patch"), "w"
                    ) as patch_file:
                        patch_file.write(git_state["unstaged_files"])
                    run_cmd(["git", "apply", "unstaged.patch"])

                if git_state["untracked_files"]:
                    untracked_files = git_state["untracked_files"].split("\n")
                    for file in untracked_files:
                        src_path = os.path.join(orig_repo_dir, file)
                        dst_path = os.path.join(repo_dir, file)
                        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                        shutil.copy2(src_path, dst_path)

            # Verify the temporary directory is deleted

        except Exception as e:
            raise Exception(f"Error creating temp dir: {e}")


if __name__ == "__main__":
    git = GitSim()
    print(git.log)
