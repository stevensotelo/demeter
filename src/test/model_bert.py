import tensorflow as tf
import pandas as pd

print(tf.__version__)

# Parameters
root = "G:\\Me\\Code\\UOC\\TFM\\demeter\\"
inputs = root + "data\\english\\intent\\"
outputs = root + "test\\src\\outputs\\"


print(inputs + "Question_Classification_Dataset.csv")
df = pd.read_csv(inputs + "Question_Classification_Dataset.csv", index_col=0)
df.head()
