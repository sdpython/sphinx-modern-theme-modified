# -*- coding: utf-8 -*-
from setuptools import setup
from subprocess import check_output
import re
import os


def get_git_tag():
    return check_output(['git', 'describe', '--tags', '--long']).decode()


def get_git_branch():
    travis_branch = os.environ.get('TRAVIS_BRANCH', '')
    if len(travis_branch) > 0:
        return travis_branch
    return check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode()


def get_version():
    """Interrogate git to find our version string.

    We require tags of the form v1.y.z

    Development builds should happen on named branches (pref. `master`).
    When crafting a release, start a new branch named 1.y

    """
    tag = get_git_tag()
    ma = re.match(r'v(\d+)\.(\d+)\.(\d+)\-(\d+)\-(\w+)', tag)
    if ma is None:
        print("The git tag '{}' does not match the format of v1.y.z-n-abcdef1")
        exit(1)
    major, minor, patch, dirty, hash = ma.groups()
    if int(dirty) > 0:
        # Convoluted logic to get the correct "dev" version based on the branch name
        branch = get_git_branch()
        ma = re.match(r'(\d)+\.(\d+)', branch)
        if ma is not None:
            branch_major, branch_minor = ma.groups()
            if int(major) == int(branch_major) and int(minor) == int(branch_minor):
                # This is a patch release since the previous tag had the same major, minor
                patch = int(patch) + 1
            else:
                # If we just made a new branch, the last tag will have a different major, minor
                patch = 0
            major = branch_major
            minor = branch_minor
        else:
            minor = int(minor) + 1
            patch = 0

    version = "{major}.{minor}.{patch}".format(major=major, minor=minor, patch=patch)

    if int(dirty) > 0:
        version = "{version}.dev0".format(version=version, dirty=dirty)
    return version


version = get_version()
print("Version:", version)

setup(
    name='sphinx_modern_theme_modified',
    version=version,
    url='http://github.com/sdpython/sphinx-modern-theme-modified',
    license='MIT',
    author='Xavier Dupré',
    author_email='xavier.dupre@gmail.com',
    description='A modern sphinx theme using Bootstrap',
    zip_safe=False,
    packages=['sphinx_modern_theme_modified'],
    package_data={
        'sphinx_modern_theme_modified': [
            'theme.conf',
            '*.html',
            'static/*.css',
            'static/*.js',
            'static/*.js_t',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Topic :: Documentation',
        'Topic :: Documentation :: Sphinx',
        'Framework :: Sphinx',
        'Framework :: Sphinx :: Theme',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
)
