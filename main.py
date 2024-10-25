import pandas as pd
import streamlit as st

# TODO (@davidgilbertson): cache this, idiot
df = pd.read_csv("data/df6_pairs.csv")
df = df.dropna(subset="Clue").reset_index(drop=True)
# df = df[df.Quality.eq(3)]
item_count = len(df)


def int_to_ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return str(n) + suffix


if "current_q_index" not in st.session_state:
    st.session_state["current_q_index"] = 0
    st.session_state["hint_level"] = 0
    st.session_state["hint_letter_pos"] = 0
    st.session_state["guess"] = ""
    st.session_state["has_guessed"] = False
    st.session_state.is_correct = None


current_question = df.iloc[st.session_state.current_q_index]
# print(current_question)
clue = current_question.Clue
pattern = current_question.Pattern
words_actual = current_question.Pair.lower().split()
word_length = len(words_actual[0])

max_hints = word_length + 1
diff_position = pattern.index("_")
hint_letter_pos = 0

# TODO (@davidgilbertson): add an info panel, use getaway comeback as an example, remove from data.

st.title(f"{current_question.Clue}")

words_guess = st.text_input(
    label="Answer",
    key="guess_input",
    autocomplete="off",
    help=f"Enter two words, separated by a space. They should be the same length and differ by only one letter.",
)
# st.write(st.session_state)
# st.caption("Enter two words of the same length that differ by only one letter")

words_guess = words_guess.lower().split()
# st.write(words_guess)
is_guess = len(words_guess) == 2 and len(words_guess[0]) == len(words_guess[1])
# st.write(is_guess)
if is_guess:
    st.session_state.has_guessed = True

# st.write(st.session_state.has_guessed)

if st.session_state.has_guessed:
    if set(words_guess) == set(words_actual):
        st.write("Correct!")
        st.balloons()
    else:
        st.write("Wrong")

# TODO (@davidgilbertson): if hint level is max, change to "I give up, show me the answer"
if st.button("Give me a hint"):
    st.session_state.hint_level += 1

if st.session_state.hint_level > 0:
    st.write(f"Hint 1: each word has {word_length} letters")

if st.session_state.hint_level > 1:
    st.write(f"Hint 2: the {int_to_ordinal(diff_position+1)} letter is different")

if st.session_state.hint_level > 2:
    if hint_letter_pos == diff_position:
        hint_letter_pos += 1
    hint_letter = pattern[hint_letter_pos]
    st.write(f"Hint 3: the {int_to_ordinal(hint_letter_pos+1)} letter is {hint_letter}")

if st.session_state.hint_level > 3:
    hint_letter_pos += 1
    if hint_letter_pos == diff_position:
        hint_letter_pos += 1
    hint_letter = pattern[hint_letter_pos]
    st.write(f"Hint 3: the {int_to_ordinal(hint_letter_pos+1)} letter is {hint_letter}")

if st.session_state.hint_level > 4:
    hint_letter_pos += 1
    if hint_letter_pos == diff_position:
        hint_letter_pos += 1
    hint_letter = pattern[hint_letter_pos]
    st.write(f"Hint 3: the {int_to_ordinal(hint_letter_pos+1)} letter is {hint_letter}")

if st.session_state.hint_level > 5:
    hint_letter_pos += 1
    if hint_letter_pos == diff_position:
        hint_letter_pos += 1
    hint_letter = pattern[hint_letter_pos]
    st.write(f"Hint 3: the {int_to_ordinal(hint_letter_pos+1)} letter is {hint_letter}")

if st.session_state.hint_level > 6:
    hint_letter_pos += 1
    if hint_letter_pos == diff_position:
        hint_letter_pos += 1
    hint_letter = pattern[hint_letter_pos]
    st.write(f"Hint 3: the {int_to_ordinal(hint_letter_pos+1)} letter is {hint_letter}")


def change_questions(delta):
    # TODO (@davidgilbertson): if you click the button fast enough, it goes past the end of the DF.
    #  So this should check to see if we're out of range
    st.session_state.guess_input = ""
    st.session_state.current_q_index += delta
    st.session_state.hint_level = 0
    st.session_state.has_guessed = False


left, mid, right = st.columns([3, 1, 3], vertical_alignment="center")
with left:
    if st.session_state.current_q_index > 0:
        st.button(
            "Previous",
            use_container_width=True,
            on_click=lambda: change_questions(-1),
        )

with mid:
    pos = f"{st.session_state.current_q_index + 1}/{item_count}"
    st.html(f"<div style='text-align: center'>{pos}</div>")

with right:
    if st.session_state.current_q_index < len(df) - 1:
        st.button(
            "Next",
            use_container_width=True,
            on_click=lambda: change_questions(1),
        )
