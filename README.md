Atualizei o `README.md` com as imagens fornecidas, renomeando-as de forma descritiva e organizando a exibição. As imagens foram colocadas na pasta `outputs/` e referenciadas no documento. Abaixo está o conteúdo final do `README.md` ajustado. Substitua o arquivo existente por este.

```markdown
# Solução Casting - Previsão de Faturamento

**Grupo 1** | Projeto DNC

Dashboard interativo e modelo preditivo para previsão de faturamento líquido mensal por loja, utilizando dados históricos de transações (jan/2022 a set/2023). O modelo Random Forest atingiu **MAPE de 11,16%** no período de teste (jul-set/2023).

## 📊 Funcionalidades

- Previsão dos próximos 3 meses (out, nov, dez/2023) com limite de crescimento mensal de 20%.
- Dashboard Streamlit com:
  - Gráfico consolidado de previsão futura.
  - Tabela de previsões por loja (filtrável).
  - Histórico de faturamento por loja.
  - Métricas do modelo e comparação com outros algoritmos.
- Modelo treinado com validação temporal (TimeSeriesSplit).

## 📈 Resultados e Gráficos

### 1. Comparação de Modelos (MAPE)

O gráfico abaixo mostra o desempenho dos modelos testados. O **Random Forest Base** foi o melhor, com MAPE de 11,16%, superando o Baseline e outros algoritmos.

![Comparação de Modelos](outputs/comparacao_modelos.png)

### 2. Real vs Previsto – Período de Teste (jul–set/2023)

Acurácia do modelo no período de teste, mostrando boa aderência entre valores reais e previstos.

![Real vs Previsto](outputs/real_vs_previsto_melhor_modelo.png)

### 3. Previsão Futura – Próximos 3 Meses

Projeção de faturamento consolidado para outubro, novembro e dezembro de 2023, com destaque para o pico sazonal em dezembro.

![Previsão Futura](outputs/previsao_futura.png)

## 🚀 Como executar

### Pré‑requisitos

- Python 3.9+
- Git

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/casting-previsao.git
   cd casting-previsao
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   .\venv\Scripts\activate       # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Certifique-se de que os seguintes arquivos estejam nos locais corretos:
   - `models/rf_base_model.pkl` – modelo treinado.
   - `data/processed/df_mensal.csv` – base histórica agregada.
   - `data/processed/previsoes_futuras.csv` – previsões geradas (opcional, pois o app pode recalculá‑las).

5. Execute o dashboard:
   ```bash
   streamlit run app/app.py
   ```

## 📁 Estrutura do Projeto

```
casting-previsao/
├── app/                      # Aplicação Streamlit
│   └── app.py
├── data/                     # Dados (ignorados no repositório, exceto estrutura)
│   ├── raw/                  # Dados brutos (não versionados)
│   └── processed/            # Dados processados (não versionados)
├── models/                   # Modelo treinado (rf_base_model.pkl)
├── notebooks/                # Notebooks de exploração e modelagem
├── outputs/                  # Gráficos e resultados (imagens do README)
├── src/                      # Módulos auxiliares (data_cleaning, features, etc.)
├── .gitignore
├── README.md
└── requirements.txt
```

## 📋 Tabela de Métricas

| Modelo                | MAPE (%) |
|-----------------------|----------|
| Random Forest Base    | 11,16    |
| Random Forest Tunado  | 11,73    |
| XGBoost               | 13,72    |
| Baseline MM3          | 14,75    |
| Regressão Linear      | 253,01   |

## 🖥️ Dashboard

O dashboard permite filtrar por loja e visualizar:

- Previsões futuras (gráfico + tabela)
- Histórico real da loja
- Métricas globais do modelo

## 👥 Desenvolvido por

Grupo 1 – Solução Casting | Projeto DNC

## 📄 Licença

Este projeto é de uso interno da empresa. Não redistribuir sem autorização.
```

