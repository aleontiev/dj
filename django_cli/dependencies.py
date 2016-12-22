from collections import OrderedDict
import re


class Dependency(object):
    parse_regex = re.compile(r'^([A-Za-z][-A-Za-z_.]+)([=><]+)([0-9.]+)$')

    def __init__(self, value):
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
        dep = Dependency(value)
        old = self.dependencies.get(dep.name)
        self.dependencies[dep.name] = dep
        self._save()
        print 'Added %s%s' % (
            value,
            ' (was %s)' % str(old) if old and old != dep else ''
        )

    @property
    def dependencies(self):
        if not hasattr(self, '_dependencies'):
            self._dependencies = self._load()
        return self._dependencies

    def _load(self):
        dependencies = OrderedDict()
        with open(self.source, 'r') as f:
            for line in f.readlines():
                d = Dependency(line)
                dependencies[d.name] = d
        return dependencies

    def _save(self):
        with open(self.source, 'w') as f:
            for dependency in self.dependencies.values():
                f.write('%s\n' % str(dependency))
