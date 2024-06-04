import openai
import click
from pydantic import BaseModel
from .key_settings import handle_openai_key, prompt_for_key, remove_openai_key
from rich.console import Console
from .git import Git, GitTree  # Assumed import

# Define your desired output structure
class GitUndoInfo(BaseModel):
    steps: str

def get_openai_client(api_key):
    """Helper function to create OpenAI client."""
    return openai.OpenAI(api_key=api_key)

def fetch_git_logs(git_tree):
    # Fetch Git logs
    return git_tree.return_log()

def process_git_logs(git_logs, openai_key):
    # Create OpenAI client with the key
    client = get_openai_client(openai_key)
    try:
        # Send the prompt to the OpenAI API and extract structured data
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"give me the steps to undo this last git action: {git_logs}"}],
        )
        return response
    except Exception as e:
        return f"Error: {e}"

def handle_prompt(console, git_tree, openai_key):
    console.print("Fetching Git logs...")
    git_logs = fetch_git_logs(git_tree)

    # Process Git logs and get the steps to undo the last action
    steps = process_git_logs(git_logs, openai_key)
    # Print the extracted steps
    console.print("Steps to undo last Git action:")
    console.print(steps)

def prompt_command(ctx):
    console = ctx.obj["console"]
    git_tree = ctx.obj["git_tree"]
    openai_key = handle_openai_key()

    handle_prompt(console, git_tree, openai_key)

if __name__ == "__main__":
    prompt_command()