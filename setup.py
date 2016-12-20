from setuptools import (
    find_packages,
    setup,
)

APP_NAME = "django_cli"
AUTHOR = "Anthony Leontiev"
AUTHOR_EMAIL = "alonetiev@gmail.com"
DESCRIPTION = "Django CLI"
REPO_NAME = "django-cli"
ORG_NAME = "aleontiev"
VERSION = "0.0.1"

EXCLUDE_FROM_PACKAGES = []

setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    include_package_data=True,
    long_description=open('README.md').read(),
    name=APP_NAME,
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    scripts=[],
    install_requires=open('install_requires.txt').readlines(),
    entry_points={
        'console_scripts': [
            'django = django_cli.commands.django:command'
        ]
    },
    test_suite='runtests.runtests',
    url='http://github.com/%s/%s' % (ORG_NAME, REPO_NAME),
    version=VERSION,
)
