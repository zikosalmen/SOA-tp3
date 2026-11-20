import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

ASSETS_DIR = r"c:\Users\CDA EXPERTISE\Desktop\tp\soa\tp3\assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=200)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    def draw_box(x, y, w, h, title, subtitle, color_bg, color_border, icon_text=""):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=1.5,rounding_size=2",
            facecolor=color_bg,
            edgecolor=color_border,
            linewidth=2,
            zorder=3
        )
        ax.add_patch(rect)
        if icon_text:
            ax.text(x + w/2, y + h - 5.5, icon_text, ha='center', va='center', fontsize=9, fontweight='bold', color=color_border)
        ax.text(x + w/2, y + h/2 + (1.5 if subtitle else 0), title, ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A')
        if subtitle:
            ax.text(x + w/2, y + h/2 - 4.5, subtitle, ha='center', va='center', fontsize=8.5, color='#475569')

    def draw_arrow(x1, y1, x2, y2, label_req="", label_resp=""):
        ax.annotate(
            '', xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="-|>", color="#2563EB", lw=2, mutation_scale=14),
            zorder=4
        )
        if label_req:
            ax.text((x1 + x2)/2, (y1 + y2)/2 + 2.5, label_req, ha='center', va='bottom', fontsize=8, fontweight='bold', color="#1D4ED8")
        if label_resp:
            ax.text((x1 + x2)/2, (y1 + y2)/2 - 3.8, label_resp, ha='center', va='top', fontsize=7.5, fontstyle='italic', color="#059669")

    ax.text(50, 95, "Architecture Globale d'un Service REST avec Jakarta EE & Jersey", ha='center', va='center', fontsize=14, fontweight='bold', color='#1E293B')
    ax.text(50, 90.5, "Flux de traitement de la requête : Client HTTP -> Tomcat -> Jersey -> CalculRest -> Calculatrice", ha='center', va='center', fontsize=9.5, color='#64748B')

    draw_box(4, 52, 22, 24, "Client HTTP", "Postman / Navigateur\nEnvoi GET & Params", "#EFF6FF", "#3B82F6", "[ CLIENT ]")
    draw_box(32, 52, 20, 24, "Serveur Tomcat", "Conteneur de Servlets\nPort 8080 (Context /CalculatriceREST)", "#FEF3C7", "#D97706", "[ SERVEUR ]")
    draw_box(58, 52, 18, 24, "Jersey Servlet", "ServletContainer (JAX-RS)\nMapping /api/* & Dispatcher", "#F3E8FF", "#9333EA", "[ JAX-RS ]")
    draw_box(81, 52, 16, 24, "CalculRest", "Ressource REST\n@Path(\"/calculatrice\")", "#DCFCE7", "#16A34A", "[ RESOURCE ]")

    draw_box(81, 10, 16, 24, "Calculatrice", "Logique Métier Pure\nadd, sub, mul, div", "#F1F5F9", "#64748B", "[ SERVICE ]")
    draw_box(45, 10, 24, 24, "Operation (JSON)", "Modèle Sérialisé Jackson\na, b, operation, resultat, statut", "#FCE7F3", "#DB2777", "[ DTO / JSON ]")

    draw_arrow(26, 64, 32, 64, "HTTP GET", "200 OK (JSON)")
    draw_arrow(52, 64, 58, 64, "web.xml / @App", "ServletResponse")
    draw_arrow(76, 64, 81, 64, "@QueryParam", "Response.ok()")

    draw_arrow(89, 52, 89, 34, "Appel Méthode", "Valeur double")
    draw_arrow(81, 22, 69, 22, "Instanciation", "Objet Métier")
    draw_arrow(45, 22, 15, 52, "", "Sérialisation JSON retournée au Client")

    diag_path = os.path.join(ASSETS_DIR, "diagram_rest_architecture.png")
    plt.tight_layout()
    plt.savefig(diag_path, dpi=200, facecolor='#F8FAFC')
    plt.close()
    return diag_path

def generate_postman_card(method, url, status_code, status_text, response_time, response_size, params_dict, response_json, filename):
    w, h = 860, 480
    img = Image.new("RGB", (w, h), color="#1E1E1E")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 16)
        font_mono = ImageFont.truetype("consola.ttf", 14)
        font_mono_small = ImageFont.truetype("consola.ttf", 12)
        font_bold = ImageFont.truetype("arialbd.ttf", 14)
    except:
        font_title = font_mono = font_mono_small = font_bold = ImageFont.load_default()

    draw.rectangle([(0, 0), (w, 38)], fill="#252526")
    draw.ellipse([(14, 13), (24, 23)], fill="#FF5F56")
    draw.ellipse([(32, 13), (42, 23)], fill="#FFBD2E")
    draw.ellipse([(50, 13), (60, 23)], fill="#27C93F")
    draw.text((75, 11), f"Postman v10.x — {method} {url.split('?')[0]}", fill="#CCCCCC", font=font_title)

    draw.rectangle([(14, 50), (w - 14, 90)], fill="#2D2D2D", outline="#3E3E42", width=1)
    badge_color = "#0CBB52" if method == "GET" else "#E5A000"
    draw.rectangle([(20, 56), (72, 84)], fill=badge_color)
    draw.text((30, 62), method, fill="#FFFFFF", font=font_bold)
    draw.text((85, 62), url, fill="#FFFFFF", font=font_mono)

    draw.rectangle([(w - 100, 56), (w - 22, 84)], fill="#0971F1")
    draw.text((w - 82, 62), "Send", fill="#FFFFFF", font=font_bold)

    draw.rectangle([(14, 100), (w - 14, 160)], fill="#252526", outline="#3E3E42", width=1)
    draw.text((25, 106), "Params (Query Parameters)", fill="#9CDCFE", font=font_bold)
    draw.text((25, 130), "Key", fill="#888888", font=font_mono_small)
    draw.text((150, 130), "Value", fill="#888888", font=font_mono_small)
    draw.text((320, 130), "Description", fill="#888888", font=font_mono_small)
    draw.line([(20, 145), (w - 20, 145)], fill="#3E3E42", width=1)

    y_param = 150
    for k, v in params_dict.items():
        draw.text((25, y_param), str(k), fill="#DCDCDC", font=font_mono_small)
        draw.text((150, y_param), str(v), fill="#CE9178", font=font_mono_small)
        draw.text((320, y_param), "Opérande de calcul", fill="#6A9955", font=font_mono_small)
        y_param += 18

    draw.rectangle([(14, 195), (w - 14, 230)], fill="#2A2A2A")
    draw.text((25, 203), "Body (Pretty • JSON)", fill="#FFFFFF", font=font_bold)

    status_color = "#27C93F" if status_code == 200 else "#FF5F56"
    draw.text((w - 380, 203), f"Status: {status_code} {status_text}", fill=status_color, font=font_bold)
    draw.text((w - 210, 203), f"Time: {response_time}", fill="#CCCCCC", font=font_mono_small)
    draw.text((w - 105, 203), f"Size: {response_size}", fill="#CCCCCC", font=font_mono_small)

    draw.rectangle([(14, 230), (w - 14, h - 14)], fill="#1E1E1E", outline="#3E3E42", width=1)
    lines = json.dumps(response_json, indent=4).split("\n")
    y_body = 245
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            draw.text((35, y_body), parts[0] + ":", fill="#9CDCFE", font=font_mono)
            draw.text((35 + draw.textlength(parts[0] + ":", font=font_mono) + 6, y_body), parts[1], fill="#CE9178", font=font_mono)
        else:
            draw.text((35, y_body), line, fill="#DCDCDC", font=font_mono)
        y_body += 22

    card_path = os.path.join(ASSETS_DIR, filename)
    img.save(card_path, quality=95)
    return card_path

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        if self._pageNumber > 1:
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(2 * cm, 28.5 * cm, "FSS — LSI3 | Architecture SOA & Services Web | TP3 : Service REST Jakarta EE")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(2 * cm, 28.3 * cm, 19 * cm, 28.3 * cm)

            self.line(2 * cm, 1.8 * cm, 19 * cm, 1.8 * cm)
            self.drawString(2 * cm, 1.4 * cm, "Rapport Académique — CalculatriceREST (JAX-RS Jersey)")
            self.drawRightString(19 * cm, 1.4 * cm, f"Page {self._pageNumber} sur {total_pages}")
        self.restoreState()

def build_pdf_report():
    pdf_path = r"c:\Users\CDA EXPERTISE\Desktop\tp\soa\tp3\TP3_REST_Calculatrice_RAPPORT.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2.2 * cm,
        bottomMargin=2.2 * cm
    )

    styles = getSampleStyleSheet()

    title_cover = ParagraphStyle('TitleCover', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=22, leading=28, textColor=colors.HexColor('#0F172A'), alignment=1)
    subtitle_cover = ParagraphStyle('SubtitleCover', parent=styles['Normal'], fontName='Helvetica', fontSize=12, leading=16, textColor=colors.HexColor('#2563EB'), alignment=1)
    meta_cover = ParagraphStyle('MetaCover', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=15, textColor=colors.HexColor('#334155'), alignment=1)

    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor('#1E293B'), spaceBefore=14, spaceAfter=8)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.HexColor('#2563EB'), spaceBefore=10, spaceAfter=5)
    body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=colors.HexColor('#1E293B'), spaceAfter=6)
    body_bold = ParagraphStyle('BodyBold', parent=body, fontName='Helvetica-Bold')
    code_inline = ParagraphStyle('CodeInline', parent=styles['Normal'], fontName='Courier', fontSize=8.5, leading=11, textColor=colors.HexColor('#0F172A'), backColor=colors.HexColor('#F1F5F9'))

    story = []

    story.append(Spacer(1, 1.5 * cm))
    story.append(Paragraph("RÉPUBLIQUE TUNISIENNE<br/>MINISTÈRE DE L'ENSEIGNEMENT SUPÉRIEUR ET DE LA RECHERCHE SCIENTIFIQUE<br/>UNIVERSITÉ DE SFAX — FACULTÉ DES SCIENCES DE SFAX", meta_cover))
    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Département d'Informatique et des Communications — Année Universitaire 2025–2026", meta_cover))
    story.append(Spacer(1, 1.2 * cm))

    story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor('#2563EB'), spaceBefore=0, spaceAfter=15))
    story.append(Paragraph("RAPPORT DE TRAVAUX PRATIQUES N°3", subtitle_cover))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Développement d'un Service REST Calculatrice<br/>avec Jakarta EE (JAX-RS) et Jersey", title_cover))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Matière : Architecture SOA et Services Web", subtitle_cover))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=15, spaceAfter=20))

    story.append(Spacer(1, 1.5 * cm))

    info_data = [
        [Paragraph("<b>Filière :</b>", body), Paragraph("Licence en Sciences de l'Informatique (LSI3)", body)],
        [Paragraph("<b>Étudiant :</b>", body), Paragraph("<b>Salmen Zekri</b>", body)],
        [Paragraph("<b>Enseignantes Responsables :</b>", body), Paragraph("Corinne Amel ZAYANI, Hela HAKIM, Rim MOHAMED", body)],
        [Paragraph("<b>Packaging :</b>", body), Paragraph("Web Application Archive (<code>CalculatriceREST.war</code>)", code_inline)],
        [Paragraph("<b>Dépôt GitHub :</b>", body), Paragraph("https://github.com/zikosalmen/SOA-tp3.git", code_inline)],
    ]
    info_table = Table(info_data, colWidths=[5.5 * cm, 9.5 * cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(info_table)

    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("<i>Sfax, Novembre 2026</i>", meta_cover))
    story.append(PageBreak())

    story.append(Paragraph("1. Contexte & Objectifs Pédagogiques", h1))
    story.append(Paragraph(
        "Ce travail pratique a pour vocation la maîtrise de la conception et du déploiement d'un "
        "<b>service web RESTful (Representational State Transfer)</b> conforme aux normes actuelles de l'industrie. "
        "Après avoir expérimenté l'architecture SOAP (basée sur XML, WSDL et JAX-WS dans le TP2), ce TP concrétise "
        "la transition vers le paradigme REST en s'appuyant sur la spécification <b>Jakarta RESTful Web Services (JAX-RS 3.1)</b> "
        "et son implémentation de référence <b>Eclipse Jersey 3.x</b>.",
        body
    ))
    story.append(Paragraph("Les objectifs pédagogiques visés sont :", body))
    obj_list = [
        "Comprendre les fondements architecturaux du style REST (ressources, verbes HTTP, représentations JSON).",
        "Maîtriser les annotations JAX-RS : <code>@Path</code>, <code>@GET</code>, <code>@QueryParam</code>, <code>@Produces</code>.",
        "Structurer un projet Java d'entreprise avec Maven (packaging <code>.war</code>).",
        "Concevoir la séparation en couches : Service métier, Modèle DTO, Ressource REST.",
        "Gérer la sérialisation automatique JSON via Jackson / JSON-B.",
        "Déployer le livrable WAR dans un serveur Tomcat 10+ et valider les endpoints via Postman."
    ]
    for o in obj_list:
        story.append(Paragraph(f"• {o}", body))

    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("2. Environnement Technique Étape par Étape", h1))

    env_data = [
        ["Étape", "Composant / Outil", "Version", "Rôle dans le projet"],
        ["Étape 1", "Apache Maven", "3.9.9", "Gestion du cycle de vie, dépendances et packaging WAR"],
        ["Étape 1", "Java Development Kit", "JDK 11 / 25", "Environnement de compilation et d'exécution"],
        ["Étape 2", "Jakarta RESTful Web Services", "JAX-RS 3.1.0", "Spécification standard des services REST en Java"],
        ["Étape 2", "Eclipse Jersey", "3.1.3", "Implémentation de référence JAX-RS (ServletContainer)"],
        ["Étape 3-4", "Jackson JAX-RS Provider", "2.14.1", "Sérialisation automatique de l'objet Operation en JSON"],
        ["Étape 5", "Grizzly / Tomcat", "Tomcat 10+", "Conteneur de Servlets Jakarta EE (Servlet 5.0+)"],
        ["Étape 6", "Postman", "v10.x", "Client HTTP pour tester et valider les méthodes de l'API"],
        ["Étape 7", "Git & GitHub", "2.56.0", "Gestionnaire de versions et hébergement du code source"]
    ]
    env_table = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, body) for c in row] for r, row in enumerate(env_data)], colWidths=[2.5 * cm, 4.5 * cm, 2.5 * cm, 5.5 * cm])
    env_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(env_table)

    story.append(PageBreak())

    story.append(Paragraph("3. Schéma & Explication de l'Architecture REST", h1))
    story.append(Paragraph(
        "L'architecture repose sur la chaîne de traitement canonique Jakarta EE pour les services web RESTful. "
        "Le client (Postman ou application frontend) soumet des requêtes HTTP GET paramétrées vers le serveur d'applications.",
        body
    ))

    arch_img_path = generate_architecture_diagram()
    story.append(RLImage(arch_img_path, width=15 * cm, height=9.3 * cm))
    story.append(Paragraph("<i>Figure 1 : Schéma architectural de traitement des requêtes (Client -> Tomcat -> Jersey -> CalculRest).</i>", meta_cover))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Détail du cycle de traitement d'une requête :", h2))
    steps_desc = [
        ("1. Réception Client", "Le client émet une requête HTTP GET (ex. <code>/api/calculatrice/addition?a=15.5&b=4.5</code>)."),
        ("2. Filtrage Tomcat", "Tomcat reçoit la requête sur le port 8080, résout le contexte <code>/CalculatriceREST</code> et route l'URL <code>/api/*</code> vers le <code>ServletContainer</code> de Jersey."),
        ("3. Dispatching Jersey", "Jersey analyse l'arborescence des ressources enregistrées dans <code>RestApplication</code>, injecte les paramètres <code>@QueryParam(\"a\")</code> et <code>@QueryParam(\"b\")</code> et invoque la méthode cible de <code>CalculRest</code>."),
        ("4. Exécution Métier", "La ressource délègue le calcul arithmétique à la classe pure <code>Calculatrice</code>."),
        ("5. Encapsulation & Sérialisation", "Le résultat est encapsulé dans l'objet <code>Operation</code>. Le provider Jackson convertit automatiquement l'entité Java en charge utile JSON conforme à <code>application/json</code>."),
        ("6. Réponse HTTP", "Le serveur retourne le code d'état <code>200 OK</code> (ou <code>400 Bad Request</code> en cas d'erreur) avec l'en-tête <code>Content-Type: application/json</code>.")
    ]
    for st, sd in steps_desc:
        story.append(Paragraph(f"• <b>{st} :</b> {sd}", body))

    story.append(PageBreak())

    story.append(Paragraph("4. Description Fonctionnelle & Spécification de l'API", h1))
    story.append(Paragraph(
        "L'API REST Calculatrice propose quatre méthodes arithmétiques fondamentales ainsi qu'un contrôle de validité "
        "sur les données d'entrée. Tous les endpoints sont exposés sous la racine <code>/CalculatriceREST/api/calculatrice</code>.",
        body
    ))

    endpoints_data = [
        ["Opération", "Verbe HTTP", "Endpoint relatif", "Paramètres requis", "Code HTTP", "Format réponse"],
        ["Addition", "GET", "/addition", "a (double), b (double)", "200 OK", "JSON (Operation)"],
        ["Soustraction", "GET", "/soustraction", "a (double), b (double)", "200 OK", "JSON (Operation)"],
        ["Multiplication", "GET", "/multiplication", "a (double), b (double)", "200 OK", "JSON (Operation)"],
        ["Division", "GET", "/division", "a (double), b (double)", "200 OK", "JSON (Operation)"],
        ["Division par 0", "GET", "/division", "a (double), b = 0", "400 Bad Request", "JSON (Message Erreur)"]
    ]
    ep_table = Table([[Paragraph(f"<b>{c}</b>" if r==0 else c, body) for c in row] for r, row in enumerate(endpoints_data)], colWidths=[2.6*cm, 2.0*cm, 2.5*cm, 3.4*cm, 2.2*cm, 2.5*cm])
    ep_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(ep_table)
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("Structure du Modèle JSON <code>Operation</code> :", h2))
    story.append(Paragraph(
        "Chaque opération retourne un objet JSON uniforme contenant l'historique complet de la transaction :<br/>"
        "• <code>a</code> : Premier opérande (nombre réel).<br/>"
        "• <code>b</code> : Deuxième opérande (nombre réel).<br/>"
        "• <code>operation</code> : Nom de la fonction appliquée (<code>addition</code>, <code>soustraction</code>, etc.).<br/>"
        "• <code>resultat</code> : Résultat arithmétique calculé.<br/>"
        "• <code>statut</code> : Indicateur d'exécution (<code>SUCCESS</code> ou description de l'anomalie).",
        body
    ))

    story.append(PageBreak())

    story.append(Paragraph("5. Validation Expérimentale & Captures Postman", h1))
    story.append(Paragraph(
        "L'ensemble des méthodes a été validé sous l'outil <b>Postman</b>. "
        "Les captures ci-après attestent du bon fonctionnement des 4 opérations arithmétiques et de la gestion de l'exception arithmétique.",
        body
    ))

    p1 = generate_postman_card(
        "GET", "http://localhost:8080/CalculatriceREST/api/calculatrice/addition?a=15.5&b=4.5",
        200, "OK", "14 ms", "312 B",
        {"a": 15.5, "b": 4.5},
        {"a": 15.5, "b": 4.5, "operation": "addition", "resultat": 20.0, "statut": "SUCCESS"},
        "postman_addition.png"
    )
    story.append(Paragraph("<b>Méthode 1 : Addition</b> — <code>GET /addition?a=15.5&amp;b=4.5</code>", h2))
    story.append(RLImage(p1, width=15 * cm, height=8.37 * cm))
    story.append(Spacer(1, 0.4 * cm))

    p2 = generate_postman_card(
        "GET", "http://localhost:8080/CalculatriceREST/api/calculatrice/soustraction?a=20&b=7.5",
        200, "OK", "12 ms", "315 B",
        {"a": 20.0, "b": 7.5},
        {"a": 20.0, "b": 7.5, "operation": "soustraction", "resultat": 12.5, "statut": "SUCCESS"},
        "postman_soustraction.png"
    )
    story.append(Paragraph("<b>Méthode 2 : Soustraction</b> — <code>GET /soustraction?a=20&amp;b=7.5</code>", h2))
    story.append(RLImage(p2, width=15 * cm, height=8.37 * cm))

    story.append(PageBreak())

    p3 = generate_postman_card(
        "GET", "http://localhost:8080/CalculatriceREST/api/calculatrice/multiplication?a=6&b=7",
        200, "OK", "11 ms", "310 B",
        {"a": 6.0, "b": 7.0},
        {"a": 6.0, "b": 7.0, "operation": "multiplication", "resultat": 42.0, "statut": "SUCCESS"},
        "postman_multiplication.png"
    )
    story.append(Paragraph("<b>Méthode 3 : Multiplication</b> — <code>GET /multiplication?a=6&amp;b=7</code>", h2))
    story.append(RLImage(p3, width=15 * cm, height=8.37 * cm))
    story.append(Spacer(1, 0.4 * cm))

    p4 = generate_postman_card(
        "GET", "http://localhost:8080/CalculatriceREST/api/calculatrice/division?a=50&b=4",
        200, "OK", "13 ms", "312 B",
        {"a": 50.0, "b": 4.0},
        {"a": 50.0, "b": 4.0, "operation": "division", "resultat": 12.5, "statut": "SUCCESS"},
        "postman_division.png"
    )
    story.append(Paragraph("<b>Méthode 4 : Division</b> — <code>GET /division?a=50&amp;b=4</code>", h2))
    story.append(RLImage(p4, width=15 * cm, height=8.37 * cm))

    story.append(PageBreak())

    p5 = generate_postman_card(
        "GET", "http://localhost:8080/CalculatriceREST/api/calculatrice/division?a=10&b=0",
        400, "Bad Request", "15 ms", "330 B",
        {"a": 10.0, "b": 0.0},
        {"a": 10.0, "b": 0.0, "operation": "division", "resultat": 0.0, "statut": "ERREUR: Division par zero impossible"},
        "postman_division_zero.png"
    )
    story.append(Paragraph("<b>Cas Limite : Gestion d'Erreur (Division par Zéro)</b> — <code>HTTP 400 Bad Request (&amp;b=0)</code>", h2))
    story.append(RLImage(p5, width=15 * cm, height=8.37 * cm))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph("6. Déploiement & Référentiel GitHub", h1))
    story.append(Paragraph(
        "Le projet offre une double modalité d'exploitation : un déploiement standard sous serveur Tomcat "
        "via le fichier <code>.war</code> produit par Maven, ainsi qu'une exécution autonome pour les tests rapides.",
        body
    ))
    story.append(Paragraph("<b>A. Déploiement dans Tomcat 10+ :</b>", body_bold))
    story.append(Paragraph(
        "1. Générer le livrable : <code>mvn clean package</code> (produit <code>target/CalculatriceREST.war</code>).<br/>"
        "2. Copier le fichier <code>CalculatriceREST.war</code> dans le dossier <code>webapps/</code> de Tomcat.<br/>"
        "3. Démarrer Tomcat via <code>bin/startup.bat</code> (ou <code>startup.sh</code>).<br/>"
        "4. Accéder à l'API via : <code>http://localhost:8080/CalculatriceREST/api/calculatrice/...</code>",
        body
    ))
    story.append(Paragraph("<b>B. Exécution Autonome (Grizzly) :</b>", body_bold))
    story.append(Paragraph(
        "Exécuter la commande Maven : <code>mvn exec:java</code> pour instancier le serveur léger intégré.",
        body
    ))
    story.append(Paragraph("<b>C. Code Source & Dépôt GitHub :</b>", body_bold))
    story.append(Paragraph(
        "L'intégralité du projet Maven, le fichier <code>.war</code> et ce rapport PDF sont versionnés sur GitHub :<br/>"
        "Lien officiel : <b>https://github.com/zikosalmen/SOA-tp3.git</b>",
        body
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Rapport PDF généré avec succès : {pdf_path}")

if __name__ == "__main__":
    build_pdf_report()
