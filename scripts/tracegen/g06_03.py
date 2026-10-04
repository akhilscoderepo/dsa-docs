from common import *
CH='06-binary-search'
def run(a,target,upper,ph):
    lo,hi=0,len(a)
    op="<=" if upper else "<"
    st=[{"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"target":str(target),"interval":f"[{lo}, {hi})"},"note":f"The half-open interval covers indexes {lo} to {hi-1} and also allows the answer {hi}."}]
    while lo<hi:
        mid=lo+(hi-lo)//2; v=a[mid]; plo,phi=lo,hi
        keep=(v<=target) if upper else (v<target)
        if keep:
            lo=mid+1; nt=f"The test nums[mid] {op} {target} holds for {v}, so index {mid} is on the left part. lo becomes {lo}."
        else:
            hi=mid; nt=f"The test nums[mid] {op} {target} fails for {v}, so index {mid} may be the answer. hi becomes {hi}."
        st.append({"at":{"lo":plo,"hi":phi,"mid":mid},"vars":{"nums[mid]":str(v),"interval":f"[{lo}, {hi})"},"note":nt})
    st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"interval":f"[{lo}, {hi})"},"note":f"The interval is empty, so the answer is index {lo}."})
    fill(CH,'03-lower-and-upper-bounds.md',block(list(a),["lo","hi","mid"],st),ph); return lo
import bisect
assert run([1,3,5,5,8],5,False,"@@TRACE1@@")==bisect.bisect_left([1,3,5,5,8],5)==2
assert run([2,4,4,4,9,9],4,True,"@@TRACE2@@")==bisect.bisect_right([2,4,4,4,9,9],4)==4
