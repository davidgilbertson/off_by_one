from pathlib import Path
import json
import pandas as pd

html = Path("src/index.html").read_text()

df = pd.read_csv("data/patterns.csv").dropna()
df = df[df.Quality.ne(-1)]  # The example question
df = df[["Clue", "Answer"]]

assert df.Clue.is_unique, "You have duplicate clues"

data_tsv = df.to_csv(index=False, header=False, sep="\t")

data_script = f"""\
<script>
const WORD_DATA = {json.dumps(data_tsv)};
</script>"""

main_script = f"""\
<script>
{Path("src/main.js").read_text()}
</script>"""

style = f"""\
<style>
{Path("src/main.css").read_text()}
</style>"""

html = html.replace('<script src="word_data.js"></script>', data_script)
html = html.replace('<script src="main.js"></script>', main_script)
html = html.replace('<script src="reload.js"></script>', "")  # dev only
html = html.replace('<link rel="stylesheet" href="main.css"></link>', style)

Path("dist/index.html").write_text(html)
