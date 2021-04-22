"""
Setuptools configuration file.
"""

import re
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# Version snippet modified from https://github.com/ncoghlan/python-packaging-user-guide/blob/master/source/guides/single-sourcing-package-version.rst
def read(*names, **kwargs):
    with open(path.join(path.dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="code-challenge",
    # Version should comply with PEP440
    version=find_version("src/code_challenge", "__init__.py"),
    description="Code challenge",
    long_description=long_description,
    author="jon",
    author_email="redacted@redacted.com",
    # Classifiers
    classifiers=[
        "Private :: Do Not Upload",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    # Install requires. For discussion of install requires vs pip requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["fastapi", "httpx", "python-dotenv", "uvicorn"],
    # Additional extra requires
    extras_require={
        "dev": [
            "black==20.8b1",  # we fix this version so that it matches the pre-commit-config version
            "coverage",
            "flake8",
            "flake8-builtins",
            "flake8-debugger",
            "flake8-docstrings",
            "flake8-import-order",
            "flake8-logging-format",
            "flake8-mutable",
            "flake8-string-format",
            "pep8-naming",
            "pydocstyle",
            "pytest",
            "pytest-asyncio",
            "pytest-cov",
            "pytest-httpx",
            "pytest-mock",
            "tox",
            "wheel",  # on some environments, wheel needs to be installed separately
        ]
    },
    # Entrypoint scripts that provide cross-platform support and allow pip to create the appropriate form of
    # executable for the target platform.
    entry_points={
        "console_scripts": [
            "code_challenge_server=code_challenge.server:start_server",
            "code_challenge_backend_server=code_challenge.backend_server:start_server",
        ]
    },
)
