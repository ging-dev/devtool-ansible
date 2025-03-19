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


def event_handler(event: dict):
    pass


app = typer.Typer()


@app.command()
def install_php(symfony: Optional[bool] = None):
    version = questionary.select(
        "Choose your PHP version", choices=get_php_versions()
    ).ask()
    if version:
        config = ansible_runner.RunnerConfig(
            private_data_dir="./project",
            playbook="php.yml",
            extravars={"php_version": version, "with_symfony": symfony},
        )
        config.prepare()
        config.suppress_output_file = True
        config.suppress_env_files = True
        r = ansible_runner.Runner(config, event_handler=event_handler)
        r.run()


@app.command()
def about():
    print("Author: ging-dev")


if __name__ == "__main__":
    app()
