import pandas as pd
import numpy as np

def criar_features(df_mensal: pd.DataFrame) -> pd.DataFrame:
    # Baseado no notebook 03 – feature engineering
    df = df_mensal.copy()
    df['ANO'] = df['PERIODO_MES'].dt.year
    df['MES_NUM'] = df['PERIODO_MES'].dt.month
    df['TRIMESTRE'] = df['PERIODO_MES'].dt.quarter
    df['INDICE_TEMPO'] = df.groupby('CLV_BANCO').cumcount() + 1

    for lag in [1,2,3]:
        df[f'LAG_{lag}'] = df.groupby('CLV_BANCO')['FAT_LIQUIDO_MES'].shift(lag)

    df['MEDIA_MOVEL_3'] = df.groupby('CLV_BANCO')['FAT_LIQUIDO_MES'].transform(
        lambda x: x.shift(1).rolling(3, min_periods=1).mean()
    )
    df['CRESCIMENTO'] = df.groupby('CLV_BANCO')['FAT_LIQUIDO_MES'].pct_change() * 100
    df['MES_SENO'] = np.sin(2 * np.pi * df['MES_NUM'] / 12)
    df['MES_COSSENO'] = np.cos(2 * np.pi * df['MES_NUM'] / 12)

    # Remover linhas com NaN nos lags (opcional, mas recomendado)
    df = df.dropna(subset=['LAG_1', 'LAG_2', 'LAG_3', 'MEDIA_MOVEL_3'])
    return df