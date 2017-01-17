from collections import OrderedDict
import re
from django_cli.utils.system import stdout
from django_cli.utils.style import white, green, red, yellow


class Dependency(object):
    parse_regex = re.compile(r'^([A-Za-z][-A-Za-z_.]+)([=><]+)([0-9.]+)$')

    def __init__(self, value):
        value = value.strip('\n')
        self.value = value
        self.name, self.operator, self.version = Dependency.parse(value)

    @classmethod
    def parse(cls, value):
        result = cls.parse_regex.match(value)
        if result:
            name = result.group(1)
            operator = result.group(2)
            version = result.group(3)
        else:
            name = value
            operator = ''
            version = ''
        return name, operator, version

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return '%s%s%s' % (
            self.name,
            self.operator,
            self.version
        )


class DependencyManager(object):

    def __init__(self, source):
        self.source = source

    def add(self, value):
        new = Dependency(value)
        old = self.dependencies.get(new.name)
        self.dependencies[new.name] = new
        if old is None or str(old) != str(new):
            self._save()
            if old:
                stdout.write(
                    red('- ') +
                    white(str(old))
                )
            stdout.write(
                green('+ ') +
                white(str(new))
            )
        else:
            stdout.write(yellow('%s already installed.' % str(new)))

    @property
    def dependencies(self):
        if not hasattr(self, '_dependencies'):
            self._dependencies = self._load()
        return self._dependencies

    def _load(self):
        dependencies = OrderedDict()
        with open(self.source, 'r') as f:
            for line in f.readlines():
                if line:
                    d = Dependency(line)
                    dependencies[d.name] = d
        return dependencies

    def _save(self):
        with open(self.source, 'w') as f:
            for dependency in self.dependencies.values():
                dependency = str(dependency)
                if not dependency.endswith('\n'):
                    dependency = dependency + '\n'
                f.write(dependency)
