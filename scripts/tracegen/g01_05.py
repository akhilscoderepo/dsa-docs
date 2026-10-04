from common import *
CH='01-arrays-core-operations'
def run(arr, copies):
    a=list(arr); w=0; st=[]
    for r,x in enumerate(arr):
        if w<copies:
            ok=True; why=f"Fewer than {copies} values are written, so {x} is admitted without a comparison."
        else:
            ref=a[w-copies]; ok=x!=ref
            why=(f"The value at index {w-copies} of the prefix is {ref}, which differs from {x}, so {x} is admitted." if ok
                 else f"The value at index {w-copies} of the prefix is {ref}, which equals {x}, so {x} is skipped.")
        if ok: a[w]=x; w+=1
        st.append({"at":{"read":r,"write":w},"vars":{"array":str(a),"kept":w},"note":f"Read {x} at index {r}. {why} The prefix is {a[:w]}."})
    return a,w,st
a1,k1,s1=run([1,1,2,2,2,4,7,7],1)
assert k1==4 and a1[:4]==[1,2,4,7]
a2,k2,s2=run([1,1,1,2,2,3],2)
assert k2==5 and a2[:5]==[1,1,2,2,3]
fill(CH,'05-sorted-deduplication.md',block([1,1,2,2,2,4,7,7],["read","write"],s1),"@@TRACE1@@")
fill(CH,'05-sorted-deduplication.md',block([1,1,1,2,2,3],["read","write"],s2),"@@TRACE2@@")
