from os import replace
from typing import List, Dict, Tuple
from collections import defaultdict
from helper import read_input_lines


def parse_replacements(replacements: List[str]) -> Dict[str, List[str]]:
    parsed_replacements = defaultdict(lambda: [])

    for replacement in replacements:
        mol, new_mol = replacement.split(' => ')
        parsed_replacements[mol].append(new_mol)

    return parsed_replacements


def calibrate(molecule: str, replacements: Dict[str, List[str]]) -> int:
    new_molecules = []

    start_char = 0

    while start_char < len(molecule):
        for atom_len in [1, 2]:
            atom = molecule[start_char:(start_char + atom_len)]
            if atom in replacements:
                for replacement in replacements[atom]:
                    new_molecules.append(
                        molecule[:start_char] + replacement + molecule[(start_char + atom_len):]
                    )
        start_char += 1

    return len(set(new_molecules))


replacements_and_molecule = read_input_lines(19)
replacements = parse_replacements(replacements_and_molecule[:-1])
molecule = replacements_and_molecule[-1]

test_replacements = '''H => HO
H => OH
O => HH'''.split('\n')
test_molecule_1 = 'HOH'
test_molecule_2 = 'HOHOHO'

test_replacements = parse_replacements(test_replacements)

assert calibrate(test_molecule_1, test_replacements) == 4
assert calibrate(test_molecule_2, test_replacements) == 7

print(calibrate(molecule, replacements))
