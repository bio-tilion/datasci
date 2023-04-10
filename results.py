from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
import pickle
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, TabPanel, Tabs


model_name = "model_k2"

# read the fitted model
with open(f"model/{model_name}.pickle", "rb") as f:
    clf_read = pickle.load(f)

# read testing dataset
df = pd.read_parquet("model/df_sublocation_test.parquet")

# dataset for storing results
df_out = df.iloc[:, [0, -1]]

# split in features (X) and labels (y)
# One of the three encodings
# 0: k=2, 1: k=3, 2: k=4
X = pd.DataFrame(df.iloc[:, 0].to_list(), columns=list(range(441)))

# ravel function outputs vector with expected shape
y = df.iloc[:, -1:].values.ravel()

# predict label
print(clf_read.score(X, y))
df_out["predicted_subcell_location_enc"] = clf_read.predict(X)

# save dataframe with predictions
df_out.to_parquet(f"results/df_sublocation_test_prediction.parquet", index=True)


# Bokeh visualisation
def my_line(fig, y_data, **line_kwargs):
    """
    Function for plotting a learning curve line
    """
    fig.line(
        # x
        np.arange(len(y_data)),
        # y
        y_data,
        **line_kwargs,
    )
    return fig


def my_tab(data_kwargs, title, **fig_kwargs):
    """
    Function for plotting a tab with any number of learning curves
    """
    p = figure(**fig_kwargs)

    # data_kwargs must be a list of tuples(data, kwargs)
    # each tuple results in a line within the same tab
    for y_data, line_kwargs in data_kwargs:
        p = my_line(p, y_data, **line_kwargs)

    tab = TabPanel(child=p, title=title)
    return tab


output_file(filename="results/sublocation_test_prediction.html", title="Data Science Coursework")
source = ColumnDataSource(data=df_out)

#p = figure(title=f"Learning curve for {model_name}", x_axis_label="Iteration (epochs)", y_axis_label="Score")

fig_param = {
    "x_axis_label": "Iteration (epochs)",
    "y_axis_label": "Score",
}

tab1 = my_tab(
    [(
        # tuple data
        clf_read.validation_scores_,
        # tuple kwargs
        {"color": "blue"}
    )],
    "Validation",
    **fig_param
)

tab2 = my_tab(
    [(
        clf_read.loss_curve_,
        {"color": "red"}
    )],
    "Loss",
    **fig_param
)

tab3 = my_tab(
    [
        (clf_read.validation_scores_,
         {"color": "blue", "legend_label": "validation scores"}),
        (clf_read.loss_curve_,
         {"color": "red", "legend_label": "loss scores"})
    ],
    "Both",
    **fig_param
)

p = Tabs(tabs=[tab1, tab2, tab3])



save(p)
