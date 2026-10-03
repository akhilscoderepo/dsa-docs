from common import *
CH='06-binary-search'
F='02-first-and-last.md'
a=[1,3,7,7,7,7,9,12]
def run(target,first):
    lo,hi=0,len(a)-1; cand=-1; st=[]
    while lo<=hi:
        mid=lo+(hi-lo)//2; v=a[mid]
        if v<target:
            note=f"Read position {mid}: {v} is too small, so lo becomes {mid+1}."; st.append((lo,hi,mid,v,cand,note)); lo=mid+1
        elif v>target:
            note=f"Read position {mid}: {v} is too large, so hi becomes {mid-1}."; st.append((lo,hi,mid,v,cand,note)); hi=mid-1
        else:
            cand=mid
            if first: note=f"Read position {mid}: {v} equals the target. Record {mid} as the candidate, and since a smaller index could still hold the target, hi becomes {mid-1}."; st.append((lo,hi,mid,v,cand,note)); hi=mid-1
            else: note=f"Read position {mid}: {v} equals the target. Record {mid} as the candidate, and since a larger index could still hold the target, lo becomes {mid+1}."; st.append((lo,hi,mid,v,cand,note)); lo=mid+1
    return [{"at":{"lo":l,"hi":h,"mid":m},"vars":{"value":v,"candidate":c},"note":n} for l,h,m,v,c,n in st],cand
s,c=run(7,True); assert c==2 and "Record 2 as the candidate" in s[2]["note"]
s.append({"at":{"lo":0,"hi":1,"mid":-1},"vars":{"candidate":c},"note":"The interval is empty, so the search ends. The last recorded candidate, position 2, is the first occurrence."}) if False else None
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE1@@")
s,c=run(7,False); assert c==5 and "too large" in s[-1]["note"]
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE2@@")
