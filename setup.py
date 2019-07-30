from setuptools import (
    find_packages,
    setup,
)


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
                    egg_version = egg[separator + 1:]
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
install_requires = dependencies[0].values()
dependency_links = dependencies[1].values()

setup(
    author='Anthony Leontiev',
    author_email='alonetiev@gmail.com',
    description='dj, the Django CLI',
    include_package_data=True,
    long_description=open('README.txt').read(),
    license=open('LICENSE.md').read(),
    name='djay',
    packages=find_packages(),
    scripts=[],
    install_requires=install_requires,
    dependency_links=dependency_links,
    entry_points={
        'console_scripts': [
            'dj = dj.commands.dj:dj'
        ]
    },
    url='http://github.com/aleontiev/dj',
    version='0.0.6'
)
