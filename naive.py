import hashlib
import itertools
import re

def salted_hash(salt, i):
    bytes = f"{salt}{i}".encode("ascii")
    return hashlib.md5(bytes).hexdigest()

def triple(s):
    # Return a triple character, or None.
    m = re.search(r"(.)\1\1", s)
    if m:
        return m.group(1)

def is_key(salt, candidate):
    # Is `candidate` a key?
    h = salted_hash(salt, candidate)
    t = triple(h)
    if t is None:
        return False

    # We have a triple. Look ahead for a quint.
    for check_ahead in range(1, 1001):
        h2 = salted_hash(salt, candidate + check_ahead)
        if t*5 in h2:
            return True

    return False

def key64(salt):
    # Find the 64th key starting with `salt`.
    candidate = 0
    num_keys = 0
    while True:
        if is_key(salt, candidate):
            num_keys += 1
            if num_keys == 64:
                return candidate
        candidate += 1

INPUT = 'zpqevtbw'
k64 = key64(INPUT)
print(f"Puzzle 1: the 64th key is at index {k64}")
