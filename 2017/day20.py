"""
2017 Advent Of Code, day 20
https://adventofcode.com/2017/day/20
Michael Bell
12/23/2017
Solutions passed
"""

class Vector(object):
    def __init__(self, xyz):

        if isinstance(xyz, str):
            xyz = (int(val.strip()) for val in xyz.split(','))

        self.xyz = tuple(xyz)
    
    def __add__(self, other_vec):
        vec_sum = (val + other_val for val, other_val in zip(self.xyz, other_vec.xyz))
        return Vector(vec_sum)
    
    def __mul__(self, factor):
        vec_prod = (val * factor for val in self.xyz)
        return Vector(vec_prod)

    def __eq__(self, other_vec):
        return all(val == other_val for val, other_val in zip(self.xyz, other_vec.xyz))

    def __repr__(self):
        return "Vector(({:}))".format(', '.join(str(val) for val in self.xyz))

    def __abs__(self):
        return sum(abs(val) for val in self.xyz)


def parse_pva(pva):
    """
    Given a particle state definition of the form
        p=<x, y, z>, v=<x, y, z>, a=<x, y, z>
    return a tuple of Vectors for the position (p), velocity (v), and acceleration (a) of the
    particle.
    """

    current = 0
    vectors = []
    for _ in range(3):
        open_ndx = pva.index('<', current)
        close_ndx = pva.index('>', current)
        vectors.append(Vector(pva[(open_ndx+1):close_ndx]))
        current = close_ndx + 1

    return tuple(vectors)


class Particle(object):
    def __init__(self, pva):
        self.position, self.velocity, self.acceleration = parse_pva(pva)

    def distance(self):
        return sum(abs(val) for val in self.position.xyz)

    def __repr__(self):
        return "Particle('p=<{:}>, v=<{:}>, a=<{:}>')".format(
            ','.join(str(val) for val in self.position.xyz), 
            ','.join(str(val) for val in self.velocity.xyz), 
            ','.join(str(val) for val in self.acceleration.xyz)
        )
    
    def update_state(self):
        self.velocity = self.velocity + self.acceleration
        self.position = self.position + self.velocity


def get_closest_particle(particle_defs):

    particle_defs = particle_defs.replace('\r', '').split('\n')
    particles = [Particle(particle_def) for particle_def in particle_defs]

    closest_particle = None
    min_accel = 1000000
    # The particle with the smallest acceleration will be nearest the origin in the long term
    for i, particle in enumerate(particles):
        if abs(particle.acceleration) < min_accel:
            closest_particle = i
            min_accel = abs(particle.acceleration)

    return closest_particle


def get_pwds(particles):

    pwds = {}

    for particle_id in particles:
        other_particle_ids = set(particles.keys()).difference([particle_id])

        for other_particle_id in other_particle_ids:
            if (other_particle_id, particle_id) not in pwds:
                diff = abs(
                    (particles[other_particle_id].position * -1) + 
                    particles[particle_id].position
                )
                pwds[(particle_id, other_particle_id)] = diff

    return pwds


def any_converging(last_pwds, this_pwds):
    
    for pair in last_pwds:

        last_dist = last_pwds[pair]

        try:
            this_dist = this_pwds[pair]
        except KeyError:
            this_dist = this_pwds[tuple(val for val in pair[::-1])]

        if this_dist <= last_dist:
            return True

    return False
    

def get_colliding_particles(pwds):
    
    colliding_particles = set()

    for pair in pwds:
        if pwds[pair] == 0:
            colliding_particles = colliding_particles | set(pair)

    return colliding_particles


def remove_colliding_particles_from_pwds(colliding_particles, pwds):
    pairs = list(pwds.keys())

    for pair in pairs:
        if pair[0] in colliding_particles or pair[1] in colliding_particles:
            _ = pwds.pop(pair)
    return pwds


def get_surviving_particles(particle_defs):
    """
    Keep track of pairwise distances (pwd) between particles...
        when a particle has 0 pwd with any other, remove
        keep track of pwd changes from step to step, when all particles are diverging, stop

    There are 1K particles, so I would need to keep a 499K long pwd record

    This isn't fast, but it works!
    """

    particle_defs = particle_defs.replace('\r', '').split('\n')
    particles = {i: Particle(particle_def) for i, particle_def in enumerate(particle_defs)}

    pwds = get_pwds(particles)
    steps = 0

    while True:

        colliding_particles = get_colliding_particles(pwds)
        for colliding_particle in colliding_particles:
            _ = particles.pop(colliding_particle)

        last_pwds = remove_colliding_particles_from_pwds(colliding_particles, pwds)

        for particle_id in particles:
            particles[particle_id].update_state()

        pwds = get_pwds(particles)
        
        if not any_converging(last_pwds, pwds):
            break

        steps += 1
        if steps % 10 == 0:
            print(steps, len(particles))
    
    return len(particles)


TEST_INPUT = '''p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>'''

TEST_INPUT2 = '''p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>    
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>'''


with open('data/day20_input.txt', 'r') as f:
    PUZZLE_INPUT = f.read()

if __name__ == '__main__':
    assert Vector((1, 2, 3)) + Vector((2, 3, 4)) == Vector((3, 5, 7))
    assert Vector('1, 2, 3') + Vector('2, 3, 4') == Vector((3, 5, 7))
    assert Vector((1, 2, 3)) * 2 == Vector((2, 4, 6))
    assert abs(Vector((1, -2, 3))) == 6

    assert parse_pva("p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>") == (
        Vector((3, 0, 0)), Vector((2, 0, 0)), Vector((-1, 0, 0))
    )

    assert Particle("p=< 3,-2, 1>, v=< 2,0,0>, a=<-1,0,0>").distance() == 6
    assert get_closest_particle(TEST_INPUT) == 0

    assert get_surviving_particles(TEST_INPUT2) == 1

    print('All tests passed')

    print('Solution 1: {:}'.format(get_closest_particle(PUZZLE_INPUT)))
    print('Solution 2: {:}'.format(get_surviving_particles(PUZZLE_INPUT)))
