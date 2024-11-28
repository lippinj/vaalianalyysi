import dataclasses
from vaalianalyysi.data.tulospalvelu import df


@dataclasses.dataclass
class Puolue:
    """Puolueen metadata"""

    tunniste: str
    nimilyhenne_suomeksi: str


@dataclasses.dataclass
class Kunta:
    """Kunnan metadata"""

    kuntanro: str
    nimi_suomeksi: str
    n: int


@dataclasses.dataclass
class Alue:
    """Kunnan äänestysalueen metadata"""

    kuntanro: str
    aluetunnus: str
    nimi_suomeksi: str
    n: int


class Vaalit:
    """Yhden vaalin kaikki tiedot"""

    def __init__(self, vaalit):
        """Vaalitiedot"""
        self.vaalit = vaalit
        self.tulokset_ehdokkaittain = df.tulokset_ehdokkaittain(vaalit)
        self.tulokset_alueittain = df.tulokset_alueittain(vaalit)
        self._cached_puolueet = None
        self._cached_kunnat = None
        self._cached_alueet = None

    @property
    def puolueet(self):
        """Puoluetunniste -> puoluetiedot"""
        if self._cached_puolueet is None:
            self._compute_puolueet()
        return self._cached_puolueet

    @property
    def kunnat(self):
        """Kuntanro -> kuntatiedot"""
        if self._cached_kunnat is None:
            self._compute_kunnat()
        return self._cached_kunnat

    @property
    def alueet(self):
        """Kuntanro-aluetunnus -> aluetiedot"""
        if self._cached_alueet is None:
            self._compute_alueet()
        return self._cached_alueet

    def _compute_puolueet(self):
        out = {}
        d = self.tulokset_ehdokkaittain
        d = d[[d.columns[7], d.columns[11]]].drop_duplicates()
        for _, row in d.iterrows():
            tunniste = row[d.columns[0]]
            lyhenne = row[d.columns[1]]
            out[tunniste] = Puolue(tunniste, lyhenne)
        self._cached_puolueet = out

    def _compute_kunnat(self):
        out = {}
        d = self.tulokset_alueittain
        d = d[d[d.columns[3]] == "K"]
        d = d[[d.columns[2], d.columns[9], d.columns[13]]].drop_duplicates()
        for _, row in d.iterrows():
            kuntanro = row[d.columns[0]]
            nimi = row[d.columns[1]]
            luku = row[d.columns[2]]
            out[kuntanro] = Kunta(kuntanro, nimi, luku)
        self._cached_kunnat = out

    def _compute_alueet(self):
        out = {}
        d = self.tulokset_alueittain
        d = d[d[d.columns[3]] == "A"]
        d = d[
            [d.columns[2], d.columns[4], d.columns[9], d.columns[13]]
        ].drop_duplicates()
        for _, row in d.iterrows():
            kuntanro = row[d.columns[0]]
            aluetunnus = row[d.columns[1]]
            nimi = row[d.columns[2]]
            luku = row[d.columns[3]]
            out[f"{kuntanro}-{aluetunnus}"] = Alue(kuntanro, aluetunnus, nimi, luku)
        self._cached_alueet = out
