"""Render the cheat sheets (../*.md) as a desktop wallpaper, "Neon · Midnight Teal".

usage: python3 build.py [out dir]        (default: this script's folder)

Writes cheatsheet-wallpaper.png (2560x1440) and cheatsheet-wallpaper@2x.png (5120x2880).
Needs Firefox (headless screenshots) and the Fira Sans Condensed, MesloLGS Nerd Font fonts.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from parse import load, render_section

W, H = 2560, 1440
HERE = Path(__file__).resolve().parent
NAME = "cheatsheet-wallpaper"

# Palette. a1 = Neovim accent, a2 = tmux, a3 = VS Code; key = key names, hl = highlighted words.
THEME = {
    "bg": "#06121a", "fg": "#c9d6d8", "muted": "#6f8b91", "line": "#16303a",
    "a1": "#4fd1c5", "a2": "#e6b450", "a3": "#e07a6f", "key": "#7fe0d6", "hl": "#e6b450",
    "kbd-bg": "rgba(79,209,197,.10)", "card": "rgba(4,14,20,.85)", "card-border": "#2c7a74",
    "titlebar": "rgba(79,209,197,.08)", "grid": "rgba(79,209,197,.16)",
    "sky1": "#040c12", "sky2": "#0a1e26", "sky3": "#0c2626",
    "ui": "'Fira Sans Condensed',sans-serif", "mono": "'MesloLGS Nerd Font Mono',monospace",
    "icon": "'MesloLGS Nerd Font','Symbols Nerd Font'",
}

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(W)dpx;height:%(H)dpx;overflow:hidden}
:root{--fs:14px;--sp:0;--ratio:.62;--nc:4;--tc:2;--pad:22px;--gap:22px;--kw:6.2em}
body{color:var(--fg);font:400 var(--fs)/1.28 var(--ui);-webkit-font-smoothing:antialiased;
 background:linear-gradient(180deg,var(--sky1) 0,var(--sky2) 55%%,var(--sky3) 100%%)}
/* perspective grid floor */
body::before{content:'';position:fixed;left:0;right:0;bottom:0;height:45%%;transform:perspective(500px) rotateX(55deg);transform-origin:bottom;
 background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:60px 60px}
#stage{width:100%%;height:100%%;padding:var(--pad);display:grid;gap:var(--gap);
 grid-template-columns:calc(var(--ratio)*100%% - var(--gap)/2) 1fr;grid-template-rows:1fr auto}

/* one window per tool: Neovim on the left, tmux top right, VS Code bottom right */
.panel{position:relative;display:flex;flex-direction:column;min-height:0;min-width:0;background:var(--card);border-radius:12px;
 border:1px solid var(--card-border);overflow:hidden;box-shadow:0 0 24px color-mix(in srgb,var(--card-border) 30%%,transparent)}
.p-nvim{grid-row:1/span 2}
.ph{display:flex;align-items:baseline;gap:.5em;background:var(--titlebar);padding:.45em .9em;margin-bottom:.7em;border-bottom:1px solid var(--line)}
.ph::before{content:'';width:.75em;height:.75em;border-radius:50%%;background:#c4524c;box-shadow:1.1em 0 0 #c49a3a,2.2em 0 0 #3f9a4a;margin-right:3em;align-self:center}
.ph .ico{font-family:var(--icon);font-weight:400;font-size:1.7em}
.ph .tn{font:700 1.15em/1 var(--ui)}
.ph .ts{color:var(--muted);font-size:.9em}
.cols{flex:1;min-height:0;padding:0 .9em .4em;column-count:var(--nc);column-gap:var(--gap);column-fill:balance;overflow:hidden}
.p-tmux .cols,.p-code .cols{column-count:var(--tc)}
.p-code .cols{flex:none}

.keep,.r,.note{break-inside:avoid}
.sec{margin-bottom:calc(.75em + var(--sp)*2em);box-decoration-break:clone}
.sh{display:flex;align-items:baseline;gap:.5em;font:700 1.08em/1.2 var(--ui);margin-bottom:.3em;padding-bottom:.15em;
 border-bottom:1px solid color-mix(in srgb,var(--acc) 45%%,transparent)}
.ph .tn,.sh{text-shadow:0 0 8px color-mix(in srgb,currentColor 45%%,transparent)}
.st{flex:1}
.par{font-weight:400;opacity:.65;font-size:.85em}
.chip{font:600 .68em/1 var(--mono);padding:.25em .45em;border-radius:.3em;background:var(--line);color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.note{color:var(--muted);font-size:.86em;margin:.1em 0 .35em;line-height:1.25}
.r{display:flex;gap:.6em;padding:calc(.14em + var(--sp)*1em) 0;align-items:baseline}
.k{flex:0 0 auto;min-width:var(--kw);max-width:62%%;font-family:var(--mono);font-size:.92em}
.d{flex:1;min-width:0}
kbd{font:inherit;font-family:var(--mono);color:var(--key);white-space:pre;background:var(--kbd-bg);padding:.02em .32em;border-radius:.3em}
.d kbd{font-size:.9em}
.d em{font-style:normal;color:var(--hl)}
.plus,.sep{color:var(--muted);margin:0 .12em;font-family:var(--mono);font-size:.85em}
.kx{color:var(--muted);font-size:.82em;font-family:var(--ui)}
.star{color:var(--hl);font-weight:700}
.badge{font:600 .7em/1 var(--mono);padding:.15em .35em;border-radius:.25em;border:1px solid var(--line);color:var(--muted);margin-right:.4em;vertical-align:.1em}
.meta{display:block;color:var(--muted);font-size:.85em}
.ml{opacity:.8}
.t-nvim{--acc:var(--a1)} .t-tmux{--acc:var(--a2)} .t-code{--acc:var(--a3)}
.sh,.ph .tn,.ph .ico{color:var(--acc)}
"""

# Try a few layouts (width split x column counts), binary-search the largest font that fits
# without overflow, then spread rows out to fill leftover height. The #z= zoom (for the 2x render)
# is applied only afterwards, so both renders get the same layout.
FIT_JS = """
(function(){
const cfgs=%(CFGS)s, root=document.documentElement;
const fits=()=>{for(const e of document.querySelectorAll('.fit'))if(e.scrollHeight>e.clientHeight+1||e.scrollWidth>e.clientWidth+1)return false;
 const b=document.body;return b.scrollHeight<=b.clientHeight+1&&b.scrollWidth<=b.clientWidth+1;};
const set=(o)=>{for(const k in o)root.style.setProperty('--'+k,o[k]);};
const search=(lo,hi,apply,n)=>{for(let i=0;i<n;i++){const m=(lo+hi)/2;apply(m);if(fits())lo=m;else hi=m;}apply(lo);return lo;};
let best=null;
for(const c of cfgs){set(c);set({sp:0});const fs=search(6,40,v=>set({fs:v+'px'}),14);if(!best||fs>best.fs)best={c,fs};}
set(best.c);set({fs:best.fs+'px'});
const base=search(0,0.6,v=>set({sp:v}),12);
for(const e of document.querySelectorAll('.fit'))search(base,base+0.8,v=>e.style.setProperty('--sp',v),12);
const z=/z=([\\d.]+)/.exec(location.hash);if(z)root.style.zoom=z[1];
})();
"""


def build_html(tools):
    panels = []
    for t in tools:
        secs = "".join(render_section(t, s) for s in t["sections"])
        fit = "" if t["id"] == "code" else " fit"  # VS Code panel sizes to its content
        title = f'<span class="ico">{t["icon"]}</span><span class="tn">{t["name"]}</span><span class="ts">{t["sub"]}</span>'
        panels.append(f'<section class="panel p-{t["id"]} t-{t["id"]}"><div class="ph">{title}</div><div class="cols{fit}">{secs}</div></section>')
    cfgs = [{"ratio": r, "nc": nc} for r in (.56, .6, .64, .68) for nc in (3, 4)]
    css = CSS % {"W": W, "H": H} + ":root{" + "".join(f"--{k}:{v};" for k, v in THEME.items()) + "}"
    return (f'<!doctype html><html><head><meta charset="utf-8"><title>Cheat sheet wallpaper</title><style>{css}</style></head>'
            f'<body><main id="stage">{"".join(panels)}</main><script>{FIT_JS % {"CFGS": json.dumps(cfgs)}}</script></body></html>')


def render(html_path, png_path, scale):
    with tempfile.TemporaryDirectory() as prof:
        subprocess.run(["firefox", "--headless", "--no-remote", "--profile", prof, "--screenshot", str(png_path),
                        f"--window-size={W * scale},{H * scale}", f"{html_path.as_uri()}#z={scale}"],
                       check=True, timeout=180, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    if not shutil.which("firefox"):
        sys.exit("build.py: firefox not found on PATH; it is needed to render the wallpaper")
    out = Path(sys.argv[1]).expanduser().resolve() if len(sys.argv) > 1 else HERE
    out.mkdir(parents=True, exist_ok=True)
    html = build_html(load(HERE.parent))
    with tempfile.TemporaryDirectory() as tmp:
        hp = Path(tmp) / f"{NAME}.html"
        hp.write_text(html)
        render(hp, out / f"{NAME}.png", 1)
        render(hp, out / f"{NAME}@2x.png", 2)
    print(f"wrote {out / NAME}.png and {NAME}@2x.png")


if __name__ == "__main__":
    main()
