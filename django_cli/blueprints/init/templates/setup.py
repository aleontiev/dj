from setuptools import (
    find_packages,
    setup,
)

APP = "{{ app }}"
AUTHOR = "{{ author }}"
AUTHOR_EMAIL = "{{ email }}"
DESCRIPTION = "{{ description }}"
VERSION = "{{ version }}"

EXCLUDE_FROM_PACKAGES = []

setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    include_package_data=True,
    long_description=open('README.md').read(),
    name=APP,
    install_requires=open('install_requires.txt').readlines(),
    dependency_links=open('dependency_links.txt').readlines(),
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    scripts=['manage.py'],
    test_suite='runtests.runtests',
    version=VERSION,
)
