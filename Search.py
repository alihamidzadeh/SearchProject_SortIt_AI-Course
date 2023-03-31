import copy

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

    @staticmethod  # extra score =)))))))
    def bds(prb: Problem) -> Solution:
        goal_state = None
        goal_solution = Search.bfs(prb)  # used BFS Method for get goal state and backwarding

        start_time = datetime.now()
        goal_state = goal_solution.state
        checkNotRpt_forward_children = {}  # Filter same states for forward_children
        checkNotRpt_backward_children = {}  # Filter same states for backward_children
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
                    if c1.__hash__() not in checkNotRpt_forward_children:
                        checkNotRpt_forward_children[c1.__hash__()] = c1
                        for c2 in backward_children:
                            if c2.__hash__() not in checkNotRpt_backward_children:
                                checkNotRpt_backward_children[c2.__hash__()] = state
                                if c1.__hash__() == c2.__hash__():
                                    print(c2.__hash__())
                                    print('DooooOOOOne!')
                                    return Solution(goal_state, prb, start_time)
                                fringe2.append(c2)
                        fringe.append(c1)

        return None

    @staticmethod
    def rbfs(prb: Problem) -> Solution:
        start_time = datetime.now()
        fringe = [prb.initState]
        checkNotRpt = {}
        while len(fringe) > 0:
            fringe.sort(key=lambda state: state.g_n + state.h_n())
            state = fringe.pop(0)
            if len(fringe) != 0:
                state2 = fringe[0]
                state2_fn = state2.h_n() + state2.g_n
            else:
                state2 = copy.deepcopy(state)
                state2_fn = 9999999
            children = prb.successor(state)
            checkNotRpt[state.__hash__()] = state
            children.sort(key=lambda state: state.g_n + state.h_n())
            limit = children[0]
            # limit = min(children, key=lambda state: state.g_n + state.h_n())
            limit_fn = limit.g_n + limit.h_n()
            if limit_fn < state2_fn:
                state2 = limit
                for c in children:
                    if c.__hash__() not in checkNotRpt:
                        checkNotRpt[c.__hash__()] = c
                        if prb.is_goal(c):
                            return Solution(c, prb, start_time)
                        fringe.append(c)
        return None

    @staticmethod
    def rbfs2(prb: Problem) -> Solution:
        start_time = datetime.now()
        state = prb.initState
        solution, res = Search.rbfs_search(prb, state, 9999999, start_time)
        if res == 1 and solution is not None:
            return solution
        else:
            return None

    @staticmethod
    def rbfs_search(prb: Problem, statee, limit: int, start_time) -> Solution:
        state = statee
        children = prb.successor(state)
        # if prb.is_goal(state):
        #     return Solution(state, prb, start_time), 1

        for c in children:
            if (c.g_n + c.h_n() < state.g_n + state.h_n()):
                c.g_n = state.g_n + state.h_n()

        children.sort(key=lambda state: state.g_n + state.h_n())
        children.reverse()
        current = children.pop()

        res = None
        if current.g_n < limit:
            current2 = children.pop()
            if current2.g_n > limit:
                res, current.g_n = Search.rbfs_search(prb, current, limit, start_time)
            else:
                res, current.g_n = Search.rbfs_search(prb, current, current2.g_n, start_time)
            if res != None:
                return res, 1
        else:
            return None, current.g_n
