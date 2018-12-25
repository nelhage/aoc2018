import sys
import re
import collections
import heapq

deps = collections.defaultdict(set)
rdeps = collections.defaultdict(set)

PAT = re.compile(r'Step (\w) must be finished before step (\w) can begin.')
for line in sys.stdin:
  m = PAT.search(line)
  if not m:
    raise ValueError(line)
  dep, step = m.groups()
  deps[step].add(dep)
  rdeps[dep].add(step)

order = []
todo  = set(rdeps.keys()) | set(deps.keys())
ready = set(rdeps.keys()) - set(deps.keys())
print("ready={}".format(ready))

workers = 5
queue = []

now = 0
while todo:
  while workers > 0 and ready:
    s = min(ready)
    ready.remove(s)
    heapq.heappush(queue, (now + 61 + ord(s) - ord('A'), s))
    workers -= 1
  t, s = heapq.heappop(queue)
  todo.remove(s)
  workers += 1
  now = t

  for n in rdeps[s]:
    deps[n].remove(s)
    if not deps[n]:
      ready.add(n)

print('t={}'.format(now))
