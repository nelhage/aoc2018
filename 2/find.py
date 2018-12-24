import sys
import os
import collections

seen = set()

words = [l.rstrip() for l in sys.stdin.readlines()]

def match(w1, w2):
  if len(w1) != len(w2):
    return False
  d = 0
  for i, c1 in enumerate(w1):
    if w2[i] != c1:
      d += 1
      if d > 1:
        return False
  return d == 1

for w1 in words:
  for w2 in words:
    if match(w1, w2):
      print(''.join(c1 for (c1, c2) in zip(w1, w2) if c1 == c2))
      sys.exit(0)
