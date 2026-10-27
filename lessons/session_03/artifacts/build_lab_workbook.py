"""Build the participant lab PDF using the teaching handbook's visual style.

Run: python lessons/session_03/artifacts/build_lab_workbook.py
"""

from html import escape
from pathlib import Path
import re
import sys

from weasyprint import HTML


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT.parent))
from build_pdfs import CSS, make_markdown, read_lesson


def build():
    paths = sorted((ROOT / "labs").glob("0[1-6]_*.md"))
    if len(paths) != 6:
        raise ValueError("Expected six participant lab guides")
    labs = [read_lesson(path, i) for i, path in enumerate(paths, 1)]
    targets = {lab["path"].name: lab["id"] for lab in labs}
    targets["README.md"] = "setup"
    md = make_markdown(targets)
    toc = [
        '<a class="toc-row" href="#setup"><span class="toc-number">00</span>'
        '<span class="toc-label"><b>Setup, safety, assets, and reset</b>'
        '<small>Facilitator preflight before delivery</small></span>'
        '<span class="toc-page" href="#setup"></span></a>'
    ]
    chapters = []
    for i, lab in enumerate(labs, 1):
        title = lab["title"].split(": ", 1)[-1]
        toc.append(
            f'<a class="toc-row" href="#{lab["id"]}">'
            f'<span class="toc-number">{i:02d}</span>'
            f'<span class="toc-label"><b>{escape(title)}</b>'
            f'<small>{lab["minutes"]} minutes of integrated practice</small></span>'
            f'<span class="toc-page" href="#{lab["id"]}"></span></a>'
        )
        content = md.render(lab["content"])
        content = re.sub(
            r"<p><strong>(?:Previous|Next):</strong>.*?</p>",
            "", content, flags=re.S,
        )
        chapters.append(
            f'<article class="lesson" id="{lab["id"]}">'
            f'<div class="lesson-label">LAB {i:02d} / {lab["minutes"]} MINUTES</div>'
            f'<h1 data-short-title="Lab {i:02d}">{escape(title)}</h1>'
            f'<div class="lesson-summary"><div class="eyebrow">WHAT YOU WILL PRODUCE</div>'
            f'<p>{escape(lab["output"])}</p></div>{content}</article>'
        )
    setup = "\n".join((ROOT / "labs/README.md").read_text().splitlines()[1:])
    style = CSS + """
    @page { @bottom-left { content: "SESSION 03 / PARTICIPANT LAB WORKBOOK"; } }
    html { font-size: 9.5pt; }
    h2 { font-size: 13.5pt; margin-top: 16pt; }
    .lesson h1 { font-size: 26pt; }
    .lesson p { margin-bottom: 7pt; }
    .lesson li { margin-bottom: 4pt; }
    .lesson ul, .lesson ol { margin: 6pt 0 10pt; }
    .lesson-summary { padding: 11pt 15pt; }
    .contents .toc-row { padding: 8pt 0; }
    .contents .intro { margin-bottom: 12pt; }
    """
    document = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
    <title>Session 03 | Participant Lab Workbook</title>
    <meta name="author" content="Brandon Campbell">
    <meta name="description" content="Six integrated labs with setup, reset, assets, and completion checks.">
    <style>{style}</style></head><body>
    <section class="cover">
      <div class="eyebrow">FABRIC / PRACTITIONER SERIES</div>
      <div class="cover-kicker">SESSION 03 / PARTICIPANT LAB WORKBOOK</div>
      <h1>Build it.<br>Explain it.<br>Repeat it.</h1>
      <p class="cover-deck">Hands-on low-code Fabric data engineering:<br>from source files to a governed reconciliation result.</p>
      <p class="cover-date">October 28, 2026<br>Companion to the Session 03 teaching handbook</p>
      <div class="cover-bottom"><div class="cover-stats">
        <div class="stat"><b>06</b><span>GUIDED LABS</span></div>
        <div class="stat"><b>96</b><span>MINUTES OF INTEGRATED PRACTICE</span></div>
        <div class="stat"><b>SQL-first</b><span>SYNTHETIC DATA / EXPLICIT CHECKS</span></div>
      </div><p class="cover-format">SETUP / EXERCISES / EXPECTED RESULTS / RESET</p></div>
    </section>
    <section class="contents" id="contents">
      <div class="lesson-number" data-session="3"></div>
      <div class="eyebrow">YOUR PRACTICE PATH</div>
      <h1>One workload, six labs</h1>
      <p class="intro">Practice fits inside the existing three-hour session. Use the setup
      runbook first and retain evidence for every completion check.</p>
      {''.join(toc)}
      <div class="reader-note"><strong>Files and live execution</strong>
      The companion source package contains the CSV, SQL, and DAX assets. Paths are relative
      to lessons/session_03/. Validate all service paths in the target GCC High tenant;
      offline checks do not establish tenant readiness.</div>
    </section>
    <article class="lesson" id="setup"><div class="lesson-label">FACILITATOR PREFLIGHT</div>
      <h1 data-short-title="Setup and reset">Setup, safety,<br>and reset</h1>{md.render(setup)}
    </article>
    {''.join(chapters)}</body></html>"""
    output = ROOT / "pdf/session_03_lab_workbook.pdf"
    output.parent.mkdir(exist_ok=True)
    HTML(string=document, base_url=str(ROOT)).write_pdf(output, pdf_tags=True)
    print(f"Created {output} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
