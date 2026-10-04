from common import *
CH='06-binary-search'
def run(a,target,ph):
    lo,hi=0,len(a)-1
    st=[{"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"target":str(target)},"note":f"Start with the whole array as the search interval, indexes {lo} to {hi}."}]
    res=-1
    while lo<=hi:
        mid=lo+(hi-lo)//2
        v=a[mid]
        if v==target:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"nums[mid]":str(v),"target":str(target)},"note":f"The value {v} equals the target, so the search returns index {mid}."}); res=mid; break
        if v<target:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"nums[mid]":str(v),"target":str(target)},"note":f"The value {v} is smaller than {target}. Indexes {lo} to {mid} are discarded, so lo becomes {mid+1}."}); lo=mid+1
        else:
            st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"nums[mid]":str(v),"target":str(target)},"note":f"The value {v} is larger than {target}. Indexes {mid} to {hi} are discarded, so hi becomes {mid-1}."}); hi=mid-1
    if res==-1:
        st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"target":str(target)},"note":f"lo is {lo} and hi is {hi}, so the interval is empty. The target is absent and the method returns -1."})
    fill(CH,'01-exact-search.md',block(list(a),["lo","hi","mid"],st),ph); return res
assert run([-1,0,3,5,9,12],9,"@@TRACE1@@")==4
assert run([1,3],2,"@@TRACE2@@")==-1
