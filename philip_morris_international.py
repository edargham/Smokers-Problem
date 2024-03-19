import threading as thr
import random


class SmokersProblem:
  def __init__(self):
    self.tobacco = False
    self.paper = False
    self.matches = False

    self.table = thr.Semaphore(1)
    self.agent = thr.Semaphore(0)

    self.simulating = True

  def agent_process(self):
    while self.simulating:
      rand_n = random.randint(1, 3)
      self.table.acquire()
      if rand_n == 1:
        print('Agent is placing on table Tobacco and Matches...')
        self.tobacco = True
        self.matches = True
        self.paper = False
      elif rand_n == 2:
        print('Agent is placing on table Tobacco and Paper...')
        self.tobacco = True
        self.matches = False
        self.paper = True
      elif rand_n == 3:
        print('Agent is placing on table Matches and Paper...')
        self.tobacco = False
        self.matches = True
        self.paper = True

      self.table.release()
      self.agent.acquire()

  def smoker_process(self, ingredient):
    while self.simulating:
      self.table.acquire()
      # print(f'Smoker with {ingredient} is checking...')
      if ingredient == 'tobacco' and self.matches and self.paper:
        print(f'Smoker with { ingredient }: Rollin my blunt...')
        self.matches = False
        self.paper = False
        self.agent.release()
      elif ingredient == 'matches' and self.tobacco and self.paper:
        print(f'Smoker with { ingredient }: Rollin my blunt...')
        self.tobacco = False
        self.paper = False
        self.agent.release()
      elif ingredient == 'paper' and self.tobacco and self.matches:
        print(f'Smoker with {ingredient}: Rollin my blunt...')
        self.tobacco = False
        self.matches = False
        self.agent.release()

      self.table.release()

  def simulate(self):
    agent_thread = thr.Thread(target=self.agent_process)
    smoker_threads = [
      thr.Thread(target=self.smoker_process, args=['tobacco']),
      thr.Thread(target=self.smoker_process, args=['matches']),
      thr.Thread(target=self.smoker_process, args=['paper']),
    ]

    agent_thread.start()

    for smoker in smoker_threads:
      smoker.start()

    agent_thread.join()
    for smoker in smoker_threads:
      smoker.join()