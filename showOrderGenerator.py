#!/usr/bin/python

import sys
import copy
import random

class Act:
  def __init__(self, title, duration, preptime, dancers):
    self.title = title
    self.dancers = dancers
    self.duration = duration
    self.preptime = preptime

  def __str__(self):
    s = self.title + '\nDuration: ' + str(self.duration) + '\nPrep time: ' + str(self.preptime)
    for dancer in self.dancers:
      s += '\n' + dancer
    return s

  def hasConflictingDancers(self, other):
    for dancer in self.dancers:
      if dancer in other.dancers:
        return True

    return False 

  def timeToChangeDuring(self, dancer, others):
    timeToChange = 120
    for other in others:
      if dancer in other.dancers:
        timeToChange = 0
      else:
        timeToChange += other.duration

    return timeToChange

  def canGoAfter(self, others):
    if len(others) > 0 and self.hasConflictingDancers(others[-1]):
      return False
    for dancer in self.dancers:
      if not self.timeToChangeDuring(dancer, others) > self.preptime:
        return False
    return True

def main():
  if len(sys.argv) != 2:
    print "usage: python showOrderGenerator.py filename"
 
  fp = open(sys.argv[1])

  acts = []
  first = True
  curActData = []
  curDancers = []
  for line in fp:
    if first:
      curActData = line.split()     
      first = False
      continue

    if line == '\n':
      first = True
      acts.append(Act(curActData[0], int(curActData[1]), int(curActData[2]), copy.deepcopy(curDancers)))
      curDancers = [] 
      curActData = []
      continue

    curDancers.append(line.strip())

  for act in acts:
    print str(act.title)
  print "\n"

  fp.close()

  potNext = copy.deepcopy(acts)
  showOrder = []
  numActs = len(acts)
  intermission = Act('Intermission', 15, 0, [])
  notAddedIntermission = True
  i = 0
  while len(showOrder) <= numActs: 
    notAddedIntermission = True
    i += 1
    if i > 100:
      print "\n\nRESTARTING..."
      i = 0
      showOrder = []
      potNext = copy.deepcopy(acts)

    nextAct = potNext[random.randint(0, len(potNext)-1)]
    if nextAct.canGoAfter(showOrder):
      print nextAct.title
      showOrder.append(nextAct)
      potNext.remove(nextAct)

    if (len(showOrder) == numActs/2) and notAddedIntermission:
      print 'Intermission'
      showOrder.append(intermission)
      notAddedIntermission = False

  
main()         
        
    
