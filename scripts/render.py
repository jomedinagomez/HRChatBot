"""Rendering helpers for the demo corpus.

Each document is a list of blocks. A block is a (kind, value) tuple:
    ('h1'|'h2'|'h3', text)      headings
    ('p', text)                 paragraph
    ('bullets', [text, ...])    bulleted list
    ('numbers', [text, ...])    numbered list
    ('table', [[row], ...])     first row is the header
    ('qa', [(question, answer), ...])
    ('note', text)              callout box
    ('break', None)             page break

Rendered with ReportLab. Each source system gets its own theme so the corpus
does not look like one template repeated.
"""

from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

COMPANY = "Meridian Financial Group"
DISCLAIMER = "Fictional sample content created for a search demo. Not a real policy."

# Each source system gets its own look, the way different systems really do.
THEMES = {
    "policyhub": {
        "body_font": "Times-Roman",
        "bold_font": "Times-Bold",
        "head_font": "Times-Bold",
        "size": 10.5,
        "leading": 14,
        "accent": colors.HexColor("#1F3864"),
        "h1_size": 15,
        "h2_size": 12,
        "underline_h2": True,
    },
    "peoplecentral": {
        "body_font": "Helvetica",
        "bold_font": "Helvetica-Bold",
        "head_font": "Helvetica-Bold",
        "size": 9.8,
        "leading": 13.5,
        "accent": colors.HexColor("#0B6A3A"),
        "h1_size": 14,
        "h2_size": 11.5,
        "underline_h2": False,
    },
    "sharepoint": {
        "body_font": "Helvetica",
        "bold_font": "Helvetica-Bold",
        "head_font": "Helvetica-Bold",
        "size": 10,
        "leading": 13.5,
        "accent": colors.HexColor("#8A3FFC"),
        "h1_size": 16,
        "h2_size": 12,
        "underline_h2": False,
    },
}


def _styles(theme):
    base = ParagraphStyle(
        "body", fontName=theme["body_font"], fontSize=theme["size"],
        leading=theme["leading"], spaceAfter=7,
    )
    return {
        "p": base,
        "h1": ParagraphStyle(
            "h1", parent=base, fontName=theme["head_font"], fontSize=theme["h1_size"],
            leading=theme["h1_size"] + 4, textColor=theme["accent"],
            spaceBefore=14, spaceAfter=9,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base, fontName=theme["head_font"], fontSize=theme["h2_size"],
            leading=theme["h2_size"] + 3, textColor=theme["accent"],
            spaceBefore=12, spaceAfter=6,
        ),
        "h3": ParagraphStyle(
            "h3", parent=base, fontName=theme["bold_font"], fontSize=theme["size"] + 0.5,
            spaceBefore=9, spaceAfter=4,
        ),
        "bullet": ParagraphStyle("bullet", parent=base, leftIndent=16, bulletIndent=5, spaceAfter=3),
        "cell": ParagraphStyle("cell", parent=base, fontSize=theme["size"] - 1.2,
                               leading=theme["size"] + 2, spaceAfter=0),
        "cellhead": ParagraphStyle("cellhead", parent=base, fontName=theme["bold_font"],
                                   fontSize=theme["size"] - 1.2, leading=theme["size"] + 2,
                                   spaceAfter=0, textColor=colors.white),
        "note": ParagraphStyle("note", parent=base, leftIndent=10, rightIndent=10,
                               spaceBefore=4, spaceAfter=4),
    }


def _table(rows, styles, theme, width):
    header = [Paragraph(escape(str(c)), styles["cellhead"]) for c in rows[0]]
    body = [[Paragraph(escape(str(c)), styles["cell"]) for c in row] for row in rows[1:]]
    columns = len(rows[0])
    table = Table([header] + body, colWidths=[width / columns] * columns, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), theme["accent"]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0A6")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F4F7")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def _note(text, styles, theme):
    cell = Paragraph(escape(text), styles["note"])
    table = Table([[cell]], colWidths=[6.4 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8E1")),
        ("BOX", (0, 0), (-1, -1), 0.8, theme["accent"]),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def write_pdf(path, blocks, theme_name, header_left, header_right, footer):
    theme = THEMES[theme_name]
    styles = _styles(theme)
    width = 6.4 * inch
    story = []
    for kind, value in blocks:
        if kind in ("h1", "h2", "h3"):
            text = escape(value)
            if kind == "h2" and theme["underline_h2"]:
                text = f"<u>{text}</u>"
            story.append(Paragraph(text, styles[kind]))
        elif kind == "p":
            story.append(Paragraph(escape(value), styles["p"]))
        elif kind == "bullets":
            for item in value:
                story.append(Paragraph(escape(item), styles["bullet"], bulletText="\u2022"))
            story.append(Spacer(1, 5))
        elif kind == "numbers":
            for position, item in enumerate(value, 1):
                story.append(Paragraph(escape(item), styles["bullet"], bulletText=f"{position}."))
            story.append(Spacer(1, 5))
        elif kind == "table":
            story.append(_table(value, styles, theme, width))
            story.append(Spacer(1, 9))
        elif kind == "qa":
            for question, answer in value:
                story.append(KeepTogether([
                    Paragraph("<b>Q. " + escape(question) + "</b>", styles["p"]),
                    Paragraph("A. " + escape(answer), styles["p"]),
                ]))
        elif kind == "note":
            story.append(_note(value, styles, theme))
            story.append(Spacer(1, 8))
        elif kind == "break":
            story.append(PageBreak())

    def decorate(canvas, document):
        canvas.saveState()
        canvas.setFont(theme["bold_font"], 8)
        canvas.setFillColor(theme["accent"])
        canvas.drawString(0.9 * inch, 10.42 * inch, header_left)
        canvas.setFont(theme["body_font"], 8)
        canvas.setFillColor(colors.HexColor("#444444"))
        canvas.drawRightString(7.6 * inch, 10.42 * inch, header_right)
        canvas.setStrokeColor(theme["accent"])
        canvas.setLineWidth(0.6)
        canvas.line(0.9 * inch, 10.32 * inch, 7.6 * inch, 10.32 * inch)
        canvas.setFont(theme["body_font"], 7.5)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawString(0.9 * inch, 0.55 * inch, footer)
        canvas.drawRightString(7.6 * inch, 0.55 * inch, f"Page {document.page}")
        canvas.drawString(0.9 * inch, 0.4 * inch, DISCLAIMER)
        canvas.restoreState()

    SimpleDocTemplate(
        str(path), pagesize=LETTER, leftMargin=0.9 * inch, rightMargin=1.1 * inch,
        topMargin=1.0 * inch, bottomMargin=0.85 * inch, invariant=1,
        title=header_right, author=COMPANY,
    ).build(story, onFirstPage=decorate, onLaterPages=decorate)
