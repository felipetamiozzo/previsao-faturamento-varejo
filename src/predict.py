import pandas as pd
import numpy as np

def gerar_previsoes(modelo, df_historico: pd.DataFrame, periodos, limite_crescimento: float = 1.2) -> pd.DataFrame:
    """
    Gera previsões recursivas para múltiplos períodos.
    
    Parâmetros:
    - modelo: modelo sklearn compatível (com .predict)
    - df_historico: DataFrame histórico completo (já com features)
    - periodos: lista de datas ou número de períodos
    - limite_crescimento: fator máximo de crescimento mensal (ex: 1.2 = 20%)
    """
    from copy import deepcopy
    
    if isinstance(periodos, int):
        # Gerar datas automaticamente (ex: 3 meses à frente)
        ultima_data = df_historico['PERIODO_MES'].max()
        periodos = pd.date_range(start=ultima_data + pd.DateOffset(months=1), periods=periodos, freq='MS')
    
    lojas = df_historico['CLV_BANCO'].unique()
    previsoes = []
    
    for loja in lojas:
        # Dados históricos da loja (já com features)
        df_loja = df_historico[df_historico['CLV_BANCO'] == loja].sort_values('PERIODO_MES').copy()
        
        # Para cada período futuro
        for data in periodos:
            # Última linha disponível (real ou prevista)
            ultima_linha = df_loja.iloc[-1:].copy()
            
            # Atualizar período e features temporais
            ultima_linha['PERIODO_MES'] = data
            ultima_linha['ANO'] = data.year
            ultima_linha['MES_NUM'] = data.month
            ultima_linha['TRIMESTRE'] = data.quarter
            ultima_linha['INDICE_TEMPO'] = ultima_linha['INDICE_TEMPO'].iloc[0] + 1
            
            # Atualizar lags: LAG_1 = último valor real/previsto
            # LAG_2 = LAG_1 anterior, etc.
            # Para simplificar, vamos usar os valores reais/previstos da própria loja
            # (A implementação completa exige shift manual)
            
            # Solução mais simples: usar valores conhecidos do histórico + previsões anteriores
            # Vamos simular usando o último valor previsto ou real
            ultimo_valor = df_loja['FAT_LIQUIDO_MES'].iloc[-1]
            ultima_linha['LAG_1'] = ultimo_valor
            ultima_linha['LAG_2'] = df_loja['LAG_1'].iloc[-1] if len(df_loja) >= 2 else ultimo_valor
            ultima_linha['LAG_3'] = df_loja['LAG_2'].iloc[-1] if len(df_loja) >= 3 else ultimo_valor
            
            # Média móvel 3
            ultima_linha['MEDIA_MOVEL_3'] = (ultima_linha['LAG_1'] + ultima_linha['LAG_2'] + ultima_linha['LAG_3']).iloc[0] / 3
            
            # Crescimento
            ultima_linha['CRESCIMENTO'] = ((ultima_linha['LAG_1'] / df_loja['LAG_1'].iloc[-1] - 1) * 100).iloc[0] if len(df_loja) > 1 else 0
            
            # Sazonalidade cíclica
            ultima_linha['MES_SENO'] = np.sin(2 * np.pi * data.month / 12)
            ultima_linha['MES_COSSENO'] = np.cos(2 * np.pi * data.month / 12)
            
            # Selecionar features
            features = ['CLV_BANCO', 'ANO', 'MES_NUM', 'TRIMESTRE', 'INDICE_TEMPO',
                        'LAG_1', 'LAG_2', 'LAG_3', 'MEDIA_MOVEL_3', 'CRESCIMENTO',
                        'MES_SENO', 'MES_COSSENO']
            X_pred = ultima_linha[features]
            
            # Previsão
            pred = modelo.predict(X_pred)[0]
            
            # Aplicar limite de crescimento
            if len(df_loja) > 0:
                ultimo_real = df_loja['FAT_LIQUIDO_MES'].iloc[-1]
                if pred > ultimo_real * limite_crescimento:
                    pred = ultimo_real * limite_crescimento
            
            # Armazenar
            previsoes.append({
                'CLV_BANCO': loja,
                'PERIODO_MES': data,
                'PREVISAO': pred
            })
            
            # Adicionar linha prevista ao DataFrame para os próximos lags
            nova_linha = ultima_linha.copy()
            nova_linha['FAT_LIQUIDO_MES'] = pred
            df_loja = pd.concat([df_loja, nova_linha], ignore_index=True)
    
    return pd.DataFrame(previsoes)