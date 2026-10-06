from common import *
CH='11-stacks-and-queues'; FILE='10-calculator-and-string-parsing.md'
def tdiv(a,b):
    q=abs(a)//abs(b); return q if (a<0)==(b<0) else -q
def terms_run(s):
    terms=[]; num=0; op='+'; steps=[]
    f=lambda: "["+", ".join(map(str,terms))+"]"
    for i in range(len(s)+1):
        c=s[i] if i<len(s) else '+'
        if c.isdigit():
            num=num*10+int(c); note=f"The digit {c} makes num {num}."
        elif c==' ':
            note="The space changes nothing."
        else:
            n=num
            if op=='+': terms.append(n); act=f"pushes {n}"
            elif op=='-': terms.append(-n); act=f"pushes {-n}"
            elif op=='*': a=terms.pop(); terms.append(a*n); act=f"multiplies the top term {a} by {n}"
            else: a=terms.pop(); terms.append(tdiv(a,n)); act=f"divides the top term {a} by {n}"
            who=f"{c} ends the number {n}." if i<len(s) else f"The end of the text ends the number {n}."
            note=f"{who} The pending operator {op} {act}."
            if i<len(s): note+=f" Now {c} is pending."
            op=c; num=0
        steps.append({"at":{"i":i},"vars":{"num":num,"op":op,"terms":f()},"note":note})
    return sum(terms),steps
def groups_run(s):
    saved=[]; result=0; sign=1; num=0; steps=[]
    f=lambda: "["+", ".join(f"({r}, {g})" for r,g in saved)+"]"
    for i,c in enumerate(s):
        if c.isdigit():
            num=num*10+int(c); note=f"The digit {c} makes num {num}."
        elif c in '+-':
            result+=sign*num; note=f"{c} adds {sign*num} to result, which is now {result}."; num=0; sign=1 if c=='+' else -1
        elif c=='(':
            saved.append((result,sign)); note=f"( saves result {result} and sign {sign}, then starts a fresh group."; result=0; sign=1
        else:
            result+=sign*num; num=0; r,g=saved.pop(); inner=result; result=inner*g+r
            note=f") finishes the inner result {inner}, multiplies it by the saved sign {g} and adds the saved result {r}, so result is {result}."
        steps.append({"at":{"i":i},"vars":{"num":num,"sign":sign,"result":result,"saved":f()},"note":note})
    result+=sign*num
    steps.append({"at":{"i":len(s)},"vars":{"num":0,"sign":sign,"result":result,"saved":"[]"},"note":f"The end of the text adds the last number, so the answer is {result}."})
    assert not saved
    return result,steps
v,st=terms_run("7 + 12*3 - 20/4"); assert v==38
fill(CH,FILE,block(list("7 + 12*3 - 20/4"),["i"],st),"@@TRACE1@@")
v,st=groups_run("20-(4-(3+2))+1"); assert v==22
fill(CH,FILE,block(list("20-(4-(3+2))+1"),["i"],st),"@@TRACE2@@")
# examples and claims
assert terms_run("8 - 3*4 + 10/3")[0]==-1 and terms_run(" 100/7/2")[0]==7 and 100//(7//2)==33
assert 7+12*3==43 and (7+12)*3==57
assert eval("120+35-8")==147 and eval("10-4-3-2")==1
assert groups_run("(1+(4-12))-(3-5)")[0]==-5 and groups_run("-(2+3)-(-4)")[0]==-1
assert eval("-4+10- -3")==9 and eval("5- - -2")==3
def moves(m):
    t=["1"]+["*","1"]*m; mv=0
    i=1
    while i<len(t):
        a=int(t[i-1]);b=int(t[i+1]); t[i-1]=str(a*b)
        for _ in range(2):
            mv+=len(t)-i-1; del t[i]
    return mv
for m in range(1,25): assert moves(m)==2*m*m-m,(m,moves(m))
assert 2*50000**2-50000==4999950000
