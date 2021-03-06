"""Defines shell commands for building and testing the package."""
import logging
import os
import shutil
import sys

from invoke import task

#################################### FORMAT ####################################


@task
def yapf(c, check=False):  # pylint: disable=redefined-outer-name
    """Format Python code in the Google style."""
    if check:
        c.run("yapf --style google -r --diff flaris test tasks.py")
    else:
        c.run("yapf --style google -ir flaris test tasks.py")


@task(yapf)
def format(c):  # pylint: disable=redefined-builtin, unused-argument
    """Format code."""


##################################### LINT #####################################


@task
def pylint(c):
    """Lint Python files with pylint."""
    c.run("pylint --score=no flaris tasks")
    c.run("pylint --score=no --rcfile ./test/.pylintrc test")


@task
def flake8(c):
    """Lint Python files with flake8."""
    c.run("flake8 flaris test")
    c.run("flake8 --ignore=E266 tasks.py")


@task
def pytype(c):
    """Lint Python files with pytype."""
    if sys.platform in {"win32", "cygwin"}:
        logging.warning("pytype is not supported on Windows.")
        return

    # NOTE(@bveeramani): 'pyi-error' is disabled because of the issue described
    # at https://github.com/google/pytype/issues/428.
    c.run("pytype --disable=pyi-error flaris test tasks.py")


@task
def radon(c):
    """Report Python code complexity with radon."""
    c.run("radon cc -a -nc flaris test tasks.py")


@task(radon)
def xenon(c):
    """Monitor Python code complexity with xenon."""
    c.run("xenon -b B -m A -a A flaris test tasks.py")


@task
def pydocstyle(c):
    """Lint Python docstrings with pydocstyle."""
    c.run("pydocstyle --convention=google --add-select=D400,D401,D404 flaris "
          "tasks.py")
    c.run("pydocstyle --convention=google --add-ignore=D104 test")


@task(yapf, pylint, flake8, pytype, xenon, pydocstyle)
def lint(c):  # pylint: disable=unused-argument
    """Format and lint code."""


##################################### TEST #####################################


@task
def unittest(c):
    """Run unit tests."""
    c.run("pytest -q test/unit")


@task
def doctest(c):
    """Run doc tests."""
    if sys.platform in {"win32", "cygwin"}:
        logging.warning("doctest task is not supported on Windows.")
        return

    c.run(r"find game -name '*.py' -exec python3 -m doctest {} \;")
    c.run(r"find test -name '*.py' -exec python3 -m doctest {} \;")


@task(doctest)
def test(c, quick=True):  # pylint: disable=unused-argument
    """Run all tests."""
    c.run("pytest -q test")


################################################################################


@task
def clean(c):  # pylint: disable=unused-argument
    """Delete files that are normally created by building the package."""
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("flaris.egg-info"):
        shutil.rmtree("flaris.egg-info")


@task
def build(c):
    """Build the package."""
    c.run("python -m build")


@task(lint, test)
def check(c):  # pylint: disable=unused-argument
    """Lints code and runs tests."""
