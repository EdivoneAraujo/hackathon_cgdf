import streamlit as st
import pandas as pd
import spacy
import re
import time
from collections import Counter
from io import BytesIO

import plotly.express as px
import plotly.io as pio

from reportlab.platypus import SimpleDocTemplate, Image, Paragraph
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import base64

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Guardian AI • CGDF",
    page_icon="imagem/logo.png",
    layout="wide"
)

# =========================================================
# SPLASH SCREEN
# =========================================================
if "splash" not in st.session_state:
    st.session_state.splash = True

if st.session_state.splash:
    splash = st.empty()

    logo_base64 = get_base64_image("imagem/logo.png")

    splash.markdown(f"""
    <style>
    /* remove padding do streamlit */
    .block-container {{
        padding-top: 0rem;
    }}

    .splash {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: #000000;
        display: grid;
        place-items: center;
        z-index: 9999;
        animation: fade 1.8s ease-in;
    }}

    .splash-content {{
        text-align: center;
    }}

    @keyframes fade {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    </style>

    <div class="splash">
        <div class="splash-content">
            <img src="data:image/png;base64,{logo_base64}" width="190"/>
            <h2 style="color:#0A2E5C; margin-top:12px;">Guardian AI</h2>
            <p>Controle Social & LGPD</p>
            <small>CGDF • Hackathon Participa DF</small>
        </div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(2)
    st.session_state.splash = False
    splash.empty()


# =========================================================
# ESTILO INSTITUCIONAL
# =========================================================
st.markdown("""
<style>
.stApp {
    background-color: #000000;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2E5C, #08305F);
}
section[data-testid="stSidebar"] * {
    color: white;
}

/* Cards */
.card {
    background: white;
    padding: 1.2rem;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    text-align: center;
}

/* Highlight */
mark {
    background: #F2C300;
    padding: 3px 6px;
    border-radius: 6px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# NLP
# =========================================================
@st.cache_resource
def load_nlp():
    try:
        return spacy.load("pt_core_news_sm")
    except OSError:
        st.warning(
            "⚠️ Modelo pt_core_news_sm não encontrado. "
            "O app continuará funcionando, mas sem NLP avançado."
        )
        return spacy.blank("pt")


nlp = load_nlp()

# =========================================================
# DETECTOR LGPD
# =========================================================
class PIIDetector:
    def __init__(self):
        self.regex = {
            "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
            "Email": r"\b[\w\.-]+@[\w\.-]+\.\w{2,}\b",
            "Telefone": r"\b(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[ -]?\d{4}\b",
            "CEP": r"\b\d{5}-?\d{3}\b",
            "Processo": r"\b\d{4,}-?\d*\b"
        }

        self.context = [
            "doença","hospital","diagnóstico","câncer",
            "filho","esposa","divórcio",
            "salário","renda","dívida",
            "crime","delegacia","processo","protocolo"
        ]

    def analyze(self, text):
        if not isinstance(text, str):
            return {"score":0,"risk":"Baixo","findings":[],"anon":""}

        findings = []
        score = 0
        doc = nlp(text)
        counter = Counter()

        for label, pattern in self.regex.items():
            matches = re.findall(pattern, text)
            if matches:
                counter[label] += len(matches)
                for m in matches:
                    findings.append({"tipo":label,"valor":m})

        score += counter["CPF"] * 20
        score += counter["Telefone"] * 15
        score += counter["Email"] * 10
        score += counter["Processo"] * 10

        for ent in doc.ents:
            if ent.label_ == "PER":
                findings.append({"tipo":"Pessoa","valor":ent.text})
                score += 10

        ctx = [c for c in self.context if c in text.lower()]
        if ctx:
            findings.append({"tipo":"Contexto Sensível","valor":", ".join(ctx)})
            score += 25

        risk = "Baixo"
        if score >= 20:
            risk = "Médio"
        if score >= 50:
            risk = "Alto"

        anon = text
        for label, pattern in self.regex.items():
            anon = re.sub(pattern, f"[{label}]", anon)

        return {
            "score": min(score,100),
            "risk": risk,
            "findings": findings,
            "anon": anon
        }

detector = PIIDetector()

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================
def highlight(text, findings):
    for f in findings:
        text = re.sub(
            re.escape(f["valor"]),
            f"<mark>{f['valor']}</mark>",
            text,
            flags=re.I
        )
    return text

def gerar_pdf_grafico(fig):
    img = pio.to_image(fig, format="png", width=900, height=500)
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = [
        Paragraph("<b>Guardian AI – Relatório LGPD</b>", styles["Title"]),
        Paragraph("CGDF • Hackathon Participa DF", styles["Normal"]),
        Image(BytesIO(img), width=450, height=260)
    ]

    doc.build(elements)
    buffer.seek(0)
    return buffer

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("imagem/Brasão_do_Distrito_Federal_(Brasil).svg.png", width=120)
    st.markdown("---")

menu = st.sidebar.radio(
    "",
    [
        "📊 Dashboard Executivo",
        "📈 Análises Estatísticas",
        "🧾 Fila de Priorização",
        "🔍 Análise Individual",
        "🏛️ Sobre / LGPD"
    ],
    label_visibility="collapsed"
)

# =========================================================
# HEADER 
# =========================================================
logo_base64 = get_base64_image("imagem/logo.png")

st.markdown(f"""
<style>
.header {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}}
</style>

<div class="header">
    <img src="data:image/png;base64,{logo_base64}" width="120"/>
    <h2 style="color:#0A2E5C; margin: 0.5rem 0 0 0;">Guardian AI</h2>
</div>
""", unsafe_allow_html=True)


# =========================================================
# UPLOAD GLOBAL
# =========================================================
file = st.file_uploader("📂 Upload CSV ou XLSX", ["csv","xlsx"])
df = None

if file:
    df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
    coluna = st.selectbox("Coluna de texto:", df.columns)

    with st.spinner("Processando dados com IA..."):
        res = df[coluna].apply(detector.analyze)

    df["Risco"] = res.apply(lambda x:x["risk"])
    df["Score"] = res.apply(lambda x:x["score"])
    df["Achados"] = res.apply(lambda x:x["findings"])

# =========================================================
# DASHBOARD EXECUTIVO
# =========================================================
if menu == "📊 Dashboard Executivo" and df is not None:
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total", len(df))
    c2.metric("Alto Risco", len(df[df["Risco"]=="Alto"]))
    c3.metric("Médio Risco", len(df[df["Risco"]=="Médio"]))
    c4.metric("Score Médio", round(df["Score"].mean(),1))

    risco_df = df["Risco"].value_counts().reset_index()
    risco_df.columns = ["Risco","Quantidade"]

    fig = px.bar(
        risco_df,
        x="Risco",
        y="Quantidade",
        color="Risco",
        text="Quantidade",
        color_discrete_map={
            "Alto":"#C62828",
            "Médio":"#F2C300",
            "Baixo":"#2E7D32"
        },
        title="Distribuição de Risco LGPD"
    )

    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    pdf = gerar_pdf_grafico(fig)
    st.download_button("📄 Exportar PDF do Gráfico", pdf, "dashboard_guardian_ai.pdf")

# =========================================================
# ANÁLISES
# =========================================================
elif menu == "📈 Análises Estatísticas" and df is not None:
    tipos = []
    for ach in df["Achados"]:
        for a in ach:
            tipos.append(a["tipo"])

    tipos_df = pd.Series(Counter(tipos)).reset_index()
    tipos_df.columns = ["Tipo","Ocorrências"]

    fig = px.bar(
        tipos_df.sort_values("Ocorrências", ascending=False),
        x="Tipo",
        y="Ocorrências",
        text="Ocorrências",
        title="Tipos de Dados Sensíveis Detectados"
    )

    fig.update_layout(template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# FILA
# =========================================================
elif menu == "🧾 Fila de Priorização" and df is not None:
    st.dataframe(
        df.sort_values("Score", ascending=False)[
            [coluna,"Risco","Score"]
        ].head(20),
        use_container_width=True
    )

# =========================================================
# INDIVIDUAL
# =========================================================
elif menu == "🔍 Análise Individual":
    texto = st.text_area("Texto do pedido:", height=160)
    if st.button("Analisar"):
        r = detector.analyze(texto)

        st.markdown(
            f"<b>Nível:</b> {r['risk']} | "
            f"<span title='Score calculado por dados pessoais, contexto e NLP'>"
            f"<b>Score:</b> {r['score']}/100</span>",
            unsafe_allow_html=True
        )

        st.subheader("🔎 Destaques")
        st.markdown(highlight(texto, r["findings"]), unsafe_allow_html=True)

        st.subheader("🔒 Texto Anonimizado")
        st.text_area("", r["anon"], height=140)

# =========================================================
# SOBRE
# =========================================================
else:
    st.markdown("""
    ## 🏛️ Guardian AI

    Solução desenvolvida para o **Hackathon Participa DF – CGDF**.

    **Objetivo:** apoiar a identificação automática de dados pessoais e sensíveis,
    em conformidade com a **Lei nº 13.709/2018 (LGPD)**.

    ✔ Não armazena dados  
    ✔ Apoia decisão humana  
    ✔ Transparência e controle social
    """)
