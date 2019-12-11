from algorithms import *
import time

def sixX6KakuroConstraints(csp,setVar,setVal,var,val):
    if(setVal==val):
        return False
    tester=csp.infer_assignment()
    tester[var]=val
    tester[setVar]=setVal
    if all(t in tester for t in("3,3","3,4","3,5","3,6")) in tester:
        #print "fok"
        sum=tester["3,3"]+tester["3,4"]+tester["3,5"]+tester["3,6"]
        if(sum!=27):
            return False
    if all(t in tester for t in("2,3","2,4","2,5","2,6")) in tester:
        #print "fok"
        sum=tester["2,3"]+tester["2,4"]+tester["2,5"]+tester["2,6"]
        if(sum!=11):
            return False
    if all(t in tester for t in("4,2","4,3")):
        print "fok"
        sum=tester["4,2"]+tester["4,3"]
        if(sum!=17):
            return False
    if all(t in tester for t in("5,2","5,3","5,4","5,5","5,6")):
        #print "fok"
        sum=tester["5,2"]+tester["5,3"]+tester["5,4"]+tester["5,5"]+tester["5,6"]
        if(sum!=30):
            return False
    if all(t in tester for t in("6,2","6,3","6,4","6,5","6,6")):
        #print "fok"
        sum=tester["6,2"]+tester["6,3"]+tester["6,4"]+tester["6,5"]+tester["6,6"]
        if(sum!=10):
            return False
    return True
def sixX6KakuroSolver():
    Variables=[
    "3,3","3,4","3,5","3,6",
    "2,3","2,4","2,5","2,6",
    "4,2","4,3","4,5","4,6",
    "5,2","5,3","5,4","5,5","5,6",
    "6,2","6,3","6,4","6,5","6,6"
    ]
    #FIX THE NEIGHBOURS
    neighbors={
    "3,3":["3,4","3,5","3,6"],
    "3,4":["3,3","3,5","3,6"],
    "3,5":["3,3","3,4","3,6"],
    "3,6":["3,3","3,4","3,5",],
    ############################
    "2,3":["2,4","2,5","2,6"],
    "2,4":["2,3","2,5","2,6"],
    "2,5":["2,4","2,3","2,6"],
    "2,6":["2,4","2,5","2,3"],
    ###########################
    "4,2":["4,3","4,5","4,6"],
    "4,3":["4,2","4,5","4,6"],
    "4,5":["4,3","4,2","4,6"],
    "4,6":["4,3","4,5","4,2"],
    #############################
    "5,2":["5,3","5,4","5,5","5,6"],
    "5,3":["5,2","5,4","5,5","5,6"],
    "5,4":["5,3","5,2","5,5","5,6"],
    "5,5":["5,3","5,4","5,2","5,6"],
    "5,6":["5,3","5,4","5,5","5,2"],
    #################################
    "6,2":["6,3","6,4","6,5","6,6"],
    "6,3":["6,2","6,4","6,5","6,6"],
    "6,4":["6,3","6,2","6,5","6,6"],
    "6,5":["6,3","6,4","6,2","6,6"],
    "6,6":["6,3","6,4","6,5","6,2"]
    }
    x=[1,2,3,4,5,6,7,8,9]
    domain={v:x for v in Variables}
    problem1=CSP(Variables,domain,neighbors,sixX6KakuroConstraints)
    print(backtracking_search(problem1,select_unassigned_variable=mrv,order_domain_values=unordered_domain_values,inference=forward_checking))
if __name__ == "__main__":
    sixX6KakuroSolver()
