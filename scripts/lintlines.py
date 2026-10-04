import re,sys
PASS=re.compile(r'\b(is|are|was|were|be|been|being)\s+(\w+ed|shown|given|made|written|kept|known|seen|chosen|taken|built|held|run|done)\b',re.I)
for f in sys.argv[1:]:
    raw=open(f).read(); txt=re.sub(r'```.*?```','',raw,flags=re.S); txt=re.sub(r'<!--.*?-->','',txt,flags=re.S)
    for ln in txt.split('\n'):
        if ln.startswith('#'): continue
        for s in re.split(r'(?<=[.!?])\s+',ln):
            if len(s.split())>30 or '->' in s or PASS.search(s) or re.search(r'\bwill\b',s,re.I): print(f.split('/')[-1],'|',s[:200])
