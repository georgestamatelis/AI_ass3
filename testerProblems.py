from algorithms import *
import time
################################################

def fourX4_kakuro1Constraints(csp,setVar,setVal,var,val):
    if(setVal==val):
        return False
    tester=csp.infer_assignment()
    tester[var]=val
    tester[setVar]=setVal
    if "2,2" in tester and "2,3" in tester:
        sum=tester["2,2"]+tester["2,3"]
        if(sum!=13):
            return False
    if ("3,2" in tester and "3,3" in tester and "3,4" in tester):
        sum=tester["3,2"] +tester["3,3"]+tester["3,4"]
        if(sum!=12):
            return False
    if "4,3" in tester and "4,4" in tester:
        sum=tester["4,3"]+tester["4,4"]
        if(sum!=3) :
            return False
    ###vertical
    if "2,2" in tester and "3,2" in tester:
        if(tester["2,2"]+tester["3,2"]!=5):
            return False
    if("2,3" in tester and "3,3" in tester and "4,3" in tester):
        if(tester["2,3"] +tester["3,3"]+tester["4,3"]!=19):
            return False
    if("3,4" in tester and "4,4" in tester):
        sum=tester["3,4"]+tester["4,4"]
        if(sum!=4):
            return False
    return True
def fourX4_kakuro1():
    two2="2,2"
    two3="2,3"
    three2="3,2"
    three3="3,3"
    three4="3,4"
    four3="4,3"
    four4="4,4"
    variables=["2,2","2,3","3,2","3,3","3,4","4,3","4,4"]
    values=[1,2,3,4,5,6,7,8,9]
    domain={v:values for v in variables}
    neighbors={
    "2,2":["2,3","3,2"],
    "2,3":["2,2","3,3","4,3"],
    "3,2":["2,2","3,3","3,4"],
    "3,3":["2,3","3,2","3,4","4,3"],
    "3,4":["4,4","3,3","3,2"],
    "4,3":["4,4","3,3","2,3"],
    "4,4":["3,4","4,3"]
    }
    problem1=CSP(variables,domain,neighbors,fourX4_kakuro1Constraints)
    problem2=CSP(variables,domain,neighbors,fourX4_kakuro1Constraints)
    problem3=CSP(variables,domain,neighbors,fourX4_kakuro1Constraints)
    start=time.time()
    solution1=backtracking_search(problem1,select_unassigned_variable=first_unassigned_variable,order_domain_values=unordered_domain_values,inference=no_inference)
    print(solution1,"in time",time.time()-start,"by backtracking")
    start=time.time()
    solution2=backtracking_search(problem2,select_unassigned_variable=mrv,order_domain_values=unordered_domain_values,inference=forward_checking)
    print(solution2,"in time",time.time()-start,"by FC+MRV")
    start=time.time()
    AC3(problem3)
    solution3=backtracking_search(problem3)
    print(solution3,"in time",time.time()-start,"by AC3 +backtracking")
###########################################################################################
def tinyKakuroConstraints(csp,setVar,setVal,var,val):
    if(setVal==val):
        return False
    tester=csp.infer_assignment()
    tester[var]=val
    tester[setVar]=setVal
    if "2,2" in tester and "2,3" in tester:
        if(tester["2,2"]+tester["2,3"]!=8):
            return False
    if "3,2" in tester and "3,3" in tester:
        if(tester["3,3"]+tester["3,2"]!=6):
            return False
    if "3,2" in tester and "2,2" in tester:
        if(tester["3,2"]+tester["2,2"]!=11):
            return False
    if "3,3" in tester and "2,3" in tester:
        if(tester["3,3"]+tester["2,3"]!=3):
            return False
    return True
def tinyKakuroSolver():
    variables=["2,2","2,3","3,2","3,3"]
    x=[1,2,3,4,5,6,7,8,9]
    domain={v:x for v in variables}
    neighbours={
    "2,2":["2,3","3,2"],
    "2,3":["2,2","3,3"],
    "3,2":["2,2","3,3"],
    "3,3":["2,3","3,2"]
    }
    problem1=CSP(variables,domain,neighbours,tinyKakuroConstraints)
    solution=(backtracking_search(problem1))
    print solution
############################################################################################
def FiveX5kakuroConstr(csp,setVar,setVal,var,val):
    if(setVal==val):
        return False
    tester=csp.infer_assignment()
    tester[var]=val
    tester[setVar]=setVal
    if("2,3" in tester and "2,4" in tester):
        if(tester["2,3"]+tester["2,4"]!=4):
            return False
    if("3,2" in tester and "3,3" in tester and "3,4" in tester and "3,5" in tester):
        if(tester["3,2"]+tester["3,3"]+tester["3,4"]+tester["3,5"]!=17):
            return False
    if("4,2" in tester and "4,3" in tester and "4,4" in tester and "4,5" in tester):
        if(tester["4,2"]+tester["4,3"]+tester["4,4"]+tester["4,5"]!=26):
            return False
    if("5,3" in tester and "5,4" in tester):
        if(tester["5,3"]+tester["5,4"]!=11):
            return False
    #######################################################
    if("4,2" in tester and "3,2" in tester):
        if(tester["4,2"] +tester["3,2"]!=4):
            return False
    if("2,3" in tester and "3,3" in tester and "4,3" in tester and "5,3" in tester):
        if(tester["2,3"] +tester["3,3"]+tester["4,3"]+tester["5,3"]!=26):
            return False
    if("2,4" in tester and "3,4" in tester and "4,4" in tester and "5,4" in tester):
        if(tester["2,4"] +tester["3,4"]+tester["4,4"]+tester["5,4"]!=12):
            return False
    if("3,5" in tester and "4,5" in tester):
        if(tester["3,5"]+tester["4,5"]!=16):
            return False
    return True
def FiveX5kakuroSolver():
    Variables=[
    "2,3","2,4",
    "3,2","3,3","3,4","3,5",
    "4,2","4,3","4,4","4,5",
    "5,3","5,4",
    ]
    x=[1,2,3,4,5,6,7,8,9]
    domain={v:x for v in Variables}
    neighbours={
    "2,3":["2,4","3,3","4,3","5,3"],
    "2,4":["2,3","4,4","3,4","5,4"],
    "3,2":["3,3","3,4","3,5","4,2"],
    "3,3":["3,2","3,4","3,5","2,3","4,3","5,3"],
    "3,4":["3,2","3,3","3,5","4,4","5,4","2,4"],
    "3,5":["3,2","3,3","3,4","4,5"],
    "4,2":["4,3","4,4","4,5","3,2"],
    "4,3":["4,2","4,4","4,5","3,3","2,3","5,3"],
    "4,4":["4,2","4,3","4,5","5,4","3,4","2,4"],
    "4,5":["4,2","4,4","4,3","3,5"],
    "5,3":["5,4","4,3","3,3","2,3"],
    "5,4":["5,3","4,4","3,4","2,4"]
    }
    problem1=CSP(Variables,domain,neighbours,FiveX5kakuroConstr)
    problem2=CSP(Variables,domain,neighbours,FiveX5kakuroConstr)
    problem3=CSP(Variables,domain,neighbours,FiveX5kakuroConstr)
    start=time.time()
    solution1=backtracking_search(problem1)
    print(solution1,"by backtracking in",time.time()-start,"seconds")
    print("\n\n")
    start=time.time()
    solution2=backtracking_search(problem2,select_unassigned_variable=mrv,order_domain_values=unordered_domain_values,inference=forward_checking)
    print(solution2,"by forward_checking +MRV in",time.time()-start,"seconds")
    print("\n\n")
    start=time.time()
    AC3(problem3)
    solution3=backtracking_search(problem3)
    print(solution3,"by AC3 in",time.time()-start,"seconds")
if __name__ == "__main__":
    #print("4x4 kakuro\n")
    #fourX4_kakuro1()
    #print("tiny kakuro\n")
    #tinyKakuroSolver()
    FiveX5kakuroSolver()
