from common import *
CH='06-binary-search'
F='05-peak-search.md'
def run(a):
    lo,hi=0,len(a)-1; st=[]
    while lo<hi:
        mid=lo+(hi-lo)//2
        if a[mid]<a[mid+1]:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"here":a[mid],"next":a[mid+1],"slope":"rising"},"note":f"Position {mid} holds {a[mid]} and the next holds {a[mid+1]}. The trail is rising, so a peak lies to the right and lo becomes {mid+1}."}); lo=mid+1
        else:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"here":a[mid],"next":a[mid+1],"slope":"falling"},"note":f"Position {mid} holds {a[mid]} and the next holds {a[mid+1]}. The trail is falling, so a peak is here or earlier and hi becomes {mid}."}); hi=mid
    st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"peak":lo,"height":a[lo]},"note":f"The edges meet at position {lo}, holding {a[lo]}, which is a peak."})
    return st,lo
a=[1,3,6,9,12,10,7,4,2]; s,p=run(a); assert p==4 and "hi becomes 4" in s[0]["note"] and "9 and the next holds 12" in s[2]["note"]
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE1@@")
a=[1,5,2,6,3,4]; s,p=run(a); assert p==5 and len(s)==3
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE2@@")
