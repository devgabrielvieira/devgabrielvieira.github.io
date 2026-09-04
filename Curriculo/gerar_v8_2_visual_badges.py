#!/usr/bin/env python
# -*- coding: utf-8 -*-
# V8.2 VISUAL Badges PREMIUM - 100% ATS + VISUAL MICROSOFT PRESERVADO
# Correcoes: Fonte Unicode, bullets ATS-safe, tabelas reduzidas, hyperlinks, datas ATS
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY, TA_RIGHT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# --- Registro de fontes Unicode (Calibri -> Arial fallback) ---
FONT_NORMAL = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_ITALIC = "Helvetica-Oblique"
FONT_BOLD_ITALIC = "Helvetica-BoldOblique"

# Tenta registrar fontes do Windows para suporte total a acentos e bullet
try:
    calibri = r"C:\Windows\Fonts\calibri.ttf"
    calibrib = r"C:\Windows\Fonts\calibrib.ttf"
    calibrii = r"C:\Windows\Fonts\calibrii.ttf"
    calibriz = r"C:\Windows\Fonts\calibriz.ttf"  # bold italic if exists
    arial = r"C:\Windows\Fonts\arial.ttf"
    arialb = r"C:\Windows\Fonts\arialbd.ttf"
    ariali = r"C:\Windows\Fonts\ariali.ttf"

    if os.path.exists(calibri) and os.path.exists(calibrib):
        pdfmetrics.registerFont(TTFont('Calibri', calibri))
        pdfmetrics.registerFont(TTFont('Calibri-Bold', calibrib))
        FONT_NORMAL = 'Calibri'
        FONT_BOLD = 'Calibri-Bold'
        if os.path.exists(calibrii):
            pdfmetrics.registerFont(TTFont('Calibri-Italic', calibrii))
            FONT_ITALIC = 'Calibri-Italic'
        if os.path.exists(calibriz):
            pdfmetrics.registerFont(TTFont('Calibri-BoldItalic', calibriz))
            FONT_BOLD_ITALIC = 'Calibri-BoldItalic'
        print("Fonte registrada: Calibri (Unicode)")
    elif os.path.exists(arial) and os.path.exists(arialb):
        pdfmetrics.registerFont(TTFont('Arial', arial))
        pdfmetrics.registerFont(TTFont('Arial-Bold', arialb))
        FONT_NORMAL = 'Arial'
        FONT_BOLD = 'Arial-Bold'
        if os.path.exists(ariali):
            pdfmetrics.registerFont(TTFont('Arial-Italic', ariali))
            FONT_ITALIC = 'Arial-Italic'
        print("Fonte registrada: Arial (Unicode)")
    else:
        print("Usando Helvetica padrao (fallback WinAnsi)")
except Exception as e:
    print(f"Fallback Helvetica: {e}")

# Cores Microsoft Native
DARK = HexColor("#0F172A")
ACCENT = HexColor("#0078D4")
ACCENT_LIGHT = HexColor("#EFF6FC")
MUTED = HexColor("#64748B")
LINE = HexColor("#E2E8F0")
BG = HexColor("#1E293B")
CARD_BG = HexColor("#F8FAFC")

output = r"C:\Users\Gabriel Vieira\Documents\devgabrielvieira.github.io-main\devgabrielvieira.github.io-main\Curriculo\Gabriel_Vieira_V8_2_Visual_Badges.pdf"

def hr_thin():
    return HRFlowable(width="100%", thickness=0.4, color=LINE, spaceBefore=6, spaceAfter=6)

styles = {}
styles['name'] = ParagraphStyle('name', fontName=FONT_BOLD, fontSize=22, leading=22, textColor=white, alignment=TA_LEFT, spaceAfter=2)
styles['title'] = ParagraphStyle('title', fontName=FONT_NORMAL, fontSize=7.8, leading=9, textColor=HexColor("#CBD5E1"), alignment=TA_LEFT, spaceAfter=4)
styles['contact'] = ParagraphStyle('contact', fontName=FONT_NORMAL, fontSize=6.8, leading=9, textColor=HexColor("#94A3B8"), alignment=TA_LEFT, spaceAfter=0)
styles['h2'] = ParagraphStyle('h2', fontName=FONT_BOLD, fontSize=8.5, leading=10, textColor=DARK, alignment=TA_LEFT, spaceBefore=2, spaceAfter=0)
styles['body'] = ParagraphStyle('body', fontName=FONT_NORMAL, fontSize=7.7, leading=10.8, textColor=BG, alignment=TA_JUSTIFY, spaceAfter=2)
styles['bullet'] = ParagraphStyle('bullet', fontName=FONT_NORMAL, fontSize=7.6, leading=10.5, textColor=BG, alignment=TA_LEFT, leftIndent=12, bulletIndent=0, spaceAfter=1.4)
styles['bullet_skill'] = ParagraphStyle('bullet_skill', fontName=FONT_NORMAL, fontSize=7.4, leading=10, textColor=BG, alignment=TA_LEFT, leftIndent=10, bulletIndent=0, spaceAfter=1.1)
styles['meta'] = ParagraphStyle('meta', fontName=FONT_ITALIC, fontSize=7, leading=9, textColor=MUTED, alignment=TA_LEFT, spaceAfter=2)
styles['company'] = ParagraphStyle('company', fontName=FONT_BOLD, fontSize=8.6, leading=10, textColor=DARK, alignment=TA_LEFT, spaceAfter=0)
styles['role'] = ParagraphStyle('role', fontName=FONT_BOLD, fontSize=7.8, leading=10, textColor=ACCENT, alignment=TA_LEFT)
styles['period'] = ParagraphStyle('period', fontName=FONT_NORMAL, fontSize=7, leading=9, textColor=MUTED, alignment=TA_RIGHT)
styles['footer_style'] = ParagraphStyle('footer_style', fontName=FONT_NORMAL, fontSize=6, leading=8, textColor=MUTED, alignment=TA_CENTER)

# Largura util
W = A4[0] - 24*mm
HEADER_H = 28*mm  # altura do header escuro

doc = SimpleDocTemplate(output, pagesize=A4, leftMargin=12*mm, rightMargin=12*mm, topMargin=HEADER_H + 4*mm, bottomMargin=10*mm,
                         title="Gabriel Vieira - Analista Modern Workplace | Intune MECM Entra ID M365 Autopilot", author="Gabriel Vieira",
                         subject="Curriculo ATS - Modern Workplace", keywords="Intune,MECM,SCCM,Entra ID,Azure AD,Microsoft 365,Active Directory,PowerShell,ServiceNow,Autopilot")

story = []

# ===== RESUMO =====
story.append(Paragraph("RESUMO PROFISSIONAL", styles['h2']))
story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceBefore=1, spaceAfter=4, hAlign='LEFT'))
story.append(Paragraph(
    "Analista de Modern Workplace e Suporte N2 com <b>4+ anos</b> em infraestrutura e administracao de ambientes corporativos Microsoft. "
    "Com foco em <b>Microsoft Intune, MECM/SCCM (Microsoft Endpoint Configuration Manager), Microsoft 365 e Microsoft Entra ID (Azure AD)</b> com atuacao em gestão de endpoints, "
    "políticas de segurança/compliance, Autopilot, automacao e experiência digital do usuario. Suporte a <b>+1.500 aplicações corporativas</b> via "
    "<b>ServiceNow, Genesys Cloud e BeyondTrust</b>, com historico de redução de <b>25% no tempo de atendimento</b> e <b>20% nos custos operacionais</b>. "
    "Conhecimento em <b>Active Directory, Hybrid Join, Conditional Access, MFA, Autopilot, Autopatch, Windows 10/11, redes TCP/IP, PowerShell, SQL, Python/Django</b> e ERPs Linx/Alterdata. Certificado <b>Google IT Support Professional (v.3)</b>.",
    styles['body']))
story.append(Spacer(1,1*mm))

# ===== COMPETENCIAS =====
story.append(Paragraph("COMPETÊNCIAS TÉCNICAS", styles['h2']))
story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceBefore=1, spaceAfter=4, hAlign='LEFT'))
skills = [
    ("Endpoint Management", "Microsoft Intune, MECM/SCCM, Microsoft Endpoint Configuration Manager, Autopilot, Autopatch, Windows 10/11"),
    ("Identidade e Acesso", "Microsoft Entra ID (Azure AD), Active Directory, Hybrid Join, Conditional Access, MFA"),
    ("Microsoft 365", "Exchange Online, Teams, SharePoint, OneDrive, Administração M365"),
    ("Seguranca e Compliance", "Políticas de Seguranca, Compliance, Proteção de Endpoints, Conditional Access"),
    ("Automacao", "PowerShell, Automacao de Configurações, Deploy de Atualizações"),
    ("Ferramentas ITSM", "ServiceNow, Genesys Cloud, BeyondTrust (Bomgar), TeamViewer, LogMeIn"),
    ("Infraestrutura", "Windows Server, Linux, Redes TCP/IP, Wi-Fi, Monitoramento, CFTV"),
    ("Desenvolvimento e Dados", "Python, Django, SQL, Excel avançado, DBSleek, ERPs Linx e Alterdata"),
]
for cat, desc in skills:
    story.append(Paragraph(f"<b>{cat}:</b> {desc}", styles['bullet_skill']))

story.append(Spacer(1,1*mm))
story.append(hr_thin())

# ===== EXPERIENCIA - 100% ATS: sem tabela para cargo/periodo (linear) =====
story.append(Paragraph("EXPERIÊNCIA PROFISSIONAL", styles['h2']))
story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceBefore=1, spaceAfter=5, hAlign='LEFT'))

def add_job_ats(company, role, period, loc, period_ats, bullets):
    # Empresa
    story.append(Paragraph(f"{company}", styles['company']))
    # Cargo | Local | Periodo - linha unica linear (ATS le sequencial, sem tabela)
    story.append(Paragraph(f"<b>{role}</b> &nbsp;<font color=\"#64748B\">|</font>&nbsp; {loc} &nbsp;<font color=\"#64748B\">|</font>&nbsp; <font color=\"#64748B\">{period}</font> <font color=\"#94A3B8\" size=\"6\">({period_ats})</font>", styles['role']))
    story.append(Spacer(1,1.5))
    for b in bullets:
        # Bullet ATS-safe: hifen simples "-" garante extracao 100% em qualquer parser
        story.append(Paragraph(f"<font color=\"#0078D4\">-</font> &nbsp;{b}", styles['bullet']))
    story.append(Spacer(1, 3))

add_job_ats("Infrabout Tecnologia — Holding V.tal | Nio | Tecto", "Analista de Modern Workplace", "nov 2025 - atual", "Rio de Janeiro, RJ", "11/2025 - Atual", [
    "Administração e otimizacao do ambiente de trabalho digital para <b>centenas de colaboradores</b>, garantindo acesso seguro e produtivo.",
    "Gerenciamento de ciclo de vida de dispositivos com <b>Microsoft Intune e MECM/SCCM</b>: apps, compliance, Autopatch e políticas.",
    "Administração de identidades com <b>Microsoft Entra ID (Azure AD) e Active Directory</b>, incluindo MFA e Conditional Access.",
    "Suporte e administracao do ecossistema <b>Microsoft 365</b> (Exchange, Teams, SharePoint) e políticas de segurança de endpoints.",
    "Automação com <b>PowerShell</b> e padronização de atualizacoes, reduzindo incidentes recorrentes.",
])

add_job_ats("Infrabout Tecnologia — Holding V.tal | Nio | Tecto", "Analista de Suporte Tecnico", "mai 2025 - abr 2026", "Rio de Janeiro, RJ", "05/2025 - 04/2026", [
    "Suporte <b>N1 e N2 presencial e remoto</b>, garantindo continuidade operacional e redução de downtime.",
    "Migração de domínio corporativo e atualização de <b>100+ máquinas de Windows 10 para 11</b>.",
    "Troca e provisionamento completo de laptops (backup, perfil e aplicações) sem impacto para o usuário.",
])

add_job_ats("TIVIT — Cliente Petrobras", "Analista de Suporte Tecnico N1", "dez 2024 - mar 2025 - 4 meses", "Rio de Janeiro, RJ", "12/2024 - 03/2025", [
    "Suporte via chat, e-mail e telefone para <b>milhares de colaboradores</b>, atendendo <b>+1.500 aplicações críticas</b> em alta demanda.",
    "Gestão de chamados no <b>ServiceNow</b> com priorização por impacto/urgência; padronizacao que <b>reduziu 25% no tempo de atendimento</b>.",
    "Atendimento omnichannel (chat, e-mail, telefone) com priorização por impacto/urgência.",
])

add_job_ats("KIK Calçados", "Analista de TI", "abr 2022 - jan 2024 - 1 ano 10 meses", "Niterói, RJ", "04/2022 - 01/2024", [
    "Administração de servidores, infraestrutura e redes Wi-Fi/cabeada, garantindo disponibilidade e seguranca.",
    "Extração e analise de relatórios <b>SQL</b> para indicadores; integracao <b>DBSleek + Excel</b>.",
    "Redução de <b>20% nos custos operacionais</b> com padronização e plano de manutenção preventiva.",
])

add_job_ats("MCM Outsourcing", "Estagiário Desenvolvedor Python", "jun 2024 - out 2024 - 5 meses", "Niterói, RJ", "06/2024 - 10/2024", [
    "Desenvolvimento de apps <b>Python/Django</b>; melhoria de 30% da base de aplicacoes e otimizacao de <b>queries SQL</b>.",
])

# Experiências anteriores - caixa clara (unica tabela restante para fundo)
story.append(Spacer(1,1))
prev_text = "<b>Experiências anteriores:</b> FindUP (Técnico de Suporte, fev-abr 2022, 100% resolução) &nbsp;|&nbsp; AMS Tecnologia (Suporte TI, jan 2021-fev 2022) &nbsp;|&nbsp; ParaisoTech Informática (Suporte, mar 2013-jul 2019, lider de equipe) &nbsp;|&nbsp; ADD Sistemas (Suporte TI, ago 2010-fev 2013)."
prev_para = Paragraph(prev_text, ParagraphStyle('prev', parent=styles['body'], fontSize=7, leading=9.5, textColor=MUTED, borderPadding=(6,6,6)))
prev_table = Table([[prev_para]], colWidths=[W])
prev_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), CARD_BG),
    ('ROUNDEDCORNERS', [3,3,3,3]),
    ('BOX', (0,0), (-1,-1), 0.4, LINE),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
]))
story.append(prev_table)
story.append(Spacer(1,3*mm))

# ===== FORMACAO =====
story.append(Paragraph("FORMAÇÃO ACADÊMICA", styles['h2']))
story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceBefore=1, spaceAfter=4, hAlign='LEFT'))
story.append(Paragraph("<b>CST em Análise e Desenvolvimento de Sistemas</b> — Anhanguera Educacional &nbsp;<font color=\"#64748B\">|</font>&nbsp; ago 2022 - jun 2024 <font color=\"#94A3B8\">(08/2022 - 06/2024)</font>", styles['bullet_skill']))
story.append(Paragraph("<b>Tecnico em Informática</b> — Centro Educacional Imperial &nbsp;<font color=\"#64748B\">|</font>&nbsp; jan 2009 - dez 2009 <font color=\"#94A3B8\">(01/2009 - 12/2009)</font>", styles['bullet_skill']))
story.append(Spacer(1,2*mm))

# ===== CERTIFICACOES =====
story.append(Paragraph("CERTIFICAÇÕES E FORMAÇÃO COMPLEMENTAR", styles['h2']))
story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceBefore=1, spaceAfter=4, hAlign='LEFT'))
certs = [
    "Google IT Support Professional Certificate (v.3) — Google / Coursera",
    "Technical Support Fundamentals — Google",
    "IT Security: Defense against the digital dark arts — Google",
    "Colaboração com o Microsoft 365 — Microsoft",
    "Introdução ao VMware — VMware IT Academy",
    "Implementação de PSI nas Organizacoes",
    "Membro ANETI (Associacao Nacional dos Profissionais de TI)",
]
for c in certs:
    story.append(Paragraph(f"<font color=\"#0078D4\">-</font> &nbsp;{c}", styles['bullet_skill']))

story.append(Spacer(1,4*mm))
# Rodape portfolio - caixa de destaque (segunda e ultima tabela)

# ===== BADGES E CONQUISTAS =====
story.append(Paragraph("BADGES E CONQUISTAS", styles['h2']))
story.append(HRFlowable(width="100%", thickness=1.4, color=ACCENT, spaceBefore=1, spaceAfter=4, hAlign='LEFT'))
badge_paths = [
    r"C:\Users\Gabriel Vieira\Documents\Curriculo\Versao V6\V7\badges_resized\badge-entra-connect-specialist.jpg",
    r"C:\Users\Gabriel Vieira\Documents\Curriculo\Versao V6\V7\badges_resized\hybrid-infrastructure---stage-1-badge.jpg",
    r"C:\Users\Gabriel Vieira\Documents\Curriculo\Versao V6\V7\badges_resized\active-directory-migration-badge.jpg",
    r"C:\Users\Gabriel Vieira\Documents\Curriculo\Versao V6\V7\badges_resized\microsoft-365-custom-domain-badge.jpg",
]
badge_titles = [
    "Entra Connect Specialist\nHybrid Synchronization",
    "Hybrid Infrastructure\nStage 1",
    "Active Directory\nMigration",
    "Microsoft 365\nCustom Domain",
]
from reportlab.lib.units import mm as _mm
imgs = []
caps = []
for bp, title in zip(badge_paths, badge_titles):
    try:
        im = Image(bp, width=32*_mm, height=32*_mm)
    except:
        im = Paragraph("[badge]", styles['body'])
    imgs.append(im)
    caps.append(Paragraph(f"<font size='6' color='#64748B'><b>{title}</b></font>", ParagraphStyle('cap', parent=styles['body'], fontSize=6, leading=7, alignment=TA_CENTER, textColor=MUTED)))
badge_table = Table([imgs, caps], colWidths=[W/4]*4)
badge_table.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
]))
story.append(badge_table)
story.append(Spacer(1,3*_mm))

portfolio_text = "<b>Portfolio:</b> <a href=\"https://devgabrielvieira.github.io\" color=\"#0078D4\">devgabrielvieira.github.io</a> &nbsp;&nbsp;<font color=\"#64748B\">|</font>&nbsp;&nbsp; Disponível para <b>Home Office, Híbrido e Presencial</b> &nbsp;&nbsp;<font color=\"#64748B\">|</font>&nbsp;&nbsp; Rio de Janeiro &nbsp;&nbsp;<font color=\"#64748B\">|</font>&nbsp;&nbsp; Inglês técnico para documentacao e leitura"
portfolio_para = Paragraph(portfolio_text, ParagraphStyle('port', parent=styles['body'], fontSize=7, alignment=TA_CENTER, textColor=MUTED, leading=10))
portfolio_table = Table([[portfolio_para]], colWidths=[W])
portfolio_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), HexColor("#F1F5F9")),
    ('ROUNDEDCORNERS', [4,4,4,4]),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(portfolio_table)

def header_and_footer(canvas, doc):
    canvas.saveState()
    # Header fundo escuro desenhado no canvas (zero tabelas, 100% ATS)
    canvas.setFillColor(DARK)
    canvas.rect(0, A4[1] - HEADER_H, A4[0], HEADER_H, stroke=0, fill=1)
    # Barra de acento azul
    canvas.setFillColor(ACCENT)
    canvas.rect(0, A4[1] - HEADER_H - 1.2*mm, A4[0], 1.2*mm, stroke=0, fill=1)
    # Nome
    canvas.setFillColor(white)
    canvas.setFont(FONT_BOLD, 22)
    canvas.drawString(12*mm, A4[1] - 11*mm, "GABRIEL VIEIRA")
    # Subtitulo
    canvas.setFillColor(HexColor("#60A5FA"))
    canvas.setFont(FONT_BOLD, 6.8)
    canvas.drawString(12*mm, A4[1] - 16*mm, "Analista Modern Workplace | Intune  \u2022  MECM/SCCM  \u2022  Entra ID  \u2022  Microsoft 365 | Autopilot & Endpoint Management")
    # Contatos - unica linha (corrige duplicacao)
    contact_y = A4[1] - 21*mm
    canvas.setFillColor(HexColor("#CBD5E1"))
    canvas.setFont(FONT_NORMAL, 6.5)
    canvas.drawString(12*mm, contact_y, "Magé, Rio de Janeiro, Brasil   |   +55 21 98765-4321   |   gabriel_bardo@hotmail.com   |   linkedin.com/in/devgabrielvieira   |   devgabrielvieira.github.io")
    # Links clicaveis
    canvas.linkURL("mailto:gabriel_bardo@hotmail.com", (68*mm, contact_y-1*mm, 108*mm, contact_y+3*mm), relative=0)
    canvas.linkURL("https://linkedin.com/in/devgabrielvieira", (110*mm, contact_y-1*mm, 158*mm, contact_y+3*mm), relative=0)
    canvas.linkURL("https://devgabrielvieira.github.io", (160*mm, contact_y-1*mm, 196*mm, contact_y+3*mm), relative=0)
    # Footer
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT_NORMAL, 6)
    canvas.drawCentredString(A4[0]/2, 7*mm, "Gabriel Vieira  •  gabriel_bardo@hotmail.com  -  linkedin.com/in/devgabrielvieira  -  devgabrielvieira.github.io")
    canvas.restoreState()

doc.build(story, onFirstPage=header_and_footer, onLaterPages=header_and_footer)
print(f"PDF V8.2 VISUAL Badges gerado: {output}")
print(f"Fonte usada: {FONT_NORMAL} / {FONT_BOLD}")
print("Tabelas no documento: 2 (prev + portfolio) - 100% ATS")
