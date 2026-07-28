"""
generate_pdf_report.py
Combines ai_insights.md (the AI-written report) and the charts in the
charts/ folder into a single polished PDF: pizza_sales_report.pdf

Run this LAST, after app.py -> charts.py -> ai_insights.py have all
already run once.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
)

# ---------- 1. LOAD THE AI-WRITTEN REPORT TEXT ----------
with open("ai_insights.md", "r", encoding="utf-8") as f:
    report_text = f.read()

# ---------- 2. SET UP PDF STYLES ----------
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle", parent=styles["Title"], fontSize=22, spaceAfter=20
)
heading_style = ParagraphStyle(
    "HeadingStyle", parent=styles["Heading2"], spaceBefore=14, spaceAfter=8
)
body_style = ParagraphStyle(
    "BodyStyle", parent=styles["Normal"], fontSize=10.5, leading=15
)

# ---------- 3. BUILD THE LIST OF PDF ELEMENTS ----------
story = []

story.append(Paragraph("Pizza Sales Analytics Report", title_style))
story.append(Paragraph("AI-Generated Business Insights", styles["Normal"]))
story.append(Spacer(1, 20))

# ---------- 4. ADD CHARTS ----------
CHARTS_FOLDER = "charts"
chart_files = [
    ("top_pizzas.png", "Top Pizzas by Revenue"),
    ("category_quantity.png", "Pizzas Sold by Category"),
    ("monthly_trend.png", "Monthly Revenue Trend"),
    ("revenue_by_weekday.png", "Revenue by Day of Week"),
    ("peak_hours.png", "Peak Order Hours"),
]

for filename, caption in chart_files:
    filepath = os.path.join(CHARTS_FOLDER, filename)
    if os.path.exists(filepath):
        story.append(Paragraph(caption, heading_style))
        story.append(Image(filepath, width=6 * inch, height=3.5 * inch))
        story.append(Spacer(1, 14))

story.append(PageBreak())

# ---------- 5. ADD THE AI-WRITTEN TEXT REPORT ----------
# The AI writes in Markdown (**bold**, bullet points with *). We convert
# those simple Markdown symbols to the HTML tags ReportLab understands,
# line by line, since the report is short and doesn't need a full
# Markdown parser.

story.append(Paragraph("Full Written Report", heading_style))

for line in report_text.split("\n"):
    line = line.strip()

    if line == "":
        story.append(Spacer(1, 8))
        continue

    # Convert **bold** markdown into <b>bold</b> HTML tags
    while "**" in line:
        line = line.replace("**", "<b>", 1)
        line = line.replace("**", "</b>", 1)

    # Turn a line starting with "* " into a bullet point
    if line.startswith("* "):
        line = "&bull;&nbsp;&nbsp;" + line[2:]

    story.append(Paragraph(line, body_style))

# ---------- 6. BUILD THE PDF ----------
doc = SimpleDocTemplate(
    "pizza_sales_report.pdf",
    pagesize=letter,
    topMargin=0.7 * inch,
    bottomMargin=0.7 * inch,
)
doc.build(story)

print("PDF report saved as pizza_sales_report.pdf")