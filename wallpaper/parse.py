"""Parse the cheat sheet markdown files into a simple model and render HTML fragments."""
import html
import re
from pathlib import Path

TOOLS = [
    # file, id, display name, subtitle, nerd-font icon
    ("NeoVim.md", "nvim", "Neovim", "leader = Space", ""),
    ("Tmux.md", "tmux", "tmux", "prefix = Ctrl+B", ""),
    ("VSCode.md", "code", "VS Code", "& desktop", "\U000f0a1e"),
]

# tmux sections whose keys are typed after the prefix
TMUX_PREFIXED = {"Help", "Copy / Paste", "Sessions", "Panes", "Windows"}
KEYNAMES = {"Ctrl", "Alt", "Shift", "Esc", "Tab", "Enter", "Space", "PgUp", "PgDn", "Home", "HOME"}

CODE_RE = re.compile(r"(`+)(.+?)\1")


def esc(s):
    return html.escape(s, quote=False)


def kbd(s):
    if s == "*":
        return '<sup class="star" title="my mapping">*</sup>'
    if re.fullmatch(r"((?:Ctrl|Alt|Shift)\+)+(.+)", s):
        return '<span class="plus">+</span>'.join(f"<kbd>{esc(p)}</kbd>" for p in s.split("+"))
    return f"<kbd>{esc(s)}</kbd>"


def is_emph(s):
    return len(s) > 1 and s not in KEYNAMES and re.fullmatch(r"[A-Za-z][A-Za-z ]*", s) is not None


def inline(text, key=False):
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    out, pos = [], 0
    for m in CODE_RE.finditer(text):
        out.append(sep(text[pos:m.start()], key))
        code = m.group(2)
        if len(m.group(1)) > 1:
            code = code.strip()
        out.append(f"<em>{esc(code)}</em>" if (not key and is_emph(code)) else kbd(code))
        pos = m.end()
    out.append(sep(text[pos:], key))
    return "".join(out)


def sep(s, key):
    if not s:
        return ""
    if not key:
        return esc(s)
    s2 = s.strip()
    if s2 == "+":
        return '<span class="plus">+</span>'
    if s2 in ("/", "or"):
        return f'<span class="sep">{esc(s2)}</span>'
    if not s2:
        return " "
    return f' <span class="kx">{esc(s2)}</span> '


def parse(path):
    sections, cur, parent, intro = [], None, None, []
    lines = Path(path).read_text().splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        i += 1
        if line.startswith("# "):
            continue
        if line.startswith("## ") or line.startswith("### "):
            lvl = 2 if line.startswith("## ") else 3
            title = line.split(" ", 1)[1].strip()
            if lvl == 2:
                parent = title
            cur = {"title": title, "parent": parent if lvl == 3 else None, "notes": [], "rows": []}
            sections.append(cur)
            continue
        if line.startswith("|"):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 1  # separator
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                i += 1
                row = {"k": inline(cells[0], key=True), "d": "", "badge": "", "meta": []}
                main_done = False
                for h, c in zip(header[1:], cells[1:]):
                    if h == "Mode":
                        row["badge"] = esc(c)
                    elif not main_done:
                        row["d"] = inline(c)
                        main_done = True
                    elif c and c != "N/A":
                        row["meta"].append((esc(h.replace(" Neovim", "")), inline(c)))
                cur["rows"].append(row)
            continue
        if not line.strip():
            continue
        m = re.fullmatch(r"`([^`]+)` to (.+?)\.?", line.strip())
        if m and cur is not None:
            d = m.group(2)
            cur["rows"].append({"k": inline(f"`{m.group(1)}`", key=True), "d": inline(d[0].upper() + d[1:]), "badge": "", "meta": []})
            continue
        (cur["notes"] if cur is not None else intro).append(inline(line.strip()))
    return intro, [s for s in sections if s["rows"] or s["notes"]]


def load(root):
    tools = []
    for fname, tid, name, sub, icon in TOOLS:
        intro, secs = parse(Path(root) / fname)
        for s in secs:
            s["prefix"] = tid == "tmux" and s["title"] in TMUX_PREFIXED
        tools.append({"id": tid, "name": name, "sub": sub, "icon": icon, "intro": intro, "sections": secs})
    return tools


def render_row(r):
    badge = f'<span class="badge">{r["badge"]}</span>' if r["badge"] else ""
    meta = "".join(f'<span class="meta"><span class="ml">{h}:</span> {v}</span>' for h, v in r["meta"])
    return f'<div class="r"><div class="k">{r["k"]}</div><div class="d">{badge}{r["d"]}{meta}</div></div>'


def render_section(tool, s):
    par = f'<span class="par">{esc(s["parent"])} ›</span> ' if s["parent"] else ""
    chip = '<span class="chip">prefix</span>' if s["prefix"] else ""
    notes = "".join(f'<div class="note">{n}</div>' for n in s["notes"])
    rows = [render_row(r) for r in s["rows"]]
    first = rows[0] if rows else ""
    head = f'<div class="keep"><div class="sh"><span class="st">{par}{esc(s["title"])}</span>{chip}</div>{notes}{first}</div>'
    return f'<div class="sec t-{tool["id"]}">{head}{"".join(rows[1:])}</div>'

