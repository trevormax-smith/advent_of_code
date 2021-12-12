from collections import defaultdict
from typing import List, Tuple
import helper


START_NODE, END_NODE = 'start', 'end'


class Map(object):
    def __init__(self, map_def: List[str]) -> None:
        self.nodes: defaultdict[str, List[str]] = defaultdict(lambda: [])
        for line in map_def:
            node_a, node_b = line.split('-')
            self.nodes[node_a].append(node_b)
            self.nodes[node_b].append(node_a)

    def get_small_caves(self) -> List[str]:
        return [k for k in self.nodes if k.islower() and k not in [START_NODE, END_NODE]]

    def find_paths_with_revisit(self) -> List[List[str]]:
        small_caves = self.get_small_caves()
        paths = []
        for cave in small_caves:
            paths.extend(self.find_paths(allowed_revisit=cave))
        return list(set([','.join(path) for path in paths]))

    def find_paths(self, current_node: str=None, current_path: List[str]=None, allowed_revisit: str=None) -> List[List[str]]:
        
        is_start = False
        if current_node == None:
            is_start = True
            current_node = START_NODE
            current_path = [START_NODE]
        
        paths = []

        for next_node in self.nodes[current_node]:
            if next_node == END_NODE:
                paths.append(current_path + [END_NODE])
            elif next_node.isupper() or (next_node not in current_path) or (next_node == allowed_revisit and current_path.count(next_node) <= 1):
                new_path = current_path.copy() + [next_node]
                new_paths = self.find_paths(next_node, new_path, allowed_revisit)
                paths.extend(new_paths)
        
        if is_start:
            paths = [path for path in paths if path[-1] == END_NODE]

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

    assert len(test_map.find_paths_with_revisit()) == 36
    assert len(test_map2.find_paths_with_revisit()) == 103
    assert len(test_map3.find_paths_with_revisit()) == 3509


    ### THE REAL THING
    puzzle_input = helper.read_input_lines()
    the_map = Map(puzzle_input)
    print(f'Part 1: {len(the_map.find_paths())}')
    print(f'Part 2: {len(the_map.find_paths_with_revisit())}')
