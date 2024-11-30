from vaalianalyysi.data.download import Download


def tulokset_otsikot() -> Download:
    """Tulosten otsikkotiedosto"""
    path = "csv_otsikot/Tulokset_otsikkorivit_FI.xlsx"
    return _cached(path)


def tulokset_alueittain(vaalit: str) -> Download:
    """Vaalitulokset alueittain"""
    dirname = vaalit.upper()
    prefix = vaalit.lower()
    path = f"{dirname}/{prefix}_taat_maa.csv"
    url = f"{dirname}/{prefix}_alu_maa.csv.zip"
    chk = f"{dirname}/{prefix}_alu_maa.csv.chk"
    return _cached(path, url, chk)


def tulokset_ehdokkaittain(vaalit: str) -> Download:
    """Vaalitulokset ehdokkaittain"""
    dirname = vaalit.upper()
    prefix = vaalit.lower()
    path = f"{dirname}/{prefix}_teat_maa.csv"
    url = f"{dirname}/{prefix}_ehd_maa.csv.zip"
    chk = f"{dirname}/{prefix}_ehd_maa.csv.chk"
    return _cached(path, url, chk)


def ehdokasasettajakohtaiset_tulokset(vaalit: str) -> Download:
    """Ehdokasasettajakohtaiset tulokset"""
    dirname = vaalit.upper()
    prefix = vaalit.lower()
    path = f"{dirname}/{prefix}_tpat_maa.csv"
    url = f"{dirname}/{prefix}_puo_maa.csv.zip"
    chk = f"{dirname}/{prefix}_puo_maa.csv.chk"
    return _cached(path, url, chk)


_CACHE = {}


def _mkdl(path, url=None, chk=None):
    return Download(
        f"tulospalvelu.vaalit.fi/{path}",
        f"https://tulospalvelu.vaalit.fi/{url or path}",
        f"https://tulospalvelu.vaalit.fi/{chk}" if chk else None,
    )


def _cached(path, url=None, chk=None):
    if path not in _CACHE:
        _CACHE[path] = _mkdl(path, url, chk)
    return _CACHE[path]
