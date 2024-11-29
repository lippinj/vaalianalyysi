import dataclasses
import numpy as np

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

    def n(self, alueet):
        """Alueittaiset äänioikeutettujen määrät"""
        return np.array([self.alueet[a].n for a in alueet])

    def v(self, alueet, puolueet):
        """
        Puolueittaiset äänimäärät

        Kun nimettyjä puolueita on N ja alueita M, tämä on matriisi
        kokoa (N+2)xM. Rivillä n on listattu nimetyn puolueen n äänet
        alueittain. Rivillä -2 on muiden puolueiden äänet ja rivillä -1
        nukkuvat äänet.
        """
        v = np.zeros((len(puolueet) + 2, len(alueet)))
        d = self.tulokset_ehdokkaittain
        d = d[d[d.columns[3]] == "A"]
        d = d[[d.columns[2], d.columns[4], d.columns[7], d.columns[34]]]
        for _, row in d.iterrows():
            kunta = row[d.columns[0]]
            alue = row[d.columns[1]]
            kuntaalue = f"{kunta}-{alue}"
            try:
                i = alueet.index(kuntaalue)
                try:
                    puolue = row[d.columns[2]]
                    j = puolueet.index(puolue)
                except ValueError:
                    j = -2
                v[j, i] += row[d.columns[3]]
            except ValueError:
                pass
        v[-1, :] = self.n(alueet) - np.sum(v, axis=0)
        return v

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

    def puoluetunnukset(self, lyhenteet):
        """Puoluetunnukset, jotka vastaavat annettuja nimilyhenteitä"""
        out = []
        for lyhenne in lyhenteet:
            for _, v in self.puolueet.items():
                if v.nimilyhenne_suomeksi == lyhenne:
                    out.append(v.tunniste)
                    break
        return sorted(out)

    @staticmethod
    def aluevastaavuudet(v1, v2, r=10.0):
        """
        Kuntaalueet, jotka ovat vastaavia vaaleissa v1 ja v2

        Kuntaalue katsotaan vastaavaksi, jos se löytyy molemmista
        vaaleista, sen nimi on molemmissa sama, ja sen äänioikeuttujen
        lukumäärä on muuttunut enentään r% vaaleista v1 vaaleihen v2.
        """
        out = []
        for alue in set(v1.alueet.keys()) & set(v2.alueet.keys()):
            a1 = v1.alueet[alue]
            a2 = v2.alueet[alue]
            if a1.nimi_suomeksi != a2.nimi_suomeksi:
                continue
            if 100 * np.abs(a2.n / a1.n - 1) > r:
                continue
            out.append(alue)
        return sorted(out)
