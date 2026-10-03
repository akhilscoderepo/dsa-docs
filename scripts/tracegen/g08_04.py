from common import *
CH='08-two-pointers'
F='04-three-way-partition.md'
def run(src):
    a=list(src); low,mid,high=0,0,len(a)-1; st=[]
    def rec(note):
        st.append({"at":{"low":low,"mid":mid,"high":high},"vars":{"row":",".join(map(str,a)),"value":a[mid] if mid<=high else "none"},"note":note})
    while mid<=high:
        v=a[mid]
        if v==0:
            if low==mid: rec(f"Position {mid} holds 0 and the middle region is empty, so it trades with itself. Both low and mid move on to {mid+1}.")
            else: rec(f"Position {mid} holds 0. It trades with position {low}, which holds a 1 from the middle region, so low becomes {low+1} and mid becomes {mid+1}.")
            a[low],a[mid]=a[mid],a[low]; low+=1; mid+=1
        elif v==1:
            rec(f"Position {mid} holds 1, which already belongs in the middle region, so mid moves to {mid+1}.")
            mid+=1
        else:
            if mid==high: rec(f"Position {mid} holds 2 and is also the last unresolved position, so it trades with itself and high becomes {high-1}.")
            else: rec(f"Position {mid} holds 2. It trades with position {high}, high becomes {high-1}, and mid stays at {mid} because the value that arrived from position {high} has not been looked at yet.")
            a[mid],a[high]=a[high],a[mid]; high-=1
    rec(f"The unresolved region is empty. Zeros fill the first {low} positions, ones fill the next {mid-low}, and twos fill the last {len(a)-mid}.")
    assert a==sorted(src)
    return a,low,mid,st
a,l,m,st=run([2,0,2,1,1,0]); assert (l,m)==(2,4)
fill(CH,F,block([2,0,2,1,1,0],["low","mid","high"],st),"@@TRACE1@@")
a,l,m,st=run([1,0,2,1,0]); assert (l,m)==(2,4)
fill(CH,F,block([1,0,2,1,0],["low","mid","high"],st),"@@TRACE2@@")
