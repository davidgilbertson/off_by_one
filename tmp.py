import pandas as pd
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")


def is_root(word):
    doc = nlp(word)
    lemma = doc[0].lemma_
    return word == lemma


df = pd.read_csv("data/words.csv", keep_default_na=False, na_values=[])
df = df.head(2_000)

df["Is_Root"] = df["Word"].apply(is_root)


# ie_or_ei_words = words_df.Word[words_df.Word.str.contains(r"ie|ei", regex=True)]
# ie_words = words_df.Word[words_df.Word.str.contains("ie")]
# ei_words = words_df.Word[words_df.Word.str.contains("ei")]
#
# # "I before E"
# i_before_e = len(ie_words) / len(ie_or_ei_words)
# print(f"{i_before_e = : .0%}")
#
# # except_c
# ie_not_c_words = words_df.Word[words_df.Word.str.contains(r"[^c]ie|cei")]
#
# ie_not_c = len(ie_not_c_words) / len(ie_or_ei_words)
# print(f"{ie_not_c = : .0%}")
