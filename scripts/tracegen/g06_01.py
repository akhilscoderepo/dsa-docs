from common import *
CH='06-binary-search'
F='01-exact-search.md'
a=[2,5,8,12,16,23,38,56,72,91]
def run(target):
    lo,hi=0,len(a)-1; st=[]
    while lo<=hi:
        mid=lo+(hi-lo)//2; v=a[mid]
        if v==target:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"value":v,"target":target},"note":f"Read position {mid}: {v} equals {target}. The search ends and returns {mid}."}); return st,mid
        if v<target:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"value":v,"target":target},"note":f"Read position {mid}: {v} is too small, so positions {lo} to {mid} are ruled out and lo becomes {mid+1}."}); lo=mid+1
        else:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"value":v,"target":target},"note":f"Read position {mid}: {v} is too large, so positions {mid} to {hi} are ruled out and hi becomes {mid-1}."}); hi=mid-1
    st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"target":target,"verdict":"absent"},"note":f"The left edge {lo} has passed the right edge {hi}, so the interval is empty and the target {target} is absent."})
    return st,-1
s,r=run(23); assert r==5 and len(s)==3
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE1@@")
s,r=run(40); assert r==-1 and s[-1]["at"]["lo"]==7 and s[-1]["at"]["hi"]==6
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE2@@")
