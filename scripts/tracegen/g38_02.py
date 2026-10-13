from common import *
CH = '38-streaming-and-temporal-state'
NAME = '02-expiring-state.md'

def logger_trace():
    gap = 10
    calls = [(1, "a"), (3, "b"), (8, "a"), (11, "a"), (11, "b"), (13, "b")]
    expect = [True, True, False, True, False, True]
    dl = {}
    st = []
    for i, (now, text) in enumerate(calls):
        d = dl.get(text)
        if d is not None and now < d:
            ok = False
            note = f"Text {text} has deadline {d} and {now} is below it, so the call is blocked and the map is unchanged."
        else:
            ok = True
            note = (f"Text {text} has no deadline, so the call prints and stores {now + gap}." if d is None
                    else f"Text {text} has deadline {d} and {now} is not below it, so the call prints and stores {now + gap}.")
            dl[text] = now + gap
        assert ok == expect[i]
        st.append({"at": {"i": i}, "vars": {"now": now, "text": text, "printed": str(ok).lower(),
                   "deadlines": ", ".join(f"{k}={v}" for k, v in sorted(dl.items()))}, "note": note})
    return block([f"{t}:{x}" for t, x in calls], ["i"], st)

def auth_trace():
    ttl = 5
    exp = {}   # insertion ordered
    calls = [("gen", "A", 0), ("gen", "B", 2), ("renew", "A", 4), ("count", "", 5),
             ("renew", "B", 7), ("count", "", 7), ("count", "", 9)]
    st = []
    res = []
    for i, (op, tok, now) in enumerate(calls):
        for k in list(exp):
            if exp[k] <= now: del exp[k]
            else: break
        if op == "gen":
            exp.pop(tok, None); exp[tok] = now + ttl; r = "none"
            note = f"Token {tok} is stored with expiry {now + ttl} at the back of the order."
        elif op == "renew":
            if tok in exp:
                del exp[tok]; exp[tok] = now + ttl; r = "renewed"
                note = f"Token {tok} is live, so its expiry becomes {now + ttl} and it moves to the back."
            else:
                r = "ignored"
                note = f"Token {tok} ended at {now} or before, so the purge removed it and the renew does nothing."
        else:
            r = str(len(exp))
            note = f"After the purge from the front, {len(exp)} token(s) remain, so the count is {len(exp)}."
        res.append(r)
        st.append({"at": {"i": i}, "vars": {"now": now, "call": op + (" " + tok if tok else ""), "result": r,
                   "order": ", ".join(f"{k}={v}" for k, v in exp.items()) or "empty"}, "note": note})
    assert res == ["none", "none", "renewed", "2", "ignored", "1", "0"]
    return block([f"{o} {t}@{n}".replace("  ", " ") for o, t, n in calls], ["i"], st)

fill(CH, NAME, logger_trace(), "@@TRACE1@@")
fill(CH, NAME, auth_trace(), "@@TRACE2@@")
