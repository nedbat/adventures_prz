import hashlib
import itertools
import re

def salted_hash(salt, i):
    bytes = f"{salt}{i}".encode("ascii")
    return hashlib.md5(bytes).hexdigest()

def triple(s):
    """Return a triple character, or None."""
    m = re.search(r"(.)\1\1", s)
    if m:
        return m.group(1)

def is_key(salt, candidate):
    """Is `candidate` a key?"""
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

def key_indexes(salt):
    """Find all the keys starting with `salt`."""
    for candidate in itertools.count():
        if is_key(salt, candidate):
            yield candidate

def complete_keys(salt):
    """Return a list of 64 key indexes for salt."""
    return list(itertools.islice(key_indexes(salt), 64))

INPUT = 'zpqevtbw'

def puzzle1():
    complete = complete_keys(INPUT)
    print(f"Puzzle 1: the 64th key is at index {complete[63]}")

if __name__ == '__main__':
    puzzle1()
