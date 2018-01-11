def pairwise(L):
    pairs = []
    for idx, item in enumerate(L):
        for element in L[idx+1:]:
            pairs.append((item, element))
    return pairs
