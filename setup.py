from setuptools import (
    find_packages,
    setup,
)

APP_NAME = "dj"
AUTHOR = "Anthony Leontiev"
AUTHOR_EMAIL = "alonetiev@gmail.com"
DESCRIPTION = "DJ, the Django CLI"
REPO_NAME = "django-cli"
ORG_NAME = "aleontiev"
VERSION = "0.0.1"

EXCLUDE_FROM_PACKAGES = []

def get_dependencies(file):
    import re

    install_requires = {}
    dependency_links = {}

    url = re.compile(r'[^/]+/.+(?:#egg=(.*))$')
    version = re.compile(r'[0-9][a-zA-Z0-9.]*')

    with open(file) as f:
        for dependency in f.readlines():
            dependency = dependency.strip()
            if dependency.startswith('-e'):
                # ignore interactive mode
                dependency = dependency[3:]

            url_match = url.match(dependency)
            if url_match and url_match.group(1):
                # some/url/dependency#egg=dependency
                egg = url_match.group(1)
                identifier = egg
                separator = egg.rfind('-')
                # check for version
                if separator:
                    egg_name = egg[:separator]
                    egg_version = egg[separator+1:]
                    if version.match(egg_version):
                        # egg=name-version
                        identifier = '%s==%s' % (egg_name, egg_version)

                install_requires[identifier] = identifier
                dependency_links[identifier] = dependency
            elif url_match:
                # /some/path/to/dependency
                name = dependency.split('/')[-1]
                install_requires[name] = name
                dependency_links[name] = dependency

            else:
                # package==version
                install_requires[dependency] = dependency

    return install_requires, dependency_links

dependencies = get_dependencies('requirements.txt')

setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    include_package_data=True,
    long_description=open('README.md').read(),
    name=APP_NAME,
    packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    scripts=[],
    install_requires=dependencies[0].values(),
    dependency_links=dependencies[1].values(),
    entry_points={
        'console_scripts': [
            'dj = dj.commands.dj:dj'
        ]
    },
    url='http://github.com/%s/%s' % (ORG_NAME, REPO_NAME),
    version=VERSION,
)
