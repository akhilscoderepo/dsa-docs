from common import *
CH='11-stacks-and-queues'; FILE='91-parse-with-a-stack.md'
def path_run(path):
    parts=[p for p in path.split("/") if p!=""]
    st=[]; steps=[]
    f=lambda: "["+", ".join(st)+"]"
    for i,p in enumerate(parts):
        if p==".": note="The component . names the current directory, so the stack stays the same."
        elif p=="..":
            if st: g=st.pop(); note=f"The component .. pops {g}, so the path moves to its parent."
            else: note="The component .. finds an empty stack, so it does nothing."
        else: st.append(p); note=f"The name {p} goes on the stack."
        steps.append({"at":{"i":i},"vars":{"stack":f()},"note":note})
    return "/"+"/".join(st),parts,steps
res,parts,st=path_run("/a/./b/../../c/"); assert res=="/c"
fill(CH,FILE,block(parts,["i"],st),"@@TRACE1@@")
def decode_run(s,limit):
    cur="";num=0;frames=[];steps=[]
    f=lambda: "["+", ".join(f'({k}, "{p}")' for k,p in frames)+"]"
    for i,c in enumerate(s):
        if c.isdigit(): num=num*10+int(c); note=f"The digit {c} makes num {num}."
        elif c=='[': frames.append((num,cur)); note=f"[ saves the count {num} and the parent text \"{cur}\", then starts an empty level."; cur="";num=0
        elif c==']':
            k,p=frames.pop(); new=len(p)+k*len(cur); assert new<=limit
            note=f"] computes the length {len(p)} + {k} * {len(cur)} = {new}, which is within the limit {limit}, then builds the text."
            cur=p+cur*k
        else: cur+=c; note=f"The letter {c} extends cur to \"{cur}\"."
        steps.append({"at":{"i":i},"vars":{"cur":f'"{cur}"',"num":num,"frames":f()},"note":note})
    return cur,steps
r,st=decode_run("2[a3[b]]",10); assert r=="abbbabbb"
fill(CH,FILE,block(list("2[a3[b]]"),["i"],st),"@@TRACE2@@")
# claims
assert path_run("/a/./b/../../c/")[0]=="/c" and path_run("/../...//x/")[0]=="/.../x"
n=100000; h=n//2; visits=sum(h-k+1 for k in range(h)); assert 1.0e9<visits<1.5e9, visits
assert abs(visits-n*n/8)<n*n/50
n=40; h=n//2; assert abs(sum(h-k+1 for k in range(h))-n*n/8)<n*n/8*0.3
assert 3*3*3*3*3==243 and 300**5>10**6
assert len("abbbabbbc")==9 and 2*3*3==18
assert 7-(10-(2+1))==0 and -(3+4)-5==-12
