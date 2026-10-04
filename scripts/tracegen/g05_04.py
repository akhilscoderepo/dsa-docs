from common import *
CH='05-sorting-and-java-comparators'; N='04-object-ordering.md'
def insertion(items,cmpfn,label,ph,ptr=("i","j")):
    a=list(items); cells=[label(x) for x in a]
    st=[{"at":{"i":0,"j":-1},"vars":{"order":str([label(x) for x in a])},"note":"Start: the first item forms a sorted prefix of length 1."}]
    for i in range(1,len(a)):
        j=i
        while j>0:
            s,why=cmpfn(a[j],a[j-1])
            if s<0:
                st.append({"at":{"i":i,"j":j-1},"vars":{"compare":f"{label(a[j])} vs {label(a[j-1])}","order":str([label(x) for x in a])},"note":f"{why} {label(a[j])} goes before {label(a[j-1])}. Swap them."})
                a[j],a[j-1]=a[j-1],a[j]; j-=1
            else:
                st.append({"at":{"i":i,"j":j-1},"vars":{"compare":f"{label(a[j])} vs {label(a[j-1])}","order":str([label(x) for x in a])},"note":f"{why} {label(a[j])} stays after {label(a[j-1])}. Stop this insertion."})
                break
    st.append({"at":{"i":len(a),"j":-1},"vars":{"order":str([label(x) for x in a])},"note":"The sort ends. Every adjacent pair follows the comparator."})
    fill(CH,N,block(cells,list(ptr),st),ph); return a
P=[("Ana",90),("Bo",85),("Cy",90),("Di",85)]
def cp(x,y):
    if x[1]!=y[1]: return (-1 if x[1]>y[1] else 1),f"The scores {x[1]} and {y[1]} differ, so the score decides."
    return (-1 if x[0]<y[0] else 1),f"The scores tie at {x[1]}, so the name decides."
r=insertion(P,cp,lambda p:f"{p[0]} {p[1]}","@@TRACE1@@")
assert [p[0] for p in r]==["Ana","Cy","Bo","Di"]
R=[[2,5],[1,3],[2,9]]
def cr(x,y):
    if x[0]!=y[0]: return (-1 if x[0]<y[0] else 1),f"The first columns {x[0]} and {y[0]} differ, so column 0 decides."
    return (-1 if x[1]>y[1] else 1),f"The first columns tie at {x[0]}, so column 1 decides in descending order."
r=insertion(R,cr,lambda p:str(p),"@@TRACE2@@")
assert r==[[1,3],[2,9],[2,5]]
