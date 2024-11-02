# Säähavaintopalvelu
YLEISKUVAUS

Palvelun perusidea on luoda sivusto, jossa tavalliset ihmiset voivat kirjata matalalla kynnyksellä säähavaintoja sekä verrata niitä meteorologin antamaan ennusteeseen. Palvelu ei ole tarkoitettu säätilan tai ennusteen katsomista varten.

Palvelussa käyttäjä voi lisätä säähavaintoja Helsingin alueen 1km x 1km hilaruudukkoon (Tilastokeskuksen hilaruudukkodata) maksimissaan kerran tunnissa. Syötettävät sääparametrit ovat:
- Lämpötila (celsius)
- Pilvisyys (selkeää, melko selkeää, puolipilvistä, melko pilvistä, pilvistä)
- Sateen voimakkuus (ei sadetta/poutaa, vähäistä sadetta, sadetta, runsasta sadetta)
- Sateen olomuoto (tihkua, vettä, räntää, lunta, rakeita)
  
Pilvisyyden, sateen voimakkuuden ja -olomuodon määrittelyissä käytetään Ilmatieteen laitoksen verkkosivuilta saatavia viitearvoja. Käyttäjä näkee nämä viitearvot sekä ohjeet lisätessään havaintoa palveluun. Parametreja on tarkoituksella vähän, sillä ajatus on, että ne voidaan havaita joko suoraan silmillä tai yleisillä kotoa löytyvillä mittalaitteilla kuten lämpömittarilla.

Käyttäjä voi havaintoa lisätessään syöttää manuaalisesti havaintopaikan koordinaatit (lat ja lon) tai käyttää palvelun HTML Geolocation APIa oman sijainnin syöttämiseen (vaatii käyttäjän hyväksynnän). Palvelu kirjaa havainnon koordinaattien mukaan lähimpään hilapisteeseen ruudukossa.

Tietokantaan kirjataan jokaisesta havainnosta:
- Sääparametrit
- Kellonaika
- Sijainti hilaruudukossa
- Havainnontekijä


Lisäksi palvelussa on "meteorologi"-käyttäjiä, jotka voivat ladata json-muotoisen, pisimmillään 24h ennusteen 1 tunnin aikaresoluutiolla yllä mainituille parametreille hilaruudukkoon. Palvelussa voi vertailla meteorologin antaman ennusteen ja käyttäjien kirjaamien havaintojen eroja jälkikäteen.

Tietokantaan lisätään jokaisesta ennusteesta:
- Ennustetut sääparametrit
- Ennustetunti
- Ennustesijainti hilaruudukossa
- Analyysiaika (hetki jolloin ennuste on tuotettu)
- Meteorologi

Kuka tahansa voi kirjautua palveluun tavallina käyttäjänä. Meteorologi-taso vaatii erillisen hyväksynnän palvelun ylläpitäjältä.

KAYTTÄJÄTASOT

1. Palvelussa on ylläpitäjiä, jotka voivat lukita sekä tavallisia käyttäjiä, että meteorologeja pois palvelusta, mikäli nämä tuottavat selvästi virheellistä dataa tai muuten eivät käytä palvelua toivotulla tavalla. Ylläpitäjät voivat myös muuttaa ja poistaa havaintoja sekä ennusteita tietokannasta. Käyttäjät ja meteorologit voivat jättää ylläpitäjälle havainnon tai ennusteen poistopyyntojä.

2. Tavalliset käyttäjät ("havainnontekijät") voivat tarkastella muiden havaintoja, mutta eivät voi poistaa antamiaan havaintoja. Kullekin tunnille annettua havaintoa voi kuitenkin muokata kyseisen tunnin aikana (esim. kello 12 SA havaintoa voi päivittää 12:59 asti). Lisäksi käyttäjät voivat tarkastella menneitä meteorologien ennusteita ja verrata niitä annettuihin havaintoihin. Käyttäjä voi myös antaa joka tunti arvosanan 1-5 meteorologin ennusteen osuvuudelle edelliselle tunnille.

Meteorologit voivat tarkastella menneitä ennusteita, mutta eivät voi poistaa niitä. Meteorologit voivat myös tarkastella menneitä havaintoja ja verrata niitä ennusteisiin.

TEKNISET LISÄTIEDOT

Tietokannan koon hillitsemiseksi ja suorituskyvyn parantamiseksi yli viikon vanhat ennusteet ja havainnot heikennetään 10km x 10km hilaresoluutioon ja 6h aikaresoluutioon. Tämä tehdään yksinkertaisesti käyttämällä harvempaa hilaruudukkoa, jossa sääparametrit lasketaan uusille hilapisteille joko havaintojen ja ennusteiden 6h keskiarvona (lämpötila) tai moodina (pilvisyys, sateen voimakkuus ja -olomuoto).

Sääparametrien lisäksi palvelu käyttää tietokantaa käyttäjätietojen säilömiseen sekä erinäisten tilastotietojen säilömiseen.

Tilastoja voidaan mahdollisesti esittää palvelussa myös graafisesti käyttäen R-ohjelmistoa. Havainto- ja ennustedataa voi mahdollisesti ladata palvelusta json formaatissa.
