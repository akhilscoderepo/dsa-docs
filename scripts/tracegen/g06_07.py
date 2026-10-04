from common import *
CH='06-binary-search'
def run(a,t,ph):
    lo,hi=0,len(a)-1
    st=[{"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"target":str(t)},"note":f"Start with the whole array, indexes {lo} to {hi}."}]
    res=-1
    while lo<=hi:
        mid=lo+(hi-lo)//2; plo,phi=lo,hi; v=a[mid]
        if v==t:
            st.append({"at":{"lo":plo,"hi":phi,"mid":mid},"vars":{"nums[mid]":str(v),"target":str(t)},"note":f"The value {v} equals the target, so the search returns index {mid}."}); res=mid; break
        if a[lo]<=a[mid]:
            half="left"; inr=a[lo]<=t<a[mid]
            if inr: hi=mid-1; nt=f"The left half is sorted, from {a[plo]} to {v}. The target {t} lies inside it, so hi becomes {hi}."
            else: lo=mid+1; nt=f"The left half is sorted, from {a[plo]} to {v}. The target {t} is outside it, so lo becomes {lo}."
        else:
            half="right"; inr=a[mid]<t<=a[hi]
            if inr: lo=mid+1; nt=f"The right half is sorted, from {v} to {a[phi]}. The target {t} lies inside it, so lo becomes {lo}."
            else: hi=mid-1; nt=f"The right half is sorted, from {v} to {a[phi]}. The target {t} is outside it, so hi becomes {hi}."
        st.append({"at":{"lo":plo,"hi":phi,"mid":mid},"vars":{"nums[mid]":str(v),"sorted half":half},"note":nt})
    if res==-1:
        st.append({"at":{"lo":min(lo,len(a)),"hi":hi,"mid":-1},"vars":{"target":str(t)},"note":"The interval is empty, so the target is absent and the search returns -1."})
    fill(CH,'07-rotated-target.md',block(list(a),["lo","hi","mid"],st),ph); return res
assert run([6,7,9,1,2,3,4],2,"@@TRACE1@@")==4
assert run([4,5,6,7,0,1,2],3,"@@TRACE2@@")==-1
