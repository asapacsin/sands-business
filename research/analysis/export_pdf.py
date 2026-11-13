"""Render deliverables (Markdown) to HTML via pandoc, then to A4 PDF via headless Chromium (Playwright)."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DELIV = ROOT / "deliverables"
JS = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const [html, pdf] of JSON.parse(process.argv[1])) {
    await p.goto('file://' + html, { waitUntil: 'load' });
    await p.pdf({ path: pdf, format: 'A4', margin: { top: '16mm', bottom: '16mm', left: '16mm', right: '16mm' },
                  displayHeaderFooter: true, headerTemplate: '<span></span>',
                  footerTemplate: '<div style="font-size:7pt;width:100%;text-align:center;color:#888">Independent research using public information · <span class="pageNumber"></span>/<span class="totalPages"></span></div>' });
  }
  await b.close();
})();
"""
pairs = []
for name in ("A_report", "B_brief", "D_interview", "experiment_protocol"):
    md, html, pdf = DELIV / f"{name}.md", DELIV / f"{name}.html", DELIV / f"{name}.pdf"
    subprocess.run(["pandoc", str(md), "-s", "--embed-resources", "--css", str(DELIV / "print.css"),
                    "--resource-path", str(DELIV), "--metadata", f"pagetitle={name}", "-o", str(html)], check=True)
    pairs.append([str(html), str(pdf)])
import json
subprocess.run(["node", "-e", JS, json.dumps(pairs)], check=True)
for _, pdf in pairs:
    print(pdf)
