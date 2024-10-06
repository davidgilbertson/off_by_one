from collections import defaultdict
from pathlib import Path
import re
import numpy as np
import pandas as pd

df = pd.read_csv("data/words.csv", keep_default_na=False, na_values=[])
df["Length"] = df.Word.str.len().astype(int)
# df = df.head(1000)
df4 = df[df.Length.eq(4)]
df5 = df[df.Length.eq(5)]
df6 = df[df.Length.eq(6)]
df7 = df[df.Length.eq(7)]
df8 = df[df.Length.eq(8)]


# %%
def diff(a: str, b: str):
    if len(a) != len(b):
        raise ValueError("Length mismatch")

    diff_count = 0
    for letter_a, letter_b in zip(a, b):
        if letter_a != letter_b:
            diff_count += 1

    return diff_count


# patterns = set()
data = defaultdict(list)
for word in df6.Word:
    for i in range(len(word)):
        # word[i] = "_"
        # patterns.add(f"{word[:i]}_{word[i+1:]}")
        pattern = f"{word[:i]}_{word[i+1:]}"
        data[pattern].append(word)

data2 = {key: value for key, value in data.items() if len(value) > 1}
# for key, value in data.items():
#     if len(value) > 1:
#         data2[key] = value
# pairs = set()

# for word_a in df6.Word:
#     for word_b in df6.Word:
#         if diff(word_a, word_b) == 1:
#             # pairs.add((word_a, word_b))
#             pairs.add(tuple(sorted([word_a, word_b])))
#
df6_pairs = pd.DataFrame(data2.items(), columns=["Pattern", "Matches"])
df6_pairs["MatchesText"] = df6_pairs.Matches.apply(lambda x: " ".join(x))
