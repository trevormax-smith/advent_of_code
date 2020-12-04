# Advent of Code 2020, Day 4
# Michael Bell
# 12/4/2020


class Passport(object):

    FIELDS = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid')
    _INT_FIELDS = ('byr', 'iyr', 'eyr')

    def __init__(self, passport_spec, optional_fields=None):
        # Initialize fields stored in a dict to None
        # If I were doing this for real, I would make these attributes of the class
        # and access below using getattr or something... I'm going to be lazy though
        self.values = {f: None for f in self.FIELDS}

        self._parse_passport_spec(passport_spec)

    def _parse_passport_spec(self, passport_spec):
        kv_pairs = passport_spec.replace('\n', ' ').split()
        
        for kv_pair in kv_pairs:
            key, value = kv_pair.split(':')

            if key in self._INT_FIELDS:
                self.values[key] = int(value)
            else:
                self.values[key] = value
    
    def check_passport(self, optional_fields=None, validate=False):
        '''
        Optional fields specifies one or more fields to skip when checking completeness or validity.
        Can be None, a string with a single field to skip, or a list of fields.
        
        Validate is a flag that indicates whether fields should be checked for valid entries as well
        as checking for completion.
        '''
        if optional_fields is None:
            optional_fields = []
        elif isinstance(optional_fields, str):
            optional_fields = [optional_fields]

        for field in self.FIELDS:
            if field not in optional_fields and not self.values[field]:
                return False
            elif validate and field not in optional_fields and not getattr(self, f'validate_{field}')():
                return False
        return True

    def validate_byr(self):
        if self.values['byr'] and 1920 <= self.values['byr'] <= 2002:
            return True
        return False
    
    def validate_iyr(self):
        if self.values['iyr'] and 2010 <= self.values['iyr'] <= 2020:
            return True
        return False
    
    def validate_eyr(self):
        if self.values['eyr'] and 2020 <= self.values['eyr'] <= 2030:
            return True
        return False
    
    def validate_hgt(self):
        hgt = self.values['hgt']
        if not hgt:
            return False
        
        units = hgt[-2:]
        try:
            value = int(hgt[:-2])
        except ValueError:
            return False
        except:
            raise

        if units == 'cm':
            if 150 <= value <= 193:
                return True
            return False
        elif units == 'in':
            if 59 <= value <= 76:
                return True
            return False
        else:
            return False 

    def validate_hcl(self):
        hcl = self.values['hcl']
        if not hcl or hcl[0] != '#':
            return False
        hcl = hcl.replace('#', '')
        return all(c in 'abcdef0123456789' for c in hcl)

    def validate_ecl(self):
        return self.values['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
    
    def validate_pid(self):
        if not self.values['pid']:
            return False
        return len(self.values['pid']) == 9

    def validate_cid(self):
        return True


def parse_batch(passport_batch):
    passport_specs = passport_batch.split('\n\n')
    passports = []
    for p in passport_specs:
        passports.append(Passport(p))
    return passports


###### TESTS #######################################################
sample_batch = '''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in'''

passports = parse_batch(sample_batch)
assert len([p for p in passports if p.check_passport(optional_fields='cid')]) == 2

passport = Passport('byr:2002')
assert passport.validate_byr()
passport = Passport('byr:2003')
assert not passport.validate_byr()

passport = Passport('hgt:60in')
assert passport.validate_hgt()
passport = Passport('hgt:190cm')
assert passport.validate_hgt()
passport = Passport('hgt:190in')
assert not passport.validate_hgt()
passport = Passport('hgt:190')
assert not passport.validate_hgt()
passport = Passport('hgt:190cd')
assert not passport.validate_hgt()

passport = Passport('hcl:#123abc')
assert passport.validate_hcl()
passport = Passport('hcl:#123abz')
assert not passport.validate_hcl()
passport = Passport('hcl:123abc')
assert not passport.validate_hcl()

passport = Passport('ecl:brn')
assert passport.validate_ecl()
passport = Passport('ecl:wtr')
assert not passport.validate_ecl()

passport = Passport('pid:000000001')
assert passport.validate_pid()
passport = Passport('pid:0123456789')
assert not passport.validate_pid()

sample_valid_passports = '''eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007'''
passports = parse_batch(sample_valid_passports)
assert len([p for p in passports if p.check_passport(optional_fields='cid', validate=True)]) == 0

sample_valid_passports = '''pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719'''
passports = parse_batch(sample_valid_passports)
assert len([p for p in passports if p.check_passport(optional_fields='cid', validate=True)]) == 4


###### THE REAL THING #######################################################

with open('./inputs/day04.txt', 'r') as f:
    batch = f.read()
passports = parse_batch(batch)
print("Part 1:", len([p for p in passports if p.check_passport(optional_fields='cid')]))
print("Part 2:", len([p for p in passports if p.check_passport(optional_fields='cid', validate=True)]))
