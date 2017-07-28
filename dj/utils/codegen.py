from __future__ import absolute_import

import pprint
from redbaron import RedBaron
from redbaron.nodes import *  # noqa


def str_format(value):
    return pprint.pformat(value, indent=4)


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
    if isinstance(node, DefNode):
        return node.name
    if isinstance(node, ReturnNode):
        return 'ReturnNode'
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
        return RedBaron(str_format(source_value))[0].dumps()

    if (
        isinstance(source, (ListNode, TupleNode)) and
        isinstance(delta, (ListNode, TupleNode))
    ):
        # two lists
        source_value = source.to_python()
        delta_value = delta.to_python()
        value = merge_lists(source_value, delta_value)
        return RedBaron(str_format(value))[0].dumps()

    if isinstance(source, LiteralyEvaluable) and isinstance(
        delta, LiteralyEvaluable
    ):
        # all other literals -> take new value
        return delta

    elif isinstance(
        source, FromImportNode
    ) and isinstance(delta, FromImportNode):
        targets = merge_lists(
            [str(x) for x in source.targets],
            [str(x) for x in delta.targets]
        )
        source.targets = ','.join(targets)
        return source

    if isinstance(source, AssignmentNode) and isinstance(
            delta, AssignmentNode
    ):
        source.value = merge(source.value, delta.value)
        return source

    if isinstance(source, ImportNode) and isinstance(delta, ImportNode):
        return delta

    if isinstance(source, ReturnNode) and isinstance(delta, ReturnNode):
        return delta

    if hasattr(source, 'node_list') and hasattr(delta, 'node_list'):
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

    raise Exception("Can't merge %s into %s" % (delta, source))
