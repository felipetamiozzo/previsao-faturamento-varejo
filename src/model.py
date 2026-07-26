import pandas as pd

# Ferramentas para criação do pipeline de transformação
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Pipeline para unir pré-processamento e modelo
from sklearn.pipeline import Pipeline

# Algoritmo utilizado no projeto
from sklearn.ensemble import RandomForestRegressor

# Biblioteca para salvar o modelo treinado
import joblib



# ============================================================
# FEATURES UTILIZADAS NO MODELO
# ============================================================

# Variáveis de entrada utilizadas pelo Random Forest
FEATURES = [

    # Identificação da loja
    "loja",

    # Variáveis temporais
    "ano",
    "mes",
    "trimestre",
    "indice_tempo",

    # Histórico de faturamento
    "lag_1_mes",
    "lag_2_meses",
    "lag_3_meses",

    # Tendência e comportamento
    "media_movel_3m",
    "taxa_crescimento",

    # Sazonalidade
    "mes_seno",
    "mes_cosseno",
]



# ============================================================
# TREINAMENTO DO MODELO
# ============================================================

def treinar_modelo(
    df_features: pd.DataFrame,
    target: str = "faturamento_liquido_mensal"
):


    # Separação das variáveis preditoras (X)
    # e variável que será prevista (y)
    X = df_features[FEATURES]

    y = df_features[target]



    # ========================================================
    # PRÉ-PROCESSAMENTO
    # ========================================================

    # Transforma a variável categórica "loja"
    # em variáveis numéricas utilizando One Hot Encoding.
    #
    # O modelo passa a receber uma coluna para cada loja.
    # handle_unknown evita erro caso apareça uma nova loja.
    preprocessador = ColumnTransformer(

        transformers=[

            (
                "loja",

                OneHotEncoder(
                    handle_unknown="ignore"
                ),

                ["loja"]
            )

        ],

        # Mantém as demais variáveis numéricas sem alteração
        remainder="passthrough"
    )



    # ========================================================
    # PIPELINE DO MODELO
    # ========================================================

    # Pipeline garante que o mesmo processo de transformação
    # seja aplicado durante treinamento e previsão.
    modelo = Pipeline([


        # Primeira etapa:
        # transformação dos dados
        (
            "preprocessador",
            preprocessador
        ),



        # Segunda etapa:
        # treinamento do Random Forest
        (
            "modelo",

            RandomForestRegressor(

                # Quantidade de árvores do modelo
                n_estimators=300,

                # Controle da complexidade das árvores
                max_depth=5,

                # Mantém resultados reproduzíveis
                random_state=42
            )
        )
    ])



    # Treinamento do modelo utilizando os dados históricos
    modelo.fit(
        X,
        y
    )


    return modelo




# ============================================================
# SALVAMENTO DO MODELO TREINADO
# ============================================================

def salvar_modelo(modelo, caminho: str):


    # Salva o pipeline completo:
    # - transformação das variáveis
    # - modelo treinado
    #
    # Permite reutilizar o modelo no Streamlit
    # sem precisar treinar novamente.
    joblib.dump(
        modelo,
        caminho
    )