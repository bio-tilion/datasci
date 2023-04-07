from src.encoding import cksaap
from src.encoding import plot_encoding
import numpy as np
import matplotlib.pyplot as plt
import random

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

def test_plot_encoding():
    """
    Test plot_encoding function
        From a peptide sequence made of a single amino acid, compare the image got using the
        plot_encoding function with the image got using the expected frequency matrix, by
        importing the two images as arrays and comparing them
    """

    aa = "ACDEFGHIKLMNPQRSTVWY"

    # get a random aa index
    n = random.randint(0, 19)

    # random length peptide made with a single amino acid
    seq = aa[n] * 10

    # encoding
    seq_enc = cksaap(seq, k=1)

    # get plot
    fig = plot_encoding(seq_enc)
    # convert image to a numpy array
    canvas = fig.figure.canvas
    canvas.draw()
    image_plot = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8)
    plt.close()

    # get expected plot
    # create frequency matrix
    expected_enc = np.zeros((20, 20))
    expected_enc[n][n] = 1
    # same settings as plot_encoding function
    fig, ax = plt.subplots()
    im = ax.imshow(expected_enc, cmap="cividis")
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
    ax.set_xticks(np.arange(20), labels=list(aa))
    ax.set_yticks(np.arange(20), labels=list(aa))
    ax.spines[:].set_visible(False)
    plt.title("Amino acids pairs frequency")
    plt.colorbar(im)
    plt.tight_layout()

    # convert image to a numpy array
    canvas = ax.figure.canvas
    canvas.draw()
    image_expected = np.frombuffer(canvas.tostring_rgb(), dtype=np.uint8)
    plt.close()

    # compare the two image arrays
    assert np.array_equal(image_plot, image_expected)
