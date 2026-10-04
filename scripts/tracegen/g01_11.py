from common import *
CH='01-arrays-core-operations'
def run(arr):
    m=n=b=arr[0]; st=[{"at":{"i":0},"vars":{"maxEndingHere":m,"minEndingHere":n,"bestOverall":b},"note":f"Index 0 holds {arr[0]}. All three values start at {arr[0]}."}]
    for i in range(1,len(arr)):
        x=arr[i]; fm,fn=m*x,n*x
        nm=max(x,fm,fn); nn=min(x,fm,fn); nb=max(b,nm)
        sw=" The negative value swaps the roles of the two values." if x<0 and (fm<fn) is False and fm!=fn else ""
        if x<0: sw=" The negative value reverses the order, so the old smallest product feeds the new largest."
        if x==0: sw=" The zero makes every candidate 0, so both values reset."
        st.append({"at":{"i":i},"vars":{"maxEndingHere":nm,"minEndingHere":nn,"bestOverall":nb},"note":f"Index {i} holds {x}. The candidates are {x}, {fm} and {fn}. The largest is {nm} and the smallest is {nn}.{sw} bestOverall is {nb}."})
        m,n,b=nm,nn,nb
    return st,b
a=[2,3,-2,4]; s,b=run(a); assert b==6
fill(CH,'11-product-state.md',block(a,["i"],s),"@@TRACE1@@")
a=[-2,3,-4]; s,b=run(a); assert b==24
fill(CH,'11-product-state.md',block(a,["i"],s),"@@TRACE2@@")
