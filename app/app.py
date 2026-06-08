import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Configuração da página
st.set_page_config(page_title="Previsão de Faturamento", layout="wide")
st.title("📊 Solução Casting - Previsão de Faturamento")
st.markdown("Modelo Random Forest | MAPE 11,16% | Horizonte 3 meses")

# Caminhos relativos (app.py está dentro da pasta app/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # sobe um nível

@st.cache_resource
def load_model():
    path = os.path.join(BASE_DIR, 'models', 'rf_base_model.pkl')
    return joblib.load(path)

@st.cache_data
def load_historical_data():
    path = os.path.join(BASE_DIR, 'data', 'processed', 'df_mensal.csv')
    df = pd.read_csv(path)
    df['PERIODO_MES'] = pd.to_datetime(df['PERIODO_MES'])
    return df

@st.cache_data
def load_predictions():
    path = os.path.join(BASE_DIR, 'data', 'processed', 'previsoes_futuras.csv')
    pred = pd.read_csv(path)
    pred['PERIODO_MES'] = pd.to_datetime(pred['PERIODO_MES'])
    return pred

try:
    model = load_model()
    df_hist = load_historical_data()
    df_pred = load_predictions()
except Exception as e:
    st.warning(f"Arquivos não encontrados. Usando dados simulados para demonstração. Erro: {e}")
    df_hist = pd.DataFrame()
    df_pred = pd.DataFrame()

# Sidebar - seleção de loja
st.sidebar.header("Filtros")
lojas = df_hist['CLV_BANCO'].unique() if not df_hist.empty else []
if len(lojas) > 0:
    loja_selecionada = st.sidebar.selectbox("Selecione a Loja", lojas)
else:
    loja_selecionada = None

# Abas
tab1, tab2, tab3 = st.tabs(["📈 Previsão Futura", "📊 Histórico vs Previsto", "📋 Métricas do Modelo"])

with tab1:
    st.header("Previsão dos Próximos 3 Meses")
    if not df_pred.empty:
        # Gráfico consolidado
        pred_cons = df_pred.groupby('PERIODO_MES')['PREVISAO'].sum().reset_index()
        fig = px.line(pred_cons, x='PERIODO_MES', y='PREVISAO', 
                      markers=True, title="Faturamento Previsto - Consolidado")
        fig.update_layout(yaxis_title="Faturamento (R$)", xaxis_title="Mês")
        fig.update_xaxes(tickformat="%b %Y", tickmode="array", tickvals=pred_cons['PERIODO_MES'])
        fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
        fig.update_traces(text=pred_cons['PREVISAO'].apply(lambda x: f'R$ {x/1e6:.1f}M'), textposition="top center")
        st.plotly_chart(fig, use_container_width=True)

        # Tabela filtrada pela loja selecionada
        st.subheader("Valores Previstos por Loja")
        if loja_selecionada:
            df_pred_filtrado = df_pred[df_pred['CLV_BANCO'] == loja_selecionada]
        else:
            df_pred_filtrado = df_pred
        st.dataframe(df_pred_filtrado.style.format({'PREVISAO': 'R$ {:,.0f}'}))
    else:
        st.info("Carregue as previsões futuras para visualizar.")

with tab2:
    st.header("Desempenho do Modelo - Histórico")
    if loja_selecionada and not df_hist.empty:
        df_loja = df_hist[df_hist['CLV_BANCO'] == loja_selecionada].copy()
        fig = px.line(df_loja, x='PERIODO_MES', y='FAT_LIQUIDO_MES',
                      title=f'Histórico de Faturamento - {loja_selecionada}',
                      markers=True)
        fig.update_layout(yaxis_title="Faturamento (R$)", xaxis_title="Mês")
        fig.update_yaxes(tickprefix="R$ ", tickformat=",.0f")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Selecione uma loja no menu lateral.")

with tab3:
    st.header("Métricas do Modelo (Validação Temporal)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("MAPE", "11,16%", "-3,59% vs Baseline")
    col2.metric("WMAPE", "8,57%", "-6,28% vs Baseline")
    col3.metric("MAE", "R$ 1.038.660", "-42% vs Baseline")
    col4.metric("RMSE", "R$ 1.540.806", "")
    
    st.subheader("Comparação de Modelos")
    metrics_df = pd.DataFrame({
        'Modelo': ['Baseline MM3', 'Regressão Linear', 'Random Forest Base', 'Random Forest Tunado', 'XGBoost'],
        'MAPE (%)': [14.75, 253.01, 11.16, 11.73, 13.72]
    })
    fig = px.bar(metrics_df, x='Modelo', y='MAPE (%)', color='Modelo', 
                 title="MAPE por Modelo", text='MAPE (%)')
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(showlegend=False, yaxis_title="MAPE (%)", xaxis_title="Modelo")
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Grupo 1 - Desenvolvido para a Solução Casting | Projeto DNC")