import sys, pathlib
sys.path.insert(0, '/home/claude/dsa-docs/scripts/tracegen')
from common import block, fill
CH='32-selection-and-ordered-data-techniques'
def part(a,lo,hi):
    m=lo+(hi-lo)//2; a[m],a[hi]=a[hi],a[m]; pv=a[hi]; s=lo
    for i in range(lo,hi):
        if a[i]<pv: a[i],a[s]=a[s],a[i]; s+=1
    a[s],a[hi]=a[hi],a[s]; return s,pv
def trace(a0,k):
    a=list(a0); lo,hi=0,len(a)-1
    steps=[{"at":{"lo":lo,"hi":hi,"p":-1},"vars":{"k":k},"note":f"The range is the whole array, lo {lo} to hi {hi}. No partition has run yet."}]
    while lo<hi:
        p,pv=part(a,lo,hi)
        if p==k: d="The pivot sits at index k, so it is the answer."; nl,nh=lo,hi
        elif k<p: d=f"Index {k} is less than {p}, so the left side stays and hi becomes {p-1}."; nl,nh=lo,p-1
        else: d=f"Index {k} is greater than {p}, so the right side stays and lo becomes {p+1}."; nl,nh=p+1,hi
        steps.append({"at":{"lo":lo,"hi":hi,"p":p},"vars":{"pivot":pv,"k":k},"note":f"The pivot {pv} lands at index {p}. The array is now {a}. {d}"})
        if p==k: break
        lo,hi=nl,nh
    assert a[k]==sorted(a0)[k]
    return block(list(a0),["lo","hi","p"],steps)
fill(CH,'01-quickselect.md',trace([7,2,9,4,1,8,3],2),"@@TRACE1@@")
fill(CH,'01-quickselect.md',trace([3,2,3,1,2,4,5,5,6],5),"@@TRACE2@@")
