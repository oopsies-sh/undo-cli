import click
from rich.console import Console
from .git import Git, GitTree


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


@click.command()
@click.pass_context
def show(ctx):
    git_tree = ctx.obj["git_tree"]
    git_tree.display_log()


cli.add_command(show)


if __name__ == "__main__":
    cli(obj={})
