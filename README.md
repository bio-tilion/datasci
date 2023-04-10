# Data Science coursework

## Sub-cellular localisation prediction
This program is made of python scripts to be run sequentially as part of a pipeline.
For simplicity, I have chosen only 6 sub-cellular categories, which are: 
Nucleus, Cell membrane, Cytoplasm, Mitochondrion, Endoplasmic reticulum, and Golgi apparatus. 

### Data acquisition
The script `data.py` is the first script, responsible for getting all the data from Uniprot, using its rest API.

First, it looks for the code that matches only the six sub-cellular categories, then it saves each result as a separate DataFrame in the `data/raw/` folder.
Each DataFrame has the following fields as columns: 
- `Entry` the uniprot_id, 
- `Entry Name` the UniProtKB/Swiss-Prot entry name, 
- `Sequence`, 
- `Subcellular location [CC]` the full Uniprot sub-cellular annotation, 
- `subcellular_location` a custom column containing the label of the location, chosen among the six categories.

### Data preprocessing
The script `preprocess_cleaning.py` performs the first step, by selecting only the 95% central range based on sequence length, in the hope of working with the most representative entries by loosing the possible outliers.
The resulting DataFrames are saved in the `data/clean/` folder.

Each DataFrame is then split 80-20% into a training and testing DataFrame, and pooled together to form a single training DataFrame, and a single testing one.
This was done in order to prevent the possibility that one category would be over- or under-represented in the working training and testing DataFrames. This way, each category should be represented in the same proportion as in the Uniprot database.
The resulting DataFrames are also saved in the `data/clean/` folder.

As a second step, the script `preprocessing_encoding.py` encodes the sequences using a CKSAAP algorithm, and the sub-location labels using a ordinal encoding, for both DataFrames, training and testing.
The resulting DataFrames are saved in the `model/` folder.

### Neural network classifier
In order to predict the sub-location, 
the script `classifier.py` a Sklearn neural network classifier with the training encoded DataFrames. 
The best parameters are chosen using an exhaustive grid search, and the resulting optimised model is saved in the `model/` folder.

### Results
The script `results.py` predicts the sub-location labels on the testing DataFrame using the saved model, and produces a HTML file with the interactive plots showing the learning curve and the DataFrame with the predicted labels.
Both HTML and DataFrame files are saved in the `results/` folder.