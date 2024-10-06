from pathlib import Path
import re
import numpy as np
import pandas as pd

desc_df = pd.read_json("data/dictionary.json", orient="index")
desc_df.columns = ["Description"]

data = []

for line in (
    Path("data/google_ngram_frequency-alpha-alldicts.txt").read_text().splitlines()
):
    if line.startswith("#"):
        continue

    rank, word = re.split(r"\s+", line)[:2]

    data.append(
        dict(
            Word=word.lower(),
            Rank=int(rank),
        )
    )

rank_df = pd.DataFrame(data)

df = rank_df.join(desc_df, on="Word")

# Note, dropping NA, they're mostly plurals, proper nouns, and conjugations
df = df.dropna().reset_index(drop=True)

df.to_csv("data/words.csv", index=False)
