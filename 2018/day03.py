# Code for the 2018 AoC, day 3
# https://adventofcode.com/2018/day/3
# Michael Bell
# 12/3/2018

class Claim(object):
    def __init__(self, claim_id, x, y, w, h):
        self.claim_id = claim_id
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Fabric(object):
    def __init__(self, w, h=None):
        self.w = w
        self.h = h if h is not None else w
        self.diagram = [[None for i in range(self.w)] for j in range(self.h)]

    def claim_areas(self, claims):
        for claim in claims:
            self.claim_area(claim)

    def claim_area(self, claim):

        for x in range(claim.x, claim.x + claim.w):
            for y in range(claim.y, claim.y + claim.h):
                if self.diagram[y][x] is None:
                    self.diagram[y][x] = [claim.claim_id]
                else:
                    self.diagram[y][x].append(claim.claim_id) 

    def claimed_area(self, min_claims=2):

        claimed_area = 0
        for row in self.diagram:
            for col in row:
                if col is not None and len(col) >= min_claims:
                    claimed_area += 1
        return claimed_area

    def non_overlapping_claims(self):
        claims_w_dupes = []
        all_claims = []
        for row in self.diagram:
            for col in row:
                if col is not None and len(col) > 1:
                    claims_w_dupes.extend(col)
                if col is not None:
                    all_claims.extend(col)
        
        claims_w_dupes = set(claims_w_dupes)
        all_claims = set(all_claims)

        return list(all_claims.difference(claims_w_dupes))
        

def parse_claim(claim_string):
    # #1 @ 1,3: 4x4

    tmp = claim_string.split('@')
    claim_id = int(tmp[0].replace('#', '').strip())
    tmp = tmp[1].split(':')
    pos = tmp[0]
    x = int(pos.split(',')[0].strip())
    y = int(pos.split(',')[1].strip())
    dims = tmp[1]
    w = int(dims.split('x')[0].strip())
    h = int(dims.split('x')[1].strip())

    return Claim(claim_id, x, y, w, h)


if __name__ == '__main__':

    test_claim_string = '#1 @ 1,3: 4x4'
    test_claim = parse_claim(test_claim_string)
    assert test_claim.claim_id == 1 and test_claim.x == 1 
    assert test_claim.y == 3 and test_claim.w == 4 and test_claim.h == 4

    test_input = '''#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2'''.split('\n')

    test_claims = [parse_claim(ti) for ti in test_input]

    test_fabric = Fabric(8)

    test_fabric.claim_areas(test_claims)
    assert test_fabric.claimed_area() == 4
    assert test_fabric.non_overlapping_claims()[0] == 3

    with open('./data/day03_input.txt', 'r') as f:
        tmp = f.readlines()
        input1 = [parse_claim(t) for t in tmp]
    
    fabric = Fabric(1000)
    fabric.claim_areas(input1)
    print(f'Solution 1: {fabric.claimed_area()}')
    print(f'Solution 2: {fabric.non_overlapping_claims()}')
