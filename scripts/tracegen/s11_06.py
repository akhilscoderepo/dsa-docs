from common import *
CH='11-stacks-and-queues'; FILE='06-nested-structure.md'
def direct(s):
    saved=[];out=[];cur=0;steps=[]
    f=lambda d:"["+", ".join(map(str,d))+"]"
    for i,c in enumerate(s):
        if c=='(':
            saved.append(cur); cur=0
            note="( pushes the partial sum of the level around it and starts a new level at 0."
        elif c==')':
            out.append(cur); cur=saved.pop()
            note=f") records {out[-1]} as the finished sum and restores the saved partial sum {cur}."
        else:
            cur+=int(c); note=f"The digit {c} adds to the current level, so the partial sum becomes {cur}."
        steps.append({"at":{"i":i},"vars":{"cur":cur,"saved":f(saved),"out":f(out)},"note":note})
    assert not saved
    return out,steps
def run(s,ph,exp):
    out,steps=direct(s); assert out==exp,out
    steps.append({"at":{"i":len(s)},"vars":{"cur":0,"saved":"[]","out":"["+", ".join(map(str,out))+"]"},"note":"The text ends with an empty saved stack, and out holds the answer."})
    fill(CH,FILE,block(list(s),["i"],steps),ph)
run("(3(15)2(4))","@@TRACE1@@",[6,4,5])
run("(2(4(6))5)","@@TRACE2@@",[6,4,11-4+0] if False else [6,4,7])
# predict claim: reads by findClose on chain of k groups equals 2k^2
def reads(k):
    s="("*k+")"*k; n=0
    def fc(o):
        nonlocal n
        d=0
        for j in range(o,len(s)):
            n+=1
            if s[j]=='(':d+=1
            elif s[j]==')':
                d-=1
                if d==0:return j
    for i in range(len(s)):
        if s[i]!='(':continue
        c=fc(i); k2=i+1
        while k2<c:
            if s[k2]=='(':k2=fc(k2)
            k2+=1
    return n
for k in range(1,15): assert reads(k)==2*k*k,(k,reads(k))
assert 2*50000**2==5_000_000_000
def incl(s):
    st=[];cur=0;out=[]
    for c in s:
        if c=='(':st.append(cur);cur=0
        elif c==')':out.append(cur);cur+=st.pop()
        else:cur+=int(c)
    return out
assert incl("(1(29)4)")==[11,16] and incl("7(3)(48)2")==[3,12]
def depth(s):
    d=m=0
    for c in s:
        d+=1 if c=='(' else -1;m=max(m,d)
    return m
assert depth("(()(()))")==3 and depth("()()()")==1
def height(s):
    st=[];cur=0
    for c in s:
        if c=='(':st.append(cur);cur=0
        else:
            if not st:return -1
            cur=max(st.pop(),cur+1)
    return -1 if st else cur
assert height("((((()))))")==5 and height(")(")==-1 and height("(()")==-1
def score(s):
    st=[];cur=0
    for c in s:
        if c=='(':st.append(cur);cur=0
        else:cur=st.pop()+max(2*cur,1)
    return cur
assert score("((()()))")==8 and score("()(())()")==4
