from common import *
CH='06-binary-search'
def run(a,ph):
    lo,hi=0,len(a)-1
    st=[{"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{},"note":f"Start with the whole array, indexes {lo} to {hi}. A peak exists inside it."}]
    while lo<hi:
        mid=lo+(hi-lo)//2; plo,phi=lo,hi
        if a[mid]<a[mid+1]:
            lo=mid+1; nt=f"The value {a[mid]} is smaller than {a[mid+1]}, so the data rises. A peak lies right of mid, and lo becomes {lo}."
        else:
            hi=mid; nt=f"The value {a[mid]} is larger than {a[mid+1]}, so the data falls. A peak lies at mid or left of it, and hi becomes {hi}."
        st.append({"at":{"lo":plo,"hi":phi,"mid":mid},"vars":{"nums[mid]":str(a[mid]),"nums[mid+1]":str(a[mid+1])},"note":nt})
    st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"peak value":str(a[lo])},"note":f"One index remains. Index {lo} is a peak with value {a[lo]}."})
    fill(CH,'05-peak-search.md',block(list(a),["lo","hi","mid"],st),ph); return lo
assert run([1,3,6,9,7,4,2],"@@TRACE1@@")==3
assert run([1,5,2,4,6,3,0],"@@TRACE2@@")==4
