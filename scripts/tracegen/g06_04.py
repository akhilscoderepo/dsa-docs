from common import *
CH='06-binary-search'
F='04-first-true.md'
flags=[False,False,False,True,True,True,True]
lo,hi=0,len(flags); st=[]
while lo<hi:
    mid=lo+(hi-lo)//2
    if flags[mid]:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"test":"true"},"note":f"Test position {mid}: true, so the first true position is {mid} or earlier and hi becomes {mid}."}); hi=mid
    else:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"test":"false"},"note":f"Test position {mid}: false, so positions up to {mid} are false and lo becomes {mid+1}."}); lo=mid+1
st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"answer":lo},"note":f"The edges meet at {lo}, the first true position."})
assert lo==3 and "lo becomes 2" in st[1]["note"]
fill(CH,F,block(["F" if not f else "T" for f in flags],["lo","hi","mid"],st),"@@TRACE1@@")
arr=[2,3,4,7,11]; k=5; lo,hi=0,len(arr); st=[]
while lo<hi:
    mid=lo+(hi-lo)//2; miss=arr[mid]-(mid+1)
    if miss>=k:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"value":arr[mid],"missingBefore":miss},"note":f"Position {mid} holds {arr[mid]} with {miss} values missing before it. That reaches {k}, so hi becomes {mid}."}); hi=mid
    else:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"value":arr[mid],"missingBefore":miss},"note":f"Position {mid} holds {arr[mid]} with {miss} values missing before it. That is below {k}, so lo becomes {mid+1}."}); lo=mid+1
st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"answer":lo+k},"note":f"The edges meet at position {lo}. The answer is {lo} + {k} = {lo+k}."})
assert lo+k==9
fill(CH,F,block(arr,["lo","hi","mid"],st),"@@TRACE2@@")
