import attr
import sys
import re
import numpy as np

@attr.s(frozen=True, slots=True)
class Claim:
  id = attr.ib()
  left = attr.ib()
  top  = attr.ib()
  width = attr.ib()
  height = attr.ib()

claims = []
PAT = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
for line in sys.stdin.readlines():
  m = PAT.search(line)
  if m is None:
    raise ArgumentError(line)
  id,l,t,w,h = map(int, m.groups())
  claims.append(Claim(id, l, t, w, h))

max_x = max(c.left+c.width for c in claims)
max_y = max(c.left+c.width for c in claims)

grid = np.zeros((max_x, max_y), dtype=np.uint64)

for cl in claims:
  grid[cl.left:cl.left+cl.width,cl.top:cl.top+cl.height] += 1

print("overlapped={}".format(np.sum(grid > 1)))

for cl in claims:
  if np.all(grid[cl.left:cl.left+cl.width,cl.top:cl.top+cl.height] == 1):
    print("unique={}".format(cl.id))
