from common import *
CH='35-advanced-search-sampling-and-geometric-state'; N='01-meet-in-middle.md'
def t1(a):
    s=[0]; st=[{"at":{"i":-1},"vars":{"sums":"0"},"note":"Start: the list holds only the empty sum 0."}]
    for i,x in enumerate(a):
        s=s+[v+x for v in s]
        st.append({"at":{"i":i},"vars":{"element":x,"count":len(s),"sums":" ".join(map(str,s))},"note":f"Add {x} to a shifted copy of the list. The list now has {len(s)} sums."})
    s2=sorted(s); st.append({"at":{"i":len(a)-1},"vars":{"count":len(s2),"sums":" ".join(map(str,s2))},"note":"Sort the list. Both copies of the sum 5 stay in the list."})
    assert s2==[0,2,3,5,5,7,8,10]; return block(a,["i"],st)
def t2(r,need):
    lo,hi=0,len(r); st=[{"at":{"lo":0,"mid":-1,"hi":hi},"vars":{"need":need},"note":f"Start: search the whole list for the first sum at or above {need}."}]
    while lo<hi:
        m=(lo+hi)//2
        if r[m]<need: lo=m+1; n=f"{r[m]} is below {need}, so lo moves to {lo}."
        else: hi=m; n=f"{r[m]} is at or above {need}, so hi moves to {hi}."
        st.append({"at":{"lo":lo,"mid":m,"hi":hi},"vars":{"need":need,"value":r[m]},"note":n})
    d1=abs(r[lo]-need); d0=abs(need-r[lo-1])
    st.append({"at":{"lo":lo,"mid":lo,"hi":hi},"vars":{"need":need,"above":f"{r[lo]} (distance {d1})","below":f"{r[lo-1]} (distance {d0})"},"note":f"The search ends at index {lo}. The neighbours {r[lo]} and {r[lo-1]} are at distance {d1} and {d0}, so the best miss is {min(d0,d1)}."})
    assert min(d0,d1)==1; return block(r,["lo","mid","hi"],st)
fill(CH,N,t1([3,5,2]),"@@TRACE1@@"); fill(CH,N,t2([0,4,7,11,15],8),"@@TRACE2@@")
