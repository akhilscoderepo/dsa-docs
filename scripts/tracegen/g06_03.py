from common import *
CH='06-binary-search'
F='03-lower-and-upper-bounds.md'
a=[1,3,5,5,5,8,9,11]
def run(target,upper):
    lo,hi=0,len(a); st=[]
    while lo<hi:
        mid=lo+(hi-lo)//2; v=a[mid]
        before = v<=target if upper else v<target
        if before:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"value":v},"note":f"Read position {mid}: {v} is {'at most' if upper else 'less than'} {target}, so it is before the answer and lo becomes {mid+1}."}); lo=mid+1
        else:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"value":v},"note":f"Read position {mid}: {v} is {'greater than' if upper else 'not less than'} {target}, so it may be the answer and hi becomes {mid}."}); hi=mid
    st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"answer":lo},"note":f"The edges meet at {lo}, which is the answer."})
    return st,lo
s,r=run(5,False); assert r==2 and len(s)==4 and "less than" in s[2]["note"] and "lo becomes 2" in s[2]["note"]
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE1@@")
s,r=run(5,True); assert r==5
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE2@@")
