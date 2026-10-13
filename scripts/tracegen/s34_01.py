from common import *
CH='34-advanced-strings'; F='01-rolling-hash.md'
B=27
def code(c): return ord(c)-96
def run(s,k,M):
    """Simulate the rolling scan; return steps and the repeat start (or -1)."""
    power=pow(B,k-1,M); h=0; seen={}; st=[]; res=-1
    for end,ch in enumerate(s):
        vars_={}
        if end>=k:
            out=code(s[end-k]); raw=h-out*power
            h=raw%M  # Python % is non-negative; equals the Java fix-up
            vars_["out"]=out; vars_["raw"]=raw
        h=(h*B+code(ch))%M
        if end<k-1: continue
        start=end-k+1; w=s[start:end+1]
        vars_.update({"window":w,"hash":h})
        direct=0
        for c in w: direct=(direct*B+code(c))%M
        assert direct==h
        note=f"end = {end}: window {w} has hash {h}."
        if end>=k:
            note=f"end = {end}: removing {s[end-k]} leaves {vars_['raw']}"+(f", which is negative, so adding {M} gives {vars_['raw']%M}" if vars_['raw']<0 else "")+f". The window {w} then has hash {h}."
        if h in seen:
            ok=[o for o in seen[h] if s[o:o+k]==w]
            if ok:
                res=start; vars_["check"]="equal"
                note+=f" The table holds start {seen[h][0]} for this hash, and all {k} letters agree, so the repeat is real."
                st.append({"at":{"end":end},"vars":vars_,"note":note}); break
            vars_["check"]="differ"
            note+=f" The table holds start {seen[h][0]} for this hash, but {s[seen[h][0]:seen[h][0]+k]} differs from {w}, so the check rejects the match."
        else: vars_["check"]="-"
        seen.setdefault(h,[]).append(start)
        st.append({"at":{"end":end},"vars":vars_,"note":note})
    return st,res
s="abcdabc"; st,res=run(s,3,10**9+7); assert res==4 and len(st)>=3
assert [x["vars"]["hash"] for x in st]==[786,1543,2296,2945,786]
fill(CH,F,block(list(s),["end"],st),"@@TRACE1@@")
s="abbcde"; st,res=run(s,3,101); assert res==-1 and len(st)==4
assert [x["vars"]["hash"] for x in st]==[78,0,28,78] and st[-1]["vars"]["check"]=="differ"
fill(CH,F,block(list(s),["end"],st),"@@TRACE2@@")
