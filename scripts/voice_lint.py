#!/usr/bin/env python3
"""Advisory voice lint. Usage: voice_lint.py [NN ...]  (no args = all chapters).
Flags: sentences over 30 words, 'will', '->' in prose, passive-voice guesses, filler nouns, banned jargon."""
import re,sys,glob
args=sys.argv[1:]
dirs=sorted(glob.glob('dsa-skills/manuscripts/*/'))
if args: dirs=[d for d in dirs if any(d.split('/')[-2].startswith(a+'-') for a in args)]
PASS=re.compile(r'\b(is|are|was|were|be|been|being)\s+(\w+ed|shown|given|made|written|kept|known|seen|chosen|taken|built|held|run|done)\b',re.I)
FILL=re.compile(r'\b(the process|the situation|the aspect|the component)\b',re.I)
JARGON=re.compile(r'\b(hostile (test|input|dry run)s?)\b',re.I)
tot={}
for d in dirs:
    n={}
    for f in sorted(glob.glob(d+'*.md')+glob.glob(d+'solutions/*.md')):
        txt=re.sub(r'```.*?```','',open(f).read(),flags=re.S)
        txt=re.sub(r'<!--.*?-->','',txt,flags=re.S)
        for ln in txt.split('\n'):
            if ln.startswith('#') or ln.lstrip().startswith(('|','-','*','>')) and False: continue
            for s in re.split(r'(?<=[.!?])\s+',ln):
                w=len(s.split())
                for k,c in (('long',w>30),('will',bool(re.search(r'\bwill\b',s,re.I))),('arrow','->' in s),('passive',bool(PASS.search(s))),('filler',bool(FILL.search(s))),('jargon',bool(JARGON.search(s)))):
                    if c: n[k]=n.get(k,0)+1
    print(d.split('/')[-2],n)
