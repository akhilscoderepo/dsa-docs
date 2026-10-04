from common import *
CH='06-binary-search'
def run(a,target,first,ph):
    lo,hi,c=0,len(a)-1,-1
    side="left" if first else "right"
    st=[{"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"target":str(target),"candidate":"-1"},"note":"Start with the whole array as the search interval. No candidate exists yet."}]
    while lo<=hi:
        mid=lo+(hi-lo)//2; v=a[mid]; plo,phi=lo,hi
        if v==target:
            c=mid
            if first: hi=mid-1; nt=f"The value {v} equals the target. Store candidate {mid} and keep only the left side, so hi becomes {hi}."
            else: lo=mid+1; nt=f"The value {v} equals the target. Store candidate {mid} and keep only the right side, so lo becomes {lo}."
        elif v<target:
            lo=mid+1; nt=f"The value {v} is smaller than {target}, so lo becomes {lo}."
        else:
            hi=mid-1; nt=f"The value {v} is larger than {target}, so hi becomes {hi}."
        st.append({"at":{"lo":plo,"hi":phi,"mid":mid},"vars":{"nums[mid]":str(v),"candidate":str(c)},"note":nt})
    st.append({"at":{"lo":min(lo,len(a)),"hi":hi,"mid":-1},"vars":{"candidate":str(c)},"note":f"The interval is empty, so the search returns candidate {c}."})
    fill(CH,'02-first-and-last.md',block(list(a),["lo","hi","mid"],st),ph); return c
assert run([5,7,7,7,7,9],7,True,"@@TRACE1@@")==1
assert run([4,7,7,7,9,9,9],7,False,"@@TRACE2@@")==3
