import streamlit as st
import pandas as pd
import spacy
import re
import time
from collections import Counter
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Guardian AI - Desafio Participa DF",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# SPLASH SCREEN
# =========================================================
if "splash" not in st.session_state:
    st.session_state.splash = True

if st.session_state.splash:
    splash = st.empty()
    splash.markdown("""
    <style>
    .splash {
        display:flex;
        flex-direction:column;
        justify-content:center;
        align-items:center;
        height:80vh;
        animation: fade 0.8s ease-in;
    }
    @keyframes fade {
        from {opacity:0;}
        to {opacity:1;}
    }
    </style>
    <div class="splash">
        <h1 style="color:#0A2E5C;">🛡️ Guardian AI</h1>
        <h3 style="color:#F2C300;">Controle Social & Transparência</h3>
        <p>CGDF • Desafio Participa DF</p>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(2)
    st.session_state.splash = False
    splash.empty()

# =========================================================
# ESTILO (CGDF + MOBILE-FIRST)
# =========================================================
st.markdown("""
<style>
@media (max-width: 768px) {
    .block-container { padding: 1rem; }
    h1,h2,h3 { text-align:center; }
}

.metric-card {
    background:#0A2E5C;
    color:white;
    padding:1rem;
    border-radius:14px;
    text-align:center;
}

section[data-testid="stSidebar"] {
    background-color:#0A2E5C;
}
section[data-testid="stSidebar"] * {
    color:white;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# CARREGAMENTO DO MODELO NLP
# =========================================================
@st.cache_resource
def load_nlp_model():
    try:
        return spacy.load("pt_core_news_sm")
    except OSError:
        st.warning("Modelo pt_core_news_sm não encontrado. Executando sem NLP.")
        return spacy.blank("pt")

nlp = load_nlp_model()

# =========================================================
# MOTOR DE DETECÇÃO
# =========================================================
class PIIDetector:
    def __init__(self):
        self.regex_patterns = {
            "CPF": r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
            "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
            "Telefone": r"\b(?:\(?\d{2}\)?\s?)?(?:9\d{4}|\d{4})[ -]?\d{4}\b",
            "CEP": r"\b\d{5}-?\d{3}\b",
            "Processo": r"\b\d{4,}-?\d*\b"
        }

        self.sensitive_context_keywords = [
            "doença","medicamento","hospital","diagnóstico","câncer","hiv",
            "esposa","marido","filho","divórcio","agressão",
            "dívida","salário","extrato","renda",
            "crime","preso","delegacia","boletim",
            "processo","protocolo","autos"
        ]

    def analyze(self, text):
        if not isinstance(text, str):
            return {"score":0,"findings":[],"risk_level":"Baixo","anonymized_text":""}

        findings = []
        risk_score = 0
        doc = nlp(text)
        counter = Counter()

        for label, pattern in self.regex_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                counter[label] += len(matches)
                for m in matches:
                    findings.append({"tipo":label,"valor":m,"origem":"Regex"})

        risk_score += counter["CPF"] * 20
        risk_score += counter["Telefone"] * 15
        risk_score += counter["Email"] * 10
        risk_score += counter["Processo"] * 10

        for ent in doc.ents:
            if ent.label_ == "PER":
                findings.append({"tipo":"Pessoa","valor":ent.text,"origem":"NLP"})
                risk_score += 10

        text_lower = text.lower()
        context_hits = [w for w in self.sensitive_context_keywords if w in text_lower]
        if context_hits:
            findings.append({
                "tipo":"Contexto Sensível",
                "valor":", ".join(context_hits),
                "origem":"Dicionário"
            })
            risk_score += 25

        risk_level = "Baixo"
        if risk_score >= 20: 
            risk_level = "Médio"
        if risk_score >= 50: 
            risk_level = "Alto"

        anonymized = text
        for label, pattern in self.regex_patterns.items():
            anonymized = re.sub(pattern, f"[{label}]", anonymized)

        return {
            "score":min(risk_score,100),
            "findings":findings,
            "risk_level":risk_level,
            "anonymized_text":anonymized
        }

detector = PIIDetector()

# =========================================================
# FUNÇÕES AUXILIARES
# =========================================================
def gerar_pdf(df):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, h-40, "Guardian AI - Relatório LGPD")
    c.setFont("Helvetica", 10)
    c.drawString(40, h-60, "CGDF • Desafio Participa DF")
    y = h-100
    for _, row in df.iterrows():
        c.drawString(40, y, f"Risco: {row['Risco']} | Score: {row['Score']}")
        y -= 15
        if y < 80:
            c.showPage()
            y = h-80
    c.save()
    buffer.seek(0)
    return buffer

def destacar_texto(texto, findings):
    for f in findings:
        texto = re.sub(
            re.escape(f["valor"]),
            f"<mark style='background:#F2C300'>{f['valor']}</mark>",
            texto,
            flags=re.IGNORECASE
        )
    return texto

# =========================================================
# MENU LATERAL
# =========================================================
st.sidebar.image("imagem/Brasão_do_Distrito_Federal_(Brasil).svg.png", width=90)
menu = st.sidebar.radio(
    "",
    ["📊 Dashboard", "🔍 Análise Individual", "🏛️ Sobre / LGPD"],
    label_visibility="collapsed"
)

st.title("🛡️ Guardian AI")

# =========================================================
# DASHBOARD
# =========================================================
if menu == "📊 Dashboard":
    st.header("📂 Análise em Lote")
    file = st.file_uploader("Upload CSV ou XLSX", ["csv","xlsx"])

    if file:
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        col = st.selectbox("Coluna de texto:", df.columns)

        if st.button("🔍 Processar"):
            res = df[col].apply(lambda x: detector.analyze(str(x)))
            df["Risco"] = res.apply(lambda x:x["risk_level"])
            df["Score"] = res.apply(lambda x:x["score"])

            c1,c2,c3 = st.columns(3)
            c1.metric("Total", len(df))
            c2.metric("Alto", len(df[df["Risco"]=="Alto"]))
            c3.metric("Médio", len(df[df["Risco"]=="Médio"]))

            st.bar_chart(df["Risco"].value_counts())

            pdf = gerar_pdf(df[df["Risco"]!="Baixo"])
            st.download_button("📄 Baixar PDF", pdf, "relatorio_guardian_ai.pdf")

# =========================================================
# ANÁLISE INDIVIDUAL
# =========================================================
elif menu == "🔍 Análise Individual":
    texto = st.text_area("Texto do pedido:", height=160)
    if st.button("Analisar"):
        r = detector.analyze(texto)

        st.markdown(f"""
        <span title="Score calculado por CPF, dados sensíveis, contexto e NLP">
        <strong>Nível:</strong> {r['risk_level']} | <strong>Score:</strong> {r['score']}/100
        </span>
        """, unsafe_allow_html=True)

        st.subheader("🔎 Destaques")
        st.markdown(destacar_texto(texto, r["findings"]), unsafe_allow_html=True)

        st.subheader("🔒 Texto Anonimizado")
        st.text_area("", r["anonymized_text"], height=140)

# =========================================================
# SOBRE / LGPD
# =========================================================
else:
    st.markdown("""
    ## 🏛️ Sobre o Guardian AI

    Solução desenvolvida para o **1º Hackathon em Controle Social – Desafio Participa DF**,
    promovido pela **Controladoria-Geral do Distrito Federal (CGDF)**.

    **Objetivo:** apoiar a identificação automática de dados pessoais e sensíveis,
    em conformidade com a **Lei nº 13.709/2018 – LGPD**.

    - Não armazena dados
    - Não compartilha informações
    - Atua como apoio à decisão

    🛡️ **Guardian AI** • Transparência e Proteção ao Cidadão
    """)
