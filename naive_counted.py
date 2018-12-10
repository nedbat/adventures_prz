"""naive.py, but with counting the calls to salted_hash"""

import hashlib
import itertools
import re

hashes = 0

def salted_hash(salt, i):
    global hashes
    hashes += 1
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

def nth_key(salt, n):
    # Find the `n`th key starting with `salt`.
    num_keys = 0
    for candidate in itertools.count():
        if is_key(salt, candidate):
            num_keys += 1
            if num_keys == n:
                return candidate

INPUT = 'zpqevtbw'  # This will be different for you.
k64 = nth_key(INPUT, 64)
print(f"Part 1: the 64th key is at index {k64}")
print(f"Total of {hashes} hashes")
