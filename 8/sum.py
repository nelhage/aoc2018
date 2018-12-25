import attr
import sys

@attr.s(frozen=True, slots=True)
class Node:
  children = attr.ib()
  metadata = attr.ib()

stream = list(map(int,sys.stdin.readline().split()))

def read(stream, i):
  nchildren = stream[i]
  i += 1
  nmeta = stream[i]
  i += 1

  children = []
  for j in range(nchildren):
    ch, i = read(stream, i)
    children.append(ch)
  meta = stream[i:i+nmeta]
  i += nmeta
  return (Node(children, meta), i)

root, i = read(stream, 0)
assert i == len(stream)

def csum(node):
  return sum(node.metadata) + sum(map(csum, node.children))

print("metasum={}".format(csum(root)))

def value(node):
  if not node.children:
    return sum(node.metadata)
  cvs = list(map(value, node.children))
  return sum(cvs[i-1] for i in node.metadata if i > 0 and i <= len(cvs))

print("value={}".format(value(root)))
