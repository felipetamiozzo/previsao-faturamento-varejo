import glob
import numpy as np
import pandas as pd



# ============================================================
# CARREGAMENTO DOS DADOS BRUTOS
# ============================================================

def carregar_dados_brutos(caminho_raw: str) -> pd.DataFrame:


    # Busca todos os arquivos CSV da base bruta
    arquivos = glob.glob(
        f"{caminho_raw}/CASTING_*.csv"
    )


    # Carrega cada arquivo e junta em um único DataFrame
    dfs = [
        pd.read_csv(f, low_memory=False)
        for f in arquivos
    ]

    df = pd.concat(
        dfs,
        ignore_index=True
    )



    # Padroniza nomes das colunas para snake_case,
    # facilitando o uso durante o projeto
    dicionario_colunas = {

        'VUF_VLRLIQFINAL': 'faturamento_liquido',
        'VUF_VLRBRUTOVENDA': 'valor_bruto_venda',
        'VUF_VLRDESCONTO': 'valor_desconto',
        'VUF_VLRTROCA': 'valor_troca',

        'VUF_CODIGO': 'id_transacao',
        'CLV_BANCO': 'loja',

        'VUF_CODIGO_BOLETO': 'codigo_boleto',

        'UND_CODIGO': 'codigo_unidade',
        'FUN_CODIGO': 'codigo_funcionario',

        'VUF_DT': 'data_venda',

        'PRO_CODIGO': 'codigo_produto',
        'CAT_CODIGO': 'codigo_categoria',

        'VUF_QTBOLETO': 'qtd_boletos',
        'VUF_QTPRODUTO': 'qtd_produtos'
    }


    df = df.rename(
        columns=dicionario_colunas
    )


    return df




# ============================================================
# TRATAMENTO DOS DADOS
# ============================================================

def tratar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza limpeza, criação de flags e variáveis temporais.
    """


    # Cria cópia para preservar a base original
    df = df.copy()



    # Conversão da coluna de data
    df["data_venda"] = pd.to_datetime(
        df["data_venda"],
        errors="coerce"
    )


    # Remove registros sem data válida
    df = df[
        df["data_venda"].notna()
    ]



    # Remove outubro/2023 por possuir mês incompleto
    # e evitar distorção na série temporal
    df = df[
        df["data_venda"] < "2023-10-01"
    ]



    # Identifica possíveis erros onde o desconto
    # supera o valor da venda
    mask = (
        (df["valor_desconto"] > df["valor_bruto_venda"])
        &
        (df["valor_bruto_venda"] > 0)
    )

    df = df[~mask]



    # Preenche produtos sem identificação
    df["codigo_produto"] = (
        df["codigo_produto"]
        .fillna("PRODUTO_NAO_MAPEADO")
    )



    # Remove coluna sem informação relevante
    if (
        "valor_troca" in df.columns
        and (df["valor_troca"] == 0).all()
    ):

        df = df.drop(
            columns="valor_troca"
        )



    # Cria indicador de inconsistência financeira
    # Compara faturamento líquido esperado
    # contra valor bruto - descontos
    valor_calculado = (
        df["valor_bruto_venda"]
        -
        df["valor_desconto"]
    )


    df["flag_inconsistencia_financeira"] = (
        (
            df["faturamento_liquido"]
            -
            valor_calculado
        )
        .abs() > 0.01
    ).astype(int)



    # Marca registros com impacto negativo no faturamento
    df["flag_devolucao"] = (
        df["faturamento_liquido"] < 0
    ).astype(int)



    # Calcula limite de alto valor por loja (P99)
    p99 = (
        df[df["faturamento_liquido"] > 0]
        .groupby("loja")["faturamento_liquido"]
        .quantile(.99)
    )


    df["limiar_p99_loja"] = (
        df["loja"]
        .map(p99)
    )


    # Identifica vendas acima do padrão da loja
    df["flag_alto_valor"] = (
        (
            df["faturamento_liquido"]
            >
            df["limiar_p99_loja"]
        )
        &
        (df["faturamento_liquido"] > 0)
    ).astype(int)



    # Criação de variáveis temporais
    df["mes_numero"] = (
        df["data_venda"]
        .dt.month
    )


    df["trimestre"] = (
        df["data_venda"]
        .dt.quarter
    )


    # Cria referência mensal para agregação
    df["mes_referencia"] = (
        df["data_venda"]
        .dt.to_period("M")
    )



    # Ordenação necessária para criação
    # das variáveis temporais futuras
    df = (
        df
        .sort_values(
            ["loja", "data_venda"]
        )
        .reset_index(drop=True)
    )


    return df




# ============================================================
# AGREGAÇÃO MENSAL
# ============================================================

def agregar_mensal(df_tratado: pd.DataFrame) -> pd.DataFrame:
    """
    Consolida os dados transacionais por mês e loja.
    """


    # Agrupa vendas por loja e mês,
    # criando indicadores utilizados na análise e modelagem
    agg = (
        df_tratado
        .groupby(
            ["mes_referencia", "loja"]
        )
        .agg(

            # Faturamento líquido mensal
            faturamento_liquido_mensal=(
                "faturamento_liquido",
                "sum"
            ),

            # Indicadores financeiros
            FAT_BRUTO_POS_MES=(
                "valor_bruto_venda",
                lambda x: x[x > 0].sum()
            ),

            TOTAL_DESCONTOS_POS=(
                "valor_desconto",
                lambda x: x[x > 0].sum()
            ),

            TOTAL_REG_NEG_VALOR=(
                "faturamento_liquido",
                lambda x: x[x < 0].sum()
            ),


            # Indicadores operacionais
            QTD_TRANSACOES=(
                "id_transacao",
                "count"
            ),

            QTD_REG_NEG=(
                "flag_devolucao",
                "sum"
            ),

            QTD_ALTO_VALOR=(
                "flag_alto_valor",
                "sum"
            ),

            QTD_INCONSIST_FINANCEIRA=(
                "flag_inconsistencia_financeira",
                "sum"
            ),


            # Métricas de ticket médio
            TICKET_MEDIO_POS=(
                "faturamento_liquido",
                lambda x: x[x > 0].mean()
            ),

            TICKET_MEDIano_POS=(
                "faturamento_liquido",
                lambda x: x[x > 0].median()
            )
        )
        .reset_index()
    )



    # Criação de indicadores percentuais
    # para análise de qualidade financeira

    agg["TAXA_REG_NEG_PCT"] = np.where(
        agg["FAT_BRUTO_POS_MES"] > 0,
        agg["TOTAL_REG_NEG_VALOR"].abs()
        /
        agg["FAT_BRUTO_POS_MES"]
        * 100,
        0
    )


    agg["TAXA_DESCONTO_PCT"] = np.where(
        agg["FAT_BRUTO_POS_MES"] > 0,
        agg["TOTAL_DESCONTOS_POS"]
        /
        agg["FAT_BRUTO_POS_MES"]
        * 100,
        0
    )


    agg["PCT_QTD_REG_NEG"] = np.where(
        agg["QTD_TRANSACOES"] > 0,
        agg["QTD_REG_NEG"]
        /
        agg["QTD_TRANSACOES"]
        * 100,
        0
    )


    agg["PCT_QTD_ALTO_VALOR"] = np.where(
        agg["QTD_TRANSACOES"] > 0,
        agg["QTD_ALTO_VALOR"]
        /
        agg["QTD_TRANSACOES"]
        * 100,
        0
    )


    agg["PCT_INCONSIST_FINANCEIRA"] = np.where(
        agg["QTD_TRANSACOES"] > 0,
        agg["QTD_INCONSIST_FINANCEIRA"]
        /
        agg["QTD_TRANSACOES"]
        * 100,
        0
    )



    # Ordenação final para manter sequência temporal
    agg = (
        agg
        .sort_values(
            ["loja", "mes_referencia"]
        )
        .reset_index(drop=True)
    )



    # Converte Period para Timestamp,
    # garantindo compatibilidade com modelagem
    agg["mes_referencia"] = (
        agg["mes_referencia"]
        .dt.to_timestamp()
    )


    return agg