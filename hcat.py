#!/usr/bin/env python3

import sys, re
from rich.console import Console
from rich.text import Text

console = Console()

# =========================
# 🎨 CUSTOM
# =========================
CUSTOM_WORDS = {}

def addhighlight(word, color):
    if not color.startswith("#"):
        console.print("[#ff4b4b]HEX only![/#ff4b4b]")
        sys.exit(1)
    CUSTOM_WORDS[word] = color


# =========================
# 🎨 COLOR MAP (VSCode style)
# =========================
COLOR_MAP = {
    "type": "#569cd6",
    "control": "#c586c0",
    "oop": "#4ec9b0",
    "template": "#c586c0",
    "spec": "#9cdcfe",
    "cast": "#dcdcaa",
    "exception": "#c586c0",
    "alt": "#c586c0",
    "modern": "#569cd6",
    "coroutine": "#c586c0",
    "module": "#c586c0",
    "io": "#4ec9b0"
}

STRING_COLOR = "#ce9178"
COMMENT_COLOR = "#6a9955"
NUMBER_COLOR = "#b5cea8"
FUNCTION_COLOR = "#dcdcaa"


# =========================
# 🧠 LANGUAGE RULES
# =========================
LANG = {
    "cpp": {
        "kw": {
            "type": ["int","float","double","char","bool","void"],
            "control": ["if","else","for","while","return","switch","case", "::",  "%d", "%s", "%f", "%c"],
            "oop": ["class","public","private","protected","new","delete"],
            "modern": ["namespace","using","nullptr","std"],
            "io": ["cout","cin","endl"]
        },
        "str": [
            re.compile(r"'[^'\n]*'"),
            re.compile(r'"[^"\n]*"'),
        ],
        "com": [
            re.compile(r"//.*"),
            re.compile(r"/\*[\s\S]*?\*/")
        ]
    },

    "py": {
        "kw": {
            "control": ["def","class","if","elif","else","for","while","return","import"],
        },
        "str": [
            re.compile(r"'''[\s\S]*?'''"),
            re.compile(r'"""[\s\S]*?"""'),
            re.compile(r"'[^'\n]*'"),
            re.compile(r'"[^"\n]*"'),
        ],
        "com": [re.compile(r"#.*")]
    }
}


# =========================
# 🧠 HELPER
# =========================
def in_ranges(pos, ranges):
    for s, e in ranges:
        if s <= pos < e:
            return True
    return False


# =========================
# 🔍 BUILD MATCHES
# =========================
def build(text, lang):
    rules = LANG.get(lang)
    if not rules:
        return []

    matches = []
    blocked = []

    # STRING
    for r in rules["str"]:
        for m in r.finditer(text):
            blocked.append((m.start(), m.end()))
            matches.append((m.start(), m.end(), STRING_COLOR))

    # COMMENT
    for r in rules["com"]:
        for m in r.finditer(text):
            blocked.append((m.start(), m.end()))
            matches.append((m.start(), m.end(), COMMENT_COLOR))

    # KEYWORDS
    for category, words in rules["kw"].items():
        color = COLOR_MAP.get(category, "#00d4ff")

        for kw in words:
            for m in re.finditer(rf"\b{kw}\b", text):
                if in_ranges(m.start(), blocked):
                    continue
                matches.append((m.start(), m.end(), color))

    # NUMBER
    for m in re.finditer(r"\b\d+(\.\d+)?\b", text):
        if in_ranges(m.start(), blocked):
            continue
        matches.append((m.start(), m.end(), NUMBER_COLOR))

    # FUNCTION NAME
    func_pattern = re.compile(r"\b([a-zA-Z_]\w*)\s*\(")

    all_keywords = sum(rules["kw"].values(), [])

    for m in func_pattern.finditer(text):
        name = m.group(1)
        start = m.start(1)

        if in_ranges(start, blocked):
            continue

        if name in all_keywords:
            continue

        matches.append((start, m.end(1), f"underline {FUNCTION_COLOR}"))

    # CUSTOM WORD
    for kw, color in CUSTOM_WORDS.items():
        for m in re.finditer(rf"\b{kw}\b", text):
            if in_ranges(m.start(), blocked):
                continue
            matches.append((m.start(), m.end(), color))

    return matches


# =========================
# 🎨 APPLY
# =========================
def apply(text, matches):
    t = Text(text)

    for s, e, c in sorted(matches, key=lambda x: x[0], reverse=True):
        t.stylize(c, s, e)

    return t


# =========================
# 🚀 MAIN
# =========================
def main():
    args = sys.argv

    if len(args) < 2:
        console.print("[#ff4b4b]Usage: hcat (ext) filename[/#ff4b4b]")
        sys.exit(1)

    if len(args) == 3:
        ext, name = args[1], args[2]
        file = f"{name}.{ext}"
        lang = ext
    else:
        file = args[1]
        lang = file.split(".")[-1] if "." in file else None

    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        console.print("[#ff4b4b]File error[/#ff4b4b]")
        sys.exit(1)

    matches = build(content, lang)
    styled = apply(content, matches)

    console.print(styled)


# =========================
# 🎯 DEFAULT CUSTOM
# =========================
addhighlight("print", "#ff4b4b")


if __name__ == "__main__":
    main()