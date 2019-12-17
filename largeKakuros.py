from algorithms import *
import time
def largeKakuroConstraints(csp,setVar,setVal,var,val):
    """
    """
    if(setVal==val):
        return False
    tester=csp.infer_assignment()
    tester[setVar]=setVal
    tester[var]=val
    if "2,2" in tester and "2,3" in tester:
        if(tester["2,2"]+tester["2,3"]!=8):
            return False
    if "2,5" in tester and "2,6" in tester:
        if(tester["2,5"]+tester["2,6"]!=9):
            return False
    if "3,2" in tester and "3,3" in tester and "3,4" in tester and "3,5" in tester and "3,6" in tester:
        if(tester["3,2"]+tester["3,3"]+tester["3,4"]+tester["3,5"]+tester["3,6"]!=30):
            return False
    if "4,3" in tester and "4,4" in tester and "4,5" in tester:
        if(tester["4,3"]+tester["4,4"]+tester["4,5"]!=17):
            return False
    if "5,2" in tester and "5,3" in tester and "5,4" in tester and "5,5" in tester and "5,6" in tester:
        if(tester["5,2"]+tester["5,3"]+tester["5,4"]+tester["5,5"]+tester["5,6"]!=35):
            return False
    if "6,2" in tester and "6,3" in tester:
        if(tester["6,2"]+tester["6,3"]!=4):
            return False
    if "6,5" in tester and "6,6" in tester:
        if(tester["6,5"]+tester["6,6"]!=9):
            return False
    ######VERTICAL SUMS#######################
    if "2,2" in tester and "3,2" in tester:
        if(tester["2,2"]+tester["3,2"]!=6):
            return False
    if "5,2" in tester and "6,2" in tester:
        if(tester["5,2"]+tester["6,2"]!=9):
            return False
    if all(x in tester for x in ["2,3","3,3","4,3","5,3","6,3"]):
        if(tester["2,3"]+tester["3,3"]+tester["4,3"]+tester["5,3"]+tester["6,3"]!=26):
            return False
    if all(x in tester for x in ["2,5","3,5","4,5","5,5","6,5"]):
        if(tester["2,5"]+tester["3,5"]+tester["4,5"]+tester["5,5"]+tester["6,5"]!=31):
            return False
    if "3,4" in tester and "4,4" in tester and "5,4" in tester:
        if(tester["3,4"]+tester["4,4"]+tester["5,4"]!=12):
            return False
    if "2,6" in tester and "3,6" in tester:
        if(tester["2,6"]+tester["3,6"]!=12):
            return False
    if "6,6" in tester and "5,6" in tester:
       if(tester["5,6"]+tester["6,6"]!=16):
            return False
    return True
def largeKakuroSolver():
    x=[1,2,3,4,5,6,7,8,9]
    Variables=["2,2","2,3","2,5","2,6","3,2","3,3","3,4","3,5","3,6"
    ,"4,3","4,4","4,5","5,2","5,3","5,4","5,5","5,6","6,2","6,3","6,5","6,6"]
    domain={v:x for v in Variables}
    neighbors={
    "2,2":["2,3","2,5","2,6","3,2","5,2","6,2"],"2,3":["2,2","2,5","2,6","3,3","4,3","5,3","6,3"],
    "2,5":["2,3","2,2","2,6","3,5","4,5","5,5","6,5"],"2,6":["2,3","2,5","2,2","3,6","5,6","6,6"],
    "3,2":["3,3","3,4","3,5","3,6","5,2","6,2","2,2"], "3,3":["3,2","3,4","3,5","3,6","4,3","5,3","6,3"],"3,4":["3,3","3,2","3,5","3,6","4,4","5,4"],
    "3,5":["3,3","3,4","3,2","3,6","4,5","5,5","6,5"], "3,6":["3,3","3,4","3,5","3,2","5,6","6,6"],
    "4,3":["4,5","4,4","5,3","6,3","2,3"],
    "4,4":["4,3","4,5","5,4","3,4"],
    "4,5":["4,3","4,4","5,5","6,5","3,5","2,5"],
    "5,2":["5,3","5,4","5,5","5,6","6,2","2,2","3,2"],
    "5,3":["5,2","5,4","5,5","5,6","6,3"],"5,4":["5,3","5,2","5,5","5,6"],"5,5":["5,3","5,4","5,2","5,6","6,5"],
    "5,6":["5,3","5,4","5,5","5,2","6,6"],
    "6,2":["6,3","6,5","6,6"],
    "6,3":["6,2","6,5","6,6"],
    "6,5":["6,2","6,3","6,6"],
    "6,6":["6,2","6,3","6,5"]
    }
    problem1=CSP(Variables,domain,neighbors,largeKakuroConstraints)
    problem2=CSP(Variables,domain,neighbors,largeKakuroConstraints)
    start=time.time()
    result=backtracking_search(problem1,select_unassigned_variable=mrv,order_domain_values=unordered_domain_values,inference=forward_checking)
    total=time.time()-start
    print(result,"in time",total,"by FC+MRV+BT")
    start=time.time()
    AC3(problem2)
    result2=backtracking_search(problem2,select_unassigned_variable=mrv)
    total=time.time()-start
    print(result2,"in time",total,"by AC3+BT+MRV")
if __name__ == "__main__":
    largeKakuroSolver()
