# 📈 Projeto de Previsão de Faturamento com Machine Learning

## Relatório Final – 2026

# 1. Visão Geral do Projeto

## Objetivo

Desenvolver uma solução de Machine Learning capaz de prever o faturamento líquido mensal de lojas utilizando dados históricos de vendas.

O objetivo principal foi criar um modelo preditivo que auxilie processos de:

- planejamento financeiro;
- definição de metas comerciais;
- projeção de receita;
- acompanhamento operacional;
- tomada de decisão baseada em dados.

A solução foi construída utilizando uma abordagem completa de Data Science, passando pelas etapas de:

**Coleta → Tratamento → Análise → Feature Engineering → Modelagem → Avaliação → Previsão → Dashboard**

---

# 2. Resultados Principais

O modelo final selecionado foi o:

##  Random Forest Regressor

Com desempenho:

| Métrica | Resultado |
|---|---:|
| MAPE | **11,20%** |
| WMAPE | **8,63%** |
| MAE | R$ 1.046.032 |
| RMSE | R$ 1.544.294 |

O modelo apresentou uma redução significativa de erro quando comparado ao baseline:

| Modelo | MAPE |
|---|---:|
| Baseline Média Móvel 3 meses | 14,75% |
| Random Forest Base | **11,20%** |

### Ganho obtido:

- Redução de aproximadamente **24% no erro percentual (MAPE)** em relação ao baseline.
- Melhor equilíbrio entre desempenho, interpretabilidade e capacidade de generalização.

---

# 3. Dados Utilizados

A base inicial possuía:

- **8.297.456 registros transacionais**
- 14 variáveis originais
- período analisado: janeiro/2022 até setembro/2023
- 8 unidades analisadas
- 21 meses completos de histórico

A variável alvo utilizada foi:

```
faturamento_liquido_mensal
```

Obtida através da agregação mensal do faturamento líquido das vendas.

---

# 4. Tratamento dos Dados

O pipeline de tratamento aplicou diversas validações para garantir qualidade dos dados:

## Principais etapas:

| Tratamento | Resultado |
|-|-|
| Remoção do mês incompleto | Outubro/2023 removido para evitar distorção temporal |
| Tratamento de datas inválidas | Registros inconsistentes removidos |
| Validação financeira | Identificação de divergências entre bruto, desconto e líquido |
| Tratamento de produtos sem identificação | Valores nulos substituídos |
| Remoção de variáveis sem informação | Colunas sem contribuição removidas |
| Criação de indicadores de qualidade | Flags de inconsistência, devolução e alto valor |

Também foram criadas variáveis auxiliares para análise:

- flag de devoluções;
- flag de inconsistências financeiras;
- identificação de vendas acima do percentil 99.

---

# 5. Feature Engineering

Para capturar comportamento histórico e sazonalidade foram desenvolvidas variáveis preditivas:

## Variáveis temporais

- ano;
- mês;
- trimestre;
- índice temporal por loja.

## Variáveis históricas

Foram utilizadas defasagens de faturamento:

- LAG 1 mês;
- LAG 2 meses;
- LAG 3 meses.

## Tendência

- média móvel dos últimos 3 meses;
- taxa de crescimento mensal.

## Sazonalidade

Aplicação de transformação cíclica:

- seno do mês;
- cosseno do mês.

Essa abordagem permitiu representar corretamente padrões sazonais, como períodos de maior faturamento.

---

# 6. Modelos Avaliados

Foram comparadas diferentes abordagens:

| Modelo | Descrição |
|-|-|
| Baseline MM3 | Média móvel dos últimos 3 meses |
| Regressão Linear | Modelo linear tradicional |
| Random Forest Base | Modelo final selecionado |
| Random Forest Tunado | Otimização via busca de hiperparâmetros |
| XGBoost | Modelo baseado em Gradient Boosting |

---

# 7. Comparação dos Modelos

| Modelo | MAE | RMSE | MAPE | WMAPE |
|-|-:|-:|-:|-:|
| Random Forest Base | R$ 1.046.032 | R$ 1.544.294 | **11,20%** | **8,63%** |
| Random Forest Tunado | R$ 1.200.307 | R$ 1.715.937 | 11,87% | 9,90% |
| XGBoost | R$ 1.552.802 | R$ 2.425.989 | 12,28% | 12,81% |
| Baseline MM3 | R$ 1.800.702 | R$ 2.723.303 | 14,75% | 14,85% |
| Regressão Linear | - | - | 253% | 96% |

---

# 8. Previsão Futura

Após o treinamento utilizando todo o histórico disponível, foram realizadas previsões para os próximos três meses.

Foi aplicado um controle de crescimento máximo mensal de 20%, evitando previsões fora do comportamento histórico.

## Resultado consolidado:

| Período | Previsão |
|-|-:|
| Outubro/2023 | R$ 89,9 milhões |
| Novembro/2023 | R$ 91,6 milhões |
| Dezembro/2023 | R$ 104,6 milhões |

O crescimento previsto para dezembro:

```
+14,3%
```

apresenta comportamento compatível com a sazonalidade observada historicamente no período de final de ano.

---

# 9. Interpretabilidade do Modelo

A análise da importância das variáveis mostrou que os principais fatores utilizados pelo modelo foram:

1. Faturamento do mês anterior;
2. Média móvel dos últimos 3 meses;
3. Histórico recente da loja;
4. Variáveis temporais.

O resultado demonstra que o comportamento recente do faturamento possui maior influência na previsão futura.

---

# 10. Aplicação Streamlit

Foi desenvolvido um dashboard interativo para disponibilização dos resultados.

Funcionalidades:

## Previsão Consolidada

- visão geral dos próximos meses;
- acompanhamento da evolução prevista.

## Previsão por Loja

- seleção individual da unidade;
- previsão específica para cada loja;
- comparação entre desempenhos.

## Histórico

- análise da evolução do faturamento;
- comportamento mensal.

## Métricas do Modelo

- comparação dos algoritmos;
- indicadores de desempenho.

## 📌 Importância das Variáveis

- interpretação dos fatores utilizados pelo modelo.

---

# 11. Arquitetura do Projeto

```
Projeto_Previsao_Faturamento/

│
├── app/
│   └── app.py                 # Dashboard Streamlit
│
├── data/
│   ├── raw/                   # Dados originais
│   └── processed/             # Dados tratados
│
├── models/
│   └── rf_model.pkl           # Modelo final treinado
│
├── notebooks/
│   ├── 01_exploracao.ipynb
│   ├── 02_tratamento.ipynb
│   └── 03_modelagem.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── features.py
│   ├── model.py
│   ├── predict.py
│   └── utils.py
│
├── main.py                    # Pipeline completo
│
└── README.md
```

---

# 12. Tecnologias Utilizadas

## Linguagem

- Python

## Manipulação de Dados

- Pandas
- NumPy

## Machine Learning

- Scikit-Learn
- Random Forest
- XGBoost

## Visualização

- Plotly
- Streamlit
- Matplotlib

## Versionamento

- Git
- GitHub

---

# 13. Como Executar o Projeto

## Instalar dependências

```bash
pip install -r requirements.txt
```

## Executar pipeline completo

```bash
python main.py
```

O pipeline irá:

1. carregar dados;
2. realizar tratamento;
3. gerar agregação mensal;
4. criar features;
5. treinar modelo;
6. gerar previsões futuras.

---

## Executar Dashboard

```bash
streamlit run app/app.py
```

---

# 14. Próximas Evoluções

Possíveis melhorias futuras:

- inclusão de variáveis externas:
  - inflação;
  - feriados;
  - campanhas promocionais;
  - indicadores econômicos.

- monitoramento contínuo do erro do modelo;

- reentreinamento automático;

- utilização de SHAP para explicabilidade individual;

- modelos avançados de séries temporais;

- integração com bancos de dados e pipelines automatizados.

---

# Conclusão

O projeto demonstrou que técnicas de Machine Learning podem ser utilizadas para prever faturamento com boa precisão, superando abordagens tradicionais baseadas apenas em médias históricas.

O modelo final alcançou:

🎯 **MAPE de 11,20%**

com capacidade de gerar previsões mensais por loja e apoiar processos de planejamento e tomada de decisão orientada por dados.

---

**Projeto desenvolvido por Grupo 1 - Felipe Tamiozzo, Felipe Barbosa, Kilian Israel**  
**Data Science | Machine Learning | Analytics**