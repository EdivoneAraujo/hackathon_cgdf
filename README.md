## 🛡️ Guardian AI - Desafio Participa DF

1º Hackathon em Controle Social da CGDF
Categoria 1: Acesso à Informação (Identificação automática de dados pessoais)

---
## 🎯 O Problema

A Lei de Acesso à Informação (LAI) exige transparência, mas a Lei Geral de Proteção de Dados (LGPD) exige privacidade.
O grande desafio não é apenas encontrar um CPF (que tem formato fixo), mas identificar relatos sensíveis (doenças, conflitos familiares, dados bancários) que cidadãos inserem inadvertidamente em pedidos de informação e que não podem ser publicados sem tratamento.

---
## 💡 A Solução: Guardian AI

O Guardian AI é uma ferramenta de auditoria inteligente que utiliza uma abordagem híbrida para classificar o risco de exposição de dados.

**Diferenciais Técnicos:**

1. Análise de Contexto Semântico: Diferente de ferramentas comuns, o Guardian AI detecta narrativas de alta intimidade (ex: "estou com depressão", "meu marido me agrediu", "tenho uma dívida") usando NLP e dicionários de risco contextual.

2. Identificação de Entidades (NER): Utiliza o modelo pt_core_news_sm (Spacy) para reconhecer nomes de pessoas e endereços no meio de textos desestruturados.

3. Dashboard de Gestão: Gera gráficos visuais (Plotly) que mostram não apenas quem violou, mas quais tipos de dados estão vazando mais, orientando ações preventivas.

4. Sugestão de Anonimização: Entrega o texto já tratado (ex: [NOME_PESSOA], [CPF_OCULTADO]) para agilizar o trabalho do servidor público.

---
## 📸 Demonstração

Painel de Controle (Dashboard)

Visão geral dos riscos encontrados na base de dados (e-SIC), com métricas e gráficos interativos.

Auditoria Detalhada

Visualização linha a linha dos pedidos, com destaque para os dados encontrados e sugestão automática de tarja (anonimização).

---
## 🛠️ Tecnologias Utilizadas

Linguagem: Python 3.10+

Interface: Streamlit (Web App interativo)

Processamento de Linguagem Natural (NLP): Spacy (pt_core_news_sm)

Visualização de Dados: Plotly Express

Manipulação de Dados: Pandas

---
## 🚀 Instalação e Execução

Siga os passos abaixo para rodar o projeto localmente:

1. Clone o repositório

git clone [https://github.com/EdivoneAraujo/hackathon_cgdf.git](https://github.com/EdivoneAraujo/hackathon_cgdf.git)
cd hackathon_cgdf

2. Crie um ambiente virtual (Opcional, mas recomendado)

python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate


3. Instale as dependências

pip install -r requirements.txt


4. Baixe o modelo de língua portuguesa

Este passo é crucial para a IA entender o contexto em português.

python -m spacy download pt_core_news_sm


5. Execute a aplicação

streamlit run app.py

O navegador abrirá automaticamente no endereço http://localhost:8501

---
## 🧠 Lógica de Classificação de Risco

O algoritmo atribui um Score de Risco (0-100) baseado na soma de fatores encontrados:

. Tipo de Dado

. Método de Detecção

. Peso no Score

. Exemplo

. CPF / Telefone / Email

. Regex (Padrão Fixo)

. +25 pts (Alto)

. 123.456.789-00

. Relato Sensível

. Dicionário Semântico

. +30 pts (Crítico)

. "tenho câncer", "agressão"

. Nome de Pessoa

. NLP (Spacy Entity)

. +15 pts (Médio)

. "João da Silva"

. Endereço Completo

. NLP (Spacy Entity)

. +10 pts (Médio)

. "Rua das Flores, 10"

. Risco Alto: Score >= 50 (Bloqueio Automático Sugerido)

. Risco Médio: Score >= 20 (Revisão Humana Necessária)

. Risco Baixo: Score < 20 (Publicação Segura)

---
## 📄 Estrutura de Arquivos

📁 hackathon_cgdf
├── 📄 app.py              # Código principal da aplicação
├── 📄 requirements.txt    # Lista de dependências
├── 📄 README.md           # Documentação
└── 📄 AMOSTRA_e-SIC.csv   # Base de dados para teste


## 👥 Equipe

[Edivone Araújo] - Desenvolvedora

Projeto desenvolvido exclusivamente para o Desafio Participa DF (CGDF).

