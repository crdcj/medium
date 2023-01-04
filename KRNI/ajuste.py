import pandas as pd


def ajustar_datas(
    datas_evento: pd.Series, datas_negociacao: pd.Series, posterior: bool = False
) -> pd.Series:
    """Ajusta cada data de evento para a primeira data igual ou anterior de negociação
    Parâmetros:
        datas_evento: serie com as datas a serem ajustadas
        datas_negociacao: serie com as datas de negociação do ativo
        posterior: se True, ajusta para a primeira data igual ou posterior de negociação


    Retorno:
        Serie com as datas dos eventos ajustadas para datas válidas de negociação
    """
    if posterior:
        return datas_evento.apply(
            lambda x: datas_negociacao[datas_negociacao >= x].min()
        )
    else:
        return datas_evento.apply(
            lambda x: datas_negociacao[datas_negociacao <= x].max()
        )
