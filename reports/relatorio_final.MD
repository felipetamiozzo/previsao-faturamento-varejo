# Projeto de Previsão de Faturamento – Solução Casting

## Relatório Final – Junho de 2026

---

## 1. Resumo Executivo

**Objetivo**  
Desenvolver um modelo preditivo para estimar o faturamento líquido mensal da Solução Casting, utilizando dados históricos de vendas, com horizonte de três meses à frente, para apoiar decisões comerciais e financeiras.

**Escopo**  
Foram analisados dados transacionais de 8 lojas (`CASTING_DB063`, `DB069`, `DB088`, `DB092`, `DB101`, `DB102`, `DB109`, `DB113`) no período de janeiro de 2022 a setembro de 2023 (21 meses completos). A variável‑alvo é o `FAT_LIQUIDO_MES`, obtido pela agregação mensal do valor líquido final das vendas (`VUF_VLRLIQFINAL`).

**Principais Resultados**  
- O modelo **Random Forest base** apresentou o melhor desempenho, com **MAPE de 11,16%** e **WMAPE de 8,57%**, superando o baseline e demais modelos testados.
- As previsões para outubro, novembro e dezembro/2023 indicam crescimento sazonal consistente com o histórico, com destaque para dezembro (R$ 104,6 milhões, +14,3% sobre novembro).

---

## 2. Metodologia

### 2.1. Exploração e Tratamento dos Dados

A base bruta continha **8.297.456 registros**, 14 colunas, de janeiro/2022 a outubro/2023. As principais ações de tratamento foram:

| Ação                                                                 | Justificativa                                                                 |
|----------------------------------------------------------------------|-------------------------------------------------------------------------------|
| Remoção de outubro/2023                                              | Mês incompleto (apenas 7.919 registros) distorce séries temporais.            |
| Remoção de 4 registros com desconto > bruto em vendas positivas      | Possíveis erros de PDV, volume insignificante.                                |
| Preenchimento de `PRO_CODIGO` nulo (3 registros) com `'PRODUTO_NAO_MAPEADO'` | Preserva a transação para faturamento.                                        |
| Remoção da coluna `VUF_VLRTROCA`                                     | Coluna totalmente zerada, sem contribuição.                                   |
| Criação de flag de inconsistência financeira                         | Sinaliza divergências entre `bruto - desconto` e `líquido` (11,86% dos registros). |
| Criação de flag de devolução (`FLAG_DEVOLUCAO`)                      | Baseada em `VUF_VLRLIQFINAL < 0` (4,52% dos registros).                       |
| Criação de flag de venda de alto valor (`FLAG_ALTO_VALOR`)           | Baseada no percentil 99 por loja (0,82% dos registros).                       |

A agregação mensal resultou em **168 observações** (8 lojas × 21 meses), prontas para modelagem.

### 2.2. Feature Engineering (Base Mensal)

Foram criadas as seguintes variáveis explicativas:

- **Temporais** – ano, mês, trimestre, índice de tempo sequencial por loja.
- **Lags** – valores do faturamento defasados em 1, 2 e 3 meses.
- **Média móvel** – média dos três meses anteriores.
- **Crescimento percentual** – variação percentual mês a mês.
- **Sazonalidade cíclica** – seno e cosseno do número do mês (12 meses).

A variável categórica `CLV_BANCO` foi codificada via **One‑Hot Encoding** no pipeline de modelagem.

### 2.3. Modelos Avaliados

| Modelo                      | Características                                                                 |
|-----------------------------|---------------------------------------------------------------------------------|
| **Baseline**                | Média simples dos últimos 3 meses (sem treinamento).                            |
| **Regressão Linear**        | Modelo linear com as mesmas features, incluindo `CLV_BANCO`.                    |
| **Random Forest (base)**    | 300 árvores, profundidade máxima 5.                                             |
| **Random Forest (tunado)**  | Otimização via GridSearch com TimeSeriesSplit (3 folds).                        |
| **XGBoost**                 | 300 árvores, `max_depth=3`, `learning_rate=0.05`, `subsample=0.9`.              |

### 2.4. Validação Temporal

- **Treino**: abril de 2022 a junho de 2023 (15 meses)
- **Teste**: julho a setembro de 2023 (3 meses)

**Métricas** – MAE, RMSE, MAPE, WMAPE.

---

## 3. Resultados

### 3.1. Comparação de Modelos

| Modelo                | MAE (R$)   | RMSE (R$)   | MAPE (%) | WMAPE (%) |
|-----------------------|------------|-------------|----------|-----------|
| **Random Forest Base**| 1.038.660  | 1.540.806   | **11,16** | 8,57       |
| Random Forest Tunado  | 1.200.307  | 1.715.937   | 11,73    | 9,90       |
| XGBoost               | 1.552.802  | 2.425.989   | 13,72    | 12,81      |
| Baseline MM3          | 1.800.702  | 2.723.303   | 14,75    | 14,85      |
| Regressão Linear      | 11.704.482 | 18.017.336  | 253,01   | 96,52      |

> **Melhor modelo**: Random Forest Base, com **MAPE de 11,16%**.

### 3.2. Análise dos Resultados

- O Random Forest base superou até mesmo a versão tunada, indicando que o conjunto de hiperparâmetros inicial já era adequado e que o GridSearch pode ter causado leve overfitting à validação temporal.
- A Regressão Linear apresentou desempenho muito inferior, confirmando a relação não linear entre as variáveis.
- O baseline (média móvel de 3 meses) serviu como referência mínima, sendo superado por todos os modelos baseados em árvores.

---

## 4. Previsão Futura

Com o modelo **Random Forest Base** treinado com todo o histórico (janeiro/2022 a setembro/2023), foram geradas previsões para os três meses seguintes, aplicando um **limite de crescimento mensal de 20%** para evitar extrapolações excessivas.

| Período       | Faturamento Previsto (R$) | Crescimento mensal |
|---------------|---------------------------|--------------------|
| Outubro/2023  | 89,9 M                    | –                  |
| Novembro/2023 | 91,6 M                    | +1,9%              |
| Dezembro/2023 | 104,6 M                   | +14,3%             |

O crescimento de dezembro (+14,3%) reflete a **sazonalidade típica de final de ano**, observada nos dados históricos (pico em dez/2022). O limite de 20% foi definido para evitar valores irrealistas, mantendo a coerência com a trajetória anterior.

### Diagnóstico do pico de dezembro

A previsão de dezembro/2023 por loja mostra que as maiores contribuições vêm de `CASTING_DB113` (R$ 34,6 M) e `CASTING_DB109` (R$ 21,7 M). Quando comparado ao dezembro de 2022, nota-se uma queda expressiva nessas lojas (cerca de -51% e -40%, respectivamente), o que é consistente com a tendência de estabilização observada ao longo de 2023. As demais lojas apresentam variações pequenas ou positivas.

---

## 5. Conclusões e Recomendações

- O **Random Forest Base** é o modelo recomendado para produção, com MAPE de 11,16%, equilibrando simplicidade e acurácia.
- A sazonalidade de dezembro é capturada corretamente – a manutenção de variáveis temporais (mês, seno/cosseno) e lags é essencial.
- As previsões para outubro, novembro e dezembro/2023 são **realistas** e podem ser usadas para planejamento de caixa, estoque e definição de metas comerciais.

**Recomendações:**
1. **Monitoramento contínuo** – comparar as previsões com os resultados reais mensalmente.
2. **Recalibração semestral** – reestimar o modelo com os novos dados a cada seis meses.
3. **Expansão** – testar previsões por vendedor ou cliente, caso a granularidade dos dados permita.

---

## 6. Próximos Passos

- Automatizar o pipeline de previsão (coleta → tratamento → modelo → entrega do relatório).
- Incluir variáveis exógenas (dias úteis, feriados, campanhas promocionais) para refinar a acurácia.
- Desenvolver um dashboard em Power BI ou Streamlit para visualização dinâmica das previsões.

---

**Responsável pela modelagem:** Grupo 1 projeto Previsão de Faturamento – Solução Casting  
**Data do relatório:** junho de 2026