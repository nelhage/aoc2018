import attr
import sys
import re
import collections

@attr.s(slots=True)
class Marble:
  value = attr.ib()
  left = attr.ib(default=None)
  right = attr.ib(default=None)

  def insert_after(self, marb):
    right = self.right
    self.right = marb
    marb.right = right
    marb.left = self
    right.left = marb
    return marb

  def delete(self):
    self.left.right, self.right.left = self.right, self.left
    return self.right

import re
PAT = re.compile(r'(\d+) players; last marble is worth (\d+) points')
m = PAT.search(sys.stdin.read())
if not m:
  raise ValueError()
players, last = int(m.group(1)), int(m.group(2))
last *= 100

scores = collections.defaultdict(int)

cur = Marble(0)
cur.left = cur
cur.right = cur

for i in range(1, last+1):
  if i % 23 == 0:
    player = i % players
    for j in range(7):
      cur = cur.left
    scores[player] += i + cur.value
    cur = cur.delete()
  else:
    cur = cur.right.insert_after(Marble(i))

w,s = max(scores.items(), key=lambda p:p[1])
print("winner={} score={}".format(w, s))
