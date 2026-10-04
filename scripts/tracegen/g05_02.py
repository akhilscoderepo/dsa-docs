from common import *
CH='05-sorting-and-java-comparators'
N='02-arrays-sort.md'
a=[9,2,7,2]; c=sorted(a)
st=[{"at":{"i":-1},"vars":{"nums":str(a),"copy":str(a)},"note":"The method copies nums. Both arrays hold 9, 2, 7, 2."},
    {"at":{"i":-1},"vars":{"nums":str(a),"copy":str(c)},"note":"The library sort orders the copy. The array nums keeps its order."}]
for i in range(1,len(c)):
    rel="equal, so equal values are adjacent" if c[i-1]==c[i] else "smaller, so the order holds"
    st.append({"at":{"i":i},"vars":{"left":c[i-1],"right":c[i],"copy":str(c)},"note":f"Compare {c[i-1]} with {c[i]}: the left value is {rel}." if c[i-1]!=c[i] else f"Compare {c[i-1]} with {c[i]}: the values are equal, so the equal values form one run."})
fill(CH,N,block(c,["i"],st),"@@TRACE1@@")
b=[8,6,4,2,0]; lo,hi=1,4
r=b[:]; r[lo:hi]=sorted(r[lo:hi]); assert r==[8,2,4,6,0]
st=[{"at":{"lo":lo,"hi":hi},"vars":{"array":str(b)},"note":"The call covers indexes 1, 2 and 3. Index 4 is the excluded end."},
    {"at":{"lo":lo,"hi":hi},"vars":{"range":str(b[lo:hi]),"array":str(b)},"note":"The range holds 6, 4, 2 before the sort."},
    {"at":{"lo":lo,"hi":hi},"vars":{"range":str(r[lo:hi]),"array":str(r)},"note":"The range holds 2, 4, 6 after the sort. The values 8 and 0 stay in place."}]
fill(CH,N,block(b,["lo","hi"],st),"@@TRACE2@@")
