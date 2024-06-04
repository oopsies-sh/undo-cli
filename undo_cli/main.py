import click
import os 
import json 
from rich.console import Console
from .git import Git, GitTree
from .key_settings import handle_openai_key, prompt_for_key, remove_openai_key
from .prompt import prompt_command

def get_shared_objects():
    console = Console()
    git = Git()
    git_tree = GitTree(git, console)
    return console, git, git_tree

@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    console, git, git_tree = get_shared_objects()
    ctx.obj["console"] = console
    ctx.obj["git"] = git
    ctx.obj["git_tree"] = git_tree

    if ctx.invoked_subcommand not in ["setkey", "removekey"]:
        # Load or prompt for the OpenAI key if not setting or removing the key
        openai_key = handle_openai_key()
        if not openai_key:
            console.print("Failed to retrieve OpenAI Key. Please enter your key.")
            try:
                openai_key = prompt_for_key()
            except ValueError as e:
                console.print(f"Error: {e}")
                ctx.exit(1)  # Exit the CLI with an error code
        ctx.obj["openai_key"] = openai_key
        ctx.obj["model"] = "gpt-4"  # Set default model

@click.command()
@click.option('--key', prompt='Enter your key', help='Key to set')
@click.pass_context
def setkey(ctx, key):
    console = ctx.obj["console"]
    settings_path = os.path.join(os.path.expanduser("~"), ".oopsies_data")
    with open(settings_path, "w") as f:
        json.dump({"OPENAI_KEY": key}, f, indent=2)
    console.print(f"Key has been set to: {key}")

@click.command()
@click.pass_context
def removekey(ctx):
    remove_openai_key()

@click.command()
@click.pass_context
def show(ctx):
    git_tree = ctx.obj["git_tree"]
    git_tree.display_log()

@cli.command()
@click.pass_context
def prompt(ctx):
    prompt_command(ctx)  # Assuming your prompt_command is designed to handle Click context.




cli.add_command(show)
cli.add_command(setkey)
cli.add_command(removekey)
cli.add_command(prompt)

if __name__ == "__main__":
    cli(obj={})