import attr
import sys
import datetime
import collections
import re
import numpy as np

@attr.s(frozen=True, slots=True)
class Event:
  timestamp = attr.ib()
  event = attr.ib()
  gid = attr.ib()

# [1518-11-04 00:02] Guard #99 begins shift
# [1518-11-04 00:36] falls asleep
# [1518-11-04 00:46] wakes up
PAT = re.compile(r'\[([^\]]+)\] (?:(Guard #(\d+) begins shift)|(falls asleep)|(wakes up))')

events = []
for line in sys.stdin.readlines():
  m = PAT.search(line)
  if m is None:
    raise ValueError(line)
  ts = datetime.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M")
  gid = m.group(3)
  if gid is not None:
    event = 'begin'
    id = m.group(3)
  elif m.group(4):
    event = 'sleep'
  elif m.group(5):
    event = 'wake'
  else:
    raise ValueError(line)
  events.append(Event(ts, event, gid))

events = list(sorted(events, key=lambda e: e.timestamp))

fs = collections.defaultdict(lambda: np.zeros(60, dtype=np.uint64))

gid = None

def wakeup(fs, gid, l, r):
  fs[gid][l:r] += 1

def sleep(fs, gid, l, r):
  pass

for ev in events:
  # print("min={:02} evt={} gid={}".format(ev.timestamp.minute, ev.event, ev.gid))
  if ev.event == 'begin':
    if gid is not None and state == 'asleep':
      wakeup(fs, gid, min, 60)
    gid = ev.gid
    state = 'awake'
    min = 0
  elif ev.event == 'sleep':
    assert state == 'awake'
    sleep(fs, gid, min, ev.timestamp.minute)
    state = 'asleep'
    min = ev.timestamp.minute
  elif ev.event == 'wake':
    assert state == 'asleep'
    wakeup(fs, gid, min, ev.timestamp.minute)
    state = 'awake'
    min = ev.timestamp.minute
  else:
    raise ValueError(ev.event)

for gid, log in fs.items():
  print("{}: {}".format(gid, log))

gid, log = max(fs.items(), key = lambda t: np.sum(t[1]))
min = np.argmax(log)

print("gid={} min={} ct={} csum={}".format(
  gid, min, np.sum(log), min*int(gid)))

maxes = [(g, np.argmax(v), np.max(v)) for (g, v) in fs.items()]
gid, min, ct = max(maxes, key = lambda t: t[2])
uniq = sum(np.sum(v == ct) for v in fs.values())
print("gid={} min={} ct={} csum={}".format(
  gid, min, ct, int(gid)*min))
