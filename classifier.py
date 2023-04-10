from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
import pickle


# read dataset
# Each row is a protein
#    First three columns contain different encoding for the same sequence
#    Last column contains encoded labels
df = pd.read_parquet("model/df_sublocation_train.parquet")

# split in features (X) and labels (y)
# One of the three encodings
# 0: k=2, 1: k=3, 2: k=4
X = pd.DataFrame(df.iloc[:, 0].to_list(), columns=list(range(441)))

# ravel function outputs vector with expected shape
y = df.iloc[:, -1:].values.ravel()

# parameters definition for exhaustive grid search
parameters = {
    "hidden_layer_sizes": [(20,), (40,), (60,), (80,), (100,),
                         (20, 1), (40, 1), (60, 1), (80, 1), (100, 1),
                         (20, 2), (40, 2), (60, 2), (80, 2), (100, 2)],
    "activation": ["relu", "logistic", "tanh"],
    "solver": ["adam", "sgd"],
    "alpha": [0.1, 0.01, 0.001, 0.0001],
}

# classifier definition
clf = MLPClassifier(
    max_iter=3000,
    validation_fraction=0.2,
    early_stopping=True,
)

# grid search definition
clf_psearch = GridSearchCV(
    clf,
    parameters,
    cv=5,
    verbose=2,
)

# optimisation
clf_psearch.fit(X, y)

# save grid search model
with open("model/model_k2_gridsearch.pickle", "wb") as f:
    pickle.dump(clf_psearch, f)

# classifier with best parameters
clf_best = clf_psearch.best_estimator_
clf_best.fit(X, y)

# save model to file
with open("model/model_k2.pickle", "wb") as f:
    pickle.dump(clf_best, f)