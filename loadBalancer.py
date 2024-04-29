#load balancer designed to spread api calls to 6 different openai models
#each model has a rate limit of 3 calls per minute and 200 per day

#might improve this with a priority queue for other purposes but
#for now, the number of resources is single digit so the overhead would be
#far slower than using dynamic arrays
#from collections import deque

class LoadBalancer():

  def __init__(self, num_resources):
    self.resources = [0 for i in range(num_resources)]

  def refresh(self):
    for i in range(len(self.resources)-1):
      self.resources[i] = 0

  def balance(self):
    minimum = min(self.resources)
    if minimum >=3:
      self.refresh()
    leastOccupied = self.resources.index(min(self.resources))
    self.resources[leastOccupied] += 1
    return leastOccupied

  
    
