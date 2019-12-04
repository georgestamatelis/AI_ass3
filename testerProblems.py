from algorithms import *
import time
################################################
def SAconstraints(CSP,setVar,setVal,var,val):
    return(setVal!=val)
#################################################
def smallDomainProblem():
    """kakuro has a pretty large domain and expensive constraint checks relatively to it's variables"""
    WA="WA"
    SA="SA"
    NT="NT"
    Q="Q"
    NSW="NSW"
    V="V"
    TAZ="TAZ"
    values=["red","green","blue"]
    variables=[WA,SA,NT,Q,V,TAZ,NSW]
    domain={v:values for v in variables}
    neighbors={WA:[NT,SA],SA:[NT,WA,Q,V,NSW],Q:[NT,SA,NSW],NSW:[Q,SA,V],V:[NSW,SA],TAZ:[],NT:[WA,SA,Q]}
    australiaColor=CSP(variables,domain,neighbors,SAconstraints)
    australiaColor2=CSP(variables,domain,neighbors,SAconstraints)
    australiaColor3=CSP(variables,domain,neighbors,SAconstraints)
    start=time.time()
    AC3(australiaColor2)
    print(backtracking_search(australiaColor2,select_unassigned_variable=first_unassigned_variable))
    end=time.time()
    print("by AC3+backtracking search in ",end-start,"seconds")
    start=time.time()
    print(backtracking_search(australiaColor,select_unassigned_variable=first_unassigned_variable))
    end=time.time()
    print("by simple backtracking search in ",end-start,"seconds")
    start=time.time()
    print(backtracking_search(australiaColor3,select_unassigned_variable=mrv,order_domain_values=unordered_domain_values,inference=forward_checking))
    end=time.time()
    print("by forward_checking+mrv in",end-start,"seconds")

if __name__ == "__main__":
    smallDomainProblem()
