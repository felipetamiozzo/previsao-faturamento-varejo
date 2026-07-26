
# Projeto com Dados Reais - Previsão de Faturamento

**Projeto de Ciência de Dados | Previsão de Faturamento com Machine Learning**

## Contexto do Projeto

Este projeto foi desenvolvido a partir de um cenário real de uma empresa prestadora de serviços de tecnologia e análise de dados para diferentes clientes do varejo.

O processo de previsão de faturamento era realizado de forma manual, utilizando análises simplificadas dos dados históricos, o que demandava tempo operacional e limitava a capacidade de gerar previsões mais precisas e escaláveis.

Como solução, foi desenvolvido um pipeline completo de Ciência de Dados capaz de automatizar a previsão de faturamento líquido mensal por loja, utilizando técnicas de Machine Learning para apoiar decisões estratégicas, reduzir esforços manuais e gerar maior valor através dos dados.

A solução contempla desde a preparação dos dados transacionais até a disponibilização dos resultados em um dashboard interativo, permitindo uma análise mais rápida do comportamento histórico e das projeções futuras.

O modelo final, baseado em **Random Forest Regressor**, alcançou **MAPE de 11,20%** no período de validação temporal.

---

# 📊 Funcionalidades

- Previsão dos próximos 3 meses (outubro, novembro e dezembro de 2023).
- Controle de crescimento máximo mensal de 20% para evitar projeções fora do comportamento histórico.
- Dashboard interativo desenvolvido em Streamlit com:

  - Gráfico consolidado de previsão futura.
  - Previsões detalhadas por loja.
  - Filtro individual por unidade.
  - Histórico de faturamento mensal.
  - Métricas de avaliação dos modelos.
  - Comparação entre algoritmos.
  - Visualização da importância das variáveis.

- Pipeline completo de Machine Learning:

  - Exploração dos dados.
  - Tratamento e validação.
  - Engenharia de atributos.
  - Treinamento do modelo.
  - Avaliação.
  - Geração de previsões futuras.

---

# 📈 Resultados e Gráficos

## 1. Comparação de Modelos (MAPE)

O gráfico apresenta o desempenho dos modelos avaliados durante a etapa de validação.

O **Random Forest Base** apresentou o melhor resultado, alcançando **MAPE de 11,20%**, superando modelos alternativos e o baseline estatístico.

![Comparação de Modelos](outputs/comparacao_modelos.png)


## 2. Real vs Previsto – Período de Teste (jul–set/2023)

Comparação entre os valores reais e previstos pelo modelo durante o período de teste.

O resultado demonstra boa capacidade do modelo em acompanhar o comportamento histórico do faturamento.

![Real vs Previsto](outputs/real_vs_previsto_melhor_modelo.png)


## 3. Previsão Futura – Próximos 3 Meses

Projeção consolidada do faturamento para outubro, novembro e dezembro de 2023.

O modelo identifica o comportamento esperado da série temporal, incluindo efeitos sazonais observados historicamente.

![Previsão Futura](outputs/previsao_futura.png)

---

# 🚀 Como executar

## Pré-requisitos

- Python 3.11+
- Git


## Passos

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/previsao-faturamento-varejo.git

cd previsao-faturamento-varejo
```


2. Crie e ative um ambiente virtual:

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\activate
```


3. Instale as dependências:

```bash
pip install -r requirements.txt
```


4. Certifique-se de que os arquivos necessários estejam disponíveis:

```
models/rf_model.pkl
data/processed/df_mensal.csv
data/processed/previsoes_futuras.csv
```


5. Execute o dashboard:

```bash
streamlit run app/app.py
```

---

# 📁 Estrutura do Projeto

```
previsao-faturamento-varejo/

├── app/
│   └── app.py                 # Dashboard Streamlit

├── data/
│   ├── raw/                   # Dados brutos (não versionados)
│   └── processed/             # Dados tratados e agregados

├── models/
│   └── rf_model.pkl           # Modelo treinado

├── notebooks/
│   ├── 01_exploracao_dados.ipynb
│   ├── 02_tratamento_dados.ipynb
│   └── 03_modelagem.ipynb

├── outputs/
│   ├── gráficos
│   └── métricas do projeto

├── src/
│   ├── data_cleaning.py       # Tratamento dos dados
│   ├── features.py            # Engenharia de atributos
│   ├── model.py               # Treinamento do modelo
│   ├── predict.py             # Geração das previsões
│   └── utils.py               # Funções auxiliares

├── .gitignore
├── README.md
└── requirements.txt
```

---

# 📋 Tabela de Métricas

| Modelo | MAPE (%) |
|-----------------------|----------|
| Random Forest Base | 11,20 |
| Random Forest Tunado | 11,87 |
| XGBoost | 12,28 |
| Baseline MM3 | 14,75 |

---

# 🖥️ Dashboard

O dashboard permite explorar os resultados do modelo através de:

- Previsões futuras consolidadas.
- Previsões individuais por loja.
- Histórico mensal de faturamento.
- Comparação de modelos.
- Métricas de desempenho.
- Análise da importância das variáveis utilizadas pelo modelo.


---

# 🧠 Principais Insights do Modelo

As variáveis que mais contribuíram para a previsão foram:

- Faturamento do mês anterior (`lag_1_mes`).
- Faturamento dos meses anteriores (`lag_2_meses` e `lag_3_meses`).
- Taxa de crescimento histórica.
- Média móvel dos últimos meses.
- Identificador da loja.

Esses resultados mostram que o comportamento recente do faturamento possui forte influência na previsão futura.


---

# 👤 Desenvolvido por

Felipe Tamiozzo - Felipe Barbosa - Kilian Israel

Projeto de Ciência de Dados aplicado à previsão de faturamento utilizando Machine Learning.


---

# 📄 Licença

Projeto desenvolvido para fins de estudo, portfólio e demonstração técnica.
