import dataclasses
import numpy as np
import pandas as pd

from vaalianalyysi.data.tulospalvelu import df

_tulokset_alueittain_map = {
     'Vaalilaji': 'vaalilaji',
     'Vaalipiiri-/hyvinvointialuenro': '',
     'Kuntanro': 'kunta_nro',
     'Alueen tyyppi': 'alueen_tyyppi',
     'Äänestysaluetunnus': 'alue_tunnus',
     'Vaalipiirin/hv-alueen lyhenne suomeksi': '',
     'Vaalipiirin/hv-alueen lyhenne ruotsiksi': '',
     'Yhdistetyn äänestysalueen tunnus': '',
     'Ennakko- ja vaalipäivän äänten yhdistely': '',
     'Kunnan/vaalipiirin/hv-alueen/äänestysalueen nimi suomeksi': 'nimi_fi',
     'Kunnan/vaalipiirin/hv-alueen/äänestysalueen nimi ruotsiksi': '',
     'Kuntamuoto': '',
     'Kielisuhde': '',
     'Äänioikeutetut yhteensä': 'N',
     'Äänioikeutetut miehet': '',
     'Äänioikeutetut naiset': '',
     'Äänioikeutetut Suomessa asuvat yhteensä': '',
     'Äänioikeutetut Suomessa asuvat miehet': '',
     'Äänioikeutetut Suomessa asuvat naiset': '',
     'Valittavien lukumäärä': 'paikkoja',
     'Äänestysalueiden lukumäärä': '',
     'Vaalitapahtuman nimilyhenne 1. vertailuvaali': '',
     'Äänioik. Suomessa asuvat yht. 1. vertailuvaali': '',
     'Ennakkoäänestysprosentti Suomessa asuvat, 1. vertailuvaali ': '',
     'Vaalipäivän äänestysprosentti Suomessa asuvat, 1. vertailuvaali': '',
     'Äänestysprosentti yht. Suomessa asuvat, 1. vertailuvaali': '',
     'Hyväksyttyjä ääniä yhteensä, 1. vertailuvaali': '',
     'Mitättömiä ääniä yhteensä, 1. vertailuvaali': '',
     'Valittavien lkm 1. vertailuvaali': '',
     'Vaalitapahtuman nimilyhenne 2. vertailuvaali': '',
     'Äänioikeutetut Suomessa asuvat yht. 2. vertailuvaali': '',
     'Ennakkoäänestysprosentti Suomessa asuvat, 2. vertailuvaali': '',
     'Vaalipäivän äänestysprosentti Suomessa asuvat, 2. vertailuvaali': '',
     'Äänestysprosentti yht. Suomessa asuvat, 2. vertailuvaali': '',
     'Hyväksyttyjä ääniä yhteensä, 2. vertailuvaali': '',
     'Mitättömiä ääniä yhteensä, 2. vertailuvaali': '',
     'Ennakkoon äänestäneet': 'n_ennakko',
     'Ennakkoon äänestäneet, miehet': '',
     'Vaalipäivänä äänestäneet': 'n_vaalipv',
     'Vaalipäivänä äänestäneet, miehet': '',
     'Äänestäneet yhteensä': 'n',
     'Äänestäneet yhteensä, miehet': '',
     'Ennakkoon äänestäneet Suomessa asuvat': '',
     'Ennakkoon äänestäneet Suomessa asuvat, miehet': '',
     'Vaalipäivänä äänestäneet Suomessa asuvat': '',
     'Vaalipäivänä äänestäneet Suomessa asuvat, miehet': '',
     'Äänestäneet Suomessa asuvat yhteensä': '',
     'Äänestäneet Suomessa asuvat yhteensä, miehet': '',
     'Ennakkoon äänestäneet ulkomailla asuvat suomalaiset': '',
     'Ennakkoon äänestäneet ulkomailla asuvat suomalaiset, miehet': '',
     'Vaalipäivänä äänestäneet ulkomailla asuvat suomalaiset': '',
     'Vaalipäivänä äänestäneet ulkomailla asuvat suomalaiset, miehet': '',
     'Äänestäneet ulkomailla asuvat suomalaiset yhteensä': '',
     'Äänestäneet ulkomailla asuvat suomalaiset yhteensä, miehet': '',
     'Ennakkoäänestysprosentti': '',
     'Vaalipäivän äänestysprosentti': '',
     'Äänestysprosentti yhteensä': '',
     'Ennakkoäänestysprosentti Suomessa asuvat': '',
     'Vaalipäivän äänestysprosentti Suomessa asuvat': '',
     'Äänestysprosentti yhteensä Suomessa asuvat': '',
     'Ennakkoäänestysprosentti ulkomailla asuvat suomalaiset': '',
     'Vaalipäivän äänestysprosentti ulkomailla asuvat suomalaiset': '',
     'Äänestysprosentti yhteensä ulkomailla asuvat suomalaiset': '',
     'Hyväksytyt ennakkoäänet': '',
     'Hyväksytyt vaalipäivän äänet': '',
     'Hyväksytyt äänet yht.': '',
     'Mitättömät ennakkoäänet': '',
     'Mitättömät vaalipäivän äänet': '',
     'Mitättömät äänet yht.': '',
     'Ennakkoäänistä laskettu prosenttia': '',
     'Vaalipäivän äänistä laskettu prosenttia': '',
     'Äänistä laskettu prosenttia': '',
     'Laskentavaihe': '',
     'Viimeisin päivitys': '',
     'Äänioikeutetut Suomessa asuvat Suomen kansalaiset': '',
     'Äänioikeutetut Suomessa asuvat Suomen kansalaiset, miehet': '',
     'Äänioikeutetut muut EU-kansalaiset': '',
     'Äänioikeutetut muut EU-kansalaiset, miehet': '',
     'Äänioikeutetut Norjan ja Islannin kansalaiset': '',
     'Äänioikeutetut Norjan ja Islannin kansalaiset, miehet': '',
     'Äänioikeutetut muiden maiden kansalaiset': '',
     'Äänioikeutetut  muiden maiden kansalaiset, miehet': '',
     'Äänioikeutetut ulkomailla asuvat suomalaiset': '',
     'Äänioikeutetut ulkomailla asuvat suomalaiset, miehet': '',
     'Ennakkoon äänestäneet Suomessa asuvat suomalaiset': '',
     'Ennakkoon äänestäneet Suomessa asuvat suomalaiset, miehet': '',
     'Vaalipäivänä äänestäneet Suomessa asuvat suomalaiset': '',
     'Vaalipäivänä äänestäneet Suomessa asuvat suomalaiset, miehet': '',
     'Ennakkoon äänestäneet muut EU-kansalaiset': '',
     'Ennakkoon äänestäneet muut EU-kansalaiset, miehet': '',
     'Vaalipäivänä äänestäneet muut EU-kansalaiset': '',
     'Vaalipäivänä äänestäneet muut EU-kansalaiset, miehet': '',
     'Ennakkoon äänestäneet Norjan ja Islannin kansalaiset': '',
     'Ennakkoon äänestäneet Norjan ja Islannin kansalaiset, miehet': '',
     'Vaalipäivänä äänestäneet Norjan ja Islannin kansalaiset': '',
     'Vaalipäivänä äänestäneet Norjan ja Islannin kansalaiset, miehet': '',
     'Ennakkoon äänestäneet muiden maiden kansalaiset': '',
     'Ennakkoon äänestäneet muiden maiden kansalaiset, miehet': '',
     'Vaalipäivänä äänestäneet muiden maiden kansalaiset': '',
     'Vaalipäivänä äänestäneet muiden maiden kansalaiset, miehet': '',
     'Mitättömät ennakkoäänet: Peruste 1': '',
     'Mitättömät vaalipäivän äänet: Peruste 1': '',
     'Mitättömät ennakkoäänet: Peruste 2': '',
     'Mitättömät vaalipäivän äänet: Peruste 2': '',
     'Mitättömät ennakkoäänet: Peruste 3': '',
     'Mitättömät vaalipäivän äänet: Peruste 3': '',
     'Mitättömät ennakkoäänet: Peruste 4': '',
     'Mitättömät vaalipäivän äänet: Peruste 4': '',
     'Mitättömät ennakkoäänet: Peruste 5': '',
     'Mitättömät vaalipäivän äänet: Peruste 5': '',
     'Mitättömät ennakkoäänet: Peruste 6': '',
     'Mitättömät vaalipäivän äänet: Peruste 6': '',
     'Mitättömät ennakkoäänet: Peruste 7': '',
     'Mitättömät vaalipäivän äänet: Peruste 7': '',
}

_tulokset_ehdokkaittain_map = {
     'Vaalilaji': '',
     'Vaalipiiri-/hyvinvointialuenro': '',
     'Kuntanro': 'kunta_nro',
     'Alueen tyyppi': 'alueen_tyyppi',
     'Äänestysaluetunnus': 'alue_tunnus',
     'Vaalipiirin/hyvinvointialueen lyhenne suomeksi': '',
     'Vaalipiirin/hyvinvointialueen lyhenne ruotsiksi': '',
     'Pysyvä puoluetunniste': 'puolue_tunniste',
     'Vakiopuoluenumero': '',
     'Listajärjestysnumero': '',
     'Vaaliliittonumero': 'vaaliliitto_nro',
     'Puolueen/ryhmän nimilyhenne suomeksi': 'puolue_lyhenne',
     'Puolueen/ryhmän nimilyhenne ruotsiksi': '',
     'Puolueen/ryhmän nimilyhenne englanniksi': '',
     'Ehdokasnumero': 'ehdokasnro',
     'Kunnan/vaalipiirin/hv-alueen/ äänestysalueen nimi suomeksi': 'alue_nimi_fi',
     'Kunnan/vaalipiirin/hv-alueen/ äänestysalueen nimi ruotsiksi': '',
     'Henkilön etunimi': 'etunimi',
     'Henkilön sukunimi': 'sukunimi',
     'Sukupuoli': 'sukupuoli',
     'Ikä vaalipäivänä': 'ikä',
     'Ammatti': '',
     'Kotikunnan koodi': '',
     'Kotikunnan nimi suomeksi': '',
     'Kotikunnan nimi ruotsiksi': '',
     'Ehdokkaan kieli': '',
     'Europarlamentaarikko': '',
     'Kansanedustaja': '',
     'Kunnanvaltuutettu': '',
     'Aluevaltuutettu': '',
     'Vaalitapahtuman nimilyhenne 1. vertailuvaali': '',
     'Ääniä 1. vertailuvaali': '',
     'Ennakkoäänet lkm': 'n_ennakko',
     'Vaalipäivän äänet lkm': 'n_vaalipv',
     'Äänet yhteensä lkm': 'n',
     'Osuus ennakkoäänistä (%)': '',
     'Osuus vaalipäivän äänistä (%)': '',
     'Osuus äänistä yht. (%)': '',
     'Valintatieto': 'val',
     'Vertausluku': 'vluk',
     'Sija': '',
     'Lopullinen sija': '',
     'Laskennan tila': '',
     'Laskentavaihe': '',
     'Viimeisin päivitys': '',
}

def map_to(src, map):
    dst = pd.DataFrame()
    for k, v in map.items():
        if len(v) > 0:
            dst[v] = src[k]
    return dst


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
    paikkoja: int


@dataclasses.dataclass
class Alue:
    """Kunnan äänestysalueen metadata"""

    kuntanro: int
    aluetunnus: str
    nimi_suomeksi: str
    n: int


class Vaalit:
    """Yhden vaalin kaikki tiedot"""

    def __init__(self, vaalit):
        """Vaalitiedot"""
        self.vaalit = vaalit
        self.tulokset_ehdokkaittain = map_to(df.tulokset_ehdokkaittain(vaalit), _tulokset_ehdokkaittain_map)
        self.tulokset_alueittain = map_to(df.tulokset_alueittain(vaalit), _tulokset_alueittain_map)
        self.ehdokasasettajakohtaiset_tulokset = df.ehdokasasettajakohtaiset_tulokset(
            vaalit
        )
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
        d = d[d.alueen_tyyppi == "A"]
        for _, row in d.iterrows():
            kuntaalue = f"{row.kunta_nro}-{row.alue_tunnus}"
            try:
                i = alueet.index(kuntaalue)
                try:
                    puolue = row.puolue_tunniste
                    j = puolueet.index(puolue)
                except ValueError:
                    j = -2
                v[j, i] += row.n
            except ValueError:
                pass
        v[-1, :] = self.n(alueet) - np.sum(v, axis=0)
        return v

    def _compute_puolueet(self):
        out = {}
        d = self.tulokset_ehdokkaittain
        d = d[["puolue_tunniste", "puolue_lyhenne"]].drop_duplicates()
        for _, row in d.iterrows():
            tunniste = row.puolue_tunniste
            lyhenne = row.puolue_lyhenne
            out[tunniste] = Puolue(tunniste, lyhenne)
        self._cached_puolueet = out

    def _compute_kunnat(self):
        out = {}
        d = self.tulokset_alueittain
        d = d[d.alueen_tyyppi == "K"]
        d = d[["kunta_nro", "nimi_fi", "N", "paikkoja"]].drop_duplicates()
        for _, row in d.iterrows():
            kuntanro = row.kunta_nro
            nimi = row.nimi_fi
            luku = row.N
            paikkoja = row.paikkoja
            out[kuntanro] = Kunta(kuntanro, nimi, luku, paikkoja)
        self._cached_kunnat = out

    def _compute_alueet(self):
        out = {}
        d = self.tulokset_alueittain
        d = d[d.alueen_tyyppi == "A"]
        d = d[["kunta_nro", "alue_tunnus", "nimi_fi", "N"]].drop_duplicates()
        for _, row in d.iterrows():
            key = f"{row.kunta_nro}-{row.alue_tunnus}"
            out[key] = Alue(int(row.kunta_nro), row.alue_tunnus, row.nimi_fi, row.N)
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
