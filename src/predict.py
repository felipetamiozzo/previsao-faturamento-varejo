import numpy as np
import pandas as pd



# ============================================================
# FEATURES UTILIZADAS NA PREVISÃO
# ============================================================

# Mesmas variáveis utilizadas durante o treinamento do modelo.
# Mantém consistência entre treino e previsão.
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
# GERAÇÃO DAS PREVISÕES FUTURAS
# ============================================================

def gerar_previsoes(
    modelo,
    df_historico: pd.DataFrame,
    periodos,
    limite_taxa_crescimento: float = 1.2
):


    # Caso seja informado apenas a quantidade de meses,
    # cria automaticamente os próximos períodos futuros.
    if isinstance(periodos, int):

        ultima_data = (
            df_historico["mes_referencia"]
            .max()
        )


        periodos = pd.date_range(
            start=ultima_data + pd.DateOffset(months=1),
            periods=periodos,
            freq="MS"
        )



    # Lista que armazenará todas as previsões geradas
    previsoes = []


    # Obtém todas as lojas existentes na base histórica
    lojas = df_historico["loja"].unique()



    # ========================================================
    # PREVISÃO INDIVIDUAL POR LOJA
    # ========================================================

    for loja in lojas:


        # Filtra histórico da loja e organiza por data
        df_loja = (
            df_historico[
                df_historico["loja"] == loja
            ]
            .sort_values("mes_referencia")
            .copy()
        )



        # Geração mês a mês
        for data in periodos:


            # Utiliza a última informação disponível
            # como base para criar as novas features
            ultima_linha = (
                df_loja
                .iloc[-1:]
                .copy()
            )


            # Atualiza variáveis temporais
            ultima_linha["mes_referencia"] = data
            ultima_linha["ano"] = data.year
            ultima_linha["mes"] = data.month
            ultima_linha["trimestre"] = data.quarter


            # Incrementa o contador temporal
            ultima_linha["indice_tempo"] += 1



            # =================================================
            # CRIAÇÃO DAS FEATURES HISTÓRICAS
            # =================================================


            # Último faturamento conhecido
            ultimo_valor = (
                df_loja[
                    "faturamento_liquido_mensal"
                ]
                .iloc[-1]
            )


            # Valores dos meses anteriores
            ultima_linha["lag_1_mes"] = ultimo_valor


            ultima_linha["lag_2_meses"] = (
                df_loja["lag_1_mes"].iloc[-1]
                if len(df_loja) >= 2
                else ultimo_valor
            )


            ultima_linha["lag_3_meses"] = (
                df_loja["lag_2_meses"].iloc[-1]
                if len(df_loja) >= 3
                else ultimo_valor
            )



            # Média dos três últimos meses
            ultima_linha["media_movel_3m"] = (

                (
                    ultima_linha["lag_1_mes"]
                    +
                    ultima_linha["lag_2_meses"]
                    +
                    ultima_linha["lag_3_meses"]
                )
                .iloc[0]
                /
                3
            )



            # Calcula crescimento percentual recente
            if len(df_loja) > 1:

                ultima_linha["taxa_crescimento"] = (

                    (
                        ultima_linha["lag_1_mes"]
                        /
                        df_loja["lag_1_mes"].iloc[-1]
                        - 1
                    )
                    * 100

                ).iloc[0]

            else:

                ultima_linha["taxa_crescimento"] = 0



            # Variáveis para capturar sazonalidade
            ultima_linha["mes_seno"] = np.sin(
                2 * np.pi * data.month / 12
            )


            ultima_linha["mes_cosseno"] = np.cos(
                2 * np.pi * data.month / 12
            )



            # =================================================
            # PREDIÇÃO DO MODELO
            # =================================================

            # Seleciona apenas as features esperadas
            X_pred = ultima_linha[FEATURES]


            # Gera a previsão do Random Forest
            pred = modelo.predict(
                X_pred
            )[0]



            # =================================================
            # CONTROLE DE CRESCIMENTO
            # =================================================

            # Último valor real observado
            ultimo_real = (
                df_loja[
                    "faturamento_liquido_mensal"
                ]
                .iloc[-1]
            )


            # Limita crescimento máximo para evitar
            # previsões fora do cenário esperado.
            if pred > ultimo_real * limite_taxa_crescimento:

                pred = (
                    ultimo_real
                    *
                    limite_taxa_crescimento
                )



            # Armazena resultado da previsão
            previsoes.append({

                "loja": loja,

                "mes_referencia": data,

                "PREVISAO": pred

            })



            # =================================================
            # PREPARAÇÃO PARA O PRÓXIMO MÊS
            # =================================================

            # Adiciona a previsão gerada ao histórico da loja.
            #
            # Isso permite que previsões futuras utilizem
            # valores previstos como histórico (previsão iterativa).
            nova_linha = ultima_linha.copy()


            nova_linha[
                "faturamento_liquido_mensal"
            ] = pred


            df_loja = pd.concat(
                [
                    df_loja,
                    nova_linha
                ],
                ignore_index=True
            )



    # Retorna DataFrame final com todas as previsões
    return pd.DataFrame(
        previsoes
    )