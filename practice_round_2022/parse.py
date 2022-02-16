#!/usr/bin/env python3
from itertools import chain, combinations

class Customer:
  def __init__(self, like, dislike, idx):
    self.like = set(like)
    self.dislike = set(dislike)
    self.idx = idx
    self.neighbour = set()
    self.cnt = len(like) + len(dislike)

  def compat(self, cus):
    return self.like & cus.dislike == set() and self.dislike & cus.like == set()

  def anticompat(self, cus):
    return self.like & cus.dislike != set() or self.dislike & cus.like != set()

  def __str__(self):
    return "{} {}".format(self.like, self.dislike)
  def __repr__(self):
    return "{} {}".format(self.like, self.dislike)


def check(ing, customers):
  score = 0
  for c in customers: 
    if compat(ing, c):
      score += 1
  return score

def compat(ing, c):
  if ing & c.dislike == set() and ing & c.like == c.like:
    return True
  return False

def build(ings):
  pizza = set()
  for ing in ings:
    pizza = pizza | ing.like
  return pizza

# https://docs.python.org/3/library/itertools.html
def powerset(iterable):
  "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
  s = list(iterable)
  return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))


def parse(path):
  with open(path) as f:
    lst = f.readlines()
    lst = [l.strip() for l in lst]
    total_customer = int(lst[0])

  customers = []
  idx = 0
  for i in range(1, total_customer*2, 2):
    like = lst[i].split(" ")   
    dislike = lst[i+1].split(" ")   
    c = Customer(like[1:], dislike[1:], idx)
    customers.append(c)
    idx += 1
  return customers
  
def format_ans(ans):
  p_ret = str(len(ans))
  for i in ans:
    p_ret = p_ret + " " + i     
  return p_ret
  

if __name__ == "__main__":
  fn1 = "a_an_example.in.txt"
  fn2 = "b_basic.in.txt"
  fn3 = "c_coarse.in.txt"
  fn4 = "d_difficult.in.txt"
  fn5 = "e_elaborate.in.txt"

  fn = fn3

  path = "input_data/{}".format(fn)

  customers = parse(path)

  ret = []
  for idx, p in enumerate(powerset(customers)):
    piz = build(p)
    score = check(piz, customers)
    ret.append((piz, score))
    if idx > 10000:
      break

  ans = max(ret, key=lambda x: x[1])
  p_ret = format_ans(ans[0]) 
  print("Score {}/{}".format(ans[1], len(customers)))
  print("Pizza", p_ret)

  with open("output_data/{}_{}".format(ans[1], fn), "w") as f:
    f.write(p_ret)
