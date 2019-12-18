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
    neighbors={v:[] for v in Variables}
    neighbors["2,3"]=["2,"+str(x) for x in range(2,7) if x!=4 and x!=3]+[str(y)+",3" for y in [3,4,5,6]]
    neighbors["2,2"]=["2,"+str(x) for x in range(3,7) if x!=4]+[str(y)+",2" for y in [3,5,6]]
    neighbors["2,5"]=["2,"+str(x) for x in range(2,7) if x!=4 and x!=5]+[str(y)+",5" for y in[3,4,5,6]]
    neighbors["2,6"]=["2,"+str(x) for x in range(2,7) if x!=4 and x!=6]+[str(y)+",6" for y in [3,5,6]]
    neighbors["3,2"]=["3,"+str(x) for x in range (3,7)]+[str(y)+",2" for y in [2,5,6]]
    neighbors["3,3"]=["3,"+str(x) for x in range(2,7) if x!=3]+[str(y)+",3" for y in [2,4,5,6]]
    neighbors["3,5"]=["3,"+str(x) for x in range(2,7) if x!=5]+[str(y)+",5" for y in[2,4,5,6]]
    neighbors["3,4"]=["3,"+str(x) for x in range(2,7) if x!=4]+[str(y)+",4" for y in [4,5]]
    neighbors["3,6"]=["3,"+str(x) for x in range(2,7) if x!=6]+[str(y)+",6" for y in [2,5,6]]
    neighbors["4,3"]=["4,"+str(x) for x in range (3,6) if x!=3]+[str(y)+",3" for y in [3,2,5,6]]
    neighbors["4,4"]=["4,"+str(x) for x in range (3,6) if x!=4]+[str(y)+",4" for y in [3,5]]
    neighbors["4,5"]=["4,"+str(x) for x in range (3,6) if x!=5]+[str(y)+",5" for y in[3,2,5,6]]
    neighbors["5,2"]=["5,"+str(x) for x in range (3,7)]+[str(y)+",2" for y in [3,2,6]]
    neighbors["5,3"]=["5,"+str(x) for x in range(2,7) if x!=3]+[str(y)+",3" for y in [3,4,2,6]]
    neighbors["5,4"]=["5,"+str(x) for x in range(2,7) if x!=4]+[str(y)+",4" for y in [4,3]]
    neighbors["5,5"]=["5,"+str(x) for x in range(2,7) if x!=5]+[str(y)+",5" for y in[3,4,2,6]]
    neighbors["5,6"]=["5,"+str(x) for x in range(2,7) if x!=6]+[str(y)+",6" for y in [3,6,2]]
    neighbors["6,2"]=["6,"+str(x) for x in[3,5,6]]+[str(y)+",2" for y in [3,5,2]]
    neighbors["6,3"]=["6,"+str(x) for x in[2,5,6]]+[str(y)+",3" for y in [3,4,5,2]]
    neighbors["6,5"]=["6,"+str(x) for x in[3,2,6]]+[str(y)+",5" for y in[3,4,5,2]]
    neighbors["6,6"]=["6,"+str(x) for x in[3,5,2]]+[str(y)+",6" for y in [3,5,2]]


    problem1=CSP(Variables,domain,neighbors,largeKakuroConstraints)
    problem2=CSP(Variables,domain,neighbors,largeKakuroConstraints)
    start=time.time()
    result=backtracking_search(problem1,select_unassigned_variable=mrv,order_domain_values=unordered_domain_values,inference=forward_checking)
    total=time.time()-start
    print(result,"in time",total,"by FC+MRV+BT")
    start=time.time()
    print(AC3(problem2))
    result2=backtracking_search(problem2,select_unassigned_variable=mrv)
    total=time.time()-start
    print(result2,"in time",total,"by AC3+BT+MRV")
if __name__ == "__main__":
    largeKakuroSolver()
