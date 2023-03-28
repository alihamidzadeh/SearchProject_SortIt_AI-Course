from Solution import Solution
from Problem import Problem
from datetime import datetime


class Search:
    @staticmethod
    def bfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do bfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        explored = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__() not in explored:
                    explored.append(c.__hash__())
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    queue.append(c)
        return None

    @staticmethod
    def dfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do dfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        explored = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop()
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__() not in explored:
                    explored.append(c.__hash__())
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    queue.append(c)
        return None
