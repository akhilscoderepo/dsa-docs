# usage: retrace.py file  -> resets filled trace blocks to @@TRACE1@@, @@TRACE2@@ ... so a generator can run again
import re,sys
p=sys.argv[1]; t=open(p).read(); k=[0]
def r(m):
    k[0]+=1; return f"@@TRACE{k[0]}@@"
t=re.sub(r"```trace\n.*?\n```",r,t,flags=re.S); open(p,'w').write(t); print(k[0],"traces reset")
