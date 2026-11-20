# -*- coding: utf-8 -*-
import html
import os
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Flowable, Image as RLImage
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.lib.colors import HexColor

NAVY       = HexColor("#0f172a")
NAVY_LIGHT = HexColor("#1e293b")
BLUE       = HexColor("#1d4ed8")
BLUE_LIGHT = HexColor("#3b82f6")
TEAL       = HexColor("#0f766e")
TEAL_LIGHT = HexColor("#14b8a6")
PURPLE     = HexColor("#6d28d9")
AMBER      = HexColor("#b45309")
GREEN      = HexColor("#047857")
RED        = HexColor("#b91c1c")
SLATE_BG   = HexColor("#f8fafc")
CARD_BG    = HexColor("#ffffff")
BORDER     = HexColor("#cbd5e1")
BORDER_LIGHT = HexColor("#e2e8f0")
MUTED      = HexColor("#64748b")
TEXT       = HexColor("#1e293b")
WHITE      = colors.white

BG_BLUE    = HexColor("#eff6ff")
BG_TEAL    = HexColor("#f0fdfa")
BG_AMBER   = HexColor("#fffbeb")
BG_RED     = HexColor("#fef2f2")
BG_GREEN   = HexColor("#ecfdf5")
BG_PURPLE  = HexColor("#faf5ff")
BG_CODE    = HexColor("#0f172a")

W, H = A4
MARGIN = 1.6 * cm
INNER_W = W - 2 * MARGIN

ASSETS_DIR = r"c:\Users\CDA EXPERTISE\Desktop\tp\soa\tp3\assets"
OUT_PDF = r"c:\Users\CDA EXPERTISE\Desktop\tp\soa\tp3\TP3_REST_Calculatrice_RAPPORT.pdf"
os.makedirs(ASSETS_DIR, exist_ok=True)

PAGE_HEADERS = [
    "",
    "1. Introduction & Architecture REST",
    "2. Environnement Technique & Cycle de Vie",
    "3. Spécification de l'API & Modèle DTO",
    "4. Code Source : Logique Métier & Modèle DTO",
    "5. Code Source : Ressource JAX-RS & Configuration",
    "6. Validation Postman : Addition & Soustraction",
    "7. Validation Postman : Multiplication & Division",
    "8. Cas Limite & Déploiement Tomcat",
]

TOTAL_PAGES = 9

class AcademicCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for i, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self._draw_decorations(i + 1, num_pages)
            super().showPage()
        super().save()

    def _draw_decorations(self, page_num, total):
        if page_num == 1:
            return

        self.setFillColor(NAVY)
        self.rect(0, H - 1.1*cm, W, 1.1*cm, fill=1, stroke=0)
        self.setFillColor(BLUE_LIGHT)
        self.rect(0, H - 1.15*cm, W, 0.05*cm, fill=1, stroke=0)

        self.setFillColor(WHITE)
        self.setFont("Helvetica-Bold", 8.5)
        self.drawString(MARGIN, H - 0.72*cm, "TP3 SOA : Service Web REST Calculatrice — Jakarta EE & Jersey")

        label = PAGE_HEADERS[page_num - 1] if page_num - 1 < len(PAGE_HEADERS) else ""
        self.setFont("Helvetica", 8)
        self.setFillColor(HexColor("#93c5fd"))
        self.drawRightString(W - MARGIN, H - 0.72*cm, label)

        self.setFillColor(SLATE_BG)
        self.rect(0, 0, W, 0.95*cm, fill=1, stroke=0)
        self.setStrokeColor(BORDER_LIGHT)
        self.setLineWidth(0.5)
        self.line(0, 0.95*cm, W, 0.95*cm)

        self.setFillColor(MUTED)
        self.setFont("Helvetica", 7.5)
        self.drawString(MARGIN, 0.35*cm, "Salmen Zekri  |  TP3 SOA  |  Architecture Orientée Services & Services Web (LSI3)")

        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(NAVY)
        self.drawRightString(W - MARGIN, 0.35*cm, f"Page {page_num} / {total}")

def style(**kwargs):
    b = dict(fontName="Helvetica", fontSize=8.5, leading=12, textColor=TEXT, spaceAfter=0)
    b.update(kwargs)
    return ParagraphStyle("s", **b)

S_PAGE_TITLE = style(fontName="Helvetica-Bold", fontSize=14, textColor=NAVY, leading=17, spaceAfter=2)
S_PAGE_SUB   = style(fontName="Helvetica", fontSize=8, textColor=MUTED, leading=11, spaceAfter=5)
S_SEC_TITLE  = style(fontName="Helvetica-Bold", fontSize=9, textColor=WHITE, leading=12)
S_BODY       = style(fontName="Helvetica", fontSize=8, leading=11.5)
S_MUTED      = style(fontName="Helvetica", fontSize=7.5, leading=10.5, textColor=MUTED)

def sec_header(title_text, bg=NAVY, tag=""):
    clean_title = title_text.upper()
    content = [Paragraph(f"<b>{clean_title}</b>", S_SEC_TITLE)]
    if tag:
        clean_tag = tag.upper()
        tag_p = Paragraph(f"<b>{clean_tag}</b>", style(fontName="Helvetica-Bold", fontSize=7, textColor=HexColor("#93c5fd"), alignment=TA_RIGHT))
        tbl = Table([[content[0], tag_p]], colWidths=[INNER_W*0.75, INNER_W*0.25])
    else:
        tbl = Table([[content[0]]], colWidths=[INNER_W])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 3.5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3.5),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return tbl

def card_box(paragraphs, bg=WHITE, border_color=BORDER, padding=5, width=INNER_W):
    if not isinstance(paragraphs, list):
        paragraphs = [paragraphs]
    tbl = Table([[paragraphs]], colWidths=[width])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX", (0,0), (-1,-1), 0.8, border_color),
        ("LEFTPADDING", (0,0), (-1,-1), padding),
        ("RIGHTPADDING", (0,0), (-1,-1), padding),
        ("TOPPADDING", (0,0), (-1,-1), padding - 1),
        ("BOTTOMPADDING", (0,0), (-1,-1), padding - 1),
        ("ROUNDEDCORNERS", [5]),
    ]))
    return tbl

def code_box(code_str, label="", width=INNER_W, font_size=6.8, leading=8.8):
    lines = [html.escape(l) for l in code_str.strip().split("\n")]
    code_html = "<br/>".join([f"<font color='#94a3b8'>{i+1:02d} </font> {line}" for i, line in enumerate(lines)])
    p_code = Paragraph(code_html, style(fontName="Courier", fontSize=font_size, leading=leading, textColor=HexColor("#e2e8f0")))
    
    cells = []
    if label:
        p_lbl = Paragraph(f"<b>SOURCE : {html.escape(label.upper())}</b>", 
                          style(fontName="Helvetica-Bold", fontSize=6.5, textColor=HexColor("#93c5fd")))
        t_lbl = Table([[p_lbl]], colWidths=[width])
        t_lbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), HexColor("#1e293b")),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("TOPPADDING", (0,0), (-1,-1), 2.2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2.2),
        ]))
        cells.append([t_lbl])
    
    t_code = Table([[p_code]], colWidths=[width])
    t_code.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), BG_CODE),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    cells.append([t_code])
    
    outer = Table(cells, colWidths=[width])
    outer.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 0.8, HexColor("#334155")),
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("ROUNDEDCORNERS", [4]),
    ]))
    return outer

def two_cols(left_content, right_content, w_left=(INNER_W-6)/2, w_right=(INNER_W-6)/2):
    if not isinstance(left_content, list): left_content = [left_content]
    if not isinstance(right_content, list): right_content = [right_content]
    tbl = Table([[left_content, right_content]], colWidths=[w_left, w_right])
    tbl.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
    ]))
    return tbl

def stat_badge(number_str, title_str, desc_str, col=BLUE, bg=BG_BLUE):
    p_num = Paragraph(f"<b>{number_str}</b>", style(fontName="Helvetica-Bold", fontSize=15, textColor=col, alignment=TA_CENTER))
    p_tit = Paragraph(f"<b>{title_str}</b>", style(fontName="Helvetica-Bold", fontSize=7.5, textColor=NAVY, alignment=TA_CENTER))
    p_desc = Paragraph(desc_str, style(fontName="Helvetica", fontSize=6.8, textColor=MUTED, alignment=TA_CENTER))
    t = Table([[p_num], [p_tit], [p_desc]], colWidths=[(INNER_W-9)/4])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX", (0,0), (-1,-1), 0.8, col),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("ROUNDEDCORNERS", [5]),
    ]))
    return t

def stat_row(items):
    cells = [stat_badge(n, t, d, c, b) for n, t, d, c, b in items]
    tbl = Table([cells], colWidths=[(INNER_W-9)/4]*4)
    tbl.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
    ]))
    return tbl

def flow_horizontal(steps, cols, w=INNER_W):
    n = len(steps)
    gap = 4
    w_box = (w - (n - 1) * 12) / n
    row = []
    for i, (st, col) in enumerate(zip(steps, cols)):
        p_st = Paragraph(f"<b>{st}</b>", style(fontName="Helvetica-Bold", fontSize=6.8, textColor=WHITE, alignment=TA_CENTER, leading=8.5))
        t_box = Table([[p_st]], colWidths=[w_box])
        t_box.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), col),
            ("LEFTPADDING", (0,0), (-1,-1), 2),
            ("RIGHTPADDING", (0,0), (-1,-1), 2),
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 4),
            ("ROUNDEDCORNERS", [4]),
        ]))
        row.append(t_box)
        if i < n - 1:
            p_arr = Paragraph("<b>&rarr;</b>", style(fontName="Helvetica-Bold", fontSize=9, textColor=MUTED, alignment=TA_CENTER))
            t_arr = Table([[p_arr]], colWidths=[12])
            t_arr.setStyle(TableStyle([
                ("LEFTPADDING", (0,0), (-1,-1), 0),
                ("RIGHTPADDING", (0,0), (-1,-1), 0),
                ("TOPPADDING", (0,0), (-1,-1), 4),
                ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ]))
            row.append(t_arr)
    outer = Table([row])
    outer.setStyle(TableStyle([
        ("LEFTPADDING", (0,0), (-1,-1), 0),
        ("RIGHTPADDING", (0,0), (-1,-1), 0),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    return outer

class CoverPageFlowable(Flowable):
    def wrap(self, avW, avH):
        self.pw = avW
        self.ph = avH
        return avW, avH

    def draw(self):
        c = self.canv
        pw, ph = self.pw, self.ph

        strips = 40
        for i in range(strips):
            ratio = i / strips
            if ratio < 0.4:
                r1, g1, b1 = 0x0f, 0x17, 0x2a
                r2, g2, b2 = 0x1e, 0x29, 0x3b
                t = ratio / 0.4
            elif ratio < 0.7:
                r1, g1, b1 = 0x1e, 0x29, 0x3b
                r2, g2, b2 = 0x0f, 0x27, 0x40
                t = (ratio - 0.4) / 0.3
            else:
                r1, g1, b1 = 0x0f, 0x27, 0x40
                r2, g2, b2 = 0x0a, 0x14, 0x28
                t = (ratio - 0.7) / 0.3
            r = int(r1 + (r2 - r1) * t)
            g = int(g1 + (g2 - g1) * t)
            b = int(b1 + (b2 - b1) * t)
            strip_h = ph / strips
            y = ph - (i + 1) * strip_h
            c.setFillColor(HexColor(f"#{r:02x}{g:02x}{b:02x}"))
            c.rect(0, y, pw, strip_h + 0.5, fill=1, stroke=0)

        c.saveState()
        c.setFillColor(HexColor("#1d4ed8"))
        c.setFillAlpha(0.06)
        c.circle(pw + 1*cm, ph + 0.5*cm, 4*cm, fill=1, stroke=0)
        c.circle(pw + 1*cm, ph + 0.5*cm, 6*cm, fill=1, stroke=0)
        c.setFillAlpha(0.0)
        c.setStrokeAlpha(0.15)
        c.setStrokeColor(HexColor("#3b82f6"))
        c.setLineWidth(1)
        c.circle(pw + 1*cm, ph + 0.5*cm, 7.5*cm, fill=0, stroke=1)

        c.setFillColor(HexColor("#14b8a6"))
        c.setFillAlpha(0.05)
        c.circle(-1*cm, -0.5*cm, 3.5*cm, fill=1, stroke=0)
        c.setStrokeAlpha(0.12)
        c.setStrokeColor(HexColor("#14b8a6"))
        c.setLineWidth(1)
        c.circle(-1*cm, -0.5*cm, 5.5*cm, fill=0, stroke=1)
        c.restoreState()

        c.setFillColor(HexColor("#1d4ed8"))
        c.rect(0, ph - 1.4*cm, pw, 4*mm, fill=1, stroke=0)
        c.setFillColor(HexColor("#3b82f6"))
        c.rect(0, ph - 1.4*cm + 4*mm, pw, 1.5*mm, fill=1, stroke=0)
        c.setFillColor(HexColor("#14b8a6"))
        c.rect(0, ph - 1.4*cm - 1*mm, pw, 1*mm, fill=1, stroke=0)

        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(HexColor("#93c5fd"))
        c.drawString(MARGIN, ph - 1.0*cm, "TRAVAUX PRATIQUES  ·  ARCHITECTURE ORIENTÉE SERVICES  ·  SOA")
        c.setFont("Helvetica", 7.5)
        c.setFillColor(HexColor("#64748b"))
        c.drawRightString(pw - MARGIN, ph - 1.0*cm, "2025 – 2026")

        cx = pw / 2
        title_y = ph * 0.74

        c.saveState()
        c.setFillColor(HexColor("#1d4ed8"))
        c.setFillAlpha(0.07)
        c.roundRect(MARGIN, title_y - 0.6*cm, pw - 2*MARGIN, 3.8*cm, 12, fill=1, stroke=0)
        c.restoreState()

        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(HexColor("#14b8a6"))
        c.drawCentredString(cx, title_y + 2.9*cm, "SERVICE WEB REST  ·  JAKARTA EE 10  ·  JAX-RS  ·  JERSEY")

        c.saveState()
        c.setStrokeColor(HexColor("#3b82f6"))
        c.setStrokeAlpha(0.4)
        c.setLineWidth(0.8)
        c.line(MARGIN + 2*cm, title_y + 2.5*cm, pw - MARGIN - 2*cm, title_y + 2.5*cm)
        c.restoreState()

        c.setFont("Helvetica-Bold", 40)
        c.setFillColor(HexColor("#f8fafc"))
        c.drawCentredString(cx, title_y + 1.3*cm, "CalculatriceREST")

        c.setFont("Helvetica", 13)
        c.setFillColor(HexColor("#93c5fd"))
        c.drawCentredString(cx, title_y + 0.3*cm, "Conception & Implémentation d'un Service Web RESTful")

        c.saveState()
        c.setStrokeColor(HexColor("#3b82f6"))
        c.setStrokeAlpha(0.4)
        c.line(MARGIN + 2*cm, title_y - 0.15*cm, pw - MARGIN - 2*cm, title_y - 0.15*cm)
        c.restoreState()

        c.setFont("Helvetica-Bold", 11)
        c.setFillColor(HexColor("#e2e8f0"))
        c.drawCentredString(cx, title_y - 0.65*cm, "Salmen Zekri")

        diag_y = ph * 0.47
        diag_cx = cx

        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(HexColor("#64748b"))
        c.drawCentredString(diag_cx, diag_y + 2.5*cm, "ARCHITECTURE DU PROJET REST")
        c.setStrokeColor(HexColor("#334155"))
        c.setLineWidth(0.5)
        label_w = 4.5*cm
        c.line(diag_cx - label_w, diag_y + 2.4*cm, diag_cx - label_w - 1*cm, diag_y + 2.4*cm)
        c.line(diag_cx + label_w, diag_y + 2.4*cm, diag_cx + label_w + 1*cm, diag_y + 2.4*cm)

        bw = 4.0*cm
        bh = 1.3*cm
        gap = 1.5*cm
        boxes = [
            (diag_cx - bw - gap - bw/2, diag_y + 0.9*cm, HexColor("#1e3a5f"), HexColor("#3b82f6"), "CLIENT REST", "Postman / HTTP"),
            (diag_cx - bw/2,            diag_y + 0.9*cm, HexColor("#0f3d38"), HexColor("#14b8a6"), "SERVEUR TOMCAT", "Port :8080 / Context"),
            (diag_cx + gap + bw/2,      diag_y + 0.9*cm, HexColor("#2d1b4e"), HexColor("#8b5cf6"), "CalculRest.java", "@Path / JAX-RS"),
        ]
        badge_labels = [
            ["HTTP GET", "QueryParam"],
            ["web.xml", "Jersey"],
            ["Operation", "JSON DTO"],
        ]
        for idx, (bx, by, bg_col, accent, label1, label2) in enumerate(boxes):
            c.setFillColor(bg_col)
            c.roundRect(bx - bw/2, by - bh/2, bw, bh, 8, fill=1, stroke=0)
            c.setFillColor(accent)
            c.roundRect(bx - bw/2, by + bh/2 - 5*mm, bw, 5*mm, 8, fill=1, stroke=0)
            c.rect(bx - bw/2, by + bh/2 - 5*mm, bw, 2*mm, fill=1, stroke=0)
            c.setStrokeColor(accent)
            c.setLineWidth(1.2)
            c.roundRect(bx - bw/2, by - bh/2, bw, bh, 8, fill=0, stroke=1)
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(HexColor("#f8fafc"))
            c.drawCentredString(bx, by + 0.15*cm, label1)
            c.setFont("Helvetica", 7)
            c.setFillColor(accent)
            c.drawCentredString(bx, by - 0.25*cm, label2)

            bl = badge_labels[idx]
            for bi, blabel in enumerate(bl):
                badge_x = bx - 0.9*cm + bi * 1.9*cm
                badge_y = by - bh/2 - 0.75*cm
                badge_w = 1.6*cm
                badge_h = 0.42*cm
                c.setFillColor(HexColor("#1e293b"))
                c.setStrokeColor(accent)
                c.setLineWidth(0.6)
                c.roundRect(badge_x - badge_w/2, badge_y - badge_h/2, badge_w, badge_h, 4, fill=1, stroke=1)
                c.setFont("Helvetica-Bold", 6.2)
                c.setFillColor(accent)
                c.drawCentredString(badge_x, badge_y - 2.2, blabel)

        arrow_y = diag_y + 0.9*cm
        for i in range(len(boxes) - 1):
            ax_start = boxes[i][0] + bw/2 + 1
            ax_end   = boxes[i+1][0] - bw/2 - 1
            ax_mid   = (ax_start + ax_end) / 2
            arr_size = 5
            c.setStrokeColor(HexColor("#3b82f6"))
            c.setLineWidth(1.5)
            c.line(ax_start + arr_size, arrow_y, ax_end - arr_size, arrow_y)

            c.setFillColor(HexColor("#3b82f6"))
            p_fwd = c.beginPath()
            p_fwd.moveTo(ax_end, arrow_y)
            p_fwd.lineTo(ax_end - arr_size, arrow_y + arr_size * 0.6)
            p_fwd.lineTo(ax_end - arr_size, arrow_y - arr_size * 0.6)
            p_fwd.close()
            c.drawPath(p_fwd, fill=1, stroke=0)

            p_bwd = c.beginPath()
            p_bwd.moveTo(ax_start, arrow_y)
            p_bwd.lineTo(ax_start + arr_size, arrow_y + arr_size * 0.6)
            p_bwd.lineTo(ax_start + arr_size, arrow_y - arr_size * 0.6)
            p_bwd.close()
            c.drawPath(p_bwd, fill=1, stroke=0)

            c.setFont("Helvetica-Bold", 6.5)
            c.setFillColor(HexColor("#93c5fd"))
            c.drawCentredString(ax_mid, arrow_y + 3.5, "HTTP/JSON")

        badge_y_row = ph * 0.22
        tech_badges = [
            ("RESTful",     HexColor("#1d4ed8")),
            ("JAX-RS 3.1",  HexColor("#0f766e")),
            ("Jersey 3.1",  HexColor("#b45309")),
            ("Jackson",     HexColor("#6d28d9")),
            ("Tomcat 10+",  HexColor("#047857")),
            ("Maven WAR",   HexColor("#b91c1c")),
        ]
        n_badges = len(tech_badges)
        badge_total_w = pw - 2 * MARGIN
        badge_slot_w = badge_total_w / n_badges
        badge_rw = badge_slot_w * 0.82
        badge_rh = 0.72*cm

        for bi, (blabel, bcolor) in enumerate(tech_badges):
            bx = MARGIN + (bi + 0.5) * badge_slot_w
            by = badge_y_row
            c.setFillColor(bcolor)
            c.roundRect(bx - badge_rw/2, by - badge_rh/2, badge_rw, badge_rh, 8, fill=1, stroke=0)
            c.setFont("Helvetica-Bold", 8.5)
            c.setFillColor(HexColor("#f8fafc"))
            c.drawCentredString(bx, by - 3, blabel)

        stamp_y = 1.6*cm
        c.setFillColor(HexColor("#0f172a"))
        c.rect(0, 0, pw, stamp_y + 0.3*cm, fill=1, stroke=0)
        c.setStrokeColor(HexColor("#1d4ed8"))
        c.setLineWidth(1.5)
        c.line(0, stamp_y + 0.3*cm, pw, stamp_y + 0.3*cm)
        c.setStrokeColor(HexColor("#14b8a6"))
        c.setLineWidth(0.5)
        c.line(0, stamp_y + 0.6*cm, pw, stamp_y + 0.6*cm)

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(HexColor("#f8fafc"))
        c.drawCentredString(cx, 0.9*cm, "Salmen Zekri  |  TP3 SOA  |  Faculté des Sciences de Sfax  |  2025–2026")


def build_perfect_report():
    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=1.35 * cm,
        bottomMargin=1.1 * cm
    )

    story = []

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 1 : COVER
    # ═════════════════════════════════════════════════════════════════════════
    story.append(CoverPageFlowable())
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 2 : INTRODUCTION & ARCHITECTURE REST
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("1. Introduction &amp; Architecture Générale", S_PAGE_TITLE))
    story.append(Paragraph("Conception d'une API REST sous Jakarta EE 10 et principes directeurs", S_PAGE_SUB))

    story.append(stat_row([
        ("4", "MÉTHODES REST", "Addition, sous, mult, div", BLUE, BG_BLUE),
        ("REST", "STYLE D'ARCHI", "Ressources & Verbes HTTP", TEAL, BG_TEAL),
        ("JSON", "FORMAT PAYLOAD", "Sérialisation Jackson DTO", AMBER, BG_AMBER),
        (".WAR", "PACKAGING MAVEN", "Déploiement Tomcat 10+", PURPLE, BG_PURPLE),
    ]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(sec_header("But &amp; Périmètre du Service CalculatriceREST", NAVY, "OBJECTIFS"))
    story.append(Spacer(1, 0.12 * cm))
    story.append(card_box([
        Paragraph("• <b>Objectif central :</b> Développer un service web RESTful universel offrant 4 opérations de calcul arithmétique.", S_BODY),
        Paragraph("• <b>Spécification :</b> Exploitation des annotations standard Jakarta RESTful Web Services (JAX-RS 3.1).", S_BODY),
        Paragraph("• <b>Points clés :</b> Indépendance totale du client, format JSON léger, stateless, gestion fine des codes HTTP.", S_MUTED),
    ], bg=WHITE, border_color=BORDER))
    story.append(Spacer(1, 0.3 * cm))

    story.append(sec_header("Architecture Distribuée des Échanges REST", BLUE, "TOPOLOGIE"))
    story.append(Spacer(1, 0.12 * cm))
    arch_flow = flow_horizontal([
        "Client HTTP\n(Postman / Web)",
        "Requête GET\nParamètres a, b",
        "Tomcat 10+\n(Port :8080)",
        "Jersey Servlet\n(/api/*)",
        "CalculRest\n(Ressource JAX-RS)",
        "Réponse JSON\n(200 OK / 400)"
    ], [BLUE, NAVY, TEAL, PURPLE, GREEN, NAVY])
    story.append(card_box([
        arch_flow,
        Spacer(1, 1.5*mm),
        Paragraph("<b>Flux de traitement :</b> Requête HTTP GET reçue par Tomcat sur le port 8080 &rarr; Filtrage via le ServletContainer Jersey &rarr; Injection des paramètres <code>@QueryParam</code> &rarr; Délégation au métier &rarr; Sérialisation JSON retournée au client.", S_MUTED)
    ], bg=SLATE_BG, border_color=BORDER))
    story.append(Spacer(1, 0.3 * cm))

    story.append(sec_header("Comparaison Architecturale : SOAP (TP2) vs REST (TP3)", TEAL, "MÉTHODOLOGIE"))
    story.append(Spacer(1, 0.12 * cm))

    col_soap = card_box([
        Paragraph("<b>[TP2] Protocole SOAP (JAX-WS)</b>", style(fontName="Helvetica-Bold", fontSize=7.8, textColor=PURPLE)),
        Spacer(1, 1*mm),
        Paragraph("• <b>Format :</b> XML très verbeux encapsulé dans une enveloppe SOAP.", S_BODY),
        Paragraph("• <b>Contrat :</b> Contrat formel obligatoire et rigide (WSDL / XSD).", S_BODY),
        Paragraph("• <b>Transport :</b> Requêtes systématiques en HTTP POST.", S_BODY),
    ], bg=BG_PURPLE, border_color=HexColor("#d8b4fe"), width=(INNER_W-6)/2)

    col_rest = card_box([
        Paragraph("<b>[TP3] Architecture REST (JAX-RS)</b>", style(fontName="Helvetica-Bold", fontSize=7.8, textColor=TEAL)),
        Spacer(1, 1*mm),
        Paragraph("• <b>Format :</b> JSON compact, léger et lisible nativement.", S_BODY),
        Paragraph("• <b>Contrat :</b> Contrat souple basé sur les URI et verbes HTTP standards.", S_BODY),
        Paragraph("• <b>Transport :</b> Exploitation optimale des méthodes GET, POST, PUT, DELETE.", S_BODY),
    ], bg=BG_TEAL, border_color=HexColor("#99f6e4"), width=(INNER_W-6)/2)

    story.append(two_cols(col_soap, col_rest))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 3 : ENVIRONNEMENT TECHNIQUE & CYCLE DE VIE
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("2. Environnement Technique &amp; Cycle de Vie", S_PAGE_TITLE))
    story.append(Paragraph("Détail des composants, outillage et gestion du build Maven", S_PAGE_SUB))

    story.append(stat_row([
        ("JAX-RS", "SPÉCIFICATION", "Jakarta REST 3.1.0", BLUE, BG_BLUE),
        ("JERSEY", "RUNTIME", "Version 3.1.3", TEAL, BG_TEAL),
        ("TOMCAT", "CONTENEUR", "Version 10.1+", AMBER, BG_AMBER),
        ("POSTMAN", "TESTS & RECETTE", "Validation HTTP", GREEN, BG_GREEN),
    ]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(sec_header("Environnement Technique Étape par Étape", NAVY, "OUTILLAGE"))
    story.append(Spacer(1, 0.12 * cm))

    table_data = [
        ["Étape", "Composant / Outil", "Version", "Rôle dans le projet"],
        ["Étape 1", "Apache Maven", "3.9.9", "Cycle de build, gestion des dépendances et packaging WAR"],
        ["Étape 1", "Java Development Kit", "JDK 11 / 25", "Compilation Java et compatibilité Jakarta EE 10"],
        ["Étape 2", "Jakarta RESTful Web Services", "JAX-RS 3.1.0", "Spécification standard des annotations REST"],
        ["Étape 2", "Eclipse Jersey", "3.1.3", "Moteur runtime de traitement et conteneur de Servlets"],
        ["Étape 3-4", "Jackson JAX-RS Provider", "2.14.1", "Sérialisation automatique de l'objet Operation en JSON"],
        ["Étape 5", "Apache Tomcat", "Tomcat 10+", "Serveur d'applications Web (Conteneur Servlet 5.0+)"],
        ["Étape 6", "Postman", "v10.x", "Client HTTP pour tester et valider les méthodes de l'API"],
        ["Étape 7", "Git & GitHub", "2.56.0", "Gestionnaire de versions et hébergement du code source"]
    ]
    t_env = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, style(fontName="Helvetica-Bold" if r==0 else "Helvetica", fontSize=7.2, leading=9.5, textColor=WHITE if r==0 else TEXT)) for c in row] for r, row in enumerate(table_data)], colWidths=[2.2*cm, 4.4*cm, 2.4*cm, INNER_W - 9.0*cm])
    t_env.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_env)
    story.append(Spacer(1, 0.3 * cm))

    story.append(sec_header("Arborescence Technique &amp; Packaging WAR", BLUE, "STRUCTURE"))
    story.append(Spacer(1, 0.12 * cm))

    col_tree = card_box([
        Paragraph("<b>Structure standardisée Maven :</b>", style(fontName="Helvetica-Bold", fontSize=7.8, textColor=NAVY)),
        Spacer(1, 1*mm),
        Paragraph("<code>tp3/pom.xml</code> &rarr; Packaging <code>&lt;packaging&gt;war&lt;/packaging&gt;</code>", S_BODY),
        Paragraph("<code>src/main/java/service/Calculatrice.java</code> &rarr; Métier", S_BODY),
        Paragraph("<code>src/main/java/model/Operation.java</code> &rarr; Modèle JSON DTO", S_BODY),
        Paragraph("<code>src/main/java/rest/CalculRest.java</code> &rarr; Ressource REST", S_BODY),
        Paragraph("<code>src/main/java/rest/RestApplication.java</code> &rarr; Config Jersey", S_BODY),
        Paragraph("<code>src/main/webapp/WEB-INF/web.xml</code> &rarr; ServletContainer", S_BODY),
    ], bg=WHITE, border_color=BORDER, width=(INNER_W-6)/2)

    col_build = card_box([
        Paragraph("<b>Commandes du cycle de vie Maven :</b>", style(fontName="Helvetica-Bold", fontSize=7.8, textColor=NAVY)),
        Spacer(1, 1*mm),
        Paragraph("• <b>Nettoyage :</b> <code>mvn clean</code>", S_BODY),
        Paragraph("• <b>Compilation :</b> <code>mvn compile</code>", S_BODY),
        Paragraph("• <b>Packaging WAR :</b> <code>mvn package</code> &rarr; <code>CalculatriceREST.war</code>", S_BODY),
        Paragraph("• <b>Serveur Autonome :</b> <code>mvn exec:java</code> (Grizzly intégré)", S_BODY),
        Paragraph("• <b>Déploiement Tomcat :</b> Copie du WAR dans <code>webapps/</code>", S_BODY),
    ], bg=SLATE_BG, border_color=BORDER, width=(INNER_W-6)/2)

    story.append(two_cols(col_tree, col_build))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 4 : SPÉCIFICATION DE L'API & MODÈLE DTO
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("3. Spécification de l'API &amp; Modèle DTO", S_PAGE_TITLE))
    story.append(Paragraph("Contrat formel des endpoints, paramètres de requête et sérialisation JSON", S_PAGE_SUB))

    story.append(stat_row([
        ("GET", "VERBE HTTP", "Idempotent & standard", BLUE, BG_BLUE),
        ("@QueryParam", "EXTRACTION", "Paramètres d'URL a et b", TEAL, BG_TEAL),
        ("200 OK", "CODE SUCCÈS", "Calcul nominal", GREEN, BG_GREEN),
        ("400 BAD", "CODE ERREUR", "Division par zéro", RED, BG_RED),
    ]))
    story.append(Spacer(1, 0.3 * cm))

    story.append(sec_header("Matrice Formelle des Endpoints REST", NAVY, "CONTRAT HTTP"))
    story.append(Spacer(1, 0.12 * cm))

    ep_data = [
        ["Opération", "Verbe", "URI Relative", "Paramètres requis", "Code HTTP", "Format Réponse"],
        ["Addition", "GET", "/api/calculatrice/addition", "a (double), b (double)", "200 OK", "JSON (Operation)"],
        ["Soustraction", "GET", "/api/calculatrice/soustraction", "a (double), b (double)", "200 OK", "JSON (Operation)"],
        ["Multiplication", "GET", "/api/calculatrice/multiplication", "a (double), b (double)", "200 OK", "JSON (Operation)"],
        ["Division", "GET", "/api/calculatrice/division", "a (double), b (double)", "200 OK", "JSON (Operation)"],
        ["Division par 0", "GET", "/api/calculatrice/division", "a (double), b = 0", "400 Bad Request", "JSON (Erreur)"]
    ]
    t_ep = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, style(fontName="Helvetica-Bold" if r==0 else "Helvetica", fontSize=7.2, leading=9.5, textColor=WHITE if r==0 else TEXT)) for c in row] for r, row in enumerate(ep_data)], colWidths=[2.5*cm, 1.8*cm, 4.4*cm, 3.2*cm, 2.3*cm, INNER_W - 14.2*cm])
    t_ep.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY_LIGHT),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.4, BORDER_LIGHT),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_ep)
    story.append(Spacer(1, 0.3 * cm))

    story.append(sec_header("Structure du Modèle de Données Sérialisé : Operation", BLUE, "DTO JSON"))
    story.append(Spacer(1, 0.12 * cm))

    json_example = """{
    "a": 15.5,
    "b": 4.5,
    "operation": "addition",
    "resultat": 20.0,
    "statut": "SUCCESS"
}"""
    col_json = code_box(json_example, "EXEMPLE DE PAYLOAD JSON RETOURNÉ", width=(INNER_W-6)/2)

    col_fields = card_box([
        Paragraph("<b>Propriétés de l'objet DTO :</b>", style(fontName="Helvetica-Bold", fontSize=7.8, textColor=NAVY)),
        Spacer(1, 1*mm),
        Paragraph("• <code>a</code> : Premier opérande numérique (<code>double</code>).", S_BODY),
        Paragraph("• <code>b</code> : Second opérande numérique (<code>double</code>).", S_BODY),
        Paragraph("• <code>operation</code> : Nom de l'opération arithmétique exécutée.", S_BODY),
        Paragraph("• <code>resultat</code> : Résultat calculé retourné par la logique métier.", S_BODY),
        Paragraph("• <code>statut</code> : Indicateur d'état (<code>SUCCESS</code> ou message d'erreur).", S_BODY),
        Spacer(1, 1*mm),
        Paragraph("<b>Rôle de Jackson :</b> Sérialisation automatique bidirectionnelle objet Java &harr; JSON.", S_MUTED),
    ], bg=WHITE, border_color=BORDER, width=(INNER_W-6)/2)

    story.append(two_cols(col_json, col_fields))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 5 : CODE SOURCE : MÉTIER & DTO
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("4. Code Source : Logique Métier &amp; Modèle DTO", S_PAGE_TITLE))
    story.append(Paragraph("Implémentation Java pure des couches Service et Modèle (aucun commentaire)", S_PAGE_SUB))

    code_calc = """package service;

public class Calculatrice {

    public double addition(double a, double b) {
        return a + b;
    }

    public double soustraction(double a, double b) {
        return a - b;
    }

    public double multiplication(double a, double b) {
        return a * b;
    }

    public double division(double a, double b) {
        if (b == 0.0) {
            throw new ArithmeticException("Division par zero impossible");
        }
        return a / b;
    }
}"""
    story.append(sec_header("Classe Métier Pure : Calculatrice.java", NAVY, "SERVICE"))
    story.append(Spacer(1, 0.12 * cm))
    story.append(code_box(code_calc, "src/main/java/service/Calculatrice.java", font_size=6.8, leading=8.6))
    story.append(Spacer(1, 0.25 * cm))

    code_op = """package model;

import java.io.Serializable;

public class Operation implements Serializable {

    private double a;
    private double b;
    private String operation;
    private double resultat;
    private String statut;

    public Operation() {}

    public Operation(double a, double b, String operation, double resultat, String statut) {
        this.a = a;
        this.b = b;
        this.operation = operation;
        this.resultat = resultat;
        this.statut = statut;
    }

    public double getA() { return a; }
    public void setA(double a) { this.a = a; }
    public double getB() { return b; }
    public void setB(double b) { this.b = b; }
    public String getOperation() { return operation; }
    public void setOperation(String operation) { this.operation = operation; }
    public double getResultat() { return resultat; }
    public void setResultat(double resultat) { this.resultat = resultat; }
    public String getStatut() { return statut; }
    public void setStatut(String statut) { this.statut = statut; }
}"""
    story.append(sec_header("Modèle de Données JSON : Operation.java", BLUE, "DTO"))
    story.append(Spacer(1, 0.12 * cm))
    story.append(code_box(code_op, "src/main/java/model/Operation.java", font_size=6.5, leading=8.0))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 6 : CODE SOURCE : RESSOURCE JAX-RS & CONFIGURATION
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("5. Code Source : Ressource JAX-RS &amp; Configuration", S_PAGE_TITLE))
    story.append(Paragraph("Endpoints annotés et configuration Jersey / Servlet 5.0 (aucun commentaire)", S_PAGE_SUB))

    code_rest = """package rest;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;
import model.Operation;
import service.Calculatrice;

@Path("/calculatrice")
public class CalculRest {

    private final Calculatrice calculatrice = new Calculatrice();

    @GET @Path("/addition") @Produces(MediaType.APPLICATION_JSON)
    public Response addition(@QueryParam("a") double a, @QueryParam("b") double b) {
        Operation op = new Operation(a, b, "addition", calculatrice.addition(a, b), "SUCCESS");
        return Response.ok(op).build();
    }

    @GET @Path("/soustraction") @Produces(MediaType.APPLICATION_JSON)
    public Response soustraction(@QueryParam("a") double a, @QueryParam("b") double b) {
        Operation op = new Operation(a, b, "soustraction", calculatrice.soustraction(a, b), "SUCCESS");
        return Response.ok(op).build();
    }

    @GET @Path("/multiplication") @Produces(MediaType.APPLICATION_JSON)
    public Response multiplication(@QueryParam("a") double a, @QueryParam("b") double b) {
        Operation op = new Operation(a, b, "multiplication", calculatrice.multiplication(a, b), "SUCCESS");
        return Response.ok(op).build();
    }

    @GET @Path("/division") @Produces(MediaType.APPLICATION_JSON)
    public Response division(@QueryParam("a") double a, @QueryParam("b") double b) {
        if (b == 0.0) {
            Operation op = new Operation(a, b, "division", 0.0, "ERREUR: Division par zero impossible");
            return Response.status(Response.Status.BAD_REQUEST).entity(op).build();
        }
        Operation op = new Operation(a, b, "division", calculatrice.division(a, b), "SUCCESS");
        return Response.ok(op).build();
    }
}"""
    story.append(sec_header("Ressource REST Principale : CalculRest.java", NAVY, "JAX-RS ENDPOINTS"))
    story.append(Spacer(1, 0.12 * cm))
    story.append(code_box(code_rest, "src/main/java/rest/CalculRest.java", font_size=6.2, leading=7.7))
    story.append(Spacer(1, 0.25 * cm))

    code_app = """package rest;

import jakarta.ws.rs.ApplicationPath;
import org.glassfish.jersey.server.ResourceConfig;

@ApplicationPath("/api")
public class RestApplication extends ResourceConfig {

    public RestApplication() {
        packages("rest", "model", "service");
    }
}"""
    story.append(sec_header("Configuration Jersey : RestApplication.java", BLUE, "RESOURCE CONFIG"))
    story.append(Spacer(1, 0.12 * cm))
    story.append(code_box(code_app, "src/main/java/rest/RestApplication.java", font_size=6.5, leading=8.0))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 7 : VALIDATION POSTMAN : ADDITION & SOUSTRACTION
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("6. Validation Postman : Addition &amp; Soustraction", S_PAGE_TITLE))
    story.append(Paragraph("Tests réels d'intégration HTTP avec vérification des QueryParams et du code 200 OK", S_PAGE_SUB))

    p1_path = os.path.join(ASSETS_DIR, "postman_addition.png")
    story.append(sec_header("Méthode 1 : Addition (a=15.5, b=4.5 → résultat=20.0)", GREEN, "200 OK"))
    story.append(Spacer(1, 0.12 * cm))
    story.append(RLImage(p1_path, width=INNER_W, height=8.4 * cm))
    story.append(Spacer(1, 0.25 * cm))

    p2_path = os.path.join(ASSETS_DIR, "postman_soustraction.png")
    story.append(sec_header("Méthode 2 : Soustraction (a=20.0, b=7.5 → résultat=12.5)", BLUE, "200 OK"))
    story.append(Spacer(1, 0.12 * cm))
    story.append(RLImage(p2_path, width=INNER_W, height=8.4 * cm))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 8 : VALIDATION POSTMAN : MULTIPLICATION & DIVISION
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("7. Validation Postman : Multiplication &amp; Division", S_PAGE_TITLE))
    story.append(Paragraph("Tests des opérations multiplicatives et de division nominale (code 200 OK)", S_PAGE_SUB))

    p3_path = os.path.join(ASSETS_DIR, "postman_multiplication.png")
    story.append(sec_header("Méthode 3 : Multiplication (a=6.0, b=7.0 → résultat=42.0)", PURPLE, "200 OK"))
    story.append(Spacer(1, 0.12 * cm))
    story.append(RLImage(p3_path, width=INNER_W, height=8.4 * cm))
    story.append(Spacer(1, 0.25 * cm))

    p4_path = os.path.join(ASSETS_DIR, "postman_division.png")
    story.append(sec_header("Méthode 4 : Division Nominale (a=50.0, b=4.0 → résultat=12.5)", TEAL, "200 OK"))
    story.append(Spacer(1, 0.12 * cm))
    story.append(RLImage(p4_path, width=INNER_W, height=8.4 * cm))
    story.append(PageBreak())

    # ═════════════════════════════════════════════════════════════════════════
    # PAGE 9 : CAS LIMITE & DÉPLOIEMENT TOMCAT
    # ═════════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("8. Cas Limite &amp; Déploiement Tomcat", S_PAGE_TITLE))
    story.append(Paragraph("Interception d'erreur HTTP 400 Bad Request et déploiement du livrable WAR", S_PAGE_SUB))

    p5_path = os.path.join(ASSETS_DIR, "postman_division_zero.png")
    story.append(sec_header("Cas Limite : Division par Zéro (b=0 → HTTP 400 Bad Request)", RED, "ERREUR GÉRÉE"))
    story.append(Spacer(1, 0.12 * cm))
    story.append(RLImage(p5_path, width=INNER_W, height=8.4 * cm))
    story.append(Spacer(1, 0.25 * cm))

    story.append(sec_header("Procédure de Déploiement &amp; Dépôt GitHub", NAVY, "LIVRABLES"))
    story.append(Spacer(1, 0.12 * cm))

    col_dep = card_box([
        Paragraph("<b>1. Déploiement Apache Tomcat 10+ :</b>", style(fontName="Helvetica-Bold", fontSize=7.8, textColor=NAVY)),
        Paragraph("• Génération : <code>mvn clean package</code> (archive <code>CalculatriceREST.war</code>).", S_BODY),
        Paragraph("• Déploiement : Déposer le fichier dans <code>%CATALINA_HOME%/webapps/</code>.", S_BODY),
        Paragraph("• Démarrage : Exécuter <code>bin/startup.bat</code>.", S_BODY),
        Paragraph("• URL d'accès : <code>http://localhost:8080/CalculatriceREST/api/calculatrice/...</code>", S_BODY),
    ], bg=WHITE, border_color=BORDER, width=(INNER_W-6)/2)

    col_git = card_box([
        Paragraph("<b>2. Référentiel GitHub Officiel :</b>", style(fontName="Helvetica-Bold", fontSize=7.8, textColor=BLUE)),
        Paragraph("• Dépôt public : <b>https://github.com/zikosalmen/SOA-tp3.git</b>", S_BODY),
        Paragraph("• Contenu : Projet Maven complet, fichier <code>.war</code>, rapport PDF, assets.", S_BODY),
        Paragraph("• Commande de clonage :<br/><code>git clone https://github.com/zikosalmen/SOA-tp3.git</code>", S_BODY),
    ], bg=BG_BLUE, border_color=HexColor("#bfdbfe"), width=(INNER_W-6)/2)

    story.append(two_cols(col_dep, col_git))

    doc.build(story, canvasmaker=AcademicCanvas)
    print("PDF généré avec succès !")

if __name__ == "__main__":
    build_perfect_report()
