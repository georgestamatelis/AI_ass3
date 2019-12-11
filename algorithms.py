"""CSP (Constraint Satisfaction Problems) problems and solvers. (Chapter 6)"""
import time
import itertools
import random
import re
import string
from collections import defaultdict, Counter
import sortedcontainers
from sortedcontainers import SortedSet
from functools import reduce
from operator import eq, neg
from utils import argmin_random_tie, count, first, extend

class CSP():
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b

    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases (for example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(n^4) for the
    explicit representation). In terms of describing the CSP as a
    problem, that's all there is.

    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP. Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        actions(state)          Return a list of actions
        result(state, action)   Return a successor of state
        goal_test(state)        Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
    """

    def __init__(self, variables, domains, neighbors, constraints):
        """Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any."""
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            del assignment[var]

    def nconflicts(self, var, val, assignment):
        """Return the number of conflicts var=val has with other variables."""
        def conflict(var2):
            return var2 in assignment and not self.constraints(self,var, val, var2, assignment[var2])

        return count(conflict(v) for v in self.neighbors[var])
    def display(self, assignment):
        """Show a human-readable representation of the CSP."""
        # Subclasses can print in a prettier way, or display with a GUI
        print(assignment)

    def goal_test(self, state):
        """The goal is to assign all variables, with all constraints satisfied."""
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    # These are for constraint propagation

    def support_pruning(self):
        """Make sure we can prune values from domains. (We want to pay
        for this only if we use it.)"""
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        """Start accumulating inferences from assuming var=value."""
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        """Rule out var=value."""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    # This is for min_conflicts search

    def conflicted_vars(self, current):
        """Return a list of variables in current assignment that are in conflict"""
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]


# ______________________________________________________________________________
# Constraint Propagation with AC3


def no_arc_heuristic(csp, queue):
    return queue


def dom_j_up(csp, queue):
    return SortedSet(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))


def AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
    csp.support_pruning()
    queue = arc_heuristic(csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = revise(csp, Xi, Xj, removals, checks)
        if revised:
            if not csp.curr_domains[Xi]:
                return False, checks  # CSP is inconsistent
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks  # CSP is satisfiable

def revise(csp, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
        conflict = True
        for y in csp.curr_domains[Xj]:
            if csp.constraints(csp,Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            csp.prune(Xi, x, removals)
            revised = True
    return revised, checks



# Constraint Propagation with AC4
# ______________________________________________________________________________
# CSP Backtracking Search

# Variable ordering


def first_unassigned_variable(assignment, csp):
    """The default variable order."""
    varL=[var for var in csp.variables if var not in assignment]
    return varL[0]


def mrv(assignment, csp):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie([v for v in csp.variables if v not in assignment],
                             key=lambda var: num_legal_values(csp, var, assignment))


def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count(csp.nconflicts(var, val, assignment) == 0 for val in csp.domains[var])


# Value ordering


def unordered_domain_values(var, assignment, csp):
    """The default value order."""
    return csp.choices(var)


def lcv(var, assignment, csp):
    """Least-constraining-values heuristic."""
    return sorted(csp.choices(var), key=lambda val: csp.nconflicts(var, val, assignment))


# Inference


def no_inference(csp, var, value, assignment, removals):
    return True


def forward_checking(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    checks=0
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(csp,var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
            checks+=1
    return True

#________________________________________________________________________________________--_____
##Backtracking search

def backtracking_search(csp, select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values, inference=no_inference):
    """[Figure 6.5]"""

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result
################## ##################################################################################################
#_________________________________________________________________________________________________________________
#MAIN FUNCTION-DEMOSTRATION OF ALGORITHMS
def isProblem(A,a,B,b):
    if(A==B and a==b):
        return True
    elif A!=B:
        if a==b:
            #print "fok", A,a,B,b
            return False
        return True

def graphColouring():
    WA="Western Australia"
    NT="Northen Territory"
    SA="South Australia"
    NSW="New South Wales"
    Q="Quensland"
    values=["red","green","blue"]
    variables=[WA,NT,SA,NSW,Q]
    C=CSP(variables,{WA:values,NT:values,SA:values,NSW:values,Q:values},{WA:[NT,SA],SA:[WA,NT,Q,NSW],NT:[WA,SA,Q],NSW:[Q,SA],Q:[NT,NSW,SA]},isProblem)
    #print(backtracking_search(C))
    #print(AC3(C))

def SmallKakuroConstraints(problem,setVar,setVal,var,val):
    """
    keep a dictionary of box:neighbours which need to be different
    """
    tester=problem.infer_assignment()
    tester[setVar]=setVal
    tester[var]=val
    if setVal==val:
        return False
    ####time to take sums into consideration
    if('2,4' in tester and '2,5' in tester):
        sum=tester['2,4']+tester['2,5']
        if(sum!=3):
            return False
    if('3,4' in tester and '2,4' in tester):
        sum=tester['3,4']+tester['2,4']
        if(sum!=6):
            return False
    if('3,5' in tester and '2,5' in tester):
        sum=tester['3,5']+tester['2,5']
        if(sum!=3):
            return False
    if('4,2' in tester and '4,3' in tester):
        sum=tester['4,2']+tester['4,3']
        if(sum!=3 ):
            return False
    if('3,2' in tester and '3,3' in tester and '3,4' in tester and '3,5' in tester):
        sum=tester['3,2']+tester['3,3']+tester['3,4']+tester['3,5']
        if(sum!=10):
            return False
    if('4,2' in tester and '3,2' in tester):
        sum=tester['4,2']+tester['3,2']
        if(sum!=4):
            return False
    if('4,3' in tester and '3,3' in tester):
        sum=tester['3,3']+tester['4,3']
        if(sum!=3 ):
            return False
    return (setVal!=val)

def SmallKakuroSolver():
    """solves the small problem for exercise 1.2"""
    x=[1,2,3,4,5,6,7,8,9]
    two4='2,4'
    two5='2,5'
    three2='3,2'
    three3='3,3'
    three4='3,4'
    three5='3,5'
    four2='4,2'
    four3='4,3'
    ############################################################
    variables=[two4,two5,three2,three3,three4,three5,four2,four3]
    ########################################################################3
    domain={v:x for v in variables}
    ###############################################################3
    neighbours={two4:[two5,three4],two5:[two4,three5],four2:[four3,three2],
    four3:[four2,three3],three2:[four2,three3,three4,three5],
    three3:[three4,three5,three2,four3],three4:[three2,three3,three5,two4],three5:[three2,three3,three4,two5]
    }
    ###########################################################################3
    problem=CSP(variables,domain,neighbours,SmallKakuroConstraints)
    problemCopy=CSP(variables,domain,neighbours,SmallKakuroConstraints)
    problemCopy2=CSP(variables,domain,neighbours,SmallKakuroConstraints)
    print "solutions:\n"
    start=time.time()
    print(backtracking_search(problemCopy2))
    end =time.time()
    print("this solution wa found in",end-start,"seconds by backtracking\n")
    start=time.time()
    print(backtracking_search(problem,select_unassigned_variable=first_unassigned_variable,order_domain_values=unordered_domain_values,inference=forward_checking))
    end=time.time()
    print("this solution was found in ",end-start,"by FC+MRV")
    start=time.time()
    isPrunable,num_of_checks=AC3(problemCopy)
    print(isPrunable,"in ",num_of_checks,"checks")
    print(backtracking_search(problemCopy,select_unassigned_variable=first_unassigned_variable))
    end=time.time()
    print("This solution was found in",end-start,"By AC3")

if __name__ == "__main__":
    SmallKakuroSolver()
    #graphColouring()
