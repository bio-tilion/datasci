import pandas as pd
import os

# get all dataframes, one per sublocation
df_names = os.listdir("data/raw")

# empty dataframes for training and testing
df_sublocation_test = pd.DataFrame()
df_sublocation_train = pd.DataFrame()

for df_name in df_names:
    # read raw dataframe
    df = pd.read_parquet("data/raw/" + df_name)

    # remove column with Uniprot entries for sublocation
    df_clean = df.iloc[:, :3]

    # rename columns with more meaningful labels
    df_clean = df_clean.rename(columns={
            'Entry': 'uniprot_id',
            'Entry Name': 'entry_name',
            'Sequence': 'sequence'
        }
    )

    # add column with length of sequence
    df_clean["length"] = df_clean["sequence"].str.len()

    # keep 'simplified' sublocation column
    df_clean["subcellular_location"] = df["subcellular_location"]

    # keep only 95% central range based on length
    df_clean = df_clean[
        (df_clean["length"] > df_clean["length"].quantile(0.10)) &
        (df_clean["length"] < df_clean["length"].quantile(0.90))
    ]

    # save cleaned dataframe
    df_clean.to_parquet("data/clean/" + df_name)

    # sample dataframe for testing and training (20-80% split)
    df_test = df_clean.sample(frac=0.2)
    df_train = df_clean.drop(df_test.index)

    # merge with global testing and training dataframes
    df_sublocation_test = pd.concat([df_sublocation_test, df_test])
    df_sublocation_train = pd.concat([df_sublocation_train, df_train])

# refactor indices and save merged dataframes
df_sublocation_test.reset_index(inplace=True)
df_sublocation_test.to_parquet("data/clean/" + "df_sublocation_test" + ".parquet")
df_sublocation_train.reset_index(inplace=True)
df_sublocation_train.to_parquet("data/clean/" + "df_sublocation_train" + ".parquet")
