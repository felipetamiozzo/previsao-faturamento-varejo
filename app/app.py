# ============================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

# Manipulação de caminhos de arquivos
import os

# Carregamento do modelo treinado salvo em arquivo .pkl
import joblib

# Manipulação e tratamento de dados
import pandas as pd

# Framework utilizado para criação da aplicação web interativa
import streamlit as st

# Biblioteca para criação dos gráficos interativos
import plotly.express as px


# ============================================================
# CONFIGURAÇÃO INICIAL DA APLICAÇÃO STREAMLIT
# ============================================================

# Define configurações gerais da página:
# - título exibido no navegador
# - ícone da aplicação
# - layout utilizando toda largura disponível
# - sidebar aberta inicialmente
st.set_page_config(
    page_title="Sistema de Previsão de Faturamento",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Título principal da aplicação
st.title("📈 Sistema de Previsão de Faturamento")


# Apresentação do objetivo do projeto e principais resultados
# obtidos pelo modelo final
st.markdown(
    """
    Aplicação desenvolvida para previsão de faturamento mensal utilizando
    **Machine Learning (Random Forest Regressor)**.

    **Desempenho do modelo**
    - 🎯 MAPE: **11,20%**
    - 📅 Horizonte de previsão: **3 meses**
    """
)


# Linha divisória visual
st.divider()



# ============================================================
# DEFINIÇÃO DOS CAMINHOS DOS ARQUIVOS DO PROJETO
# ============================================================


# Identifica automaticamente o diretório raiz do projeto.
# Isso evita depender de caminhos absolutos da máquina.
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# Caminho do modelo treinado pelo notebook de modelagem
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "rf_model.pkl"
)


# Caminho da base histórica mensal utilizada para gráficos
# e filtros da aplicação
HISTORICAL_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sample",
    "df_mensal.csv"
)


# Caminho contendo as previsões futuras geradas pelo pipeline
PREDICTIONS_PATH = os.path.join(
    BASE_DIR,
    "data",
    "sample",
    "previsoes_futuras.csv"
)


# Caminho da imagem gerada com a importância das variáveis
# utilizadas pelo modelo Random Forest
FEATURE_IMPORTANCE_PATH = os.path.join(
    BASE_DIR,
    "outputs",
    "feature_importance.png"
)



# ============================================================
# FUNÇÕES DE CARREGAMENTO
# ============================================================


# Cache de recurso:
# Mantém o modelo carregado na memória para evitar
# recarregar o arquivo a cada interação do usuário.
@st.cache_resource
def load_model():

    return joblib.load(MODEL_PATH)



# Cache de dados:
# Carrega a base histórica mensal e realiza ajustes necessários.
@st.cache_data
def load_historical_data():

    # Leitura da base consolidada mensal
    df = pd.read_csv(HISTORICAL_PATH)


    # Conversão da coluna de referência para formato de data
    # permitindo filtros e gráficos temporais
    df["mes_referencia"] = pd.to_datetime(
        df["mes_referencia"]
    )


    return df



# Carrega as previsões futuras geradas pelo modelo
@st.cache_data
def load_predictions():

    pred = pd.read_csv(PREDICTIONS_PATH)


    # Conversão da data para formato temporal
    pred["mes_referencia"] = pd.to_datetime(
        pred["mes_referencia"]
    )


    return pred



# ============================================================
# CARREGAMENTO DOS ARQUIVOS PRINCIPAIS
# ============================================================


# Bloco de segurança:
# tenta carregar modelo e bases.
# Caso algum arquivo esteja ausente, informa o erro
# ao usuário ao invés de quebrar a aplicação.
try:

    model = load_model()

    df_hist = load_historical_data()

    df_pred = load_predictions()


except Exception as erro:


    st.error(
        f"""
        Não foi possível carregar os arquivos do projeto.

        Verifique se os modelos e bases estão nas pastas corretas.

        Erro encontrado:
        {erro}
        """
    )


    # Interrompe a execução caso os arquivos essenciais
    # não estejam disponíveis
    st.stop()



# ============================================================
# SIDEBAR - FILTROS DA APLICAÇÃO
# ============================================================


st.sidebar.header("⚙️ Filtros")


# Lista todas as lojas disponíveis para seleção
lojas = sorted(
    df_hist["loja"].unique()
) if not df_hist.empty else []


# Cria um filtro interativo para selecionar uma loja
loja_selecionada = (
    st.sidebar.selectbox(
        "Selecione a Loja",
        options=lojas
    )
    if len(lojas) > 0
    else None
)



st.sidebar.markdown("---")


# Informações gerais do projeto exibidas na barra lateral
st.sidebar.info(
    """
    **Projeto de Machine Learning**

    Modelo: Random Forest Regressor

    Horizonte de previsão: 3 meses
    """
)



# ============================================================
# INDICADORES PRINCIPAIS DAS PREVISÕES
# ============================================================


# Caso existam previsões disponíveis,
# calcula o faturamento total previsto por mês
if not df_pred.empty:


    consolidado = (
        df_pred
        .groupby("mes_referencia")["PREVISAO"]
        .sum()
        .reset_index()
    )


    # Cria três cartões KPI para os meses previstos
    col1, col2, col3 = st.columns(3)


    for coluna, (_, linha) in zip(
        [col1, col2, col3],
        consolidado.iterrows()
    ):


        coluna.metric(
            linha["mes_referencia"]
            .strftime("%B/%Y")
            .capitalize(),

            f"R$ {linha['PREVISAO']/1e6:.1f} M"
        )



st.divider()



# ============================================================
# CRIAÇÃO DAS ABAS PRINCIPAIS
# ============================================================


# Organização da aplicação em quatro áreas:
# 1 - Previsões futuras
# 2 - Histórico financeiro
# 3 - Métricas dos modelos
# 4 - Explicabilidade do modelo
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📈 Previsões",
        "📊 Histórico",
        "🤖 Modelos",
        "📌 Importância das Variáveis"
    ]
)

# ============================================================
# ABA 1 - PREVISÕES FUTURAS
# ============================================================

# Área responsável por apresentar:
# - previsão consolidada dos próximos meses
# - previsão individual por loja
# - tabela detalhada das previsões

with tab1:


    st.subheader(
        "Previsão Consolidada"
    )


    # Verifica se existem previsões geradas
    if not df_pred.empty:


        # Soma todas as previsões das lojas
        # para obter o faturamento total previsto por mês
        pred_cons = (
            df_pred
            .groupby("mes_referencia")["PREVISAO"]
            .sum()
            .reset_index()
        )


        # Criação do gráfico de linha
        # mostrando evolução do faturamento previsto
        fig = px.line(

            pred_cons,

            x="mes_referencia",

            y="PREVISAO",

            markers=True
        )



        fig.update_layout(

            title="Previsão de Faturamento",

            xaxis_title="Mês",

            yaxis_title="Faturamento (R$)"

        )



        # Formatação do eixo Y para moeda
        fig.update_yaxes(

            tickprefix="R$ ",

            tickformat=",.0f"

        )


        # Formatação do eixo X para mês/ano
        fig.update_xaxes(

            tickformat="%b/%Y"

        )


        # Exibe o gráfico na aplicação
        st.plotly_chart(

            fig,

            width="stretch"

        )



        # ----------------------------------------------------
        # PREVISÃO POR LOJA
        # ----------------------------------------------------

        st.subheader(
            "Previsões por Loja"
        )



        # Caso uma loja tenha sido selecionada,
        # mostra apenas suas previsões.
        #
        # Caso contrário, mostra todas as lojas.
        if loja_selecionada:


            tabela = df_pred[
                df_pred["loja"] == loja_selecionada
            ]


        else:


            tabela = df_pred



        # Exibe tabela de previsões
        st.dataframe(

            tabela.style.format(

                {
                    "PREVISAO": "R$ {:,.0f}"
                }

            ),

            width="stretch"

        )



        # ----------------------------------------------------
        # GRÁFICO INDIVIDUAL DA LOJA
        # ----------------------------------------------------

        # Só aparece quando uma loja é selecionada
        if loja_selecionada:


            st.subheader(

                f"Previsão da Loja Selecionada - {loja_selecionada}"

            )



            # Consolida previsão mensal da loja escolhida
            pred_loja = (

                tabela

                .groupby("mes_referencia")["PREVISAO"]

                .sum()

                .reset_index()

            )



            # Cria gráfico específico da loja
            fig_loja = px.line(

                pred_loja,

                x="mes_referencia",

                y="PREVISAO",

                markers=True

            )



            fig_loja.update_layout(

                title=f"Previsão de Faturamento - {loja_selecionada}",

                xaxis_title="Mês",

                yaxis_title="Faturamento (R$)"

            )



            fig_loja.update_yaxes(

                tickprefix="R$ ",

                tickformat=",.0f"

            )



            fig_loja.update_xaxes(

                tickformat="%b/%Y"

            )



            # Adiciona valores acima dos pontos do gráfico
            fig_loja.update_traces(

                text=[

                    f"R$ {v/1e6:.2f} M"

                    for v in pred_loja["PREVISAO"]

                ],

                textposition="top center"

            )



            st.plotly_chart(

                fig_loja,

                width="stretch"

            )



    else:


        # Mensagem caso o arquivo de previsão
        # não tenha dados disponíveis
        st.info(

            "Nenhuma previsão encontrada."

        )



# ============================================================
# ABA 2 - HISTÓRICO DE FATURAMENTO
# ============================================================

# Apresenta o comportamento histórico
# do faturamento líquido mensal por loja.

with tab2:


    st.subheader(

        "Histórico de Faturamento"

    )



    # Necessário selecionar uma loja
    # para visualizar o histórico individual
    if loja_selecionada:



        # Filtra dados históricos da loja escolhida
        df_loja = df_hist[

            df_hist["loja"] == loja_selecionada

        ]



        # Gráfico da evolução histórica
        fig = px.line(

            df_loja,

            x="mes_referencia",

            y="faturamento_liquido_mensal",

            markers=True

        )



        fig.update_layout(

            title=f"Histórico - {loja_selecionada}",

            xaxis_title="Mês",

            yaxis_title="Faturamento"

        )



        fig.update_yaxes(

            tickprefix="R$ ",

            tickformat=",.0f"

        )



        st.plotly_chart(

            fig,

            width="stretch"

        )



    else:


        st.warning(

            "Selecione uma loja."

        )
        
# ============================================================
# ABA 3 - DESEMPENHO DOS MODELOS
# ============================================================

# Apresenta as métricas utilizadas para avaliar
# o desempenho do modelo final e comparação
# com os demais algoritmos testados.

with tab3:


    st.subheader(
        "Desempenho dos Modelos"
    )


    # Criação dos cartões com as principais métricas
    # do modelo escolhido (Random Forest Base)
    c1, c2, c3, c4 = st.columns(4)



    c1.metric(
        "MAPE",
        "11,20%"
    )


    c2.metric(
        "WMAPE",
        "8,63%"
    )


    c3.metric(
        "MAE",
        "R$ 1.046.032"
    )


    c4.metric(
        "RMSE",
        "R$ 1.544.294"
    )



    st.markdown(
        "### Comparação entre Modelos"
    )



    # DataFrame contendo os resultados
    # dos modelos avaliados durante a modelagem
    metrics_df = pd.DataFrame({

        "Modelo": [

            "Baseline MM3",

            "Random Forest Base",

            "Random Forest Tunado",

            "XGBoost"

        ],

        "MAPE (%)": [

            14.75,

            11.20,

            11.87,

            12.28

        ]

    })



    # Gráfico comparativo do erro percentual
    # entre os modelos testados
    fig = px.bar(

        metrics_df,

        x="Modelo",

        y="MAPE (%)",

        text="MAPE (%)"

    )



    # Configuração dos valores exibidos
    # acima das barras
    fig.update_traces(

        texttemplate="%{text:.2f}%",

        textposition="outside"

    )



    fig.update_layout(

        showlegend=False,

        yaxis_title="MAPE (%)"

    )



    # Exibe gráfico comparativo
    st.plotly_chart(

        fig,

        width="stretch"

    )





# ============================================================
# ABA 4 - IMPORTÂNCIA DAS VARIÁVEIS
# ============================================================

# Apresenta a interpretação do modelo,
# mostrando quais variáveis tiveram maior influência
# nas previsões do Random Forest.

with tab4:


    st.subheader(
        "Importância das Variáveis"
    )


    # Importação realizada apenas quando
    # essa aba é carregada.
    # Evita carregar recursos desnecessários.
    from PIL import Image



    # Verifica se o arquivo de importância
    # das variáveis foi gerado pelo pipeline
    if os.path.exists(
        FEATURE_IMPORTANCE_PATH
    ):



        try:


            # Carrega a imagem criada na etapa
            # de análise do modelo
            img = Image.open(

                FEATURE_IMPORTANCE_PATH

            )



            # Exibe o gráfico dentro do Streamlit
            st.image(

                img,

                width="stretch"

            )



        except Exception as erro:


            # Captura possíveis problemas
            # na leitura da imagem
            st.error(

                f"Erro ao carregar a imagem: {erro}"

            )



    else:


        # Mensagem caso a etapa de feature importance
        # ainda não tenha gerado o arquivo
        st.info(

            "Arquivo feature_importance.png não encontrado."

        )