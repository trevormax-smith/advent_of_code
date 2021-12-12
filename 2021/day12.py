from collections import defaultdict
from typing import List, Tuple
import helper


def is_cave_small(node: str) -> bool:
    return node.islower()


class Map(object):
    def __init__(self, map_def: List[str]) -> None:
        self.nodes = defaultdict(lambda: [])
        for line in map_def:
            node_a, node_b = line.split('-')
            self.nodes[node_a].append(node_b)
            self.nodes[node_b].append(node_a)

    def find_paths(self, current_node: str=None, current_path: List[str]=None) -> List[List[str]]:
        start_node, end_node = 'start', 'end'
        is_start = False
        if current_node == None:
            is_start = True
            current_node = start_node
            current_path = [start_node]
        
        paths = []

        for next_node in self.nodes[current_node]:
            if next_node == end_node:
                paths.append(current_path + [end_node])
            elif next_node.isupper() or (next_node not in current_path):
                new_path = current_path.copy() + [next_node]
                new_paths = self.find_paths(next_node, new_path)
                paths.extend(new_paths)
        
        if is_start:
            paths = [path for path in paths if path[-1] == end_node]
            
        return paths 


if __name__ == '__main__':
    ### THE TESTS
    test_map = Map('''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''.split('\n'))

    test_map2 = Map('''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc'''.split('\n'))

    test_map3 = Map('''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''.split('\n'))

    assert len(test_map.find_paths()) == 10
    assert len(test_map2.find_paths()) == 19
    assert len(test_map3.find_paths()) == 226


    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    the_map = Map(puzzle_input)
    print(f'Part 1: {len(the_map.find_paths())}')
    print(f'Part 2: {""}')
