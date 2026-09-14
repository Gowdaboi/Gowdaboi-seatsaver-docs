#!/usr/bin/env python3
"""
Render README.md to README.html so the overview has a shareable link of its own.

Without this, "here is what the app does" means sending someone to a GitHub
repository page and asking them to read a source file. This produces a page that
matches privacy-policy.html and delete-account.html, so the three public pages
look like one site.

    python3 tools/build_readme_html.py

Deliberately a small converter rather than a dependency: this renders exactly
the Markdown README.md uses — headings, bold, inline code, links, bullet lists,
italics and paragraphs — and nothing else. If the README grows a table or an image,
extend this rather than assuming it silently worked.
"""
import html
import re

SRC, OUT = "README.md", "README.html"

STYLE = """
  :root {
    --bg: #fdf6f4; --fg: #2b2320; --muted: #6b5b55;
    --accent: #8c4a3c; --card: #ffffff; --border: #e8d9d4;
  }
  @media (prefers-color-scheme: dark) {
    :root {
      --bg: #1b1614; --fg: #f2e9e6; --muted: #b9a7a1;
      --accent: #e29684; --card: #261f1d; --border: #3a302d;
    }
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 32px 20px 64px;
    background: var(--bg); color: var(--fg);
    font: 16px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }
  main { max-width: 680px; margin: 0 auto; }
  h1 { font-size: 1.85rem; line-height: 1.2; margin: 0 0 20px; }
  h2 { font-size: 1.2rem; margin: 36px 0 10px; padding-top: 14px; border-top: 1px solid var(--border); }
  h3 { font-size: 1.02rem; margin: 26px 0 8px; color: var(--accent); }
  p { margin: 12px 0; }
  a { color: var(--accent); }
  ul { padding-left: 22px; margin: 12px 0; }
  li { margin: 6px 0; }
  strong { font-weight: 650; }
  em { font-style: italic; }
  code {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 4px; padding: 1px 5px; font-size: 0.9em;
  }
  footer {
    margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--border);
    color: var(--muted); font-size: 0.9rem;
  }
"""


def inline(t):
    """Escape first, then re-introduce only the markup we intend."""
    t = html.escape(t, quote=False)
    t = re.sub(r'`([^`]+)`', r'<code>\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    t = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', t)
    # after strong, so the ** pairs are already consumed
    t = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', t)
    return t


def convert(md):
    out, para, in_list = [], [], False

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in md.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            flush_para(); close_list(); continue
        h = re.match(r'^(#{1,3})\s+(.*)$', line)
        if h:
            flush_para(); close_list()
            lvl = len(h.group(1))
            out.append(f"<h{lvl}>{inline(h.group(2))}</h{lvl}>")
            continue
        b = re.match(r'^[-*]\s+(.*)$', line)
        if b:
            flush_para()
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append("<li>" + inline(b.group(1)) + "</li>")
            continue
        if in_list and line.startswith("  "):
            # continuation of the previous bullet
            out[-1] = out[-1][:-len("</li>")] + " " + inline(line.strip()) + "</li>"
            continue
        close_list()
        para.append(line.strip())
    flush_para(); close_list()
    return "\n".join(out)


def main():
    md = open(SRC).read()
    body = convert(md)
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Seat Saver — overview</title>
<meta name="description" content="Seating and service management for catered events, built for Indian wedding-style functions where guests are seated and served in timed rounds.">
<link rel="icon" href="favicon.png">
<style>{STYLE}</style>
</head>
<body>
<main>
{body}
<footer>
  <a href="index.html">Open the app</a> ·
  <a href="privacy-policy.html">Privacy policy</a> ·
  <a href="delete-account.html">Delete your account</a>
</footer>
</main>
</body>
</html>
"""
    open(OUT, "w").write(page)
    print(f"{OUT}  {len(page):,} bytes")


if __name__ == "__main__":
    main()
