import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
import joblib

def treinar_modelo(df_features: pd.DataFrame, target: str = 'FAT_LIQUIDO_MES') -> Pipeline:
    features = ['CLV_BANCO', 'ANO', 'MES_NUM', 'TRIMESTRE', 'INDICE_TEMPO',
                'LAG_1', 'LAG_2', 'LAG_3', 'MEDIA_MOVEL_3',
                'CRESCIMENTO', 'MES_SENO', 'MES_COSSENO']

    X = df_features[features]
    y = df_features[target]

    preprocessador = ColumnTransformer(
        transformers=[('loja', OneHotEncoder(handle_unknown='ignore'), ['CLV_BANCO'])],
        remainder='passthrough'
    )

    modelo = Pipeline([
        ('preprocessador', preprocessador),
        ('modelo', RandomForestRegressor(n_estimators=300, max_depth=5, random_state=42))
    ])

    modelo.fit(X, y)
    return modelo

def salvar_modelo(modelo, caminho: str):
    joblib.dump(modelo, caminho)