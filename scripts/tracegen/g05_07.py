from common import *
CH='05-sorting-and-java-comparators'; N='07-sort-and-deduplicate.md'
def run(feed,ph,tail,detail):
    s=sorted(feed); n=len(s); i=0; rep=[]
    st=[{"at":{"i":0,"j":0},"vars":{"report":"[]"},"note":"Start: the first run begins at index 0."}]
    while i<n:
        j=i
        while j<n and s[j]==s[i]:
            j+=1
            if detail: st.append({"at":{"i":i,"j":min(j,n)},"vars":{"value":s[i],"report":str(rep)},"note":f"Index {j-1} holds {s[i]}, so the run extends. The end index moves to {j}."})
        rep.append((s[i],j-i))
        st.append({"at":{"i":i,"j":j},"vars":{"value":s[i],"report":str(rep)},"note":f"The run of {s[i]} spans indexes {i} to {j-1}, so the length is {j-i}. Emit ({s[i]}, {j-i}) and continue at index {j}."})
        i=j
    st.append({"at":{"i":n,"j":n},"vars":{"report":str(rep)},"note":tail})
    fill(CH,N,block(s,["i","j"],st),ph); return rep
assert run([4,7,4,9,7,4],"@@TRACE1@@","The loop ends because i reaches the array length. The report holds three pairs.",False)==[(4,3),(7,2),(9,1)]
assert run([4,4,4],"@@TRACE2@@","The loop ends because i reaches the array length. The single run was emitted without a later value.",True)==[(4,3)]
