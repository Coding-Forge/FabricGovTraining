"""Build the Session 03 presenter guide using the existing handbook style.

Run: python lessons/session_03/artifacts/build_delivery_guide.py
"""

from html import escape
from pathlib import Path
import re
import sys

from weasyprint import HTML


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT.parent))
from build_pdfs import CSS, make_markdown


def build():
    source = (ROOT / "delivery_guide.md").read_text()
    md = make_markdown({})
    tokens = md.parse("\n".join(source.splitlines()[1:]))
    toc = []
    number = 0
    for i, token in enumerate(tokens):
        if token.type == "table_open":
            first_cell = next(
                (cell.content for cell in tokens[i + 1:] if cell.type == "inline"),
                "",
            )
            if first_cell == "ET window":
                token.attrSet("class", "time-table")
        if token.type == "heading_open" and token.tag == "h2":
            number += 1
            target = f"delivery-{number}"
            token.attrSet("id", target)
            label = re.sub(r"^\d+\.\s*", "", tokens[i + 1].content)
            toc.append(
                f'<a class="toc-row" href="#{target}">'
                f'<span class="toc-number">{number:02d}</span>'
                f'<span class="toc-label"><b>{escape(label)}</b></span>'
                f'<span class="toc-page" href="#{target}"></span></a>'
            )
        if token.type != "inline":
            continue
        link_stack = []
        for child in token.children or []:
            if child.type == "link_open":
                href = child.attrGet("href") or ""
                external_file = not re.match(r"^(https?://|mailto:|#)", href)
                link_stack.append(external_file)
                if external_file:
                    child.tag = "span"
                    child.attrs = {}
            elif child.type == "link_close" and link_stack.pop():
                child.tag = "span"
    content = md.renderer.render(tokens, md.options, {})
    style = CSS + """
    @page { @bottom-left { content: "SESSION 03 / CUSTOMER DELIVERY GUIDE"; } }
    html { font-size: 9.5pt; }
    body { line-height: 1.4; }
    p { margin-bottom: 6pt; }
    h2 { font-size: 16pt; string-set: chapter-title content(); bookmark-level: 1; }
    h3 { margin-top: 12pt; bookmark-level: 2; }
    blockquote { padding: 10pt 14pt; }
    th, td { padding: 6pt 8pt; }
    .time-table th:first-child, .time-table td:first-child {
      white-space: nowrap; width: 1.05in; font-size: 7.7pt;
    }
    .toc-row { padding: 7pt 0; }
    .toc-label b { font-size: 10pt; }
    """
    document = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
    <title>Session 03 | Customer Delivery Guide</title>
    <meta name="author" content="Brandon Campbell">
    <meta name="description" content="Integrated presenter run of show for the Session 03 deck, lessons, labs, and customer handoff.">
    <style>{style}</style></head><body>
    <section class="cover">
      <div class="eyebrow">FABRIC / PRACTITIONER SERIES</div>
      <div class="cover-kicker">SESSION 03 / PRESENTER DELIVERY GUIDE</div>
      <h1>Deliver one<br>connected<br>experience.</h1>
      <p class="cover-deck">The presentation, lessons, and labs:<br>one fluid customer delivery, from opening to handoff.</p>
      <p class="cover-date">October 28, 2026 / 11:00 AM-2:00 PM ET<br>Lead: Brandon Campbell</p>
      <div class="cover-bottom"><div class="cover-stats">
        <div class="stat"><b>180</b><span>MINUTES / ONE RUN OF SHOW</span></div>
        <div class="stat"><b>54</b><span>SLIDES / EXACT HANDOFFS</span></div>
        <div class="stat"><b>06</b><span>LESSONS AND INTEGRATED LABS</span></div>
      </div><p class="cover-format">PREPARE / EXPLAIN / DEMONSTRATE / APPLY / DEBRIEF</p></div>
    </section>
    <section class="contents" id="contents">
      <div class="lesson-number" data-session="3"></div>
      <div class="eyebrow">PRESENTER NAVIGATION</div><h1>Delivery at a glance</h1>
      <p class="intro">Keep this guide on the private presenter screen. Participants use the lab workbook;
      the teaching handbook supplies the deeper explanations.</p>
      {''.join(toc)}
    </section>
    <article class="guide">{content}</article>
    </body></html>"""
    output = ROOT / "pdf/session_03_delivery_guide.pdf"
    output.parent.mkdir(exist_ok=True)
    HTML(string=document, base_url=str(ROOT)).write_pdf(output, pdf_tags=True)
    print(f"Created {output} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build()
