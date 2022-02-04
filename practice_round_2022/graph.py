#!/usr/bin/env python3
from parse import parse, format_ans, check
import sys

sys.setrecursionlimit(1000000)

b = (0, {})
def dfs(node, visited, piz, l):
  global b 
  if node not in visited:
    #print(node)
    piz = piz | node.like
    #print(piz)
    if l > b[0]:
      b = (l, piz)
    #print(format_ans(piz))
    visited.add(node)
    for neighbour in node.neighbour:
      if compat(piz, neighbour) is True:
        dfs(neighbour, visited, piz, l+1)

def compat(ing, c):
  if ing & c.dislike == set():
    return True
  return False
    
   
if __name__ == "__main__":
  fn1 = "a_an_example.in.txt"
  fn2 = "b_basic.in.txt"
  fn3 = "c_coarse.in.txt"
  fn4 = "d_difficult.in.txt"
  fn5 = "e_elaborate.in.txt"

  fn = fn4

  path = "input_data/{}".format(fn)

  customers = parse(path)

  print(fn)

  print("build tree...")
  for c in customers:
    for j in customers:
      if c != j:
        c.add_compat(j)
  print("build complete")

  #for c in customers:
  #  print(len(c.neighbour), c, c.neighbour)
  #print()
  print("start")
  dfs(customers[0], set(), set(), 1)

  fa = format_ans(b[1])
  print(fa)

  score = check(b[1], customers) 
  print("{}/{}".format(score, len(customers)))
  with open("output_data/{}_{}".format(score, fn), "w") as f:
    f.write(fa)
