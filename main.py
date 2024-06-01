import click

@click.command()
def greet():
    click.echo("Hello, World!")

if __name__ == '__main__':
    greet()