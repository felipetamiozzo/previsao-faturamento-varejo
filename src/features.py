import pandas as pd
import numpy as np



# ============================================================
# CRIAÇÃO DE FEATURES PARA O MODELO
# ============================================================

def criar_features(df_mensal: pd.DataFrame) -> pd.DataFrame:
    """
    Cria as variáveis utilizadas pelo modelo de previsão.
    """


    # Cria uma cópia para preservar a base original
    df = df_mensal.copy()



    # ========================================================
    # FEATURES TEMPORAIS
    # ========================================================

    # Extrai informações de calendário para capturar
    # padrões sazonais e tendência ao longo do tempo
    df["ano"] = (
        df["mes_referencia"]
        .dt.year
    )


    df["mes"] = (
        df["mes_referencia"]
        .dt.month
    )


    df["trimestre"] = (
        df["mes_referencia"]
        .dt.quarter
    )


    # Cria um contador sequencial de meses por loja,
    # permitindo identificar evolução temporal
    df["indice_tempo"] = (
        df.groupby("loja")
        .cumcount()
        + 1
    )



    # ========================================================
    # FEATURES DE HISTÓRICO (LAGS)
    # ========================================================

    # Recupera o faturamento dos meses anteriores.
    #
    # Essas variáveis ajudam o modelo a entender
    # o comportamento histórico da loja.

    df["lag_1_mes"] = (
        df.groupby("loja")
        ["faturamento_liquido_mensal"]
        .shift(1)
    )


    df["lag_2_meses"] = (
        df.groupby("loja")
        ["faturamento_liquido_mensal"]
        .shift(2)
    )


    df["lag_3_meses"] = (
        df.groupby("loja")
        ["faturamento_liquido_mensal"]
        .shift(3)
    )



    # ========================================================
    # MÉDIA MÓVEL
    # ========================================================

    # Calcula a média dos últimos 3 meses anteriores.
    #
    # Reduz oscilações pontuais e representa
    # uma tendência mais estável do faturamento.
    df["media_movel_3m"] = (
        df.groupby("loja")
        ["faturamento_liquido_mensal"]
        .transform(
            lambda x:
            x.shift(1)
            .rolling(
                3,
                min_periods=1
            )
            .mean()
        )
    )



    # ========================================================
    # TAXA DE CRESCIMENTO
    # ========================================================

    # Calcula a variação percentual do faturamento
    # em relação ao mês anterior.
    df["taxa_crescimento"] = (
        df.groupby("loja")
        ["faturamento_liquido_mensal"]
        .pct_change()
        * 100
    )



    # ========================================================
    # REPRESENTAÇÃO DE SAZONALIDADE
    # ========================================================

    # Transforma o mês em variáveis cíclicas.
    #
    # Isso permite que o modelo entenda que meses próximos
    # no calendário possuem comportamento semelhante
    # (exemplo: dezembro e janeiro).
    df["mes_seno"] = (
        np.sin(
            2 * np.pi * df["mes"] / 12
        )
    )


    df["mes_cosseno"] = (
        np.cos(
            2 * np.pi * df["mes"] / 12
        )
    )



    return df