from common import *
CH='08-two-pointers'
F='03-two-way-partition.md'
def run(src):
    a=list(src); lo,hi=0,len(a)-1; st=[]
    def rec(note):
        st.append({"at":{"lo":lo,"hi":hi},"vars":{"row":",".join(map(str,a)),"evensSoFar":lo},"note":note})
    while lo<=hi:
        if a[lo]%2==0:
            rec(f"Position {lo} holds {a[lo]}, which is even and already in the front region, so lo moves to {lo+1}."); lo+=1
        elif lo==hi:
            rec(f"Both pointers sit on position {lo}, which holds the odd {a[lo]}. It is in the back region, so hi moves to {hi-1}."); hi-=1
        elif a[hi]%2!=0:
            rec(f"Position {lo} holds the odd {a[lo]}, and position {hi} holds {a[hi]}, which is odd and already in the back region, so hi moves to {hi-1}."); hi-=1
        else:
            rec(f"Position {lo} holds the odd {a[lo]} and position {hi} holds the even {a[hi]}. They form a misplaced pair, so both are exchanged and the pointers move to {lo+1} and {hi-1}.")
            a[lo],a[hi]=a[hi],a[lo]; lo+=1; hi-=1
    rec(f"The pointers have crossed, so no position is unresolved. The first {lo} positions are even and the rest are odd.")
    assert all(x%2==0 for x in a[:lo]) and all(x%2!=0 for x in a[lo:]) and sorted(a)==sorted(src)
    return a,lo,st
a,lo,st=run([3,8,5,6,2,7,4,1]); assert lo==4
fill(CH,F,block([3,8,5,6,2,7,4,1],["lo","hi"],st),"@@TRACE1@@")
a,lo,st=run([12,7,9,10,5]); assert lo==2
fill(CH,F,block([12,7,9,10,5],["lo","hi"],st),"@@TRACE2@@")
