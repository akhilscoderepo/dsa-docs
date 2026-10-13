from common import *
import itertools
CH='29-dynamic-programming-intervals-and-advanced-states'
def brute(c):
    R=len(c);C=len(c[0])
    return min(sum(c[r][cols[r]] for r in range(R)) for cols in itertools.combinations_with_replacement(range(C),R))
def run(cost, ph, expect):
    R=len(cost);C=len(cost[0]); dp=[0]*C
    cells=[v for row in cost for v in row]
    st=[{"at":{"cell":-1},"vars":{"r":-1,"j":-1,"old":0,"run":0,"dp":0},"note":"Start: dp holds zeros, which stand for an empty plan with total 0."}]
    for r in range(R):
        run_=10**9
        for j in range(C):
            old=dp[j]; run_=min(run_,old); dp[j]=cost[r][j]+run_
            st.append({"at":{"cell":r*C+j},"vars":{"r":r,"j":j,"old":old,"run":run_,"dp":dp[j]},
              "note":f"Row {r}, column {j}: old is {old}, so the running minimum is {run_}. The entry writes {cost[r][j]} + {run_} = {dp[j]}."})
    ans=min(dp)
    assert ans==brute(cost)==expect
    st.append({"at":{"cell":R*C-1},"vars":{"r":R-1,"j":C-1,"old":0,"run":0,"dp":ans},"note":f"All rows are done. The smallest value in dp is {ans}, which is the cheapest plan."})
    fill(CH,'07-optimization-proofs.md',block(cells,["cell"],st),ph); return dp
print(run([[3,1,4],[2,5,1],[4,2,3]],"@@TRACE1@@",5))
print(run([[5,2,6,3],[4,7,1,5],[6,3,2,1]],"@@TRACE2@@",4))
