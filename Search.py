from Solution import Solution
from Problem import Problem
from datetime import datetime


class Search:
    @staticmethod
    def bfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do bfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        fringe = []
        checkNotRpt = []
        state = prb.initState
        fringe.append(state)
        while len(fringe) > 0:
            state = fringe.pop(0)
            children = prb.successor(state)
            for c in children:
                if c.__hash__() not in checkNotRpt:
                    checkNotRpt.append(c.__hash__())
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    fringe.append(c)
        return None

    @staticmethod
    def dfs(prb: Problem) -> Solution:  # this method get a first state of Problem and do dfs for find solution if no
        # solution is find return None else return the solution
        start_time = datetime.now()
        fringe = []
        checkNotRpt = []
        state = prb.initState
        fringe.append(state)
        while len(fringe) > 0:
            state = fringe.pop()
            children = prb.successor(state)
            for c in children:
                if c.__hash__() not in checkNotRpt:
                    checkNotRpt.append(c.__hash__())
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    fringe.append(c)
        return None

    @staticmethod
    def ucs(prb: Problem) -> Solution:
        start_time = datetime.now()
        fringe = []
        checkNotRpt = []
        state = prb.initState
        fringe.append(state)
        while len(fringe) > 0:
            fringe.sort(key=lambda state: state.g_n)
            state = fringe.pop(0)
            children = prb.successor2(state)
            for c in children:
                if c.__hash__() not in checkNotRpt:
                    checkNotRpt.append(c.__hash__())
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    fringe.append(c)

        return None

    @staticmethod
    def dls(prb: Problem, depthLimit: int) -> Solution:
        start_time = datetime.now()
        fringe = []
        checkNotRpt = {}
        state = prb.initState
        fringe.append(state)
        while len(fringe) > 0:
            state = fringe.pop(0)
            checkNotRpt[state.__hash__()] = state
            children = prb.successor(state)
            for c in children:
                if c.__hash__() not in checkNotRpt and c.g_n <= depthLimit:
                    checkNotRpt[c.__hash__()] = c
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    fringe.append(c)
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
        fringe = []
        checkNotRpt = {}
        state = prb.initState
        fringe.append(state)
        while len(fringe) > 0:
            fringe.sort(key=lambda state: state.g_n + state.h_n())
            state = fringe.pop(0)
            checkNotRpt[state.__hash__()] = state
            children = prb.successor(state)
            for c in children:
                if c.__hash__() not in checkNotRpt:
                    checkNotRpt[c.__hash__()] = c
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    fringe.append(c)
        return None

    @staticmethod
    def dla_star(prb: Problem, cut_off: int) -> Solution:
        start_time = datetime.now()
        fringe = []
        arr = []  # not expanded nodes
        checkNotRpt = {}
        state = prb.initState
        fringe.append(state)

        while len(fringe) > 0:
            state = fringe.pop()
            checkNotRpt[state.__hash__()] = state
            children = prb.successor(state)

            for c in children:
                arr.append(c)

            for c in children:
                if (c.__hash__() not in checkNotRpt) and (c.g_n + c.h_n() <= cut_off):
                    checkNotRpt[c.__hash__()] = c
                    if prb.is_goal(c):
                        return Solution(c, prb, start_time)
                    arr.remove(c)
                    fringe.append(c)

    @staticmethod
    def ida_star(prb: Problem) -> Solution:  # Iterative deepening A*
        state = prb.initState
        cut_off = state.h_n() + state.g_n  # cut_off = prb.initState.h_n() + prb.initState.g_n()

        while True:
            result = Search.dla_star(prb, cut_off)
            if not type(result) is Solution:
                cut_off = result
            else:
                return result

    @staticmethod
    def rbfs(prb: Problem) -> Solution:
        print()

        # start_time = datetime.now()
        # fringe = []
        # arr = []  # not expanded nodes
        # checkNotRpt = {}
        # state = prb.initState
        # fringe.append(state)
        # cut_off = 99999999
        # cut_off_state = prb.initState
        #
        # current = state.h_n() + state.g_n
        # while len(fringe) > 0:
        #     state = fringe.pop()
        #
        #     checkNotRpt[state.__hash__()] = state
        #     children = prb.successor(state)
        #
        #     min = cut_off
        #     min_state = None
        #     for c in children:
        #         if min > c.g_n + c.h_n:
        #             min = c.g_n + c.h_n
        #             min_state = c
        #     cut_off = min
        #     cut_off_state = min_state
        #
        #     for c in children:
        #         if (c.__hash__() not in checkNotRpt) and (current <= cut_off):
        #             checkNotRpt[c.__hash__()] = c
        #             if prb.is_goal(c):
        #                 return Solution(c, prb, start_time)
        #             fringe.append(c)
        #
        #         elif (c.__hash__() not in checkNotRpt) and (current > cut_off):
        #
        # return None

    @staticmethod
    def rbfs_search(node, cut_off):
        print()

    @staticmethod  # extra score =)))))))
    def bds(prb: Problem) -> Solution:
        start_time = datetime.now()
        goal_state = None
        goal_solution = Search.bfs(prb)  # used BFS Method for get goal state and backwarding
        goal_state = goal_solution.state
        arr1 = {}
        arr2 = {}
        if goal_state is not None:
            fringe = []
            fringe2 = []
            state = prb.initState
            fringe.append(state)
            fringe2.append(goal_state)

            while len(fringe) > 0 and len(fringe2) > 0:
                forward_children = prb.successor(fringe.pop())
                backward_children = prb.successor(fringe2.pop())

                for c1 in forward_children:
                    if c1.__hash__() not in arr1:
                        arr1[c1.__hash__()] = c1
                        for c2 in backward_children:
                            if c2.__hash__() not in arr2:
                                arr2[c2.__hash__()] = state
                                if c1.__hash__() == c2.__hash__():
                                    print(c2.__hash__())
                                    print('DooooOOOOne!')
                                    return Solution(goal_state, prb, start_time)
                                fringe2.append(c2)
                        fringe.append(c1)

        return None
