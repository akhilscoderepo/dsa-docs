from common import *
CH='06-binary-search'
F='06-rotated-minimum.md'
def run(a,dups):
    lo,hi=0,len(a)-1; st=[]
    while lo<hi:
        mid=lo+(hi-lo)//2; m,r=a[mid],a[hi]
        if m>r:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"middle":m,"rightEnd":r},"note":f"Position {mid} holds {m}, larger than the right end {r}. The middle is in the first stretch, so the drop is to its right and lo becomes {mid+1}."}); lo=mid+1
        elif m<r or not dups:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"middle":m,"rightEnd":r},"note":f"Position {mid} holds {m}, smaller than the right end {r}. The minimum is at {mid} or earlier, so hi becomes {mid}."}); hi=mid
        else:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"middle":m,"rightEnd":r},"note":f"Position {mid} holds {m}, equal to the right end {r}. The middle gives no advice, so drop one copy of the right end and hi becomes {hi-1}."}); hi-=1
    st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"minimum":a[lo]},"note":f"The edges meet at position {lo}, which holds the minimum {a[lo]}."})
    return st,lo
a=[4,5,6,7,0,1,2]; s,p=run(a,False); assert p==4 and "hi becomes 4" in s[2]["note"]
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE1@@")
a=[2,2,2,0,1,2]; s,p=run(a,True); assert p==3 and "equal to the right end" in s[0]["note"]
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE2@@")
