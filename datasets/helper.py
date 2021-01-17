import json
from tqdm import tqdm

full_dataset = {
    "catalog": [],
}

with open(
    "3000_articles_dataset_economic_culture_hightech.json",
) as final_json:
    final = json.load(final_json)

with open("1000_articles_dataset_sport.json") as sport_json:
    sport = json.load(sport_json)
# create a str from list (move this logic to scrapper)
for elem in tqdm(final["catalog"]):
    try:
        elem["tags"] = elem["tags"][0]
    except:
        elem["tags"] = None
    full_dataset["catalog"].append(elem)

for elem in tqdm(sport):
    try:
        elem["tags"] = elem["tags"][0]
    except:
        elem["tags"] = None
    full_dataset["catalog"].append(elem)


with open("final_dataset.json", "w") as out_file:
    json.dump(
        full_dataset,
        out_file,
        sort_keys=True,
        indent=4,
        ensure_ascii=False,
    )
print("Finish")
