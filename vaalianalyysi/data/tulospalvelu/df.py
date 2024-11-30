import pandas as pd
from vaalianalyysi.data.tulospalvelu import dl


def tulokset_alueittain(vaalit: str) -> pd.DataFrame:
    """Vaalitulokset alueittain"""
    return _tulokset_csv(dl.tulokset_alueittain(vaalit), 0)


def tulokset_ehdokkaittain(vaalit: str) -> pd.DataFrame:
    """Vaalitulokset ehdokkaittain"""
    return _tulokset_csv(dl.tulokset_ehdokkaittain(vaalit), 2)


def ehdokasasettajakohtaiset_tulokset(vaalit: str) -> pd.DataFrame:
    """Ehdokasasettajakohtaiset tulokset"""
    return _tulokset_csv(dl.ehdokasasettajakohtaiset_tulokset(vaalit), 1)


def _tulokset_csv(csv_dl, wsn):
    """Oikeusministeriön tieto- ja tulospalvelun CSV"""
    head = dl.tulokset_otsikot().workbook()
    df = csv_dl.csv(
        sep=";",
        header=0,
        names=_first_row_of(head.worksheets[wsn]),
        index_col=False,
        encoding="ISO-8859-1",
        low_memory=False,
    )
    for col in df.columns.values:
        if isinstance(df[col].iloc[0], str):
            df[col] = df[col].str.rstrip()
    return df


def _first_row_of(worksheet):
    """Excel-tiedoston ensimmäinen rivi tyhjään soluun asti"""
    row = []
    cell = worksheet["A1"]
    while cell.value:
        row.append(cell.value)
        cell = cell.offset(0, 1)
    return row
