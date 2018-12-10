"""Cache the hash, so part 2 will be reasonable."""

import hashlib
import itertools
import re

import pytest

def make_salted_hash(n):
    cache = {}
    def _salted_hash(salt, i):
        result = cache.get((salt, i))
        if result is not None:
            return result
        val = f"{salt}{i}"
        for _ in range(n):
            val = hashlib.md5(val.encode("ascii")).hexdigest()
        cache[(salt, i)] = val
        return val
    return _salted_hash

salted_hash_1 = make_salted_hash(1)
salted_hash_2017 = make_salted_hash(2017)

def test_salted_hash():
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

def is_key(salt, candidate, hash_fn):
    # Is `candidate` a key?
    h = hash_fn(salt, candidate)
    t = triple(h)
    if t is None:
        return False

    # We have a triple. Look ahead for a quint.
    for check_ahead in range(1, 1001):
        h2 = hash_fn(salt, candidate + check_ahead)
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
    assert is_key(salt, candidate, salted_hash_1) == result

def nth_key(salt, n, hash_fn):
    # Find the `n`th key starting with `salt`.
    num_keys = 0
    for candidate in itertools.count():
        if is_key(salt, candidate, hash_fn):
            num_keys += 1
            if num_keys == n:
                return candidate

def test_nth_key():
    assert nth_key("abc", 64, salted_hash_1) == 22728

if __name__ == "__main__":
    INPUT = 'zpqevtbw'  # This will be different for you!
    k64 = nth_key(INPUT, 64, salted_hash_1)
    print(f"Part 1: the 64th key is at index {k64}")
    k64 = nth_key(INPUT, 64, salted_hash_2017)
    print(f"Part 2: the 64th key is at index {k64}")
