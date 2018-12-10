"""The naive code for part 1"""

import hashlib
import itertools
import re

import pytest

def salted_hash(salt, i):
    bytes = f"{salt}{i}".encode("ascii")
    return hashlib.md5(bytes).hexdigest()

def triple(s):
    # Return a triple character, or None.
    m = re.search(r"(.)\1\1", s)
    if m:
        return m.group(1)

def test_triple():
    assert triple("helloaaathere") == "a"

@pytest.mark.parametrize("s, t", [
    ("hello there all", None),
    ("aaa", "b"),
    ("0123345xxx112315zzz124xx", "x"),
])
def test_triples(s, t):
    assert triple(s) == t

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

@pytest.mark.parametrize("salt, candidate, result", [
    ('abc', 17, False),         # no triple
    ('abc', 18, False),         # triple, no quint
    ('abc', 39, True),          # a key
    ('abc', 92, True),          # a key
    ('abc', 22727, False),      # near a key
    ('abc', 22728, True),       # a key
    ('abc', 22729, False),      # near a key
])
def test_is_key(salt, candidate, result):
    assert is_key(salt, candidate) == result

def nth_key(salt, n):
    # Find the `n`th key starting with `salt`.
    num_keys = 0
    for candidate in itertools.count():
        if is_key(salt, candidate):
            num_keys += 1
            if num_keys == n:
                return candidate

def test_nth_key():
    assert nth_key("abc", 64) == 22728

if __name__ == "__main__":
    INPUT = 'zpqevtbw'  # This will be different for you!
    k64 = nth_key(INPUT, 64)
    print(f"Puzzle 1: the 64th key is at index {k64}")
