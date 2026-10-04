from common import *
CH='01-arrays-core-operations'
def run(arr, keep, why):
    a=list(arr); w=0; st=[]
    for r,x in enumerate(arr):
        if keep(x):
            a[w]=x; note=f"Read {x} at index {r}. The rule {why} accepts it, so it copies to index {w}."; w+=1
            note+=f" The accepted prefix is now {a[:w]}."
        else:
            note=f"Read {x} at index {r}. The rule rejects it, so nothing is written and the write index stays {w}."
        st.append({"at":{"read":r,"write":w},"vars":{"array":str(a),"kept":w},"note":note})
    st.append({"at":{"read":len(arr),"write":w},"vars":{"array":str(a),"kept":w},"note":f"The scan ends. The return value is {w}, and only the first {w} positions are meaningful."})
    return a,w,st
a1,k1,s1=run([2,7,2,5,9,2,8],lambda x:x!=2,"keep everything except 2")
assert k1==4 and a1[:4]==[7,5,9,8]
a2,k2,s2=run([5,8,0,3,0,1],lambda x:x!=0,"keep every non-zero value")
assert k2==4 and a2[:4]==[5,8,3,1]
fill(CH,'04-stable-compaction.md',block([2,7,2,5,9,2,8],["read","write"],s1),"@@TRACE1@@")
fill(CH,'04-stable-compaction.md',block([5,8,0,3,0,1],["read","write"],s2),"@@TRACE2@@")
