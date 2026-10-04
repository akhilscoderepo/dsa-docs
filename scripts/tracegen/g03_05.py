from common import *
CH='03-strings'; F='05-fixed-alphabet-counts.md'
def run(s):
    t=[0]*26; st=[{"at":{"i":-1},"vars":{},"note":"Start: every entry of the table is 0."}]
    for i,c in enumerate(s):
        t[ord(c)-97]+=1
        v={chr(97+k):t[k] for k in range(26) if t[k]}
        st.append({"at":{"i":i},"vars":v,"note":f"Index {i} holds '{c}', so the entry of {c} rises to {t[ord(c)-97]}."})
    best=0
    for k in range(1,26):
        if t[k]>t[best]: best=k
    ans=chr(97+best)
    st.append({"at":{"i":len(s)},"vars":{chr(97+k):t[k] for k in range(26) if t[k]},"note":f"The loop ends. The scan over the table keeps the first largest entry, so the answer is '{ans}'."})
    return st,ans
for ph,s,exp in (("@@TRACE1@@","banana","a"),("@@TRACE2@@","cabab","a")):
    st,a=run(s); assert a==exp
    assert a==min(sorted(set(s)),key=lambda ch:(-s.count(ch),ch))
    fill(CH,F,block(list(s),["i"],st),ph)
