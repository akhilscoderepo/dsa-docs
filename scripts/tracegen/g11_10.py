from common import *
CH='11-stacks-and-queues'
F='10-calculator-and-string-parsing.md'
s="3+2*4-6/2"
terms=[]; num=0; op='+'; st=[]
for i in range(len(s)+1):
    c=s[i] if i<len(s) else '+'
    if c.isdigit():
        num=num*10+int(c)
        note=f"The digit {c} is read, so the number in progress is {num}."
    else:
        if op=='+': terms.append(num); act=f"the pending plus pushes the term {num}"
        elif op=='-': terms.append(-num); act=f"the pending minus pushes the term {-num}"
        elif op=='*':
            t=terms.pop(); terms.append(t*num); act=f"the pending times replaces the top term {t} by {t*num}"
        else:
            t=terms.pop(); q=int(t/num); terms.append(q); act=f"the pending divide replaces the top term {t} by {q}"
        note=f"The character {c if i<len(s) else 'end of input'} commits the number {num}: {act}."
        op=c; num=0
    if i<len(s):
        st.append({"at":{"i":i},"vars":{"terms":str(terms).replace(' ',''),"op":op,"num":num},"note":note})
    else:
        st[-1]["note"]+= " The end of the tape then commits the last number the same way."
        st[-1]["vars"]["terms"]=str(terms).replace(' ','')
assert sum(terms)==8
# the final commit changed terms after the last char; rebuild last step for accuracy
fill(CH,F,block(list(s),["i"],st),"@@TRACE1@@")
s="1-(4+(2-3))"
saved=[]; result=0; num=0; sign=1; st=[]
for i,c in enumerate(s):
    if c.isdigit():
        num=num*10+int(c); note=f"The digit {c} is read, so the number in progress is {num}."
    elif c in '+-':
        result+=sign*num; note=f"The {c} commits the number {num} with its sign, so the level total is {result}, and the next sign is {c}."
        num=0; sign=1 if c=='+' else -1
    elif c=='(':
        saved.append((result,sign)); note=f"An opening bracket saves the total {result} and the sign {'+' if sign==1 else '-'}, then the inside restarts at zero."
        result=0; sign=1
    else:
        result+=sign*num; num=0; r,sg=saved.pop(); inner=result; result=r+sg*inner
        note=f"A closing bracket finishes the inside with value {inner}, and the saved total plus the saved sign times that value gives {result}."
    st.append({"at":{"i":i},"vars":{"result":result,"sign":sign,"saved":str(saved).replace(' ','')},"note":note})
assert result+sign*num==-2 or True
final=result+sign*num
assert final==-2, final
fill(CH,F,block(list(s),["i"],st),"@@TRACE2@@")
E=0
