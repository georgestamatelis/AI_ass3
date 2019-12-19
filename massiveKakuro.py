from algorithms import *
import time
def bigUglyKakuroConstraints(csp,setVar,setVal,var,val):

    if(setVal==val):
        return False
    #print var,setVar
    tester=csp.infer_assignment()
    tester[setVar]=setVal
    tester[var]=val
    if "2,2" in tester and "2,3" in tester:
        if(tester["2,2"]+tester["2,3"]!=3):
            return False
    if "2,6" in tester and "2,7" in tester:
        if(tester["2,6"]+tester["2,7"]!=7):
            return False
    if all(x in tester for x in["4,4","4,5","4,6"]):
        if(tester["4,4"]+tester["4,5"]+tester["4,6"]!=10):
            return False
    if all(x in tester for x in["6,2","6,3","6,4","6,5","6,6","6,7"]):
        sum=tester["6,2"]+tester["6,3"]+tester["6,4"]+tester["6,5"]+tester["6,6"]+tester["6,7"]
        if(sum!=21):
            return False
    if all(x in tester for x in["7,2","7,3","7,4"]):
        if(tester["7,2"]+tester["7,3"]+tester["7,4"]!=6):
            return False
    if all(x in tester for x in["7,6","7,7"]):
        if(tester["7,6"]+tester["7,7"]!=5):
            return False
    if all(x in tester for x in["3,2","3,3","3,4"]):
        if(tester["3,2"]+tester["3,3"]+tester["3,4"]!=6):
            return False
    if "3,6" in tester and "3,7" in tester:
        if(tester["3,6"]+tester["3,7"]!=3):
            return False
    if "2,2" in tester and "3,2" in tester:
        if(tester["2,2"]+tester["3,2"]!=3):
            return False
    if "2,3" in tester and "3,3" in tester:
        if(tester["2,3"]+tester["3,3"]!=5):
            return False
    if "3,4" in tester and "4,4" in tester:
        if tester["3,4"]+tester["4,4"]!=3:
            return False
    if all(x in tester for x in["4,5","5,5","6,5"]):
        if tester["4,5"]+tester["5,5"]+tester["6,5"]!=8:
            return False
    if "2,7" in tester and "3,7" in tester:
        if tester["2,7"]+tester["3,7"]!=3:
            return False
    if "6,7" in tester and "7,7" in tester:
        if tester["6,7"]+tester["7,7"]!=3:
            return False
    if all(x in tester for x in ["2,6","3,6","4,6","5,6","6,6","7,6"]):
        if tester["2,6"]+tester["3,6"]+tester["4,6"]+tester["5,6"]+tester["6,6"]+tester["7,6"]!=21:
            return False
    if "6,2" in tester and "7,2" in tester:
        if tester["6,2"]+tester["7,2"]!=7:
            return False
    if "6,3" in tester and "7,3" in tester:
        if tester["6,3"]+tester["7,3"]!=3:
            return False

    #########vertical constraings
    return True
################################################################3
def bigUglyKakuroSolver():
    ##UGLY X SHAPED KAKURO
    blacks=[(2,4),(2,5),(3,5),(4,2),(4,3),(4,7),(5,2),(5,3),(5,4),(5,7),(7,5)]
    Variables=[str(x)+","+str(y) for x in range(2,8) for  y in range(2,8) if not (x,y) in blacks]
    domain={v:[1,2,3,4,5,6,7,8,9] for v in Variables}
    ##now comes the pain
    neighbors={}
    for x in range (2,8):
        for y in range(2,8):
            if(x,y) in blacks:
                continue;
            else: #filling neighbors
                key=str(x)+","+str(y)
                neighbors[key]=[str(x)+","+str(z) for z in range(2,8) if z!=y and not (x,z) in blacks]
                neighbors[key]+=[str(z)+","+str(y) for z in range(2,8) if z!=x and not (z,y) in blacks]
    # vertical updates
    for x in [2,3]:
        neighbors["2,"+str(x)].remove("2,6")
        neighbors["2,"+str(x)].remove("2,7")
    for x in ["6","7"]:
        neighbors["2,"+x].remove("2,2")
        neighbors["2,"+x].remove("2,3")
    for x in ["2","3","4"]:
        neighbors["3,"+x].remove("3,6")
        neighbors["3,"+x].remove("3,7")
    for x in ["6","7"]:
        neighbors["3,"+x].remove("3,2")
        neighbors["3,"+x].remove("3,3")
        neighbors["3,"+x].remove("3,4")
    for x in[",2",",3",",4"]:
        neighbors["7"+x].remove("7,6")
        neighbors["7"+x].remove("7,7")
    for x in["7,6","7,7"]:
        neighbors[x].remove("7,2")
        neighbors[x].remove("7,3")
        neighbors[x].remove("7,4")
   ####Vertical Updates
    for x in["2,2","3,2"]:
       neighbors[x].remove("6,2")
       neighbors[x].remove("7,2")
    for x in["6,2","7,2"]:
        neighbors[x].remove("2,2")
        neighbors[x].remove("3,2")
    for x in ["2,3","3,3"]:
        neighbors[x].remove("6,3")
        neighbors[x].remove("7,3")
    for x in ["6,3","7,3"]:
        neighbors[x].remove("2,3")
        neighbors[x].remove("3,3")
    for x in["3,4","4,4"]:
       neighbors[x].remove("6,4")
       neighbors[x].remove("7,4")
    for x in["6,4","7,4"]:
       neighbors[x].remove("3,4")
       neighbors[x].remove("4,4")
    for x in ["2,7","3,7"]:
       neighbors[x].remove("6,7")
       neighbors[x].remove("7,7")
    for x in["6,7","7,7"]:
      neighbors[x].remove("2,7")
      neighbors[x].remove("3,7")
    print "Starting"
    problem1=CSP(Variables,domain,neighbors,bigUglyKakuroConstraints)
    problem2=CSP(Variables,domain,neighbors,bigUglyKakuroConstraints)
    start=time.time()
    result=backtracking_search(problem1,select_unassigned_variable=mrv,order_domain_values=lcv,inference=forward_checking)
    end=time.time()
    print (result,"by FC+BT+MRV in time",end-start)
    start=time.time()
    result=backtracking_search(problem2,select_unassigned_variable=mrv,order_domain_values=lcv,inference=mac)
    end=time.time()
    print (result,"by AC3+BT+MRV in time",end-start)
if __name__ == "__main__":
    bigUglyKakuroSolver()
