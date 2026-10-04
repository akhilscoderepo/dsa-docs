import sys,json
# usage: rep.py file <<< json list of [old,new]; applies to file, error if missing
f=sys.argv[1]; t=open(f).read()
for a,b in json.load(sys.stdin):
    assert t.count(a)==1,("count",t.count(a),a[:40]); t=t.replace(a,b)
open(f,'w').write(t)
