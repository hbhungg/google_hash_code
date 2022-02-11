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
    
class Node:
  def __init__(self, val=None, prev=None, nxt=None):
    self.val = val
    self.prev = prev
    self.nxt = nxt

  def __repr__(self):
    return str(self.val)

class LinkedList:
  def __init__(self, lst):
    # start and end node
    self.start = Node()
    self.end = Node()

    # Transform list into linked list
    curr = self.start
    for l in lst:
      n = Node(l, prev=curr)
      curr.nxt = n
      curr = n
    
    # Attach end to the linked list
    curr.nxt = self.end
    self.end.prev = curr

  def __iter__(self): 
    self.curr = self.start.nxt
    return self

  def __next__(self):
    if self.curr is self.end:
      raise StopIteration
    else:
      ret = self.curr
      self.curr = self.curr.nxt
      return ret

  def remove(self):
    # Remove prev of curr
    # Since for every next, the curr is return and then move up
    # Hence what we saw in the loop is the prev of curr
    remove_curr = self.curr.prev
    prev = remove_curr.prev
    
    # Unlink the removed node
    prev.nxt = self.curr 
    self.curr.prev = prev

def clique_compat(cus, clique):
  for c in clique:
    if c not in cus.neighbour:
      return False
  return True

def maximal_clique(start, ll):
  clique = [start]
  for l in ll:
    if clique_compat(l.val, clique) is True:
      clique.append(l.val) 
      ll.remove()
  return clique
      

if __name__ == "__main__":
  fn1 = "a_an_example.in.txt"
  fn2 = "b_basic.in.txt"
  fn3 = "c_coarse.in.txt"
  fn4 = "d_difficult.in.txt"
  fn5 = "e_elaborate.in.txt"

  fn = fn5

  path = "input_data/{}".format(fn)

  customers = parse(path)
  
  print(fn)
  print("build tree...")
  for c in customers:
    for j in customers:
      if c != j:
        c.add_compat(j)
  print("build complete")

  start = customers[2]
  # Remove the starting elements
  customers.pop(2)
  ll = LinkedList(customers)
  result = maximal_clique(start, ll)
  print(len(result), result)

  piz = set()
  for r in result:
    piz = piz | r.like

  fa = format_ans(piz)
  score = check(piz, customers) 
  print("{}/{}".format(score, len(customers)))
  with open("output_data/{}_{}".format(score, fn), "w") as f:
    f.write(fa)


  #for c in customers:
  #  print(len(c.neighbour), c, c.neighbour)
  #print()
  #print("start")
  #print(maximal_clique({customers[0]}))
  #dfs(customers[4225], set(), set(), 1)

  #print(len(b[1]))
  #print(fa)

