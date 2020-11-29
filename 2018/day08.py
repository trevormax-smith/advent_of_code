# Code for the 2018 AoC, day 8
# https://adventofcode.com/2018/day/8
# Michael Bell
# 12/8/2018


class Node(object):
    def __init__(self, parent=None):
        self.children = []
        self.metadata = []
        self.parent = parent


def parse_node(in_tree_spec, parent=None):

    tree_spec = in_tree_spec.copy()

    n_children = tree_spec[0]
    n_metadata = tree_spec[1]
    tree_spec = tree_spec[2:]

    this_node = Node(parent)

    children = []
    for i in range(n_children):
        this_child, tree_spec = parse_node(tree_spec, this_node)
        children.append(this_child)
    
    metadata = tree_spec[:n_metadata]
    tree_spec = tree_spec[n_metadata:]

    this_node.children.extend(children)
    this_node.metadata.extend(metadata)

    return this_node, tree_spec 


def tally_metadata(node):

    metadata_tally = sum(node.metadata)
    for child in node.children:
        metadata_tally += tally_metadata(child)
    return metadata_tally


def parse_list(in_string):
    return [int(c) for c in in_string.split()]


def get_node_value(node):

    if not node.children:
        value = sum(node.metadata)
    else:
        value = 0
        for child_index in node.metadata:
            if len(node.children) >= child_index > 0:
                value += get_node_value(node.children[child_index-1])
    return value


if __name__ == '__main__':

    test_input = '''2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'''
    test_list = parse_list(test_input)

    test_root_node, _ = parse_node(test_list) 
    assert tally_metadata(test_root_node) == 138
    assert get_node_value(test_root_node) == 66 

    with open('./data/day08_input.txt', 'r') as f:
        input1 = f.read()
    tree_list = parse_list(input1)

    root_node, _ = parse_node(tree_list)
    print(f'Solution 1: {tally_metadata(root_node)}')
    print(f'Solution 2: {get_node_value(root_node)}')
