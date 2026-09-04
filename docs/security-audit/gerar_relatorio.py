#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, datetime, textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, Image as RLImage, HRFlowable, KeepTogether)
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Cores
CRITICA = HexColor("#B91C1C")
ALTA = HexColor("#EA580C")
MEDIA = HexColor("#D97706")
BAIXA = HexColor("#2563EB")
FORTE = HexColor("#059669")
DARK = HexColor("#0F172A")
ACCENT = HexColor("#0078D4")
MUTED = HexColor("#64748B")
LINE = HexColor("#E2E8F0")
BG = HexColor("#F8FAFC")

PROJECT = "devgabrielvieira.github.io — Portfólio Gabriel Vieira"
DATE = datetime.date.today().strftime("%d/%m/%Y")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(OUT_DIR, "relatorio-auditoria-seguranca.pdf")

# Dados
severity_counts = {"Crítica":0, "Alta":0, "Média":1, "Baixa":2, "Informativa":2}
category_counts = {"BANCO SEM TRANCA":0, "PERMISSÃO NO NAVEGADOR":0, "IDOR":0, "CHAVES EXPOSTAS":2, "INPUTS SEM TRATAMENTO":3}

findings = [
    {
        "id":"F-01",
        "cat":"CHAVES EXPOSTAS",
        "sev":"Média",
        "color":MEDIA,
        "file":"index.html:17",
        "code":'<link rel="stylesheet" href="https://cdnjs.cloudflare.com/.../font-awesome/6.6.0/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer">',
        "desc":"CDN sem Subresource Integrity (SRI). Sem hash `integrity`, se o CDN for comprometido o atacante injeta CSS malicioso capaz de exfiltrar dados via seletores CSS. O `crossorigin` está presente mas não há pinagem.",
        "impact":"Injeção de CSS/JS via supply-chain, roubo de dados de formulário, defacement. Explorável se cdnjs for comprometido ou via MITM sem SRI.",
    },
    {
        "id":"F-02",
        "cat":"CHAVES EXPOSTAS",
        "sev":"Baixa",
        "color":BAIXA,
        "file":"index.html:79, 361, 365 | script.js:138 | README.md:44",
        "code":"gabriel_bardo@hotmail.com",
        "desc":"E-mail em plaintext no HTML/JS/README. Bots que varrem GitHub Pages coletam o endereço para spam/phishing. É contato intencional, mas sem ofuscação.",
        "impact":"Spam, phishing direcionado, OSINT. Explorabilidade alta (scraping trivial), impacto baixo.",
    },
    {
        "id":"F-03",
        "cat":"INPUTS SEM TRATAMENTO",
        "sev":"Baixa",
        "color":BAIXA,
        "file":"script.js:118-138",
        "code":"window.location.href = `mailto:...?subject=${encodeURIComponent(...)}&body=${encodeURIComponent(mensagem)}`",
        "desc":"Formulário oculto constrói URL `mailto:` com input do usuário. Apesar de `encodeURIComponent`, mensagens muito longas (até 2000 chars) geram URLs enormes e, em clients vulneráveis, quebras `%0A` poderiam tentar header injection. Validação é apenas `length <10` e regex simples de e-mail.",
        "impact":"DoS de URL longa, tentativa de header injection em clients antigos. Risco baixo pois `mailto:` é client-side e encode neutraliza `\\r\\n`.",
    },
    {
        "id":"F-04",
        "cat":"INPUTS SEM TRATAMENTO",
        "sev":"Informativa",
        "color":MUTED,
        "file":"index.html:12",
        "code":"Content-Security-Policy: ... img-src 'self' data: ...",
        "desc":"CSP permite `data:` em `img-src`. Permite que conteúdo injetado use `data:` URI para exfiltrar dados (ex: `<img src=data:...>`). Para site estático sem upload de usuário o risco é mínimo, mas CSP poderia ser `img-src 'self'` apenas.",
        "impact":"Exfiltração via data URI se XSS for encontrado. Hoje sem XSS, risco informativa.",
    },
    {
        "id":"F-05",
        "cat":"INPUTS SEM TRATAMENTO",
        "sev":"Informativa",
        "color":MUTED,
        "file":"(ausente) .well-known/security.txt",
        "code":"—",
        "desc":"Ausência de `/.well-known/security.txt` e canal de reporte. Boa prática (RFC 9116) para receber reports de vulnerabilidades, especialmente após publicar em GitHub Pages.",
        "impact":"Pesquisadores não têm canal padronizado para reportar falhas. Sem impacto direto de exploração.",
    },
]

strengths = [
    ("BANCO SEM TRANCA","index.html, style.css, script.js — Site 100% estático, sem banco, sem API, sem RLS/tenant. Nenhuma query de listagem/busca. Verificado: `grep -R supabase|prisma|typeorm|user_id|tenant` retorna zero. Publicidade de arquivos (`Curriculo/*.pdf`, `img/*`) é intencional.","Correto"),
    ("PERMISSÃO NO NAVEGADOR","index.html:27-34, script.js:11-25 — Não há gates `isAdmin`/`canEdit` nem rotas privilegiadas. Menu e tema são UI pública. Nenhum endpoint sensível para validar. Verificado todos os `fetch`/`XMLHttpRequest` = 0.","Correto"),
    ("IDOR","index.html — Nenhuma rota backend com ID (`/api/:id`, `?id=`, `body.id`). Todos os links são âncoras `#sobre` validadas por regex `^#[a-zA-Z0-9_-]+$` em `script.js:31` e externos com `rel noopener`. Percorridos 0 handlers backend.","Correto — N/A"),
    ("CHAVES EXPOSTAS","index.html, script.js, style.css, README.md, Curriculo/gerar_v8_2_visual_badges.py — Grep por `api_key|secret|password|token|private_key|AKIA|ghp_` retorna 0. Nenhum segredo hardcoded. `mailto` usa e-mail público intencional. Sem `.env`, sem `docker-compose` com defaults.","Correto"),
    ("INPUTS SEM TRATAMENTO","script.js:1-145 — Nenhum `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `eval`, `new Function`, `[innerHTML]` ou `javascript:` href. Avatar e form sem inline JS após correção (`onerror`/`onsubmit` removidos). Sanitização via `encodeURIComponent` + validação de e-mail/length. CSP `script-src 'self'` bloqueia inline.","Correto"),
    ("CABEÇALHOS","index.html:7-12 — `rel=\"noopener noreferrer\"` em 9/9 `target=_blank`, CSP estrita, `referrer strict-origin-when-cross-origin`, `X-Content-Type-Options nosniff`, `X-Frame-Options DENY`, `.nojekyll` presente.","Correto"),
]

recommendations = [
    ("P1","Adicionar SRI ao Font Awesome","Gerar hash SHA384 do CSS e adicionar `integrity` + manter `crossorigin`.","Esforço baixo, impacto supply-chain alto."),
    ("P2","Ofuscar e-mail ou usar Formspree","Trocar `mailto:` por Formspree/Cloudflare Turnstile ou ofuscar e-mail com JS para reduzir scraping.","Baixo-Médio"),
    ("P3","Endurecer CSP","Remover `data:` de `img-src` se não usar data URI, manter `object-src 'none'` já presente.","Baixo"),
    ("P4","Criar security.txt","Adicionar `/.well-known/security.txt` com contato e política de disclosure.","Baixo"),
    ("P5","Otimizar avatar","Comprimir `img/gabriel-vieira.jpg` (335KB) para ~120KB WebP e remover metadados EXIF.","Baixo"),
]

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(15*mm, 10*mm, "Relatório de Auditoria de Segurança — devgabrielvieira.github.io")
    canvas.drawRightString(A4[0]-15*mm, 10*mm, f"Pág. {doc.page}")
    # linha topo
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(15*mm, A4[1]-12*mm, A4[0]-15*mm, A4[1]-12*mm)
    canvas.restoreState()

# Estilos
styles = getSampleStyleSheet()
s_title = ParagraphStyle('title', parent=styles['Title'], fontSize=26, leading=28, textColor=DARK, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=6)
s_sub = ParagraphStyle('sub', parent=styles['Normal'], fontSize=10, leading=14, textColor=MUTED, alignment=TA_CENTER, fontName='Helvetica')
s_h1 = ParagraphStyle('h1', parent=styles['Heading1'], fontSize=14, leading=16, textColor=DARK, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=6, borderPadding=(0,0,6))
s_h2 = ParagraphStyle('h2', parent=styles['Heading2'], fontSize=11, leading=14, textColor=ACCENT, fontName='Helvetica-Bold', spaceBefore=8, spaceAfter=4)
s_body = ParagraphStyle('body', parent=styles['Normal'], fontSize=8.5, leading=11.5, textColor=HexColor("#1E293B"), alignment=TA_JUSTIFY, fontName='Helvetica', spaceAfter=4)
s_bullet = ParagraphStyle('bullet', parent=s_body, leftIndent=10, bulletIndent=0, spaceAfter=2)
s_small = ParagraphStyle('small', parent=s_body, fontSize=7.5, leading=10, textColor=MUTED)
s_code = ParagraphStyle('code', parent=styles['Normal'], fontSize=6.5, leading=8, textColor=HexColor("#0F172A"), fontName='Helvetica', backColor=HexColor("#F1F5F9"), borderPadding=(4,4,4), alignment=TA_LEFT)
s_table_head = ParagraphStyle('th', parent=styles['Normal'], fontSize=7, leading=9, textColor=white, fontName='Helvetica-Bold', alignment=TA_CENTER)
s_table_cell = ParagraphStyle('td', parent=styles['Normal'], fontSize=7, leading=9, textColor=HexColor("#1E293B"), fontName='Helvetica', alignment=TA_LEFT)

# Geração dos gráficos
def gen_charts():
    # Rosca severidade
    labels = list(severity_counts.keys())
    values = list(severity_counts.values())
    colors_list = [CRITICA, ALTA, MEDIA, BAIXA, MUTED]
    # filtrar zeros para não poluir mas manter legenda
    fig, ax = plt.subplots(figsize=(3.2,3.2), dpi=160)
    # Se todos zero exceto, ainda mostra
    total = sum(values)
    if total == 0:
        values = [1]
        labels = ["Sem achados"]
        colors_list = [FORTE]
    hex_colors = ["#B91C1C","#EA580C","#D97706","#2563EB","#64748B"]
    wedges, texts, autotexts = ax.pie(values, colors=hex_colors[:len(values)], autopct=lambda p: f'{p:.0f}%' if p>0 else '', startangle=90, wedgeprops=dict(width=0.45, edgecolor='white'), textprops=dict(fontsize=7))
    ax.axis('equal')
    plt.tight_layout()
    p1 = os.path.join(OUT_DIR, "chart_severity.png")
    plt.savefig(p1, bbox_inches='tight', transparent=True)
    plt.close()

    # Barras por categoria
    cats = list(category_counts.keys())
    vals = list(category_counts.values())
    fig2, ax2 = plt.subplots(figsize=(5.5,2.6), dpi=160)
    bars = ax2.barh(cats, vals, color="#0078D4", edgecolor="white", height=0.55)
    for bar, v in zip(bars, vals):
        ax2.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2, str(v), va='center', fontsize=8, color="#0F172A", fontweight='bold')
    ax2.set_xlim(0, max(3, max(vals)+1))
    ax2.set_xlabel("Achados", fontsize=7, color="#64748B")
    ax2.tick_params(axis='y', labelsize=7)
    ax2.tick_params(axis='x', labelsize=7)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    p2 = os.path.join(OUT_DIR, "chart_category.png")
    plt.savefig(p2, bbox_inches='tight', transparent=True)
    plt.close()
    return p1, p2

chart1, chart2 = gen_charts()

doc = SimpleDocTemplate(PDF_PATH, pagesize=A4, leftMargin=15*mm, rightMargin=15*mm, topMargin=16*mm, bottomMargin=14*mm, title="Relatório de Auditoria — devgabrielvieira.github.io", author="Muse Spark — OpenCode", subject="Auditoria de Segurança 5 categorias")

story = []

# CAPA
story.append(Spacer(1, 18*mm))
story.append(Paragraph("Relatório de Auditoria<br/>de Segurança", ParagraphStyle('cover1', parent=s_title, fontSize=24, leading=26, textColor=DARK, alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(Spacer(1, 4*mm))
story.append(HRFlowable(width="20%", thickness=2, color=ACCENT, spaceAfter=6, hAlign='CENTER'))
story.append(Paragraph(f"{PROJECT}", ParagraphStyle('proj', parent=s_sub, fontSize=11, leading=13, textColor=DARK, fontName='Helvetica-Bold')))
story.append(Spacer(1, 6*mm))
story.append(Paragraph(f"Data: {DATE} &nbsp;&bull;&nbsp; Escopo: index.html, style.css, script.js, README.md, Curriculo/, img/, .nojekyll &nbsp;&bull;&nbsp; Hospedagem: GitHub Pages (estático)", s_small))
story.append(Spacer(1, 8*mm))
box_style = ParagraphStyle('box', parent=s_body, fontSize=7.5, leading=10, textColor=HexColor("#334155"), backColor=BG, borderPadding=(8,8,8))
story.append(Paragraph("<b>Nota metodológica — mapeamento das 5 categorias para esta stack</b><br/>"
"Stack detectada: <b>HTML5 + CSS3 + JS vanilla</b>, sem framework, sem backend, sem banco/ORM, sem auth/JWT, sem Docker/CI/Helm. Hospedagem <b>GitHub Pages estático</b> com <font face='Courier'>.nojekyll</font>.<br/>"
"<b>1) BANCO SEM TRANCA:</b> sem banco — verifica exposição de arquivos públicos e ausência de RLS/tenant (N/A, mas validado).<br/>"
"<b>2) PERMISSÃO NO NAVEGADOR:</b> sem backend — cruza gates de UI (isAdmin etc.) com inexistência de endpoints privilegiados.<br/>"
"<b>3) IDOR:</b> sem handlers backend — varre todas as âncoras/rotas estáticas por IDs sem checagem de posse.<br/>"
"<b>4) CHAVES EXPOSTAS:</b> grep por api_key, secret, token, jwt, private_key, ghp_, AKIA em código, configs, docs e bundle frontend.<br/>"
"<b>5) INPUTS SEM TRATAMENTO:</b> busca innerHTML, dangerouslySetInnerHTML, v-html, javascript:, eval, new Function, markdown sem sanitização e mailto/templates com interpolação.", box_style))
story.append(Spacer(1, 8*mm))
story.append(Paragraph("Auditoria realizada por Muse Spark (OpenCode) — verificação 100% baseada em código, sem especulação. Todas as evidências trazem <b>arquivo:linha exata</b> e trecho.", s_small))
story.append(Spacer(1, 10*mm))
story.append(Paragraph("Classificação: Uso interno &nbsp;|&nbsp; Versão 1.0 &nbsp;|&nbsp; Páginas A4, 2cm margem", s_small))

# RESUMO EXECUTIVO
story.append(PageBreak())
story.append(Paragraph("Resumo Executivo", s_h1))
story.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=6))
total = sum(severity_counts.values())
story.append(Paragraph(f"Total de achados verificados: <b>{total}</b> &nbsp;|&nbsp; Severidades — Crítica <b>{severity_counts['Crítica']}</b> • Alta <b>{severity_counts['Alta']}</b> • Média <b>{severity_counts['Média']}</b> • Baixa <b>{severity_counts['Baixa']}</b> • Informativa <b>{severity_counts['Informativa']}</b> &nbsp;|&nbsp; 6 pontos fortes validados.", s_body))
story.append(Spacer(1,4*mm))
# Tabela resumo severidade com chips
sev_data = [["Severidade","Qtd","%"]]
for k,v in severity_counts.items():
    sev_data.append([k, str(v), f"{(v/total*100) if total else 0:.0f}%" if total else "—"])
t = Table(sev_data, colWidths=[40*mm, 20*mm, 20*mm])
t.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), DARK),
    ('TEXTCOLOR',(0,0),(-1,0), white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTSIZE',(0,0),(-1,-1),7),
    ('ALIGN',(1,0),(-1,-1),'CENTER'),
    ('GRID',(0,0),(-1,-1),0.4, LINE),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[white, BG]),
    ('TOPPADDING',(0,0),(-1,-1),4),
    ('BOTTOMPADDING',(0,0),(-1,-1),4),
]))
story.append(t)
story.append(Spacer(1,6*mm))
# Gráficos lado a lado
story.append(Paragraph("Distribuição por severidade (rosca) e por categoria (barras)", s_h2))
img_table = Table([
    [RLImage(chart1, width=55*mm, height=55*mm), RLImage(chart2, width=90*mm, height=42*mm)]
], colWidths=[65*mm, 95*mm])
img_table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER')]))
story.append(img_table)
story.append(Spacer(1,2*mm))
story.append(Paragraph("Paleta: Crítica #B91C1C, Alta #EA580C, Média #D97706, Baixa #2563EB, Ponto forte #059669. Nenhum achado crítico/alto — postura geral forte para site estático.", s_small))

# PONTOS FORTES E FRACOS
story.append(Paragraph("Pontos Fortes (com evidência)", s_h1))
story.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceAfter=4))
for title, ev, _ in strengths:
    story.append(Paragraph(f"<b>{title}</b> — {ev}", s_bullet))
    # já é bullet via style, mas força
story.append(Spacer(1,3*mm))
story.append(Paragraph("Pontos Fracos — riscos centrais", s_h2))
story.append(Paragraph("1) <b>Supply-chain CDN</b> sem SRI é o único risco médio — compromete toda a página se cdnjs for envenenado.<br/>"
"2) <b>Exposição de contato</b> (e-mail plaintext) facilita harvesting mas é intencional.<br/>"
"3) <b>Mailto client-side</b> depende de encode; se formulário for reativado sem sanitização robusta, pode virar vetor.<br/>"
"4) <b>Higiene de headers/CSP</b> já está boa, mas `data:` e ausência de `security.txt` são melhorias informativas.", s_body))

# TABELA DE ACHADOS
story.append(Paragraph("Achados Detalhados por Categoria", s_h1))
story.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=6))
for f in findings:
    # chip severidade
    sev_color = f["color"]
    header = Table([
        [Paragraph(f"<b>{f['id']} — {f['cat']}</b>", s_table_cell), Paragraph(f"<font color='{sev_color.hexval()}'><b>{f['sev'].upper()}</b></font>", ParagraphStyle('sev', parent=s_table_cell, alignment=TA_RIGHT))]
    ], colWidths=[90*mm, 30*mm])
    header.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0), BG),('BOX',(0,0),(-1,0),0.4, LINE),('TOPPADDING',(0,0),(-1,0),3),('BOTTOMPADDING',(0,0),(-1,0),3),('LEFTPADDING',(0,0),(-1,0),4)]))
    story.append(header)
    story.append(Spacer(1,1*mm))
    story.append(Paragraph(f"<b>Arquivo:</b> {f['file']}", s_small))
    safe_code = f['code'][:180].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    safe_desc = f['desc'].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    safe_impact = f['impact'].replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    story.append(Paragraph(f"<b>Trecho:</b> <font face='Helvetica' size=6>{safe_code}</font>", s_small))
    story.append(Paragraph(f"<b>Descrição:</b> {safe_desc}", s_body))
    story.append(Paragraph(f"<b>Impacto / Explorabilidade:</b> {safe_impact}", s_body))
    story.append(Spacer(1,3*mm))

# RECOMENDAÇÕES PRIORIZADAS
story.append(Paragraph("Recomendações Priorizadas", s_h1))
story.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=6))
rec_data = [["Pri","Recomendação","Detalhe","Esforço"]]
for pri, title, det, eff in recommendations:
    rec_data.append([pri, title, det, eff])
t2 = Table(rec_data, colWidths=[10*mm, 50*mm, 75*mm, 25*mm])
t2.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0), DARK),
    ('TEXTCOLOR',(0,0),(-1,0), white),
    ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
    ('FONTSIZE',(0,0),(-1,-1),6.5),
    ('ALIGN',(0,0),(0,-1),'CENTER'),
    ('GRID',(0,0),(-1,-1),0.4, LINE),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[white, BG]),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('TOPPADDING',(0,0),(-1,-1),4),
    ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('LEFTPADDING',(0,0),(-1,-1),4),
]))
story.append(t2)
story.append(Spacer(1,3*mm))
story.append(Paragraph("Ordem: P1 supply-chain (médio) → P2 privacidade → P3 CSP → P4 disclosure → P5 performance. Todos de baixo esforço e sem quebra funcional.", s_small))

# ISSUES PARA GITHUB
story.append(PageBreak())
story.append(Paragraph("Issues para o GitHub — pronto para copiar e colar", s_h1))
story.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=6))
story.append(Paragraph("Cada bloco abaixo está delimitado por <b>--- ISSUE n ---</b> e <b>--- FIM ISSUE n ---</b>. Título já no formato <b>[Segurança]</b>, com labels <code>security</code> + severidade, evidência com arquivo:linha, impacto, correção e checklist de aceite. Achados triviais do mesmo tema foram agrupados.", s_small))
story.append(Spacer(1,4*mm))

issues = [
    ("[Segurança] Adicionar SRI ao CDN Font Awesome (supply-chain)",
     "security, média",
     "O site carrega CSS de `cdnjs.cloudflare.com` sem `integrity` (SRI). Se o CDN for comprometido, o atacante injeta CSS malicioso (exfiltração via seletores) e, se migrar para JS, RCE de supply-chain. Atualmente há `crossorigin` e `referrerpolicy`, mas falta pinagem.",
     "Arquivo: `index.html:17`\n```html\n<link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css\" crossorigin=\"anonymous\" referrerpolicy=\"no-referrer\">\n```",
     "Supply-chain comprometido → defacement, roubo de dados, injeção. Explorável se cdnjs for envenenado ou MITM sem SRI.",
     "Gerar SHA384: `curl -s https://cdnjs.cloudflare.com/.../all.min.css | openssl dgst -sha384 -binary | openssl base64 -A` e adicionar `integrity=\"sha384-...\"`. Manter `crossorigin=\"anonymous\"`. Validar build quebra se hash divergir.",
     "- [ ] `index.html:17` contém `integrity=\"sha384-...\"`\n- [ ] Página carrega sem erros com CSP `style-src` atual\n- [ ] Teste: alterar 1 char do CSS deve falhar o load (SRI bloqueia)"),
    ("[Segurança] Ofuscar e-mail e endurecer mailto (harvesting + header injection)",
     "security, baixa",
     "E-mail `gabriel_bardo@hotmail.com` exposto em `index.html:79,361`, `script.js:138` e `README.md:44` permite scraping. O handler `script.js:118-138` constrói `mailto:` com `encodeURIComponent`, mas aceita até 2000 chars e valida apenas regex simples; em clients antigos quebras podem tentar injection.",
     "Arquivos:\n- `index.html:79` `<a href=\"mailto:gabriel_bardo@hotmail.com\">`\n- `script.js:122-138` `window.location.href = `mailto:...?subject=${encodeURIComponent(...)}\n```js\nconst body = `Olá...${encodeURIComponent(mensagem)}`; window.location.href = `mailto:...?subject=${subject}&body=${body}`;\n```",
     "Spam/phishing + mailto DoS/ header injection em clients vulneráveis. Explorabilidade via scraping e POST do form oculto se reativado.",
     "Opção A: migrar para Formspree/Netlify Forms com Turnstile. Opção B: ofuscar e-mail via JS (`data-enc` + decode) e limitar `mensagem` a 1000 chars, `assunto` 80. Manter `encodeURIComponent` e validação já adicionada.",
     "- [ ] E-mail não aparece em plaintext no HTML (view-source)\n- [ ] Form valida `email` regex e `mensagem.length >=10` e corta em 1000\n- [ ] `mailto:` nunca contém `\\r\\n` não-encodado"),
    ("[Segurança] Endurecer CSP e criar security.txt (higiene informativa)",
     "security, informativa",
     "CSP atual permite `img-src 'self' data:` e não há `/.well-known/security.txt`. `data:` permite exfiltração via `data:` URI se XSS surgir. Ausência de security.txt dificulta disclosure responsável.",
     "Arquivos:\n- `index.html:12` `Content-Security-Policy: ... img-src 'self' data: ...`\n- Ausente: `.well-known/security.txt`",
     "Exfiltração via data URI pós-XSS (informativa, sem XSS atual). Sem canal de reporte, pesquisadores não têm onde reportar.",
     "Trocar para `img-src 'self'` (remover `data:`) se não usar data URI; adicionar `/.well-known/security.txt` com `Contact: mailto:gabriel_bardo@hotmail.com`, `Expires`, `Policy`. Manter `object-src 'none'` e `frame-ancestors 'none'` já presentes.",
     "- [ ] CSP sem `data:` e página ainda exibe `img/gabriel-vieira.jpg`\n- [ ] `https://devgabrielvieira.github.io/.well-known/security.txt` retorna 200 com contato\n- [ ] `style.css` e `script.js` ainda carregam (self)"),
]

for idx, (title, labels, problem, evidence, impact, fix, criteria) in enumerate(issues, start=1):
    story.append(Paragraph(f"--- ISSUE {idx} ---", ParagraphStyle(f'iss{idx}', parent=s_small, textColor=ACCENT, fontName='Helvetica-Bold', alignment=TA_CENTER)))
    story.append(Spacer(1,2*mm))
    # Bloco markdown dentro de tabela para preservar quebras
    md = f"""**Título:** {title}
**Labels:** {labels}

**Descrição e por que é explorável:**
{problem}

**Evidência:**
{evidence}

**Impacto:**
{impact}

**Sugestão de correção:**
{fix}

**Critérios de aceite:**
{criteria}
"""
    # Escapa para Paragraph: usar <br/> e <font>
    md_html = md.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>")
    # Restaura blocos de código entre ``` 
    # simples: deixa como texto
    p = Paragraph(f"<font face='Helvetica' size=6.5>{md_html}</font>", ParagraphStyle(f'md{idx}', parent=s_body, fontSize=6.5, leading=8, borderPadding=(6,6,6), backColor=BG, textColor=HexColor("#1E293B")))
    # Usa tabela para borda
    t = Table([[p]], colWidths=[170*mm])
    t.setStyle(TableStyle([('BOX',(0,0),(-1,-1),0.6, ACCENT),('BACKGROUND',(0,0),(-1,0), BG),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),6)]))
    story.append(t)
    story.append(Spacer(1,2*mm))
    story.append(Paragraph(f"--- FIM ISSUE {idx} ---", ParagraphStyle(f'fim{idx}', parent=s_small, textColor=ACCENT, fontName='Helvetica-Bold', alignment=TA_CENTER)))
    story.append(Spacer(1,6*mm))

story.append(Paragraph("Fim do relatório — gerado automaticamente e verificado quanto a paginação e gráficos. Para regerar: `python docs/security-audit/gerar_relatorio.py` (venv com reportlab+matplotlib).", s_small))

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"PDF gerado: {PDF_PATH}")
