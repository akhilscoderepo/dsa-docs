from common import *
from tr import *
CH='15-trees-dfs'
F='06-balance-sentinels.md'
def run(arr,ph):
    L,R=parse(arr); st=[]
    def go(i):
        if i is None: return 0
        l=go(L[i])
        if l==-1:
            st.append({"at":{"node":i},"vars":{"returns":-1},"note":f"The left report of the rod {arr[i]} is the failure value, so it returns failure at once without asking the right side."})
            return -1
        r=go(R[i])
        if r==-1:
            st.append({"at":{"node":i},"vars":{"returns":-1},"note":f"The right report of the rod {arr[i]} is the failure value, so the failure is passed up untouched."})
            return -1
        if abs(l-r)>1:
            st.append({"at":{"node":i},"vars":{"returns":-1},"note":f"The rod {arr[i]} has reaches {l} and {r}, which differ by more than one, so it reports failure."})
            return -1
        h=1+max(l,r)
        st.append({"at":{"node":i},"vars":{"returns":h},"note":f"The rod {arr[i]} has reaches {l} and {r}, a difference within one, so it reports the height {h}."})
        return h
    res=go(0)
    fill(CH,F,block(cells(arr),["node"],st),ph)
    return res
assert run([3,9,20,None,None,15,7],"@@TRACE1@@")==3
assert run([1,2,3,4,None,None,None,5],"@@TRACE2@@")==-1
