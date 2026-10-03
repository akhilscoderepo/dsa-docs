from common import *
CH='06-binary-search'
F='07-rotated-target.md'
def run(a,t,dups):
    lo,hi=0,len(a)-1; st=[]
    while lo<=hi:
        mid=lo+(hi-lo)//2
        base={"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"middle":a[mid],"target":t}}
        if a[mid]==t:
            st.append({**base,"note":f"Position {mid} holds {a[mid]}, which equals the target {t}. The search ends and reports position {mid}."}); return st,mid
        if dups and a[lo]==a[mid]==a[hi]:
            st.append({**base,"note":f"The first, middle and last values are all {a[mid]}, so neither half can be proved sorted. Drop both ends: lo becomes {lo+1} and hi becomes {hi-1}."}); lo+=1; hi-=1
        elif a[lo]<=a[mid]:
            if a[lo]<=t<a[mid]:
                st.append({**base,"note":f"The left half {a[lo]} to {a[mid]} is sorted and the target {t} lies in its range, so hi becomes {mid-1}."}); hi=mid-1
            else:
                st.append({**base,"note":f"The left half {a[lo]} to {a[mid]} is sorted and the target {t} is outside its range, so lo becomes {mid+1}."}); lo=mid+1
        else:
            if a[mid]<t<=a[hi]:
                st.append({**base,"note":f"The right half {a[mid]} to {a[hi]} is sorted and the target {t} lies in its range, so lo becomes {mid+1}."}); lo=mid+1
            else:
                st.append({**base,"note":f"The right half {a[mid]} to {a[hi]} is sorted and the target {t} is outside its range, so hi becomes {mid-1}."}); hi=mid-1
    return st,-1
a=[4,5,6,7,0,1,2]; s,r=run(a,0,False); assert r==4 and len(s)==3 and "lies in its range" in s[1]["note"]
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE1@@")
a=[1,0,1,1,1]; s,r=run(a,0,True); assert r==1 and "all 1" in s[0]["note"]
fill(CH,F,block(a,["lo","hi","mid"],s),"@@TRACE2@@")
