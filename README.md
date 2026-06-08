

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
├── outputs/                  # Gráficos e resultados (opcional)
├── src/                      # Módulos auxiliares (data_cleaning, features, etc.)
├── .gitignore
├── README.md
└── requirements.txt
```

## 📈 Resultados

- **Modelo final:** Random Forest Base
- **MAPE:** 11,16% (melhor que Baseline MM3 com 14,75%)
- **Previsão para dezembro/2023:** R$ 104,6 M (consolidado)

### Comparação de Modelos

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

![Dashboard Preview](outputs/dashboard_sample.png) *(adicione uma imagem se desejar)*

## 👥 Desenvolvido por

Grupo 1 – Solução Casting | Projeto DNC

## 📄 Licença

Este projeto é de uso interno da empresa. Não redistribuir sem autorização.
```

> **Observação:** Substitua `seu-usuario` pelo nome real do repositório. Se não quiser incluir a imagem, remova a linha do `Dashboard Preview`.

---

## 3. Instruções adicionais

- **Arquivos a serem commitados:**  
  - `app/app.py` (código final corrigido)  
  - `src/` (todos os `.py` de apoio, se existirem e estiverem completos)  
  - `notebooks/` (opcional – notebooks limpos, sem dados sensíveis)  
  - `requirements.txt`  
  - `.gitignore`  
  - `README.md`  
  - `models/rf_base_model.pkl` (se optar por versionar)  
  - `outputs/` (apenas imagens, se quiser documentar)  

- **Não commitar:** pastas `data/raw`, `data/processed`, `venv/`, `__pycache__/`, `presentation/` (se conter slides finais grandes), `reports/`.

- **Antes do commit, verifique se não há senhas ou caminhos absolutos nos arquivos.**

Caso precise de ajuda para gerar o `requirements.txt` definitivo ou para ajustar a estrutura, é só pedir.