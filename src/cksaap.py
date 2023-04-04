import numpy as np


def cksaap(seq: str, k=2) -> np.ndarray:
    """
    Composition of k-spaced amino acid pair (CKSAAP) encoding implementation
    CKSAAP depicts the frequencies of all possible 400 amino acid pairs that are
    separated by k other amino acids within the peptide sequence.

    Arguments
        seq     Amino acids sequence, provided as string of single letters amino acids
        k       Integer, number of spaces between the pair of amino acids
                (Default 2)

    Return a Numpy array of the encoded sequence
    """
    # get all possible permutations of pairs of amino acids
    aminoacids = "ACDEFGHIKLMNPQRSTVWY"
    permutations = [i+j for i in aminoacids for j in aminoacids]

    # initialize dictionary for encoding
    dict_enc = {i: 0 for i in permutations}

    # step 'n' relative to 'k', where 'k' is the number of spaces between aa
    n = k + 1

    for i in range(len(seq)-n):
        # pairs of aa: first position + step 'n'
        pair = seq[i] + seq[i+n]

        # count of aa pairs occurrence
        dict_enc[pair] += 1

    # transform dict of count into dict of frequencies
    # count / total number of pairs
    dict_enc = {k: v/(len(seq)-n) for k, v in dict_enc.items()}

    # transform dict of frequency into numpy array
    seq_encoded = np.array(list(dict_enc.values()))

    return seq_encoded


if __name__ == '__main__':
    #print(cksaap("ATAKAFCGAP", k=1))
    help(cksaap)
