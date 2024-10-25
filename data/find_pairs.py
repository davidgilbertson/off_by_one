from collections import defaultdict
from pathlib import Path
import re
import numpy as np
import pandas as pd

df = pd.read_csv("words.csv")
# Drop na since 'nan' and 'none' are words, but I won't use them
df = df.dropna().head(25_000)
df["Length"] = df.Word.str.len().astype(int)

df3 = df[df.Length.eq(3)]
df4 = df[df.Length.eq(4)]
df5 = df[df.Length.eq(5)]
df6 = df[df.Length.eq(6)]
df7 = df[df.Length.eq(7)]
df8 = df[df.Length.eq(8)]
df9 = df[df.Length.eq(9)]


def get_pairs(dfn):
    data = defaultdict(list)
    for word in dfn.Word:
        for i in range(len(word)):
            pattern = f"{word[:i]}_{word[i+1:]}"
            data[pattern].append(word)

    df_data = {key: " ".join(value) for key, value in data.items() if len(value) > 1}
    pairs_df = pd.DataFrame(df_data.items(), columns=["Pattern", "Matches"])
    return pairs_df


all_pairs = pd.concat(
    get_pairs(x)
    for x in [
        df3,
        df4,
        df5,
        df6,
        df7,
        df8,
        df9,
    ]
)

# I got a head start on 6-letter words, mix these results in again
df6_pairs = pd.read_csv("df6_pairs.csv").query("Reviewed")

final_df = pd.merge(
    all_pairs[["Pattern", "Matches"]],
    df6_pairs[["Pattern", "Matches", "Clue", "Answer", "Quality", "Reviewed"]],
    on=["Pattern", "Matches"],
    how="left",
)

# final_df.sample(frac=1).to_csv("patterns.csv", index=False)
