from common import *
CH='06-binary-search'
def run(flags,ph):
    n=len(flags); lo,hi=0,n
    st=[{"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"interval":f"[{lo}, {hi})"},"note":f"The half-open interval covers builds {lo} to {hi-1}. The value {hi} stands for no failing build."}]
    while lo<hi:
        mid=lo+(hi-lo)//2; plo,phi=lo,hi
        if flags[mid]:
            hi=mid; nt=f"Build {mid} fails, so it may be the first failing build. hi becomes {hi}."
        else:
            lo=mid+1; nt=f"Build {mid} passes, so every earlier build passes too. lo becomes {lo}."
        st.append({"at":{"lo":plo,"hi":phi,"mid":mid},"vars":{"fails":str(bool(flags[mid])).lower(),"interval":f"[{lo}, {hi})"},"note":nt})
    st.append({"at":{"lo":lo,"hi":hi,"mid":-1},"vars":{"interval":f"[{lo}, {hi})"},"note":f"The interval is empty, so the search returns {lo}."+(" That value equals the number of builds, so no build fails." if lo==n else "")})
    fill(CH,'04-first-true.md',block(list(flags),["lo","hi","mid"],st),ph); return lo
assert run([0,0,0,1,1,1,1,1],"@@TRACE1@@")==3
assert run([0,0,0,0,0],"@@TRACE2@@")==5
