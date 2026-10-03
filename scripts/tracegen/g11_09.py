from common import *
CH='11-stacks-and-queues'
F='09-nested-decoding.md'
def run(s):
    counts=[];rows=[];cur="";count=0;st=[]
    for i,c in enumerate(s):
        if c.isdigit():
            count=count*10+int(c)
            note=f"The digit {c} is read, so the count becomes {count}."
        elif c=='[':
            counts.append(count); rows.append(cur)
            note=f"An opening bracket parks the row '{cur}' with the count {count}, then starts an empty row and a zero count."
            cur=""; count=0
        elif c==']':
            body=cur; k=counts.pop(); cur=rows.pop()+body*k
            note=f"A closing bracket repeats '{body}' {k} times and appends it to the parked row, so the current row becomes '{cur}'."
        else:
            cur+=c; note=f"The letter {c} is appended to the current row, which becomes '{cur}'."
        st.append({"at":{"i":i},"vars":{"count":count,"row":cur,"parked":str(rows).replace(' ','').replace("'",'')},"note":note})
    return st,cur
s="2[a3[b]]"; st,out=run(s); assert out=="abbbabbb"
assert "'b' 3 times and appends it to the parked row, so the current row becomes 'abbb'" in st[6]["note"]
fill(CH,F,block(list(s),["i"],st),"@@TRACE1@@")
s="12[ab]c"; st,out=run(s); assert out=="ab"*12+"c"
assert "count becomes 12" in st[1]["note"]
fill(CH,F,block(list(s),["i"],st),"@@TRACE2@@")
