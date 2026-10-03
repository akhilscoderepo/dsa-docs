from common import *
CH='07-prefix-sums-and-difference-arrays'
F='05-earliest-balance.md'
def run(vals,labels):
    first={0:-1}; b=0; best=0; st=[]
    for i,v in enumerate(vals):
        b+=v
        if b in first:
            L=i-first[b]; best=max(best,L)
            st.append({"at":{"i":i},"vars":{"balance":b,"earliest":first[b],"length":L,"best":best},"note":f"The balance is {b}, first reached at index {first[b]}, so the stretch has length {L} and the best is {best}."})
        else:
            first[b]=i
            st.append({"at":{"i":i},"vars":{"balance":b,"best":best},"note":f"The balance {b} is new, so record index {i} as its first position. The best stays {best}."})
    return st,best
a=[0,1,0,0,1,1,0]
st,best=run([1 if x==1 else -1 for x in a],a)
assert best==6 and st[5]["vars"]["length"]==6 and st[5]["vars"]["earliest"]==-1
fill(CH,F,block([str(x) for x in a],["i"],st),"@@TRACE1@@")
s="ABxxBAxA"
st,best=run([1 if c=='A' else -1 if c=='B' else 0 for c in s],s)
assert best==7 and st[3]["vars"]["balance"]==0 and st[3]["vars"]["length"]==4
fill(CH,F,block(list(s),["i"],st),"@@TRACE2@@")
