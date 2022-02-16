#!/usr/bin/env python3
import sys
import random
from parse import parse, format_ans, check

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

  def add(self, node):
    # Take the last node
    last = self.end.prev

    # New last node is attach
    last.nxt = node
    # Attach last node to new last node
    node.prev = last
    # Attach end to the new node
    node.nxt = self.end
    # Attach new node to end node
    self.end.prev = node


def clique_compat(cus, clique):
  for c in clique:
    if c not in cus.neighbour:
      return False
  return True

def independent_compat(cus, ind):
  for c in ind:
    if c in cus.neighbour:
      return False
  return True

def find_group(start, ll, f):
  clique = [start]
  for l in ll:
    if f(l.val, clique) is True:
      clique.append(l.val) 
      ll.remove()
    elif len(clique) == 1:
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
        if c.anticompat(j):
          c.neighbour.add(j)
  print("build complete")

  customers = sorted(customers, key=lambda x: len(x.neighbour))
  start = customers[0]
  # Remove the starting elements
  customers.pop(0)
  ll = LinkedList(customers)
  result = find_group(start, ll, independent_compat)
  # Very scuff
  customers.append(start)
  # Very scuff


  piz = set()
  for r in result:
    piz = piz | r.like

  fa = format_ans(piz)


  #score = check(piz, customers) 
  score = len(result)
  print("{}/{}".format(score, len(customers)))
  with open("output_data/{}_{}".format(score, fn), "w") as f:
    f.write(fa)

