# FD Mine(r(U))
# Input: A relation r(U) over U = {v_1, ... ,v_m}
# Output: A set F of functional dependences over r(U)
# F = Null_Set
# E = Null_Set
# C_1 = U
# k = 1
#
# C_k = CalculatePartition(C_k, r(U))
# C_k = InitialClosure(C_k)
# while Cardinality(C_k) > 0:
# {
#   k += 1
#   C_k = Apriori_Gen(C_km1)
#   C_k = CalculatePartition(C_k, r(U))
#   C_k = InitialClosure(C_k)
#   F = F *Union* ObtainFDs(C_km1)
#   E = E *Union* ObtainEquivalences(C_km1, F)
#   C_k = Prune(C_km1, C_k, E)
# }

__version__ = "0.1.7"


import pandas as pd
import sys, time, argparse, ntpath, pickle, csv
from .modules import binaryRepr, Apriori_Gen, GetFDs, ObtainEquivalences, Prune, keyRun
from string import ascii_lowercase


def main(result_queue=None, df=None, max_k_level=None):
    global globalTimer
    global globalCount

    ### DEBUG
    # import polars as pl
    # df = pd.read_csv(r"C:\Users\trofi\dev\FDTool\data\input\Table1.csv")
    # df = pl.from_pandas(df)

    rv = "Functional Dependencies: "  # stirng for accumulating all results

    # Define header; Initialize k;
    U = list(df.columns)
    k = 0

    try:
        # Create dictionary to convert column names into alphabetical characters
        Alpha_Dict = {U[i]: ascii_lowercase.upper()[i] for i in range(len(U))}
    except IndexError:
        result_queue.put("Table exceeds max column count")
        return

    # Initialize lattice with singleton sets at 1-level
    C = [[[item] for item in U]] + [None for level in range(len(U) - 1)]
    # Create Generator to find next k-level attribute subsets
    Subset_Gen = (
        [x for x in Apriori_Gen.powerset(U) if len(x) == k]
        for k in range(1, len(max(Apriori_Gen.powerset(U), key=len)) + 1)
    )
    # Initialize Closure as Python dict
    Closure = {binaryRepr.toBin(Subset, U): set(Subset) for Subset in next(Subset_Gen)}
    # Initialize Cardinality as Python dict
    Cardinality = {element: None for element in Closure}
    # Create counter for number of Equivalences and FDs; initialize list to store FDs; list to store equivalences;
    Counter = [0, 0]
    FD_Store = []
    E_Set = []

    while True:

        # Increment k; initialize C_km1
        k += 1
        C_km1 = C[k - 1]
        # Initialize Closure at next next k-level; update dict accordinaly
        Closure_k = {
            binaryRepr.toBin(Subset, U): set(Subset) for Subset in next(Subset_Gen)
        }
        Closure.update(Closure_k)
        # Update Cardinality dict with next k-level
        Cardinality.update({element: None for element in Closure_k})

        if k > 1:
            # Dereference Closure and Cardinality at (k-2)-level
            for Subset in C[k - 2]:
                binRepr = binaryRepr.toBin(Subset, U)
                del Closure[binRepr], Cardinality[binRepr]
            # Dereference (k-2)-level
            C[k - 2] = None

        # Run Apriori_Gen to get k-level Candidate row from (k-1)-level Candidate row
        C_k = Apriori_Gen.oneUp(C_km1)
        # Run GetFDs to get closure and set of functional dependencies
        Closure, F, Cardinality = GetFDs.f(C_km1, df, Closure, U, Cardinality)
        # Run Obtain Equivalences to get set of attribute equivalences
        E = ObtainEquivalences.f(C_km1, F, Closure, U)
        # Run Prune to reduce next k-level iterateion and delete equivalences; initialize C_k
        C_k, Closure, df = Prune.f(C_k, E, Closure, df, U)
        C[k] = C_k
        # Increment counter for the number of Equivalences/FDs added at this level
        Counter[0] += len(E)
        Counter[1] += len(F)
        E_Set += E

        # Print out FDs
        for FunctionalDependency in F:
            # Store well-formatted FDs in empty list
            FD_Store.append(
                [
                    "".join(sorted([Alpha_Dict[i] for i in FunctionalDependency[0]])),
                    Alpha_Dict[FunctionalDependency[1]],
                ]
            )
            # Create string for functional dependency
            String = (
                "{"
                + ", ".join(FunctionalDependency[0])
                + "} -> {"
                + str(FunctionalDependency[1])
                + "}"
            )
            # Print FD String
            rv += "\n" + String

        # Break while loop if cardinality of C_k is 0
        if not len(C_k) > 0:
            break
        # Break while loop if k-level reaches level set in config
        if k is not None and max_k_level == k:
            break

    # Print equivalences
    rv += "\n\n" + "Equivalences: "

    # Iterate through equivalences returned
    for Equivalence in E_Set:
        # Create string for functional dependency
        String = (
            "{"
            + ", ".join(Equivalence[0])
            + "} <-> {"
            + ", ".join(Equivalence[1])
            + "}"
        )
        # Print equivalence string
        rv += "\n" + String

    # Print out keys
    rv += "\n\n" + "Keys: " + "\n"

    # Get string of column names sorted to alphabetical characters
    SortedAlphaString = "".join(sorted([Alpha_Dict[item] for item in Alpha_Dict]))
    # Run required inputs through keyList module to determine keys with
    keyList = keyRun.f(U, SortedAlphaString, FD_Store)
    # Iterate through keys returned
    for key in keyList:
        # Write keys to file
        rv += str(key) + "\n"

    # Write info at bottom
    rv += "\nNumber of FDs checked: " + str(GetFDs.CardOfPartition.calls)

    result_queue.put(rv)


### DEBUG
# main()
