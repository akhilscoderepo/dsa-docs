from common import *
CH='06-binary-search'
def search(cells,ok,unit,ph,expect,fmt):
    lo,hi=0,len(cells)-1
    st=[{"at":{"lo":0,"hi":hi,"mid":-1},"vars":{},"note":f"Start with every candidate, {unit} {cells[0]} to {cells[-1]}."}]
    while lo<hi:
        mid=lo+(hi-lo)//2
        r,detail=ok(cells[mid])
        if r: hi=mid; note=f"{fmt} {cells[mid]} {detail} and passes, so hi moves to {cells[mid]}."
        else: lo=mid+1; note=f"{fmt} {cells[mid]} {detail} and fails, so lo moves to {cells[lo]}."
        st.append({"at":{"lo":lo,"hi":hi,"mid":mid},"vars":{"candidate":str(cells[mid]),"passes":"yes" if r else "no"},"note":note})
    assert cells[lo]==expect
    st.append({"at":{"lo":lo,"hi":hi,"mid":lo},"vars":{"answer":str(cells[lo])},"note":f"The range holds one candidate, {cells[lo]}, so the search returns it."})
    fill(CH,'08-integer-answers.md',block(cells,["lo","hi","mid"],st),ph)
P=[5,9,14,20]
def ok1(k):
    h=sum(-(-x//k) for x in P); return h<=9,f"needs {h} hours"
search(list(range(1,21)),ok1,"speeds","@@TRACE1@@",7,"Speed")
W=[4,2,7,1,5,3]
def ok2(c):
    d=1;l=0
    for x in W:
        if l+x>c:d+=1;l=0
        l+=x
    return d<=3,f"needs {d} days"
search(list(range(7,27)),ok2,"capacities","@@TRACE2@@",8,"Capacity")
