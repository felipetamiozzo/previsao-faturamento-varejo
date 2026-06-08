from src.data_cleaning import carregar_dados_brutos, tratar_dados, agregar_mensal
from src.features import criar_features
from src.model import treinar_modelo, salvar_modelo
from src.predict import gerar_previsoes
from src.utils import calcular_metricas, salvar_resultados

def main():
    # 1. Limpeza e agregação
    df_bruto = carregar_dados_brutos("data/raw/")
    df_tratado = tratar_dados(df_bruto)
    df_mensal = agregar_mensal(df_tratado)
    df_mensal.to_csv("data/processed/df_mensal.csv", index=False)

    # 2. Feature engineering
    df_features = criar_features(df_mensal)
    df_features.to_csv("data/processed/df_features.csv", index=False)

    # 3. Treinamento do modelo
    modelo = treinar_modelo(df_features)
    salvar_modelo(modelo, "models/random_forest.pkl")

    # 4. Previsão futura
    previsoes = gerar_previsoes(modelo, df_mensal, periodos=3)
    previsoes.to_csv("outputs/previsoes_futuras.csv", index=False)

    # 5. Métricas (se houver teste)
    # ...

if __name__ == "__main__":
    main()