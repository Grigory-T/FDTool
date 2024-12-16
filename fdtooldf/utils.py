def result_dict_to_str(d, m, cut):
    """
    pretty printing
    ensure to sort elements in some logical order
    """
    s = ""

    s += ">>> FD (functional dependancies):\n"
    temp = sorted(
        ((sorted(el1, key=m.get), el2) for el1, el2 in d["FD"]),
        key=lambda el: [len(el[0])] + el[0] + [el[1]],
    )
    for el1, el2 in temp:
        s += " | ".join(el[:cut] for el in el1)
        s += " -> "
        s += el2[:cut]
        s += "\n"
    s += "\n"

    s += ">>> EQ (equivalences):\n"
    temp = sorted(
        (
            (
                [el[:cut] for el in sorted(el1, key=m.get)],
                [el[:cut] for el in sorted(el2, key=m.get)],
            )
            for el1, el2 in d["EQ"]
        ),
        key=lambda el: [len(el[0] + el[1])] + el[0] + el[1],
    )
    for el1, el2 in temp:
        s += " | ".join(el[:cut] for el in el1)
        s += " <-> "
        s += " | ".join(el[:cut] for el in el2)
        s += "\n"
    s += "\n"

    s += ">>> CK (candidate keys):\n"
    temp = sorted(
        (sorted(el, key=m.get) for el in d["CK"]), key=lambda el: [len(el)] + el
    )
    for el in temp:
        s += " | ".join(el[:cut] for el in el)
        s += "\n"

    return s


def convert_col_name_back(d, m):
    """
    if order does not matter - change sequence to frozenset
    change columns name back to normal
    """

    d["FD"] = frozenset(
        (frozenset(m[el] for el in el1), m[el2]) for el1, el2 in d["FD"]
    )

    d["EQ"] = frozenset(
        frozenset(
            [
                frozenset(m[el] for el in el1),
                frozenset(m[el] for el in el2),
            ]
        )
        for el1, el2 in d["EQ"]
    )

    d["CK"] = frozenset(frozenset(m[v] for v in el) for el in d["CK"])

    return d
