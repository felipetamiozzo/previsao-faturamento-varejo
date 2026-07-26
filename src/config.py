from pathlib import Path


# ============================================================
# CAMINHOS DO PROJETO
# ============================================================

# Diretório raiz do projeto
ROOT_DIR = Path(__file__).resolve().parent.parent


# Organização das pastas de dados
DATA_DIR = ROOT_DIR / "data"

# Dados originais (sem tratamento)
RAW_DIR = DATA_DIR / "raw"

# Dados tratados e preparados para modelagem
PROCESSED_DIR = DATA_DIR / "processed"


# Pasta onde ficam os modelos treinados
MODELS_DIR = ROOT_DIR / "models"


# Pasta onde ficam arquivos gerados pelo projeto
OUTPUTS_DIR = ROOT_DIR / "outputs"

# Imagem utilizada no Streamlit para exibir importância das variáveis
FEATURE_IMPORTANCE_PATH = OUTPUTS_DIR / "feature_importance.png"



# ============================================================
# CONFIGURAÇÕES DO MODELO
# ============================================================

# Variável que o modelo irá prever
TARGET = "faturamento_liquido_mensal"


# Variáveis utilizadas como entrada do modelo
#
# Incluem:
# - identificação da loja
# - informações temporais
# - valores históricos (lags)
# - médias e taxas de crescimento
# - comportamento sazonal
FEATURES = [
    "loja",
    "ano",
    "mes",
    "trimestre",
    "indice_tempo",
    "lag_1_mes",
    "lag_2_meses",
    "lag_3_meses",
    "media_movel_3m",
    "taxa_crescimento",
    "mes_seno",
    "mes_cosseno",
]


# ============================================================
# PARÂMETROS DO RANDOM FOREST
# ============================================================

# Mantém os resultados reproduzíveis
RANDOM_STATE = 42


# Quantidade de árvores utilizadas no modelo
N_ESTIMATORS = 300


# Profundidade máxima das árvores
MAX_DEPTH = 5



# ============================================================
# REGRA DE NEGÓCIO
# ============================================================

# Limite máximo de crescimento permitido nas previsões.
# Evita aumentos fora de um cenário esperado.

LIMITE_CRESCIMENTO = 1.20