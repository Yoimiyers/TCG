"""Nox file."""
from __future__ import annotations

import functools
import logging
import os
import pathlib
import typing

import nox

nox.options.sessions = ["reformat", "lint", "type-check", "verify-types", "test"]

PACKAGE = "invokator"
GENERAL_TARGETS = ["./invokator", "./tests", "./noxfile.py", "./setup.py"]
PRETTIER_TARGETS = ["*.md", "carddata/**/*.json", ".github/**/*.yml"]
PYRIGHT_ENV = {"PYRIGHT_PYTHON_FORCE_VERSION": "latest"}

LOGGER = logging.getLogger("nox")

NoxCallback = typing.Callable[[nox.Session], None]
NoxCallbackT = typing.TypeVar("NoxCallbackT", bound=NoxCallback)


def isverbose() -> bool:
    """Whether the verbose flag is set."""
    return LOGGER.getEffectiveLevel() == logging.DEBUG - 1


def verbose_args() -> typing.Sequence[str]:
    """Return --verbose if the verbose flag is set."""
    return ["--verbose"] if isverbose() else []


def install_requirements(session: nox.Session, *requirements: str) -> None:
    """Install requirements."""
    session.install("--upgrade", "pip", "-r", "requirements.txt", *requirements, silent=not isverbose())


def requires(*requirements: str) -> typing.Callable[[NoxCallback], NoxCallback]:
    """Install requirements before running a session."""

    def decorator(func: NoxCallbackT) -> NoxCallbackT:
        @functools.wraps(func)
        def wrapper(session: nox.Session) -> None:
            install_requirements(session, *requirements)
            func(session)

        return typing.cast(NoxCallbackT, wrapper)

    return decorator


@nox.session()
@requires("flake8", "flake8-annotations-complexity", "flake8-docstrings", "flake8-print")
def lint(session: nox.Session) -> None:
    """Run this project's modules against the pre-defined flake8 linters."""
    session.run("flake8", "--version")
    session.run("flake8", *GENERAL_TARGETS, *verbose_args())


@nox.session()
@requires("black", "isort", "sort-all")
def reformat(session: nox.Session) -> None:
    """Reformat this project's modules to fit the standard style."""
    session.run("black", *GENERAL_TARGETS, *verbose_args())
    session.run("isort", *GENERAL_TARGETS, *verbose_args())

    session.log("sort-all")
    LOGGER.disabled = True
    session.run("sort-all", *map(str, pathlib.Path(PACKAGE).glob("**/*.py")), success_codes=[0, 1])
    LOGGER.disabled = False


@nox.session()
@requires("pytest", "pytest-asyncio", "pytest-cov")
def test(session: nox.Session) -> None:
    """Run this project's tests using pytest."""
    os.makedirs(".coverage", exist_ok=True)
    session.run(
        "pytest",
        "--asyncio-mode=auto",
        "-r",
        "sfE",
        *verbose_args(),
        "--cov",
        PACKAGE,
        "--cov-report",
        "term",
        "--cov-report",
        "html",
        "--cov-report",
        "xml",
        *session.posargs,
    )


@nox.session(name="type-check")
@requires("pyright")
def type_check(session: nox.Session) -> None:
    """Statically analyse and veirfy this project using pyright."""
    session.run("pyright", PACKAGE, *verbose_args(), env=PYRIGHT_ENV)


@nox.session(name="verify-types")
@requires("pyright")
def verify_types(session: nox.Session) -> None:
    """Verify the "type completeness" of types exported by the library using pyright."""
    install_requirements(session, ".", "--force-reinstall", "--no-deps")

    session.run("pyright", "--verifytypes", PACKAGE, "--ignoreexternal", *verbose_args(), env=PYRIGHT_ENV)


@nox.session(python=False)
def prettier(session: nox.Session) -> None:
    """Run prettier on markdown and json files."""
    session.run("prettier", "--tab-width", "4", "-w", *PRETTIER_TARGETS, *verbose_args())


@nox.session(name="prettier-check", python=False)
def prettier_check(session: nox.Session) -> None:
    """Run prettier on markdown and json files."""
    session.run("prettier", "--tab-width", "4", "--check", *PRETTIER_TARGETS, *verbose_args())
