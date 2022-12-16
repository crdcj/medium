import pandas as pd


def ajustar_precos(df_precos: pd.DataFrame, df_divs: pd.DataFrame) -> pd.DataFrame:
    """Insere as colunas "preco_aj" "valor_div" contendo o preço ajustado e o
    valor do dividendo declarado. O preço é ajustado para trás, sendo que a
    data_com do dividendo é a data base, data anterior à data ex-dividendo.

    Parâmetros:
        df_precos: dataFrame com as colunas "data" e "preco" do ativo
        df_divs: dataFrame com as colunas "data_com" e "valor_div"

    Retorno:
        dataFrame com as colunas originais de "df_precos" mais as colunas "preco_aj"
        e "valor_div"
    """
    # Ajustar as datas de dividendos para que a data tenha tido necessariamente negociação
    df_divs["data_com"] = df_divs["data_com"].apply(
        lambda x: df_precos.query("data <= @x")["data"].max()
    )
    # Incorporar os dados de dividendos em df_precos
    df_precos = df_precos.merge(
        df_divs, how="left", left_on="data", right_on="data_com"
    )
    # A coluna "data_com" não é mais necessária
    df_precos.drop(columns="data_com", inplace=True)
    # Calcular o fator de ajuste
    df_precos["ajuste"] = 1 - df_precos["valor_div"] / df_precos["preco"]
    # Preencher os valores faltantes com 1 para o cálculo do acumulado
    df_precos["ajuste"] = df_precos["ajuste"].fillna(1)
    # Ordenar as datas da mais nova p/ a mais antiga -> preço inalterado na data mais recente
    df_precos.sort_values("data", ascending=False, ignore_index=True, inplace=True)
    # Calcular o acumulado do fator de ajuste
    df_precos["ajuste_acum"] = df_precos["ajuste"].cumprod()
    # Ajustar o preço do ativo
    df_precos["preco_aj"] = df_precos["preco"] * df_precos["ajuste_acum"]
    # Remover colunas criadas para o cálculo do ajuste
    df_precos.drop(columns=["ajuste", "ajuste_acum"], inplace=True)
    # Voltar a ordenar as datas da mais antiga p/ a mais nova
    # Mover a coluna "valor_div" para a última posição
    cols = df_precos.columns.tolist()
    cols.remove("valor_div")
    cols.append("valor_div")
    df_precos = df_precos[cols]
    df_precos.sort_values("data", ascending=True, ignore_index=True, inplace=True)
    return df_precos
