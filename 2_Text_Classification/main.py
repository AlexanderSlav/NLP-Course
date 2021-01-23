import nlp_utils
from time import time
import matplotlib.pyplot as plt

dataset = nlp_utils.NewsTextDataset()
dataset.load(
    "/home/alexander/HSE_Stuff/NLP-Course/datasets/final_dataset_4k.json",
)
start = time()
dataset.preprocess()
dataset.save(
    "/home/alexander/HSE_Stuff/NLP-Course/datasets/final_dataset_4k_cleaned.json",
)
print(time() - start)
data = dataset.dump_to_pandas()
print(data.head())
data.groupby("category").text.count().plot.bar(ylim=0)
plt.show()
