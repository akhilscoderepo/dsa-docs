from common import *
CH='05-sorting-and-java-comparators'; N='03-comparator-contracts.md'
names=["bb","a","cc"]
def bad(a,b): return -1 if len(a)<len(b) else 1
def good(a,b): return (len(a)>len(b))-(len(a)<len(b))
def run(cmp,ph,tail):
    st=[]
    for i in range(3):
        for j in range(i+1,3):
            x,y=names[i],names[j]; p,q=cmp(x,y),cmp(y,x)
            if p==q:
                note=f'Both orders return {p}. '+("Each name claims to go second, which is a contradiction." if p==1 else "The two names are interchangeable by length.")
            else:
                note=f'The answers {p} and {q} mirror each other, so the order is clear.'
            st.append({"at":{"i":i,"j":j},"vars":{"first":f'compare("{x}", "{y}") = {p}',"second":f'compare("{y}", "{x}") = {q}'},"note":note})
    st.append({"at":{"i":3,"j":-1},"vars":{},"note":tail})
    fill(CH,N,block(names,["i","j"],st),ph)
run(bad,"@@TRACE1@@","One pair contradicts itself, so the rule is not a valid comparator.")
run(good,"@@TRACE2@@","Every pair mirrors or ties, so the rule is a valid comparator.")
