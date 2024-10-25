(() => {
    // Some helper functions
    const set = (id, attr, value) => document.getElementById(id)[attr] = value;
    const on = (id, event, func) => document.getElementById(id).addEventListener(event, func)
    const save = (key, value) => localStorage.setItem(key, JSON.stringify(value))
    const load = (key) => {
        const raw = localStorage.getItem(key);
        return raw ? JSON.parse(raw) : raw
    }

    // Parse the raw data
    const doneClues = load('doneClues') || []
    const doneItems = []
    const newItems = []

    WORD_DATA.trim().split('\n').forEach(row => {
        let [clue, answer] = row.split('\t');
        answer = answer.trim().toLowerCase()
        const len = answer.indexOf(' ');
        const diffPos = clue.indexOf("_")


        const thisItem = { clue, answer, len, diffPos };
        if (doneClues.includes(clue)) {
            doneItems.push(thisItem);
        } else {
            newItems.push(thisItem);
        }
    });
    const items = doneItems.concat(newItems);
    // const items = WORD_DATA.trim().split('\n').map(row => {
    //     let [clue, answer] = row.split('\t');
    //     answer = answer.trim().toLowerCase()
    //     const len = answer.indexOf(' ');
    //     const diffPos = clue.indexOf("_")
    //
    //     return { clue, answer, len, diffPos };
    // });

    let item_index = doneItems.length;
    let item = items[item_index];
    let hint_level = 0

    function intToOrdinal(n) {
      let suffix;
      if (n % 100 >= 10 && n % 100 <= 20) {
        suffix = "th";
      } else {
        suffix = { 1: "st", 2: "nd", 3: "rd" }[n % 10] || "th";
      }
      return n.toString() + suffix;
    }

    function set_question(delta) {
        document.getElementById("answer").innerText = ""
        item_index += delta;
        item = items[item_index]
        hint_level = 0
        set("clue", "innerText", item.clue)
        set("answer", "value", "")
        set("status", "innerHTML", "")
        set("hints", "innerHTML", "")
        set("hint", "disabled", false);
        set("prev", "disabled", item_index < 1);
        set("next", "disabled", item_index >= items.length - 1);
        set("counter", "innerText", `${item_index + 1}/${items.length}`)  // ⠿ one day
    }

    function mark_done() {
        // Marks the current item as done
        if (!doneClues.includes(item.clue)) {
            doneClues.push(item.clue)
            save('doneClues', doneClues)
        }
    }

    function show_hint(e) {
        hint_level += 1
        const hints = []

        if (hint_level >= 1) {
            hints.push(`Each word has ${item.len} letters`)
        }

        if (hint_level >= 2) {
            const max_letter_i = Math.min(hint_level - 2, item.len - 1)
            const [word1, word2] = item.answer.split(' ')

            let letter_i = 0
            while (letter_i <= max_letter_i) {
                if (word1[letter_i] !== word2[letter_i]) {
                    hints.push(`The ${intToOrdinal(letter_i + 1)} letter is different`);
                } else {
                    hints.push(`The ${intToOrdinal(letter_i + 1)} letter is ${item.answer.at(letter_i)}`);
                }
                letter_i += 1
            }
        }
        if (hint_level === item.len + 1) {
            set("hint", "disabled", true);
        }

        set('hints', "innerHTML", hints.join("<br>"));
    }

    function check_answer(e) {
        const answer = e.target.value.toLowerCase();
        let status = ""
        if (answer.includes(" ")) {
            const words = answer.split(" ");
            // We wait for the user to type two words of the same length before telling them they're right/wrong
            if (words.length === 2 && words[0].length === words[1].length) {
                if (answer === item.answer || words.reverse().join(' ') === item.answer) {
                    // TODO (@davidgilbertson): "Correct" as a popup with 'Next' or something?
                    status = "🎉 Correct! 🎉"
                    mark_done()
                    set('hints', "innerHTML", "");
                } else {
                    status = "Wrong"
                }
            }
        }
        set("status", "innerHTML", status);
    }

    // Bind events
    on("answer", 'input', check_answer)
    on("hint", 'click', show_hint)
    on("help-button", 'click', () => set("help", "hidden", false))
    on("help-close-button", 'click', () => set("help", "hidden", true))
    on("help-background", 'click', () => set("help", "hidden", true))
    on("prev", 'click', () => set_question(-1))
    on("next", 'click', () => set_question(1))

    // Init the page
    set_question(0)
})()
