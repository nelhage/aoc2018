import numpy as np
import sys

hdr = sys.stdin.readline().rstrip()
if not hdr.startswith('initial state: '):
  raise ValueError()
initial = hdr.lstrip('initial state: ')
sys.stdin.readline()

transitions = []
for line in sys.stdin:
  l, r = line.rstrip().split(' => ')
  transitions.append((l,r))

lookup = np.zeros((32,), dtype=np.uint8)
for a, b in transitions:
  i = 0
  for ch in a:
    i = i << 1
    if ch == '#':
      i += 1
  lookup[i] = int(b == '#')

NGEN = 200

PAD = NGEN*4
state = np.array([0]*PAD +
                 [int(s == '#') for s in initial] +
                 [0]*PAD, dtype=np.uint8)

# print("init: {}".format(state))
# print("edges: {}".format(lookup))

indices = np.zeros(state.shape, dtype=np.uint8)

prev=0
for i in range(NGEN):
  indices[:2] = 0
  indices[-2:] = 0
  indices[2:-2] = state[:-4] << 4
  indices[2:-2] += state[1:-3] << 3
  indices[2:-2] += state[2:-2] << 2
  indices[2:-2] += state[3:-1] << 1
  indices[2:-2] += state[4:]
  state[:] = lookup[indices]
  # print("i={:3} state={}".format(i, ''.join('#' if b else '.' for b in state)))
  sum = np.sum(np.arange(-PAD, len(state)-PAD)[state != 0])
  print("gen={:3} sum={} d={}".format(
    i+1, sum, sum-prev))
  prev = sum
