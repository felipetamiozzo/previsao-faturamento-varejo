import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def calcular_metricas(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mask = y_true != 0
    mape = np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    wmape = np.sum(np.abs(y_true - y_pred)) / np.sum(np.abs(y_true)) * 100
    return {'MAE': mae, 'RMSE': rmse, 'MAPE': mape, 'WMAPE': wmape}

def salvar_resultados(df, caminho):
    df.to_csv(caminho, index=False)