from common import *
CH='19-recursion-and-backtracking'; F='08-proof-based-pruning.md'
a=[3,4,6,9]; st=[]; path=[]; n=[0]
def go(start,rem):
    for i in range(start,len(a)):
        if a[i]>rem:
            st.append({"at":{"start":start},"vars":{"remain":rem,"events":n[0]},"note":f"The value {a[i]} exceeds the remaining target {rem}, so the loop stops. Every later value is larger still."}); return
        path.append(a[i]); n[0]+=1; nr=rem-a[i]
        note=f"The call with start {start} chooses {a[i]}, so the remaining target becomes {nr}."
        if nr==0: note+=f" The path [{','.join(map(str,path))}] adds up to 10, so the search returns true."
        st.append({"at":{"start":start},"vars":{"remain":nr,"events":n[0]},"note":note})
        if nr==0: return True
        if go(i+1,nr): return True
        path.pop()
go(0,10)
fill(CH,F,block([str(x) for x in a],["start"],st),"@@TRACE1@@")
print(len(st))
st=[{"at":{"start":0},"vars":{"remain":2,"events":0},"note":"The root call needs 2 and its values can reach totals from -3 to 5, so the target lies inside that range and the search continues."},
    {"at":{"start":0},"vars":{"remain":-3,"events":1},"note":"The call chooses 5, so the remaining target becomes -3. A positive-value rule would stop here, but the next value may be negative."},
    {"at":{"start":1},"vars":{"remain":0,"events":2},"note":"The call with start 1 chooses -3, so the remaining target becomes 0. The set [5,-3] adds up to 2, and the search returns true."}]
fill(CH,F,block(["5","-3"],["start"],st),"@@TRACE2@@")
