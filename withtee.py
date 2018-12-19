"""Part 2, with a peekable iterable."""

import collections
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

def hashes_2017(salt):
    for i in itertools.count():
        yield salted_hash_2017(salt, i)

def test_hashes_2017():
    them = hashes_2017("abc")
    assert next(them) == 'a107ff634856bb300138cac6568c0f24'
    assert next(them) == '65490b7e1ceeff8ade55d803c02bf553'
    assert next(them) == 'dff53117a11213b0e5c4cf63fe3c5198'

def key_indexes(salt):
    """Produce all key indexes from `salt`."""
    p = hashes_2017(salt)
    index = 0
    while True:
        hash = next(p)
        t = triple(hash)
        if t:
            p, sidebar = itertools.tee(p)
            for ahead in itertools.islice(sidebar, 1000):
                if t*5 in ahead:
                    yield index
        index += 1

def test_key_indexes():
    ki = key_indexes("abc")
    assert next(ki) == 10

def n_keys(salt, n):
    all_keys = key_indexes(salt)
    return list(itertools.islice(all_keys, n))

if __name__ == "__main__":
    INPUT = 'zpqevtbw'  # Yours will be different!
    first_64 = n_keys(INPUT, 64)
    k64 = first_64[-1]
    print(f"Part 2: the 64th key is at index {k64}")
