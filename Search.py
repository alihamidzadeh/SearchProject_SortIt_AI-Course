from Solution import Solution
from Problem import Problem
from datetime import datetime


class Search:
    @staticmethod
    def bfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do bfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        checkNotRpt = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__() not in checkNotRpt:
                    checkNotRpt.append(c.__hash__())
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    queue.append(c)
        return None

    @staticmethod
    def dfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do dfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        queue = []
        checkNotRpt = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop()
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__() not in checkNotRpt:
                    checkNotRpt.append(c.__hash__())
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    queue.append(c)
        return None

    @staticmethod
    def ucs(prb: Problem) -> Solution:
        start_time = datetime.now()
        queue = []
        checkNotRpt = []
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            queue.sort(key=lambda state: state.g_n)
            state = queue.pop(0)
            neighbors = prb.successor2(state)
            for c in neighbors:
                if c.__hash__() not in checkNotRpt:
                    checkNotRpt.append(c.__hash__())
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    queue.append(c)

        return None

    @staticmethod
    def dls(prb: Problem, depthLimit: int) -> Solution:
        start_time = datetime.now()
        queue = []
        checkNotRpt = {}
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            state = queue.pop(0)
            checkNotRpt[state.__hash__()] = state
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__() not in checkNotRpt and c.g_n <= depthLimit:
                    checkNotRpt[c.__hash__()] = c
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    queue.append(c)
        return None

    @staticmethod
    def ids(prb: Problem) -> Solution:
        depthLimit = -1
        while True:
            depthLimit += 1
            result = Search.dls(prb, depthLimit)
            if result is not None:
                return result
        return None

    @staticmethod
    def a_star(prb: Problem) -> Solution:
        start_time = datetime.now()
        queue = []
        checkNotRpt = {}
        state = prb.initState
        queue.append(state)
        while len(queue) > 0:
            queue.sort(key=lambda state: state.g_n + state.h_n())
            state = queue.pop(0)
            checkNotRpt[state.__hash__()] = state
            neighbors = prb.successor(state)
            for c in neighbors:
                if c.__hash__() not in checkNotRpt:
                    checkNotRpt[c.__hash__()] = c
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    queue.append(c)
        return None

    @staticmethod
    def dla_star(prb: Problem, cut_off: int) -> Solution:
        start_time = datetime.now()
        queue = []
        arr = []
        checkNotRpt = {}
        state = prb.initState
        queue.append(state)

        while len(queue) > 0:
            state = queue.pop()
            checkNotRpt[state.__hash__()] = state
            neighbors = prb.successor(state)

            for c in neighbors:
                arr.append(c)

            for c in neighbors:
                if (c.__hash__() not in checkNotRpt) and (c.g_n + c.h_n() <= cut_off):
                    checkNotRpt[c.__hash__()] = c
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    queue.append(c)
                    arr.remove(c)

    @staticmethod
    def ida_star(prb: Problem) -> Solution:
        state = prb.initState
        cut_off = state.h_n() + state.g_n

        while True:
            result = Search.dla_star(prb, cut_off)
            if not type(result) is Solution:
                cut_off = result
            else:
                return result
