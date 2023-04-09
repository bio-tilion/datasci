from sklearn.neural_network import MLPClassifier
import pandas as pd
import matplotlib.pyplot as plt


# read dataset
df = pd.read_parquet("model/df_sublocation_train.parquet")

# split in features (X) and labels (y)
# One encoding at a time
X = pd.DataFrame(df.iloc[:, 0].to_list(), columns=list(range(441)))
#X = pd.DataFrame(X["seq_c2saap_enc"].to_list(), columns=list(range(441)))

# Only last column
# ravel function outputs vector with expected shape
y = df.iloc[:, -1:].values.ravel()

clf = MLPClassifier(
    # solver [‘lbfgs’, ‘sgd’, ‘adam’]
    solver="adam",
    # for consistency
    random_state=42,
    # activation [‘identity’, ‘logistic’, ‘tanh’, ‘relu’]
    activation="relu",
    max_iter=1000,
)
clf = MLPClassifier(
    activation="relu",
    max_iter=3000,
    validation_fraction=0.2,
    early_stopping=True,
)
clf.fit(X, y)

