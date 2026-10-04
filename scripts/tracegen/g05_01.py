from common import *
CH='05-sorting-and-java-comparators'
def wrap(x): return (x+2**31)%2**32-2**31
def sub_cmp(a,b): return wrap(a-b)
def safe_cmp(a,b): return (a>b)-(a<b)
def run(vals, cmp, ph, label):
    a=list(vals); n=len(a)
    st=[{"at":{"i":0,"j":-1},"vars":{"array":str(a)},"note":"Start: the value at index 0 is a sorted prefix of length 1."}]
    for i in range(1,n):
        j=i
        while j>0:
            s=cmp(a[j-1],a[j]) if False else cmp(a[j],a[j-1])
            tag="negative" if s<0 else ("zero" if s==0 else "positive")
            if s<0:
                st.append({"at":{"i":i,"j":j-1},"vars":{"compare":f"{a[j]} vs {a[j-1]}","sign":tag,"array":str(a)},"note":f"The sign is {tag}, so {a[j]} goes before {a[j-1]}. Swap them."})
                a[j],a[j-1]=a[j-1],a[j]; j-=1
            else:
                st.append({"at":{"i":i,"j":j-1},"vars":{"compare":f"{a[j]} vs {a[j-1]}","sign":tag,"array":str(a)},"note":f"The sign is {tag}, so {a[j]} stays after {a[j-1]}. Stop this insertion."})
                break
        else:
            pass
    st.append({"at":{"i":n,"j":-1},"vars":{"array":str(a)},"note":label})
    fill(CH,'01-ordering-contracts.md',block(list(vals),["i","j"],st),ph); return a
V=[2000000000,5,-2000000000]
r1=run(V,sub_cmp,"@@TRACE1@@","The sort ends with the array "+str(sorted(V,key=lambda x:x))[:0]+"[5, 2000000000, -2000000000], which is not sorted.")
assert r1==[5,2000000000,-2000000000] and r1!=sorted(V)
r2=run(V,safe_cmp,"@@TRACE2@@","The sort ends with the array [-2000000000, 5, 2000000000], which is sorted.")
assert r2==sorted(V)
