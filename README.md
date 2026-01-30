<p align="center">
  <img src="imagem/logo.png" alt="Guardian AI" width="120">
</p>

<h1 align="center">Guardian AI — CGDF</h1>


![Status](https://img.shields.io/badge/status-em%20desenvolvimento-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-app-red)
![LGPD](https://img.shields.io/badge/LGPD-compliance-success)
![Hackathon](https://img.shields.io/badge/Hackathon-Participa%20DF-yellow)

**Guardian AI** é uma aplicação desenvolvida para o **Hackathon Participa DF – CGDF**, com foco em **controle social**, **transparência pública** e **conformidade com a LGPD**.

A solução analisa textos administrativos (pedidos, processos, manifestações, protocolos etc.) e identifica **dados pessoais e sensíveis**, auxiliando a priorização de riscos e a tomada de decisão humana.

---
## 🎯 Objetivo

Apoiar órgãos públicos na:
- Identificação automática de **dados pessoais (PII)**
- Classificação de **nível de risco LGPD**
- Priorização de análises sensíveis
- Promoção da **transparência** e do **controle social**

> ⚠️ O sistema **não substitui análise humana** e **não armazena dados**.

---
## 🧠 Funcionalidades

✔ Detecção automática de dados sensíveis (CPF, e-mail, telefone, processos etc.)  
✔ Score de risco LGPD (0–100)  
✔ Classificação: **Baixo / Médio / Alto risco**  
✔ Destaque visual (highlight) dos dados sensíveis  
✔ Texto anonimizado automaticamente  
✔ Dashboards executivos interativos  
✔ Fila de priorização por risco  
✔ Análise individual de textos  
✔ Exportação de relatório em **PDF institucional**  
✔ Interface responsiva (mobile-first)  
✔ Identidade visual alinhada à **CGDF**

---
## 🧩 Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit**
- **spaCy (pt_core_news_sm)**
- **Pandas**
- **Plotly**
- **ReportLab**
- **Regex (detecção estruturada)**
- **HTML + CSS customizado**

---
## 📁 Estrutura do Projeto

hackathon_cgdf/

├── app.py # Aplicação principal

├── requirements.txt # Dependências

├── README.md # Documentação

├── LICENSE # Licença MIT

├── .gitignore

├── .venv

├── imagem/

│ ├── logo.png

│ ├── logo_nome.png
  
│ └── Brasão_do_Distrito_Federal_(Brasil).png

---
## ⚙️ Instalação Local

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/EdivoneAraujo/hackathon_cgdf.git
cd hackathon_cgdf
````
### 2️⃣ Crie um ambiente virtual (opcional)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

### 3️⃣ Instale as dependências
pip install -r requirements.txt

### 4️⃣ Instale o modelo NLP
python -m spacy download pt_core_news_sm

### 5️⃣ Execute o app
streamlit run app.py

---
## ☁️ Deploy (Streamlit Cloud)

1. Suba o projeto no GitHub

2. Acesse: https://streamlit.io/cloud

3. Conecte o repositório

4. Selecione app.py

5. Deploy automático 🚀

---
## 🔐 LGPD & Ética

- **❌ Nenhum dado é armazenado**

- **✔ Processamento local e temporário**

- **✔ Apoio à decisão humana**

- **✔ Transparência algorítmica**

- **✔ Finalidade pública e social**

---
## 🏛️ Contexto Institucional

Projeto desenvolvido no contexto do:

Hackathon Participa DF
Controladoria-Geral do Distrito Federal (CGDF)

---
## 📄 Licença

Este projeto está sob a licença MIT.
Veja o arquivo LICENSE
 para mais detalhes.

---
## 👩‍💻 Autoria

<p align="center"> <a href="https://www.linkedin.com/in/edivone-araujo"> <img src="https://img.shields.io/badge/LinkedIn-Edivone%20Araújo-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"> </a> <a href="https://github.com/EdivoneAraujo"> <img src="https://img.shields.io/badge/GitHub-Edivone%20Araújo-black?style=for-the-badge&logo=github"> </a>

---
## 🏆 Observação para Avaliadores

Este projeto foi concebido com foco em:

- Escalabilidade

- Clareza institucional

- Conformidade legal

- Experiência do usuário

- Transparência pública

