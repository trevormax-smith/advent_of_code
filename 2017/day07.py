# Code for the 2017 Advent Of Code, day 7
# http://adventofcode.com/2017
# Michael Bell
# 12/13/2017
# Solutions passed!

# NOTE: This is pretty sloppy. Might think about refactoring.

class TreeNode(object):
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.children = []
        self.parent = None
    def add_child(self, child):
        if not isinstance(child, TreeNode):
            raise TypeError('Child must be a TreeNode object.')

        if not any(c.name == child.name for c in self.children):
            child.add_parent(self)
            self.children.append(child)
    def add_parent(self, parent):
        if not isinstance(parent, TreeNode):
            raise TypeError('Parent must be a TreeNode object.')

        self.parent = parent
    def get_subtower_weight(self):
        total_weight = self.weight
        for child in self.children:
            total_weight += child.get_subtower_weight()
        return total_weight
    def is_balanced(self):
        weights = []
        for child in self.children:
            weight = child.get_subtower_weight()
            weights.append(weight)
        if len(weights) > 0 and len(set(weights)) > 1:
            return False
        else:
            return True


class Tree(object):
    def __init__(self):
        self.nodes = {}
    def add_node(self, node):
        self.nodes[node.name] = node
    def get_node(self, node_name):
        return self.nodes[node_name]
    def get_root(self):
        # Start anywhere in the tree and climb up until you find a node without
        # a parent

        node = self.nodes[list(self.nodes.keys())[0]]
        while node.parent is not None:
            node = node.parent
        return node


def get_imbalanced_node(node):

    if not node.is_balanced() and all(child.is_balanced() for child in node.children):
        return node
    elif not node.is_balanced():
        for child in node.children:
            result = get_imbalanced_node(child)
            if result is not None:
                return result
    else:
        return None


def balance_node(node):
    max_weight = -1
    max_weight_node = None
    weights = []
    for i, child in enumerate(node.children):
        weight = child.get_subtower_weight()
        weights.append(weight)
        if weight > max_weight:
            max_weight = weight
            max_weight_node = child
    other_weight = min(weights)
    max_weight_node.weight -= max_weight - other_weight

    return max_weight_node
    
def parse_program(program_line):
    parts = program_line.replace('(', '').replace(')', '').replace('->', '').replace(',', '').split()

    name = parts[0]
    weight = int(parts[1])
    if len(parts) > 2:
        childrens_names = parts[2:]
    else:
        childrens_names = []

    return name, weight, childrens_names


def build_tree(program_list):
    
    program_list = program_list.replace('\r', '').split('\n')
    
    tree = Tree()

    children = {}

    for program in program_list:
        if len(program) == 0:
            continue
        name, weight, childrens_names = parse_program(program)
        node = TreeNode(name, weight)
        tree.add_node(node)
        if len(childrens_names) > 0:
            children[name] = childrens_names

    for parent_name in children:
        parent = tree.get_node(parent_name)
        for child in children[parent_name]:
            parent.add_child(tree.get_node(child))

    return tree


test_program_list = '''pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)'''

with open('data/day07_input.txt', 'r') as f:
    puzzle_input = f.read()

if __name__ == '__main__':
    tree = build_tree(test_program_list)
    assert tree.get_root().name == 'tknk'
    assert not tree.get_root().is_balanced()
    assert tree.get_node('ugml').is_balanced()
    assert tree.get_node('ugml').get_subtower_weight() == 251
    assert get_imbalanced_node(tree.get_root()).name == 'tknk'
    imbalanced_node = get_imbalanced_node(tree.get_root())
    corrected_node = balance_node(imbalanced_node)
    assert corrected_node.weight == 60
    print("All tests passed")

    tree = build_tree(puzzle_input)
    imbalanced_node = get_imbalanced_node(tree.get_root())
    corrected_node = balance_node(imbalanced_node)

    print("Solution 1: {:}".format(tree.get_root().name))
    print("Solution 2: {:}".format(corrected_node.weight))
