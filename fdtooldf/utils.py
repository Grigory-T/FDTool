def result_dict_to_str(d, m):
    s = ""
    n = 10

    s += ">>> FD (functional dependancies):\n"
    l = []
    for vs, v in d["FD"]:
        ss = ""
        ss += " | ".join(el[:n] for el in sorted(vs, key=m.get))
        ss += " -> "
        ss += str(v)
        l.append(ss)
    s += "\n".join(sorted(l, key=lambda el: (len(el), el)))
    s += "\n\n"

    s += ">>> EQ (equivalences):\n"
    for el in sorted(d["EQ"], key=lambda el: len(el[0]) + len(el[1])):
        s += " | ".join(el[:n] for el in sorted(el)[0])
        s += " <-> "
        s += " | ".join(el[:n] for el in sorted(el)[1])
        s += "\n"
    s += "\n"

    s += ">>> CK (candidate keys):\n"
    for el in sorted(d["CK"], key=lambda el: (len(el), sorted(el))):
        s += " | ".join(el[:n] for el in sorted(el))
        s += "\n"
    s = s[:-1]

    return s


def convert_col_name_back(d, m):

    d["FD"] = frozenset((frozenset(m[el] for el in vs), m[v]) for vs, v in d["FD"])

    d["EQ"] = frozenset(
        (
            frozenset(m[el] for el in sorted(el)[0]),
            frozenset(m[el] for el in sorted(el)[1]),
        )
        for el in d["EQ"]
    )

    d["CK"] = frozenset(frozenset(m[v] for v in el) for el in d["CK"])

    return d
