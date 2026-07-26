from pathlib import Path


# Importa configurações de caminhos do projeto
from src.config import (
    RAW_DIR,
    PROCESSED_DIR,
    MODELS_DIR
)



# Importa funções de carregamento,
# tratamento e agregação dos dados
from src.data_cleaning import (
    carregar_dados_brutos,
    tratar_dados,
    agregar_mensal
)



# Importa criação das variáveis para o modelo
from src.features import criar_features



# Importa treinamento e salvamento do modelo
from src.model import (
    treinar_modelo,
    salvar_modelo
)



# Importa função responsável pelas previsões futuras
from src.predict import gerar_previsoes




# ============================================================
# PIPELINE PRINCIPAL
# ============================================================

def main():


    print("=" * 70)

    print(
        "INICIANDO PIPELINE DE PREVISÃO DE FATURAMENTO"
    )

    print("=" * 70)



    # ========================================================
    # PREPARAÇÃO DOS DIRETÓRIOS
    # ========================================================

    # Cria pastas necessárias caso ainda não existam
    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )


    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )



    # ========================================================
    # 1) CARREGAMENTO DOS DADOS BRUTOS
    # ========================================================

    print(
        "\n1) Carregando dados..."
    )


    # Lê todos os arquivos CSV da pasta raw
    df_bruto = carregar_dados_brutos(
        RAW_DIR
    )


    print(
        f"Registros carregados: {len(df_bruto):,}"
    )


    print(
        df_bruto.columns.tolist()
    )



    # ========================================================
    # 2) TRATAMENTO DOS DADOS
    # ========================================================

    print(
        "\n2) Tratando dados..."
    )


    # Aplica limpeza, criação de flags
    # e variáveis temporais
    df_tratado = tratar_dados(
        df_bruto
    )


    # Salva base tratada para auditoria
    df_tratado.to_csv(
        PROCESSED_DIR / "df_tratado.csv",
        index=False
    )



    # ========================================================
    # 3) AGREGAÇÃO MENSAL
    # ========================================================

    print(
        "\n3) Agregando base mensal..."
    )


    # Consolida transações em nível:
    # mês + loja
    df_mensal = agregar_mensal(
        df_tratado
    )


    # Salva base mensal utilizada no projeto
    df_mensal.to_csv(
        PROCESSED_DIR / "df_mensal.csv",
        index=False
    )



    # ========================================================
    # 4) FEATURE ENGINEERING
    # ========================================================

    print(
        "\n4) Criando features..."
    )


    # Criação das variáveis utilizadas
    # pelo modelo de Machine Learning
    df_features = criar_features(
        df_mensal
    )


    # Salva base final para modelagem
    df_features.to_csv(
        PROCESSED_DIR / "df_features.csv",
        index=False
    )



    # ========================================================
    # 5) TREINAMENTO DO MODELO
    # ========================================================

    print(
        "\n5) Treinando Random Forest..."
    )


    # Treina o modelo utilizando as features criadas
    modelo = treinar_modelo(
        df_features
    )


    # Salva o pipeline completo:
    # pré-processamento + modelo treinado
    salvar_modelo(
        modelo,
        MODELS_DIR / "rf_model.pkl"
    )



    # ========================================================
    # 6) GERAÇÃO DAS PREVISÕES FUTURAS
    # ========================================================

    print(
        "\n6) Gerando previsões..."
    )


    # Gera previsão dos próximos 3 meses
    previsoes = gerar_previsoes(
        modelo=modelo,

        df_historico=df_features,

        periodos=3
    )


    # Salva previsões finais
    previsoes.to_csv(
        PROCESSED_DIR / "previsoes_futuras.csv",

        index=False
    )



    print(
        "\nPipeline executado com sucesso!"
    )


    print("=" * 70)




# Executa o pipeline somente quando
# este arquivo for chamado diretamente
if __name__ == "__main__":

    main()