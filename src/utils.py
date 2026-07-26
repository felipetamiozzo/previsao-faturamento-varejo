import pandas as pd
import numpy as np

# Métricas utilizadas para avaliar modelos de regressão
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)



# ============================================================
# CÁLCULO DAS MÉTRICAS DO MODELO
# ============================================================

def calcular_metricas(y_true, y_pred):


    # Converte os valores para arrays NumPy
    # facilitando os cálculos matemáticos
    y_true = np.array(y_true)

    y_pred = np.array(y_pred)



    # Erro absoluto médio (MAE)
    #
    # Representa o erro médio das previsões
    # na mesma unidade do faturamento.
    mae = mean_absolute_error(
        y_true,
        y_pred
    )



    # Raiz do erro quadrático médio (RMSE)
    #
    # Penaliza erros maiores e ajuda a identificar
    # previsões muito distantes do valor real.
    rmse = np.sqrt(
        mean_squared_error(
            y_true,
            y_pred
        )
    )



    # Máscara para evitar divisão por zero
    # no cálculo do MAPE
    mask = y_true != 0



    # Erro percentual médio absoluto (MAPE)
    #
    # Mostra o erro médio percentual do modelo.
    mape = (
        np.mean(
            np.abs(
                (
                    y_true[mask]
                    -
                    y_pred[mask]
                )
                /
                y_true[mask]
            )
        )
        * 100
    )



    # Erro percentual absoluto ponderado (WMAPE)
    #
    # Métrica mais adequada para faturamento,
    # pois considera o peso financeiro dos valores.
    wmape = (
        np.sum(
            np.abs(
                y_true - y_pred
            )
        )
        /
        np.sum(
            np.abs(y_true)
        )
        * 100
    )



    # Retorna todas as métricas organizadas
    return {

        "MAE": mae,

        "RMSE": rmse,

        "MAPE": mape,

        "WMAPE": wmape

    }



# ============================================================
# SALVAMENTO DOS RESULTADOS
# ============================================================

def salvar_resultados(df, caminho):


    # Exporta DataFrame para CSV.
    #
    # Utilizado para salvar:
    # - previsões
    # - resultados de avaliação
    # - tabelas geradas pelo pipeline
    df.to_csv(
        caminho,
        index=False
    )