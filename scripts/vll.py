import re,sys,glob
sys.argv=[sys.argv[0]]+sys.argv[1:]
exec(open('scripts/voice_lint.py').read().split('tot={}')[0].replace("args=sys.argv[1:]","args=[]"))
for f in sorted(glob.glob('dsa-skills/manuscripts/%s-*/*.md'%sys.argv[1])+glob.glob('dsa-skills/manuscripts/%s-*/solutions/*.md'%sys.argv[1])):
    t=re.sub(r'<!--.*?-->','',re.sub(r'```.*?```','',open(f).read(),flags=re.S),flags=re.S)
    for s in re.split(r'(?<=[.!?])\s+|\n',t):
        if s.startswith('#'):continue
        if len(s.split())>30 or PASS.search(s) or re.search(r'\bwill\b',s) or '->' in s or FILL.search(s): print(f.split('/')[-1],'|',s[:200])
