from common import *
CH = '37-iterators-encodings-and-versioned-state'
NAME = '01-iterator-protocols.md'

def token_trace():
    toks = ["let", "x", "=", "5"]
    pos = 0
    st = [{"at": {"pos": 0}, "vars": {"call": "new", "result": "none"}, "note": "Start: pos is 0, so the first token is next."}]
    def log(call, res, note):
        st.append({"at": {"pos": pos}, "vars": {"call": call, "result": res}, "note": note})
    def peek():
        if pos == len(toks): raise IndexError
        return toks[pos]
    r = peek(); log("peek()", r, "peek returns let and leaves pos at 0.")
    r = peek(); log("peek()", r, "A second peek returns let again, because observation does not move pos.")
    r = peek(); pos += 1; log("next()", r, "next returns let and moves pos to 1.")
    for t in ["x", "=", "5"]:
        r = peek(); assert r == t; pos += 1
        log("next()", r, f"next returns {r} and moves pos to {pos}.")
    assert pos == len(toks)
    log("hasNext()", "false", "pos equals the number of tokens, so hasNext returns false and changes nothing.")
    try:
        peek(); raise AssertionError
    except IndexError:
        pass
    log("next()", "throws", "The cursor lies past the last token, so next throws NoSuchElementException and pos stays at 4.")
    return block(toks, ["pos"], st)

def run_trace():
    syms = ["a", "b", "c"]; counts = [2, 0, 1]
    run = 0; used = 0
    st = [{"at": {"run": 0}, "vars": {"used": 0, "call": "new", "result": "none"}, "note": "Start: run 0 holds the next element and nothing is used."}]
    def settle():
        nonlocal run, used
        while run < len(counts) and used == counts[run]:
            run += 1; used = 0
    def nxt():
        nonlocal used
        settle(); assert run < len(counts); used += 1; return syms[run]
    out = []
    r = nxt(); out.append(r)
    st.append({"at": {"run": run}, "vars": {"used": used, "call": "next()", "result": r}, "note": "next returns a and raises used to 1."})
    r = nxt(); out.append(r)
    st.append({"at": {"run": run}, "vars": {"used": used, "call": "next()", "result": r}, "note": "next returns a and raises used to 2. Run 0 is now used up, but no call has asked for more yet, so run stays 0."})
    r = nxt(); out.append(r)
    st.append({"at": {"run": run}, "vars": {"used": used, "call": "next()", "result": r}, "note": "next passes the used-up run 0 and the empty run 1, lands on run 2 and returns c with used 1."})
    settle(); has = run < len(counts)
    st.append({"at": {"run": run}, "vars": {"used": used, "call": "hasNext()", "result": str(has).lower()}, "note": "hasNext passes the used-up run 2 and reaches run 3, one past the last run, so it returns false."})
    assert out == ["a", "a", "c"] and not has
    return block(["a x2", "b x0", "c x1"], ["run"], st)

fill(CH, NAME, token_trace(), "@@TRACE1@@")
fill(CH, NAME, run_trace(), "@@TRACE2@@")
