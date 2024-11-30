# Vaalidatan analyysityökaluja

Voit tarkastella [oikeusministeriön tieto- ja tulospalvelun](https://tulospalvelu.vaalit.fi/fi/index.html) vaalidatoja `pandas.DataFrame`-muodossa.
Esimerkiksi eduskuntavaalien 2023 ehdokkaittaiset tulokset:

```py
>>> import vaalianalyysi as va
>>> e23 = va.data.tulospalvelu.vaalit("EKV-2023")
>>> e23.tulokset_ehdokkaittain
       Vaalilaji  Vaalipiiri-/hyvinvointialuenro Kuntanro Alueen tyyppi Äänestysaluetunnus Vaalipiirin/hyvinvointialueen lyhenne suomeksi  ... Vertausluku  Sija  Lopullinen sija  Laskennan tila  Laskentavaihe Viimeisin päivitys
0              E                               1      091             A               001A                                            HEL  ...           0     0                0               V              T     20230404160757
1              E                               1      091             A               001A                                            HEL  ...           0     0                0               V              T     20230404160757
2              E                               1      091             A               001A                                            HEL  ...           0     0                0               V              T     20230404160757
3              E                               1      091             A               001A                                            HEL  ...           0     0                0               V              T     20230404160757
4              E                               1      091             A               001A                                            HEL  ...           0     0                0               V              T     20230404160757
...          ...                             ...      ...           ...                ...                                            ...  ...         ...   ...              ...             ...            ...                ...
483685         E                              13      ***             V               ****                                            LAP  ...      153875   102              102               V              T     20230405170638
483686         E                              13      ***             V               ****                                            LAP  ...      205167    97               97               V              T     20230405170638
483687         E                              13      ***             V               ****                                            LAP  ...      410333    83               83               V              T     20230405170638
483688         E                              13      ***             V               ****                                            LAP  ...      307750    89               89               V              T     20230405170638
483689         E                              13      ***             V               ****                                            LAP  ...      615500    79               79               V              T     20230405170638

[483690 rows x 45 columns]
```

Saatavia dataframeja ovat `tulokset_ehdokkaittain`, `tulokset_alueittain` ja `ehdokasasettajakohtaiset_tulokset`.
Lisätietoja taulukon sisällöstä saat [täältä](https://tulospalvelu.vaalit.fi/EKV-2023/ohje/EKV2023_CSV-tiedostojen_kuvaus_fi.pdf).

Vaalien nimitunnisteet (esim. eduskuntavaalit 2023 `EKV-2023`, kunnallisvaalit 2017 `KV-2017`) eivät aina ole johdonmukaisia.
Tarkista [tulospalvelun sisällysluettelon](https://tulospalvelu.vaalit.fi/fi/index.html) linkeistä, mikä on haluamasi vaalien käyttämä tunniste.