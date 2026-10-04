from common import *
CH='05-sorting-and-java-comparators'; N='05-stability-and-ties.md'
T=["A2","B2","C1"]; pr=lambda s:int(s[1:])
a=list(T); st=[{"at":{"i":0,"j":-1},"vars":{"order":str(a)},"note":"Start: the scan looks for the smallest priority from index 0."}]
for i in range(len(a)-1):
    sm=i
    for j in range(i+1,len(a)):
        smaller=pr(a[j])<pr(a[sm])
        st.append({"at":{"i":i,"j":j},"vars":{"smallest":a[sm],"order":str(a)},"note":(f"{a[j]} has a smaller priority than {a[sm]}, so it becomes the smallest." if smaller else f"{a[j]} is not smaller than {a[sm]}, so the smallest stays {a[sm]}.")})
        if smaller: sm=j
    if sm!=i:
        a[i],a[sm]=a[sm],a[i]
        st.append({"at":{"i":i,"j":sm},"vars":{"order":str(a)},"note":f"Swap index {i} with index {sm}. The array is now {a}."})
st.append({"at":{"i":3,"j":-1},"vars":{"order":str(a)},"note":"The sort ends. B2 now comes before A2, so the tie order changed."})
assert a==["C1","B2","A2"]
fill(CH,N,block(T,["i","j"],st),"@@TRACE1@@")
a=list(T); st=[{"at":{"i":0,"j":-1},"vars":{"order":str(a)},"note":"Start: the first ticket forms a sorted prefix of length 1."}]
for i in range(1,len(a)):
    j=i
    while j>0:
        if pr(a[j])<pr(a[j-1]):
            st.append({"at":{"i":i,"j":j-1},"vars":{"order":str(a)},"note":f"{a[j]} has a strictly smaller priority than {a[j-1]}. Move it left."})
            a[j],a[j-1]=a[j-1],a[j]; j-=1
        else:
            st.append({"at":{"i":i,"j":j-1},"vars":{"order":str(a)},"note":f"{a[j]} is not strictly smaller than {a[j-1]}. It stays, so a tie keeps its order."})
            break
st.append({"at":{"i":3,"j":-1},"vars":{"order":str(a)},"note":"The sort ends. A2 still comes before B2."})
assert a==["C1","A2","B2"]
fill(CH,N,block(T,["i","j"],st),"@@TRACE2@@")
