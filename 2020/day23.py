# Advent of Code 2020, Day 23
# Michael Bell
# 12/23/2020


class CDLLNode(object):
    '''
    Circular double linked list
    '''
    def __init__(self, label):
        self.label = label
        self.previous = None
        self.next = None
    
    def set_next(self, next_node):
        self.next = next_node
        next_node.previous = self
    
    def set_previous(self, previous_node):
        self.previous = previous_node
        previous_node.next = self


def build_cdll(labels, extended=False):

    labels = [int(label) for label in labels]
    if extended:
        max_label = max(labels)
        labels.extend(list(range(max_label + 1, 1_000_001)))

    first_node = CDLLNode(labels[0])
    last_node = first_node
    
    for label in labels[1:]:
        node = CDLLNode(label)
        node.set_previous(last_node)
        last_node = node
    
    node.set_next(first_node)

    return first_node


def get_labels(cdll):
    labels = [cdll.label]

    node = cdll.next
    
    while node != cdll:
        labels.append(node.label)
        node = node.next

    return labels


def get_max_label(cdll):
    labels = get_labels(cdll)
    return max(labels)


def get_min_label(cdll):
    labels = get_labels(cdll)
    return min(labels)


def find_node(cdll, label, direction='backward'):
    node = cdll
    while True:
        if node.label == label:
            break
        else:
            if direction == 'forward':
                node = node.next
            else:
                node = node.previous
            
    return node


def node_lookup_table(cdll):
    lookup_table = {cdll.label: cdll}
    node = cdll.next
    while node != cdll:
        lookup_table[node.label] = node
        node = node.next
    return lookup_table


def game(current_cup, n_moves=100, verbose=False):

    max_label = get_max_label(current_cup)
    min_label = get_min_label(current_cup)

    lookup_table = node_lookup_table(cdll)

    for move in range(n_moves):

        if verbose:
            print(f'-- move {move+1} --')
            print('cups:', print_cdll(current_cup))

        first_to_pickup = current_cup.next
        last_to_pickup = first_to_pickup.next.next
        current_cup.set_next(last_to_pickup.next)
        last_to_pickup.set_next(first_to_pickup)
        if verbose:
            print('pick up:', print_cdll(first_to_pickup))

        picked_up_labels = set([first_to_pickup.label, last_to_pickup.label, first_to_pickup.next.label])
        
        destination_cup_label = current_cup.label - 1
        while True:
            if destination_cup_label < min_label:
                destination_cup_label = max_label
            if destination_cup_label not in picked_up_labels:
                break
            destination_cup_label = destination_cup_label - 1
        
        destination_cup = lookup_table[destination_cup_label]

        if verbose:
            print('destination:', destination_cup.label)
            print()

        destination_cup.next.set_previous(last_to_pickup)
        destination_cup.set_next(first_to_pickup)

        current_cup = current_cup.next


def print_cdll(cdll):
    node = cdll.next
    labels = [str(cdll.label)]
    while node != cdll:
        labels.append(str(node.label))
        node = node.next
    return ' '.join(labels)


def label_order(cdll):
    node_1 = find_node(cdll, 1)
    node = node_1.next
    labels = []
    while node != node_1:
        labels.append(str(node.label))
        node = node.next
    return ''.join(labels)


### TESTS ##################################################
sample_input = '32415'
cdll = build_cdll(sample_input)
assert get_max_label(cdll) == 5

sample_input = '389125467'
cdll = build_cdll(sample_input)
game(cdll, n_moves=10, verbose=False)
assert label_order(cdll) == '92658374'

cdll = build_cdll(sample_input, extended=True)
game(cdll, n_moves=10_000_000)
node_1 = find_node(cdll, 1)
assert node_1.next.label * node_1.next.next.label == 149245887792


### THE REAL THING #########################################
puzzle_input = '247819356'
current_cup = build_cdll(puzzle_input)
game(current_cup)
print('Part 1:', label_order(current_cup))

cdll = build_cdll(puzzle_input, extended=True)
game(cdll, n_moves=10_000_000)
node_1 = find_node(cdll, 1)
print('Part 2:', node_1.next.label * node_1.next.next.label)
