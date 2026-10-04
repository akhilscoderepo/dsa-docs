from common import *
CH='06-binary-search'
def run(a,ph):
    lo,hi=0,len(a)-1
    st=[{"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{},"note":f"Start with the whole array, indexes {lo} to {hi}. The pivot lies inside it."}]
    while lo<hi:
        mid=lo+(hi-lo)//2; plo,phi=lo,hi
        if a[mid]>a[hi]:
            lo=mid+1; nt=f"The value {a[mid]} is larger than the right endpoint {a[phi]}, so mid is in the high run. The pivot lies right of mid, and lo becomes {lo}."
        else:
            hi=mid; nt=f"The value {a[mid]} is not larger than the right endpoint {a[phi]}, so the pivot is at mid or left of it. hi becomes {hi}."
        st.append({"at":{"lo":plo,"hi":phi,"mid":mid},"vars":{"nums[mid]":str(a[mid]),"nums[hi]":str(a[phi])},"note":nt})
    st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"minimum":str(a[lo])},"note":f"One index remains. The pivot is index {lo}, and the minimum is {a[lo]}."})
    fill(CH,'06-rotated-minimum.md',block(list(a),["lo","hi","mid"],st),ph); return lo
assert run([3,4,5,1,2],"@@TRACE1@@")==3
assert run([2,4,6,8,10],"@@TRACE2@@")==0
