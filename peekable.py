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

class PeekableIterable:
    """Peek ahead into infinite iterables"""
    def __init__(self, source):
        self.source = iter(source)
        self.lookahead = collections.deque()

    def __iter__(self):
        while True:
            if self.lookahead:
                yield self.lookahead.popleft()
            else:
                yield next(self.source)

    def peek_ahead(self, index):
        assert index > 0
        while index > len(self.lookahead):
            self.lookahead.append(next(self.source))
        return self.lookahead[index-1]

def test_peekable():
    p = PeekableIterable(itertools.count())
    pi = iter(p)

    assert next(pi) == 0
    assert next(pi) == 1
    assert p.peek_ahead(1) == 2
    assert p.peek_ahead(100) == 101

    assert next(pi) == 2
    assert p.peek_ahead(1) == 3

def key_indexes(salt):
    """Produce all key indexes from `salt`."""
    p = PeekableIterable(hashes_2017(salt))
    for index, hash in enumerate(p):
        t = triple(hash)
        if t:
            for i in range(1, 1001):
                ahead = p.peek_ahead(i)
                if t*5 in ahead:
                    yield index

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
