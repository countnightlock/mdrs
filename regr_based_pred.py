import itertools
import ast
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from regression import get_coefficients

# Get theta and X
X = pd.read_csv("regr_data.csv", sep=",")
theta = get_coefficients()
# theta = [[ 0, 0.5, 0.35, 0.15 ]]
y_pred = []

# Calculate predicted y via theta dot X[idx]
for idx, row in X.iterrows():
    idx1, idx2 = ast.literal_eval(row["id_pair"])
    x = np.asarray([
        row["tfidf_simil"],
        row["genre_simil"],
        row["age_simil"],
        row["length_simil"]
    ])
    y_pred.append(np.dot(theta[0], x))


# Get names for reference
df = pd.read_csv("./books_final.csv", usecols=["title"])

def get_title_from_id(idx):
    return df.iloc[idx]["title"]


# Make intermediate df to store id-pairs and similarities
pairs_and_simil = pd.DataFrame(data={
    "id_pair": X["id_pair"],
    "overall_simil": y_pred
})

# Since data exists in batches of 1000 with the same idx1
batch_size = 100

for i in range(11):
    # For all items in subset, idx1 is the same
    subset = pairs_and_simil[i * batch_size : (i+1) * batch_size]
    # print(subset.info())

    simils = np.asarray(subset["overall_simil"])

    # Go from first-last to tenth-last, in reverse
    indices = np.argsort(simils)[-1:-10:-1]

    print("Items similar to %s:" % (get_title_from_id(i)))
    for idx in indices:
        print("%4d - %s" % (idx, get_title_from_id(idx)))

    print("*" * 50)

print("Mean squared error: %.5f"
      % mean_squared_error(X["collab_simil"], y_pred))

print('Variance score: %.5f' % r2_score(X["collab_simil"], y_pred))

X.to_csv("regr_data.csv", index = False) 