from common import *
CH='19-recursion-and-backtracking'; F='09-partition-generation.md'
def run(s, rule, label):
    path=[]; res=[]; steps=[]
    def cut(start):
        if start==len(s):
            res.append(list(path))
            steps.append({"at":{"start":start,"end":-1},"vars":{"path":str(path),"recorded":len(res)},"note":f"The start has reached {len(s)}, so nothing is left uncut and a copy of {path} is recorded as partition {len(res)}."})
            return
        fit=False
        for end in range(start+1,len(s)+1):
            bow=s[start:end]
            if not rule(bow): continue
            fit=True
            path.append(bow)
            steps.append({"at":{"start":start,"end":end},"vars":{"path":str(path),"recorded":len(res)},"note":f"The bow {bow} runs from {start} to {end} and is accepted, so the path is {path} and the next call starts at {end}."})
            cut(end)
            path.pop()
            steps.append({"at":{"start":start,"end":end},"vars":{"path":str(path) if path else "empty","recorded":len(res)},"note":f"The bow {bow} is taken off again, so the path is {path if path else 'empty'}."})
        if not fit:
            steps.append({"at":{"start":start,"end":-1},"vars":{"path":str(path),"recorded":len(res)},"note":f"The start is {start} with {len(s)-start} letters left and no acceptable bow can be cut from them, so the call returns without recording anything."})
    cut(0)
    return res,steps
res,steps=run("abc",lambda b:True,"all")
assert res==[["a","b","c"],["a","bc"],["ab","c"],["abc"]]
fill(CH,F,block(list("abc"),["start","end"],steps),"@@TRACE1@@")
res,steps=run("abcde",lambda b:len(b) in (2,3),"len")
assert res==[["ab","cde"],["abc","de"]]
fill(CH,F,block(list("abcde"),["start","end"],steps),"@@TRACE2@@")
