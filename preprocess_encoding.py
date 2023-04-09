from src.encoding import cksaap
from sklearn.preprocessing import OneHotEncoder
import pandas as pd


def encode_seq(seq_series: pd.Series, ks: list[int]) -> pd.DataFrame:
    """
    Function for CKSAAP encoding a Series of sequences, given a list of k values
    Returns a dataframe where columns are encodings using a different k value
    """
    df = pd.DataFrame()
    for k in ks:
        feature = f"seq_c{k}saap_enc"
        df[feature] = seq_series.apply(cksaap, k=k)
    return df


def encode_label(label_series: pd.Series) -> pd.Series:
    """
    Function for OneHot encoding a Series of labels
    Returns a Series of encoded labels
    """
    encoder = OneHotEncoder()
    label_array = label_series.values.reshape(
        # shape accepted by encoder
        (len(label_series), 1)
    )
    # fit data and get the encoded array
    label_enc = encoder.fit_transform(label_array).toarray()

    # return a pandas Series
    return pd.Series(label_enc.tolist())


# list of k for cksaap encoding
ks = [2, 3, 4]

df_names = ["df_sublocation_train.parquet", "df_sublocation_test.parquet"]

for df_name in df_names:
    # read in dataframe for encoding
    df = pd.read_parquet(f"data/clean/{df_name}")

    # encode sequence
    df_encoded = encode_seq(df["sequence"], ks)
    # encode label
    df_encoded["subcell_location_enc"] = encode_label(df["subcellular_location"])

    # change index to Uniprot ID
    df_encoded.set_index(df["uniprot_id"])

    # save encoded dataframe
    df_encoded.to_parquet(f"model/{df_name}")

