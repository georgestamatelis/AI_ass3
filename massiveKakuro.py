from algorithms import *
import time
def massiveKakuroConstraints(csp,setVar,setVal,var,val):

    if(setVal==val):
        return False
    #print var,setVar
    tester=csp.infer_assignment()
    tester[setVar]=setVal
    tester[var]=val
    if all(i in tester for i in["2,2","2,3"]):
        if(tester["2,2"]+tester["2,3"]!=4):
            return False
    """if "2,8" in tester and "2,9" in tester:
        if(tester["2,9"]+tester["2,8"]!=3):
            return False"""
    #if "3,2" in tester and "3,3" in tester and "3,4" in tester and "3,5" in tester:
    #    if(tester["3,2"]+tester["3,3"]+tester["3,4"]+tester["3,5"]!=10):
    #        print setVar,var
    #        return False
    if "3,8" in tester and "3,9" in tester:
        if(tester["3,9"]+tester["3,8"]!=7):
            return False
    """if all(i in tester for i in["4,4","4,5","4,6","4,7","4,8"]):
        if(tester["4,4"]+tester["4,5"]+tester["4,6"]+tester["4,7"]+tester["4,8"]!=16):
            print setVar,var
            return False"""
    if "5,3" in tester and "5,4" in tester:
        if(tester["5,3"]+tester["5,4"]!=3):
            return False
    """if("5,6" in tester and "5,7" in tester and "5,8" in tester):
        if(tester["5,6"]+tester["5,7"]+tester["5,8"]!=11):
            print setVar,setVal
            return False"""
    if "6,3" in tester and "6,4" in tester and "6,5" in tester:
        if(tester["6,3"]+tester["6,4"]+tester["6,5"]!=6):
            return False
    if "6,7" in tester and "6,8" in tester:
        if(tester["6,7"]+tester["6,8"]!=10):
            return False
    return True
################################################################3
def massiveKakuroSolver():
    blacks=[(1,1),(1,2),(1,3),(1,4),(1,6),(1,5),(1,7),(1,8),(1,9),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),
    (4,2),(4,3),(5,2),(5,5),(6,2),(6,6),(7,2),(7,8),(7,9),(8,4),(8,5),(9,4),(9,5),(9,6),(9,7),
    (2,4),(2,5),(2,6),(2,7),(3,6),(3,7),(4,9),(5,9),(6,9),
    ]
    Variables=[str(x)+","+str(y) for x in range(1,10) for  y in range(1,10) if not (x,y) in blacks]
    domain={v:[1,2,3,4,5,6,7,8,9] for v in Variables}
    ##now comes the pain
    neighbors={}
    for x in range (2,10):
        for y in range(2,10):
            if(x,y) in blacks:
                continue;
            else: #filling neighbors
                key=str(x)+","+str(y)
                neighbors[key]=[str(x)+","+str(z) for z in range(2,10) if z!=y and not (x,z) in blacks]
                neighbors[key]+=[str(z)+","+str(y) for z in range(2,10) if z!=x and not (z,y) in blacks]
    print neighbors["2,8"]
    problem1=CSP(Variables,domain,neighbors,massiveKakuroConstraints)
    problem2=CSP(Variables,domain,neighbors,massiveKakuroConstraints)
    #start=time.time()
    #result=backtracking_search(problem1,select_unassigned_variable=mrv,order_domain_values=unordered_domain_values,inference=forward_checking)
    #end=time.time()
    #print (result,"by FC+BT+MRV in time",end-start)
    start=time.time()
    AC3(problem2)
    result=backtracking_search(problem2,select_unassigned_variable=mrv)
    end=time.time()
    print (result,"by AC3+BT+MRV in time",end-start)
if __name__ == "__main__":
    massiveKakuroSolver()
