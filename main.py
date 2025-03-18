import ansible_runner
import questionary
import requests
import typer
from rich import print
from typing import Optional


def get_php_versions() -> list[str]:
    """
    Get PHP versions from the official website.
    """
    php_versions = []
    version_matrix: dict = requests.get("https://www.php.net/releases/active").json()
    for _, versions in version_matrix.items():
        for version in versions:
            php_versions.append(version)
    return php_versions


app = typer.Typer()


@app.command()
def install_php(symfony: Optional[bool] = None):
    version = questionary.select(
        "Choose your PHP version", choices=get_php_versions()
    ).ask()
    if version:
        ansible_runner.run(
            private_data_dir="./project",
            playbook="php.yml",
            extravars={"php_version": version, "with_symfony": symfony},
        )


@app.command()
def about():
    print("Author: ging-dev")


if __name__ == "__main__":
    app()
