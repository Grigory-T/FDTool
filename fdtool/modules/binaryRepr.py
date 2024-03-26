# Replaces candidates with binary representation, 1 where attribute exists, 0 otherwise

def toBin(Candidate, U):
    m = {U.index(element) for element in Candidate}
    # Create generator to fill in '1' for slots in U that candidate fills; '0' otherwise
    Gen = (['1' if k in m else '0' for k in range(len(U))])
    # Join generator to string
    return "".join(Gen);
