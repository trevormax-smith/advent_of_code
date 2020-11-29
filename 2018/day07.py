# Code for the 2018 AoC, day 7
# https://adventofcode.com/2018/day/7
# Michael Bell
# 12/7/2018


class Step(object):
    def __init__(self, step_id):
        self.step_id = step_id
        self.parents = []
        self.children = []
    
    def add_parent(self, parent):
        
        if parent not in self.parents:
            self.parents.append(parent)

    def add_child(self, child):
        
        if child not in self.children:
            self.children.append(child)

    def __repr__(self):
        return f'Step({self.step_id})'


def create_instruction_graph(instructions):
    step_seqs = [
        [step for i, step in enumerate(instruction.split()) if i in (1, 7)]
        for instruction in instructions
    ]

    graph = dict()
    for steps in step_seqs:
        
        parent_step_id = steps[0]
        child_step_id = steps[1]

        if parent_step_id not in graph:
            graph[parent_step_id] = Step(parent_step_id)
        if child_step_id not in graph:
            graph[child_step_id] = Step(child_step_id)
        
        graph[parent_step_id].add_child(graph[child_step_id])
        graph[child_step_id].add_parent(graph[parent_step_id])
    
    return graph


def get_root_nodes(graph):
    return [node for node in graph.values() if len(node.parents) == 0]


def get_step_sequence(graph):

    root_nodes = get_root_nodes(graph)

    steps = []
    next_nodes = sorted(root_nodes, key=lambda x: x.step_id)

    while len(next_nodes) > 0:
        next_node = next_nodes[0]
        steps.append(next_node)

        new_candidates = []
        for child in next_node.children:
            all_parents_cleared = True
            for parent in child.parents:
                if parent not in steps:
                    all_parents_cleared = False
                    break
            if all_parents_cleared:
                new_candidates.append(child) 

        next_nodes = sorted(new_candidates + next_nodes[1:], key=lambda x: x.step_id)
    
    return ''.join([s.step_id for s in steps])


def compute_build_time(graph, n_workers=5, base_step_time=60):
    '''
    Christ this is a mess!
    '''
    root_nodes = get_root_nodes(graph)
    step_times = {
        step_id: base_step_time + i + 1 
        for i, step_id in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    }

    completed_steps = []  # Steps already completed
    next_nodes = sorted(root_nodes, key=lambda x: x.step_id)  # Steps in prog or next up
    current_time = 0
    # A catalog of what workers are doing and how long they have left
    workers = {
        worker_id: {'step': None, 'timer': None} 
        for worker_id in range(n_workers)
    }

    while len(next_nodes) > 0:
        # Are any workers jobs done (their timers run down)?
        finished_workers = [
            worker_id for worker_id in workers 
            if workers[worker_id]['step'] is not None and workers[worker_id]['timer'] <= 0
        ]

        # Get the steps just completed
        finished_steps = sorted(
            [
                workers[finished_worker_id]['step'] for finished_worker_id in finished_workers
            ], 
            key=lambda x: x.step_id
        )

        # Clear the tasks these workers were working on
        for finished_worker_id in finished_workers:
            workers[finished_worker_id]['step'] = None

        # Add the newly finished steps to the list of completed steps
        completed_steps.extend(finished_steps)

        # Remove the finished steps from the queue of next steps
        for finished_step in finished_steps:
            next_nodes.remove(finished_step)

        # For finished steps, add their follow-up steps to the list of next available steps if all 
        # prereqs are done        
        for finished_step in finished_steps:
            new_candidates = []
            for child in finished_step.children:
                all_parents_cleared = True
                for parent in child.parents:
                    if parent not in completed_steps:
                        all_parents_cleared = False
                        break
                if all_parents_cleared:
                    new_candidates.append(child)
            next_nodes.extend(new_candidates)

        # Sort next nodes alphabetically and create a list of all next nodes that are currently
        # being worked on
        next_nodes = sorted(next_nodes, key=lambda x: x.step_id)
        active_nodes = [
            workers[worker_id]['step'] 
            for worker_id in workers if workers[worker_id]['step'] is not None
        ]

        # Assign available workers to take on the next available step
        for worker_id in workers:
            if workers[worker_id]['step'] is None:
                available_nodes = [
                    next_node for next_node in next_nodes if next_node not in active_nodes
                ]
                if len(available_nodes) > 0:
                    workers[worker_id]['step'] = available_nodes[0]
                    workers[worker_id]['timer'] = step_times[available_nodes[0].step_id]
                    active_nodes.append(available_nodes[0])

        # Decrement the timers for steps
        for worker_id in workers:
            if workers[worker_id]['step'] is not None:
                workers[worker_id]['timer'] -= 1
        
        # Increment the current time
        current_time += 1
                
    return ''.join([s.step_id for s in completed_steps]), current_time - 1


if __name__ == '__main__':

    test_instructions = '''Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.'''.split('\n')

    test_graph = create_instruction_graph(test_instructions)
    assert get_step_sequence(test_graph) == 'CABDFE'
    test_build_steps, test_build_time = compute_build_time(test_graph, 2, 0)
    assert test_build_steps == 'CABFDE'
    assert test_build_time == 15

    with open('./data/day07_input.txt', 'r') as f:
        input1 = f.readlines()
        input1 = [l for l in input1 if len(l) > 0]
    
    graph = create_instruction_graph(input1)
    print(f'Solution 1: {get_step_sequence(graph)}')
    build_steps, build_time = compute_build_time(graph)
    print(f'Solution 2: {build_time} s  ({build_steps})')
