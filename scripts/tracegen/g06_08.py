from common import *
import math
CH='06-binary-search'
F='08-integer-answers.md'
piles=[3,6,7,11]; h=8
cands=list(range(1,12)); lo,hi=0,len(cands)-1; st=[]
while lo<hi:
    mid=(lo+hi)//2; s=cands[mid]; hrs=sum(math.ceil(p/s) for p in piles)
    if hrs<=h:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"speed":s,"hours":hrs},"note":f"Try speed {s}. The jobs need {hrs} hours, within the limit of {h}, so the answer is {s} or slower and hi comes down to speed {s}."}); hi=mid
    else:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"speed":s,"hours":hrs},"note":f"Try speed {s}. The jobs need {hrs} hours, over the limit of {h}, so every speed up to {s} fails and lo moves to speed {s+1}."}); lo=mid+1
st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"answer":cands[lo]},"note":f"The edges meet at speed {cands[lo]}, the slowest speed that finishes in time."})
assert cands[lo]==4 and "lo moves to speed 4" in st[1]["note"]
fill(CH,F,block([str(c) for c in cands],["lo","hi","mid"],st),"@@TRACE1@@")
nums=[7,2,5,10,8]; k=2
cands=list(range(10,33)); lo,hi=0,len(cands)-1; st=[]
def parts(limit):
    used,sm=1,0
    for x in nums:
        if sm+x>limit: used+=1; sm=0
        sm+=x
    return used
while lo<hi:
    mid=(lo+hi)//2; s=cands[mid]; u=parts(s)
    if u<=k:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"limit":s,"parts":u},"note":f"Try a limit of {s}. Greedy cutting needs {u} parts, which is at most {k}, so hi comes down to {s}."}); hi=mid
    else:
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"limit":s,"parts":u},"note":f"Try a limit of {s}. Greedy cutting needs {u} parts, more than {k}, so lo moves to {s+1}."}); lo=mid+1
st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"answer":cands[lo]},"note":f"The edges meet at {cands[lo]}, the smallest limit that needs at most {k} parts."})
assert cands[lo]==18
fill(CH,F,block([str(c) for c in cands],["lo","hi","mid"],st),"@@TRACE2@@")
