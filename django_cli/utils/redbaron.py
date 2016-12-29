from __future__ import absolute_import

from redbaron import RedBaron
from redbaron.nodes import *  # noqa


def merge_lists(source, delta):
    source_set = set(source)
    for d in delta:
        if d not in source_set:
            source.append(d)
    return source


def get_id(node):
    if isinstance(node, AssignmentNode):
        return node.target.dumps()
    if isinstance(node, FromImportNode):
        return node.value.dumps()
    if isinstance(node, ImportNode):
        return node.name.dumps()
    return None


def merge(source, delta):
    if isinstance(source, basestring):
        source = RedBaron(source)
    if isinstance(delta, basestring):
        delta = RedBaron(delta)

    if isinstance(source, DictNode) and isinstance(delta, DictNode):
        # two dictionaries
        source_value = source.to_python()
        delta_value = delta.to_python()
        source_value.update(delta_value)
        return RedBaron(str(source_value))[0].dumps()

    elif isinstance(source, ListNode) and isinstance(delta, ListNode):
        # two lists
        source_value = source.to_python()
        delta_value = delta.to_python()
        value = merge_lists(source, delta)
        return RedBaron(str(value))[0].dumps()

    elif isinstance(source, LiteralyEvaluable) and isinstance(delta, LiteralyEvaluable):
        # all other literals -> take new value
        return delta

    elif isinstance(
        source, FromImportNode
    ) and isinstance(delta, FromImportNode):
        targets = merge_lists(
            [repr(x) for x in source.targets],
            [repr(x) for x in delta.targets]
        )
        source.targets = ','.join(targets)
        return source

    elif isinstance(source, AssignmentNode) and isinstance(delta, AssignmentNode):
        source.value = merge(source.value, delta.value)
        return source

    elif isinstance(source, ImportNode) and isinstance(delta, ImportNode):
        return delta

    elif hasattr(source, 'node_list') and hasattr(delta, 'node_list'):
        # two node lists
        for delta_node in delta:
            found = False
            delta_id = get_id(delta_node)
            if delta_id:
                for i, source_node in enumerate(source):
                    source_id = get_id(source_node)
                    if (
                        source_node.type == delta_node.type and
                        delta_id == source_id
                    ):
                        # found node with matching id
                        # => replace with merged node
                        source[i] = merge(source_node, delta_node)
                        found = True
                        break
            if not found:
                # no matching node, append to list
                source.append(delta_node)
        return source.dumps()

    else:
        raise Exception("Can't merge %s into %s" % (delta, source))
