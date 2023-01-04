import pandas as pd


def ajustar_datas(
    datas_evento: pd.Series, datas_negociacao: pd.Series, anterior: bool = True
) -> pd.Series:
    """Ajusta cada data de evento para que necessariamente ocorra em uma data com negociação
    Parâmetros:
        datas_evento: serie com as datas a serem ajustadas
        datas_negociacao: serie com as datas de negociação do ativo
        anterior: se "True" (default), ajusta para a primeira data igual ou anterior à de negociação
                  se "False", ajusta para a primeira data igual ou posterior à de negociação



    Retorno:
        Serie com as datas dos eventos ajustadas para datas válidas de negociação
    """
    if anterior:
        return datas_evento.apply(
            lambda x: datas_negociacao[datas_negociacao <= x].max()
        )

    else:
        return datas_evento.apply(
            lambda x: datas_negociacao[datas_negociacao >= x].min()
        )
