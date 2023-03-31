from src.cksaap import cksaap

def test_cksaap():
    for i, aa in enumerate("ACDEFGHIKLMNPQRSTVWY"):
        seq = aa * 10
        seq_enc = cksaap(seq, k=1)
        assert seq_enc[i + (20 * i)] == 1
