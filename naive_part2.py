"""The naive code for part 1"""

import hashlib
import itertools
import re

import pytest

def salted_hash_2017(salt, i):
    val = f"{salt}{i}"
    for _ in range(2017):
        val = hashlib.md5(val.encode("ascii")).hexdigest()
    return val

def test_salted_hash_2017():
    assert salted_hash_2017("abc", 0) == "a107ff634856bb300138cac6568c0f24"

def triple(s):
    # Return a triple character, or None.
    m = re.search(r"(.)\1\1", s)
    if m:
        return m.group(1)

def test_triple():
    assert triple("helloaaathere") == "a"

@pytest.mark.parametrize("s, t", [
    ("hello there all", None),
    ("aaa", "a"),
    ("0123345xxx112315zzz124xx", "x"),
])
def test_triples(s, t):
    assert triple(s) == t

def is_key(salt, candidate):
    # Is `candidate` a key?
    h = salted_hash_2017(salt, candidate)
    t = triple(h)
    if t is None:
        return False

    # We have a triple. Look ahead for a quint.
    for check_ahead in range(1, 1001):
        h2 = salted_hash_2017(salt, candidate + check_ahead)
        if t*5 in h2:
            return True

    return False

@pytest.mark.parametrize("salt, candidate, result", [
    ('abc', 4, False),          # no triple
    ('abc', 5, False),          # triple, no quint
    ('abc', 10, True),          # a key
    ('abc', 22551, True),       # a key
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

if __name__ == "__main__":
    INPUT = 'zpqevtbw'  # This will be different for you!
    k64 = nth_key(INPUT, 64)
    print(f"Part 1: the 64th key is at index {k64}")
