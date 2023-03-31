import numpy as np


def cksaap(seq: str, k=2) -> np.ndarray:
    """

    :param seq:
    :param k:
    :return:
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
        pep = seq[i] + seq[i+n]

        # count of pairs aa occurrence
        dict_enc[pep] += 1

    # transform dict of count into dict of frequencies
    # count / total number of pairs
    dict_enc = {k: v/(len(seq)-n) for k, v in dict_enc.items()}

    # transform dict of frequency into numpy array
    seq_encoded = np.array(list(dict_enc.values()))

    return seq_encoded


if __name__ == '__main__':
    print(cksaap("ATAKAFCGAP", k=1))
