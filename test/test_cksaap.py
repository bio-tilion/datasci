from src.cksaap import cksaap

def test_cksaap():
    """
    Test cksaap function
        For peptide sequences made from a single amino acid, the encoded sequence is equal to an array
        of zeroes with only the value corresponding to the homo-pair (AA, CC, etc) is equal to 1
    """
    for i, aa in enumerate("ACDEFGHIKLMNPQRSTVWY"):
        # random length peptide made with a single amino acid
        seq = aa * 10

        # encoding
        seq_enc = cksaap(seq, k=1)

        # encoded array is a raveled 20x20 matrix
        # in this case the diagonal has to be 1
        assert seq_enc[i + (20 * i)] == 1
