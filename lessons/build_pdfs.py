"""Create a styled PDF handbook for each session containing Markdown lessons.

Run from any directory: python lessons/build_pdfs.py
Individual documents: python lessons/build_pdfs.py --session session_04 --individual
Requires WeasyPrint, markdown-it-py, and Pygments.
"""

import argparse
from html import escape
import logging
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlsplit

from markdown_it import MarkdownIt
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.util import ClassNotFound
from weasyprint import HTML


ROOT = Path(__file__).resolve().parent
CSS = r"""
@font-face {
  font-family: Handbook;
  src: url("file:///usr/share/fonts/truetype/dejavu/DejaVuSans.ttf");
}
@font-face {
  font-family: Handbook;
  font-weight: 700;
  src: url("file:///usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf");
}
@font-face {
  font-family: Code;
  src: url("file:///usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf");
}
@page {
  size: Letter;
  margin: 0.78in 0.72in 0.72in;
  @top-left {
    content: "FABRIC  /  SESSION " string(session-number);
    font: 7.5pt Handbook;
    color: #617580;
    vertical-align: bottom;
    padding-bottom: 0.16in;
    border-bottom: 0.5pt solid #dce6e8;
  }
  @top-right {
    content: string(chapter-title);
    font: 7pt Handbook;
    color: #617580;
    vertical-align: bottom;
    padding-bottom: 0.16in;
    border-bottom: 0.5pt solid #dce6e8;
  }
  @bottom-left {
    content: "LOW-CODE FABRIC DATA ENGINEERING";
    font: 7pt Handbook;
    color: #617580;
  }
  @bottom-right {
    content: counter(page, decimal-leading-zero);
    font: 8pt Handbook;
    font-weight: 700;
    color: #087f8c;
  }
}
@page cover {
  margin: 0;
  @top-left { content: none; border: none; }
  @top-right { content: none; border: none; }
  @bottom-left { content: none; }
  @bottom-right { content: none; }
}
* { box-sizing: border-box; }
html { font-family: Handbook, sans-serif; color: #193540; font-size: 10pt; }
body { margin: 0; line-height: 1.5; }
a { color: #087580; text-decoration: none; }
strong { font-weight: 700; }
p { margin: 0 0 8pt; orphans: 3; widows: 3; }
h1, h2, h3 { line-height: 1.25; break-after: avoid; }
h1 { font-size: 29pt; letter-spacing: -0.8pt; margin: 12pt 0 18pt; }
h2 {
  font-size: 15pt; letter-spacing: -0.25pt;
  margin: 18pt 0 9pt; color: #123d4b;
  bookmark-level: 2;
}
h3 { font-size: 11pt; margin: 17pt 0 8pt; color: #087580; bookmark-level: 3; }
ul, ol { padding-left: 19pt; margin: 8pt 0 13pt; }
li { margin-bottom: 5pt; orphans: 2; widows: 2; }
li p { margin-bottom: 5pt; }
blockquote {
  border-left: 3pt solid #08929c;
  background: #edf7f4;
  padding: 11pt 15pt;
  margin: 15pt 0;
  color: #164a50;
  break-inside: avoid;
}
blockquote p:last-child { margin-bottom: 0; }
code { font-family: Code, monospace; font-size: 0.88em; color: #14586a; }
p code, li code, td code {
  background: #eef3f5; padding: 1pt 3pt;
  overflow-wrap: anywhere;
}
pre {
  margin: 0; font: 8.1pt/1.55 Code, monospace;
  white-space: pre-wrap; overflow-wrap: anywhere; tab-size: 4;
}
pre code { font-size: inherit; color: #193540; }
.codeblock {
  margin: 13pt 0 16pt;
  padding: 11pt 13pt;
  background: #f1f5f7;
  border-left: 2pt solid #9fc8cc;
  box-decoration-break: clone;
}
.codeblock.short { break-inside: avoid; }
.code-label {
  font-size: 7pt; font-weight: 700;
  color: #087580; letter-spacing: 1pt;
  margin-bottom: 8pt; break-after: avoid;
}
.highlight .k, .highlight .kc, .highlight .kd, .highlight .kn,
.highlight .kp, .highlight .kr, .highlight .kt { color: #005f79; font-weight: 700; }
.highlight .s, .highlight .s1, .highlight .s2 { color: #8b4c20; }
.highlight .c, .highlight .c1, .highlight .cm { color: #526b70; }
.highlight .m, .highlight .mi, .highlight .mf { color: #6d4080; }
table {
  width: 100%; border-collapse: collapse; table-layout: auto;
  font-size: 8.2pt; line-height: 1.45; margin: 12pt 0 15pt;
  break-inside: avoid;
}
thead { display: table-header-group; }
tr { break-inside: avoid; }
th {
  background: #173b49; color: white;
  font-size: 8pt; font-weight: 700;
  text-align: left; padding: 7pt 8pt;
  border: 0.5pt solid #173b49;
}
td {
  padding: 7pt 8pt; vertical-align: top;
  border-bottom: 0.5pt solid #dbe6e9;
  overflow-wrap: anywhere;
}
tbody tr:nth-child(even) { background: #f0f5f7; }
.cover {
  page: cover; break-after: page;
  width: 8.5in; height: 11in;
  background: #132f3e; color: white;
  padding: 0.77in;
  position: relative; overflow: hidden;
}
.cover:before {
  content: ""; position: absolute;
  top: 0; left: 0; width: 8.5in; height: 0.1in; background: #21b9a9;
}
.eyebrow { font-size: 8pt; letter-spacing: 1.8pt; font-weight: 700; color: #087580; }
.cover .eyebrow { color: #9cdbd1; }
.cover-kicker { margin-top: 0.85in; font-size: 10pt; color: #9cdbd1; letter-spacing: 2pt; }
.cover h1 {
  font-size: 43pt; line-height: 1.12; letter-spacing: -1.9pt;
  margin: 22pt 0; color: white; bookmark-level: none;
}
.cover-deck { width: 5.85in; font-size: 15pt; line-height: 1.55; color: #c5dce2; }
.cover-date { margin-top: 25pt; color: #9cdbd1; font-size: 10pt; }
.cover-bottom {
  position: absolute; left: 0.77in; right: 0.77in; bottom: 0.7in;
  border-top: 0.5pt solid #4f717c; padding-top: 20pt;
}
.cover-stats { display: flex; gap: 30pt; }
.stat { flex: 1; }
.stat b { display: block; font-size: 25pt; color: white; }
.stat span { font-size: 8pt; color: #b6d1d7; }
.cover-format { margin: 19pt 0 0; font-size: 8pt; letter-spacing: 1pt; color: #9cdbd1; }
.contents { break-after: page; }
.contents h1 { margin-top: 9pt; bookmark-level: 1; }
.intro { color: #526b75; font-size: 11pt; margin-bottom: 18pt; }
.toc-row {
  display: block; padding: 10pt 0;
  border-bottom: 0.6pt solid #dce6e8;
  break-inside: avoid; color: #193540;
}
.toc-number { display: inline-block; width: 31pt; font-weight: 700; color: #087f8c; }
.toc-label { display: inline-block; width: 350pt; vertical-align: top; }
.toc-label b { display: block; font-size: 11pt; line-height: 1.3; }
.toc-label small { display: block; font-size: 8pt; color: #617580; margin-top: 4pt; }
.toc-page { float: right; color: #087f8c; font-size: 10pt; }
.toc-page:after { content: target-counter(attr(href), page, decimal-leading-zero); }
.reader-note {
  border-top: 2pt solid #087f8c; background: #f0f6f6;
  padding: 10pt 15pt; margin-top: 16pt; font-size: 9pt;
  break-inside: avoid;
}
.reader-note strong { display: block; color: #087580; margin-bottom: 5pt; }
.lesson { break-before: page; }
.lesson-number { string-set: session-number attr(data-session); }
.lesson h1 { bookmark-level: 1; string-set: chapter-title attr(data-short-title); }
.lesson-label { font-size: 8pt; font-weight: 700; color: #087580; letter-spacing: 1.2pt; }
.lesson-summary {
  background: #e9f5f0; border-left: 3pt solid #16a085;
  padding: 13pt 15pt; margin: 0 0 20pt;
  break-inside: avoid;
}
.lesson-summary .eyebrow { margin-bottom: 5pt; letter-spacing: 1pt; }
.lesson-summary p { margin: 0; font-size: 10pt; }
.reference-line { font-size: 8pt; color: #526b75; }
.navigation { font-size: 8pt; padding-top: 9pt; border-top: 0.5pt solid #dce6e8; }
.lesson-end { break-inside: avoid; }
.practice-and-close { break-inside: avoid; }
"""


def make_markdown(lesson_targets):
    formatter = HtmlFormatter(nowrap=True)

    def highlight_code(value, language, _attrs):
        try:
            lexer = get_lexer_by_name(language or "text")
        except ClassNotFound:
            lexer = TextLexer()
        return highlight(value, lexer, formatter)

    md = MarkdownIt("commonmark", {"html": False, "highlight": highlight_code})
    md.enable("table")
    default_link = md.renderer.rules.get("link_open")

    def link_open(tokens, index, options, env):
        token = tokens[index]
        href = token.attrGet("href") or ""
        filename = href.split("#")[0].split("/")[-1]
        if filename in lesson_targets:
            token.attrSet("href", "#" + lesson_targets[filename])
        elif href and not re.match(r"^(https?://|mailto:|#)", href):
            token.attrSet("href", "#contents")
        if default_link:
            return default_link(tokens, index, options, env)
        return md.renderer.renderToken(tokens, index, options, env)

    def fence(tokens, index, options, env):
        token = tokens[index]
        language = token.info.strip().split()[0] if token.info.strip() else "text"
        content = highlight_code(token.content, language, "")
        short = " short" if len(token.content.splitlines()) <= 22 else ""
        return (
            f'<div class="codeblock{short}">'
            f'<div class="code-label">{escape(language.upper())}</div>'
            f'<pre class="highlight"><code>{content}</code></pre></div>'
        )

    md.renderer.rules["link_open"] = link_open
    md.renderer.rules["fence"] = fence
    return md


def read_lesson(path, index):
    source = path.read_text()
    lines = source.splitlines()
    title = lines[0].lstrip("# ").strip()
    short_title = re.sub(r"^Lesson \d+:\s*", "", title)
    match = re.search(r"\*\*Session (\d+) \| ([^|]+) \| (\d+) minutes\*\*", source)
    if not match:
        raise ValueError(f"Missing session/date/duration metadata in {path}")
    session, date, minutes = match.groups()
    output = re.search(r"\*\*Lesson output:\*\*\s*(.+)", source)
    if not output:
        raise ValueError(f"Missing lesson output in {path}")
    content = "\n".join(
        line for line in lines[1:]
        if not line.startswith(("**Session ", "**Blueprint:", "**Lesson output:"))
    ).strip()
    return {
        "path": path,
        "id": f"lesson-{index}",
        "title": title,
        "short_title": short_title,
        "minutes": int(minutes),
        "session": session,
        "date": date.strip(),
        "output": output.group(1),
        "content": content,
    }


def build_session(session_dir):
    sources = sorted(session_dir.glob("[0-9][0-9]_*.md"))
    if not sources:
        print(f"Skipped {session_dir.name}: no lesson Markdown.")
        return
    lessons = [read_lesson(path, i) for i, path in enumerate(sources, 1)]
    number = lessons[0]["session"]
    if any(item["session"] != number for item in lessons):
        raise ValueError(f"Mixed session numbers in {session_dir}")
    date = lessons[0]["date"]
    minutes = sum(item["minutes"] for item in lessons)
    title = "Low-code Fabric Data Engineering" if number == "3" else f"Fabric Training / Session {number}"
    targets = {item["path"].name: item["id"] for item in lessons}
    md = make_markdown(targets)
    toc = []
    chapters = []
    for i, item in enumerate(lessons, 1):
        target = item["id"]
        toc.append(
            f'<a class="toc-row" href="#{target}">'
            f'<span class="toc-number">{i:02d}</span>'
            f'<span class="toc-label"><b>{escape(item["short_title"])}</b>'
            f'<small>{item["minutes"]} minutes</small></span>'
            f'<span class="toc-page" href="#{target}"></span></a>'
        )
        content = md.render(item["content"])
        content = re.sub(
            r"<p>(<strong>(?:Product references?|Environment boundary):)",
            r'<p class="reference-line">\1', content,
        )
        content = re.sub(
            r"<p>(<strong>(?:Previous|Next|Session outline):)",
            r'<p class="navigation">\1', content,
        )
        conclusion = content.find("<h2>Lesson conclusion</h2>")
        if conclusion >= 0:
            content = (
                content[:conclusion] + '<div class="lesson-end">'
                + content[conclusion:] + "</div>"
            )
        final_practice = content.rfind("<h3>Practice:")
        if final_practice >= 0:
            content = (
                content[:final_practice] + '<div class="practice-and-close">'
                + content[final_practice:] + "</div>"
            )
        chapters.append(
            f'<article class="lesson" id="{target}">'
            f'<div class="lesson-number" data-session="{escape(number)}"></div>'
            f'<div class="lesson-label">LESSON {i:02d} / {item["minutes"]} MINUTES</div>'
            f'<h1 data-short-title="Lesson {i:02d}">{escape(item["short_title"])}</h1>'
            f'<div class="lesson-summary"><div class="eyebrow">WHAT YOU WILL PRODUCE</div>'
            f'<p>{escape(item["output"])}</p></div>'
            f'{content}</article>'
        )
    display_title = "Low-code Fabric<br>Data Engineering" if number == "3" else escape(title)
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Session {number} | {escape(title)}</title>
<meta name="author" content="Brandon Campbell">
<meta name="description" content="Session {number} teaching handbook: {len(lessons)} lessons, {minutes} minutes.">
<style>{CSS}</style></head><body>
<section class="cover">
  <div class="eyebrow">FABRIC / PRACTITIONER SERIES</div>
  <div class="cover-kicker">SESSION {int(number):02d} / TEACHING HANDBOOK</div>
  <h1>{display_title}</h1>
  <p class="cover-deck">From source extracts to an explainable,<br>repeatable, governed analytical workload.</p>
  <p class="cover-date">{escape(date)}<br>SQL and Power Query practitioners</p>
  <div class="cover-bottom">
    <div class="cover-stats">
      <div class="stat"><b>{len(lessons):02d}</b><span>DEVELOPED LESSONS</span></div>
      <div class="stat"><b>{minutes}</b><span>MINUTES OF LEARNING</span></div>
      <div class="stat"><b>SQL-first</b><span>PRACTICAL DELIVERY</span></div>
    </div>
    <p class="cover-format">CONCEPTS / WORKED EXAMPLES / PRACTICE / OPERATIONS</p>
  </div>
</section>
<section class="contents" id="contents">
  <div class="lesson-number" data-session="{escape(number)}"></div>
  <div class="eyebrow">YOUR LEARNING PATH</div>
  <h1>From decision to delivery</h1>
  <p class="intro">One reconciliation workload connects the lessons. Follow the decisions,
  engineering patterns, and operating controls from source to consumer.</p>
  {''.join(toc)}
  <div class="reader-note"><strong>How to use this handbook</strong>
  Read the explanations, inspect the worked examples, and complete each lesson's output.
  Contents and lesson links are clickable; PDF bookmarks provide section-level navigation.</div>
  <div class="reader-note"><strong>Environment and execution boundary</strong>
  Examples use synthetic data and an isolated training Warehouse. Validate live paths in the
  target GCC High tenant. General documentation is not proof of tenant availability.
  SQL examples require preflight before execution.</div>
</section>
{''.join(chapters)}
</body></html>"""
    output_dir = session_dir / "pdf"
    output_dir.mkdir(exist_ok=True)
    output = output_dir / f"{session_dir.name}_teaching_handbook.pdf"
    HTML(string=document, base_url=str(session_dir)).write_pdf(output, pdf_tags=True)
    print(f"Created {output} ({output.stat().st_size:,} bytes)")


def build_individual_documents(session_dir):
    output_dir = session_dir / "pdf"
    sources = sorted(
        path for path in session_dir.rglob("*.md") if output_dir not in path.parents
    )
    repository_url = "https://github.com/Coding-Forge/FabricGovTraining"
    number = session_dir.name.rsplit("_", 1)[1]
    document_css = CSS + f"""
@page {{
  @top-left {{ content: "FABRIC / SESSION {number}"; }}
  @top-right {{ content: "NOTEBOOKS / PRACTICAL GUIDE"; }}
  @bottom-left {{ content: "FABRIC NOTEBOOK TRAINING"; }}
}}
h1 {{ font-size: 24pt; bookmark-level: 1; }}
table {{ table-layout: fixed; break-inside: auto; }}
th {{ overflow-wrap: anywhere; }}
.source-note {{ font-size: 8pt; color: #526b75; margin-top: 20pt; }}
"""
    outputs = []
    for source in sources:
        text = source.read_text(encoding="utf-8")
        title = next(line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("# "))
        md = make_markdown({})

        def link_open(tokens, index, options, env):
            token = tokens[index]
            href = token.attrGet("href") or ""
            parsed = urlsplit(href)
            if href and not parsed.scheme and not parsed.netloc and not href.startswith("#"):
                target = (source.parent / unquote(parsed.path)).resolve()
                relative = target.relative_to(ROOT.parent)
                kind = "tree" if target.is_dir() else "blob"
                url = f"{repository_url}/{kind}/main/{quote(relative.as_posix())}"
                if parsed.fragment:
                    url += "#" + parsed.fragment
                token.attrSet("href", url)
            return md.renderer.renderToken(tokens, index, options, env)

        def heading_ids(state):
            seen = {}
            for index, token in enumerate(state.tokens):
                if token.type == "heading_open":
                    label = state.tokens[index + 1].content
                    slug = re.sub(r"[^\w\- ]", "", label.lower()).replace(" ", "-")
                    occurrence = seen.get(slug, 0)
                    seen[slug] = occurrence + 1
                    token.attrSet("id", slug if not occurrence else f"{slug}-{occurrence}")

        md.renderer.rules["link_open"] = link_open
        md.core.ruler.after("inline", "heading_ids", heading_ids)
        relative = source.relative_to(session_dir)
        source_url = f"{repository_url}/blob/main/{quote(source.relative_to(ROOT.parent).as_posix())}"
        document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{escape(title)}</title>
<style>{document_css}</style></head><body>
<div class="lesson-label">SESSION {escape(number)} / PRINTABLE GUIDE</div>
{md.render(text)}
<p class="source-note">Source: <a href="{escape(source_url)}">{escape(relative.as_posix())}</a>.
Companion-material links open the repository originals.</p>
</body></html>"""
        output = output_dir / relative.with_suffix(".pdf")
        output.parent.mkdir(parents=True, exist_ok=True)
        HTML(string=document, base_url=str(source.parent)).write_pdf(output, pdf_tags=True)
        outputs.append(output)
        print(f"Created {output} ({output.stat().st_size:,} bytes)")
    return outputs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", choices=sorted(path.name for path in ROOT.glob("session_[0-9][0-9]") if path.is_dir()))
    parser.add_argument("--individual", action="store_true", help="Render each Markdown file separately, preserving subfolders.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING)
    directories = [ROOT / args.session] if args.session else sorted(ROOT.glob("session_[0-9][0-9]"))
    for directory in directories:
        if directory.is_dir():
            if args.individual:
                build_individual_documents(directory)
            else:
                build_session(directory)
