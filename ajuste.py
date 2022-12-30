import pandas as pd


def ajustar_precos(df_precos: pd.DataFrame, df_divs: pd.DataFrame) -> pd.DataFrame:
    """Insere as colunas "preco_aj" "valor_div" contendo o preço ajustado e o
    valor do dividendo declarado. O preço é ajustado para trás, sendo que a
    data_com do dividendo é a data base, data anterior à data ex-dividendo.

    Parâmetros:
        precos: dataFrame com as colunas "data" e "preco" do ativo
        divs: dataFrame com as colunas "data_com" e "valor_div"

    Retorno:
        dataFrame com as colunas originais de "precos" mais as colunas "preco_aj"
        e "valor_div"
    """
    # Copiar os dataFrames para não alterar os originais
    precos = df_precos.copy()
    divs = df_divs[["data_com", "valor_div"]].copy()

    # Ajustar as datas de dividendos para que a data tenha tido necessariamente negociação
    divs["data_com"] = divs["data_com"].apply(
        lambda x: precos.query("data <= @x")["data"].max()
    )
    # Agrupar dividendos na mesma data e somar os valores
    divs = divs.groupby("data_com", as_index=False).sum().reset_index(drop=True)
    # Incorporar os dados de dividendos em precos
    precos = precos.merge(divs, how="left", left_on="data", right_on="data_com")
    # A coluna "data_com" não é mais necessária
    precos.drop(columns="data_com", inplace=True)
    # Calcular o fator de ajuste
    precos["ajuste"] = 1 - precos["valor_div"] / precos["preco"]
    # Preencher os valores faltantes com 1 para o cálculo do acumulado
    precos["ajuste"] = precos["ajuste"].fillna(1)
    # Ordenar as datas da mais nova p/ a mais antiga -> preço inalterado na data mais recente
    precos.sort_values("data", ascending=False, ignore_index=True, inplace=True)
    # Calcular o acumulado do fator de ajuste
    precos["ajuste_acum"] = precos["ajuste"].cumprod()
    # Ajustar o preço do ativo
    precos["preco_aj"] = precos["preco"] * precos["ajuste_acum"]
    # Remover colunas criadas para o cálculo do ajuste
    precos.drop(columns=["ajuste", "ajuste_acum"], inplace=True)
    # Voltar a ordenar as datas da mais antiga p/ a mais nova
    # Mover a coluna "valor_div" para a última posição
    cols = precos.columns.tolist()
    cols.remove("valor_div")
    cols.append("valor_div")
    precos = precos[cols]
    precos.sort_values("data", ascending=True, ignore_index=True, inplace=True)
    return precos
