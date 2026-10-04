import re,sys
exec(open('scripts/voice_lint.py').read().split('def stage_check')[0].split('args=sys.argv')[0])
PASS=re.compile(r'\b(is|are|was|were|be|been|being)\s+(\w+ed|shown|given|made|written|kept|known|seen|chosen|taken|built|held|run|done)\b',re.I)
for f in sys.argv[1:]:
    txt=re.sub(r'<!--.*?-->','',re.sub(r'```.*?```','',open(f).read(),flags=re.S),flags=re.S)
    for ln in txt.split('\n'):
        if ln.startswith('#'): continue
        for s in re.split(r'(?<=[.!?])\s+',ln):
            if len(s.split())>25 or PASS.search(s) or re.search(r'\bwill\b|->',s): print(f.split('/')[-1][:12],len(s.split()),s[:160])
