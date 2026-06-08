import pandas as pd
import glob

def carregar_dados_brutos(caminho_raw: str) -> pd.DataFrame:
    arquivos = glob.glob(f"{caminho_raw}/CASTING_*.csv")
    dfs = [pd.read_csv(f, low_memory=False) for f in arquivos]
    return pd.concat(dfs, ignore_index=True)

def tratar_dados(df: pd.DataFrame) -> pd.DataFrame:
    # Copie a função tratamento_dados_transacionais do notebook 02
    # (remover outubro/2023, criar flags, etc.)
    # Retorne o DataFrame tratado (transacional)
    pass

def agregar_mensal(df_tratado: pd.DataFrame) -> pd.DataFrame:
    # Copie a função agregar_mensal do notebook 02
    pass