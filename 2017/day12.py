"""
Code for the 2017 Advent Of Code, day 12
https://adventofcode.com/2017/day/12
Michael Bell
12/17/2017
Solutions passed
"""

class Node(object):
    """
    A simple container for a node in a graph that has an id PID and a set of nodes to which
    it is connected.
    """
    def __init__(self, pid):
        self.pid = pid
        self.connections = set()
    def __repr__(self):
        return "{:} <-> {:}".format(
           str(self.pid), ', '.join([str(c.pid) for c in self.connections])
        )


def encode_node_listing(pid, connecting_pids):
    return "{:} <-> {:}".format(str(pid), ", ".join([str(p) for p in connecting_pids]))

def parse_node_listing(listing):
    """
    Split a node listing like 
        0 <-> 1, 2
    into an integer node ID (0 in this case) and a list of node IDs to which it is connected
    ([1, 2] in this case).
    """
    parts = listing.split(' <-> ')
    pid = int(parts[0])
    connecting_pids = [int(p) for p in parts[1].split(', ')]
    return pid, connecting_pids


class Graph(object):
    """
    A collection of connected nodes.
    """
    def __init__(self, nodes=None):
        if nodes is None:
            self._nodes = {}
        else:
            self._nodes = {n.pid: n for n in nodes}

    @property
    def node_count(self):
        """
        The number of nodes in the graph.
        """
        return len(self._nodes)

    def add_node(self, node_pid, connecting_pids):
        """
        Given a node ID and the nodes IDs to which it is connected, add the node and all connecting
        nodes to the graph, and make connections between nodes.
        """
        if node_pid not in self._nodes:
            node = Node(node_pid)
            self._nodes[node_pid] = node
        else:
            node = self._nodes[node_pid]

        for cpid in connecting_pids:
            if cpid in self._nodes:
                cnode = self._nodes[cpid]
            else:
                cnode = Node(cpid)
                self._nodes[cpid] = cnode
            
            if cnode not in node.connections:
                node.connections.add(cnode)
            if node not in cnode.connections:
                cnode.connections.add(node)
            

    def get_group_containing(self, pid):
        """
        Given a node id, return a Graph containing only nodes to which the given node is connected.
        """
        if not pid in self._nodes:
            return Graph()
        else:
            node = self._nodes[pid]
            group_nodes = set([node])

            def add_cnx_to_group(cnx):
                for cnode in cnx:
                    if cnode in group_nodes:
                        continue
                    else:
                        group_nodes.add(cnode)
                        add_cnx_to_group(cnode.connections)

            add_cnx_to_group(node.connections)

            return Graph(group_nodes)

    def get_groups(self):
        """
        Return a list of Graphs, each of which is fully connected (meaning you can reach all 
        nodes in the graph starting from any node in the graph).
        """
        pids = set([n for n in self._nodes])
        groups = []
        while pids:
            pid = pids.pop()
            group = self.get_group_containing(pid)
            groups.append(group)
            pids = pids.difference(
                set([n for n in group._nodes])
            )
        return groups

    def build_graph(self, node_list):
        """
        Construct a graph from a text listing of nodes and their connections.
        """
        node_list = node_list.replace('\r', '').split('\n')
        for listing in node_list:
            pid, connecting_pids = parse_node_listing(listing)
            self.add_node(pid, connecting_pids)


TEST_LISTING = """0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""

with open('data/day12_input.txt', 'r') as f:
    PUZZLE_LISTING = f.read()

if __name__ == '__main__':
    # TESTS
    test_graph = Graph()
    test_graph.build_graph(TEST_LISTING)
    assert test_graph.get_group_containing(0).node_count == 6
    test_groups = test_graph.get_groups()
    assert len(test_groups) == 2
    assert encode_node_listing(2, [4, 5]) == "2 <-> 4, 5"

    print('ALL TESTS PASSED!')
    
    graph = Graph()
    graph.build_graph(PUZZLE_LISTING)
    print('Solution 1: {:}'.format(graph.get_group_containing(0).node_count))
    groups = graph.get_groups()
    print('Solution 2: {:}'.format(len(groups)))
