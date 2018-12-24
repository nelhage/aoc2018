import sys
import os
import collections

seen = set()

words = [l.rstrip() for l in sys.stdin.readlines()]

twos = 0
threes = 0

for word in words:
  c = collections.Counter(word)
  if 2 in c.values():
    twos += 1
  if 3 in c.values():
    threes += 1
print(twos*threes)
