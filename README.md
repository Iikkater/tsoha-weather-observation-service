# Säähavaintopalvelu
## YLEISKUVAUS

Palvelu, jossa tavalliset ihmiset voivat kirjata matalalla kynnyksellä säähavaintoja sekä verrata niitä meteorologin antamaan ennusteeseen. Palvelun tarkoitus on tuotaa meteorologille dataa ennusteen osuvuudesta sekä tarjota palvelun josta voi tarkastella historiatietoja menneistä havainnoista ja ennusteista. Palvelu ei ole tarkoitettu säätilan tai ennusteen reaaliaikaista tarkastekua varten.

Palvelussa käyttäjä voi lisätä säähavaintoja Uudenmaan postinumeroalueille maksimissaan kerran tunnissa per postinumeroalue. Syötettävät sääparametrit ovat:
- Lämpötila (celsius)
- Pilvisyys (selkeää, melko selkeää, puolipilvistä, melko pilvistä, pilvistä) https://www.ilmatieteenlaitos.fi/pilvisyys
- Sateen voimakkuus (ei sadetta/poutaa, vähäistä sadetta, sadetta, runsasta sadetta) https://www.ilmatieteenlaitos.fi/sade
- Sateen olomuoto (pouta, tihkua, vettä, räntää, lumijyväset, lunta, rakeita) https://www.ilmatieteenlaitos.fi/sateen-olomuodot
  
Pilvisyyden, sateen voimakkuuden ja -olomuodon määrittelyissä käytetään Ilmatieteen laitoksen verkkosivuilta saatavia viitearvoja. Käyttäjä näkee nämä viitearvot sekä ohjeet lisätessään havaintoa palveluun. Parametreja on tarkoituksella vähän, sillä ajatus on, että käyttäjä voi havaita ne joko suoraan silmillä tai yleisillä kotoa löytyvillä mittalaitteilla kuten lämpömittarilla.

Käyttäjä voi havaintoa lisätessään syöttää manuaalisesti postinumeroalueen. Palvelu tarjoaa käyttäjälle myös automaattisesti hänen kotipostinumeroaluettaan.

Tietokantaan kirjataan jokaisesta havainnosta:
- Havaitut sääparametrit
- Havainnon päivämäärä ja kellonaika
- Havainnon postinumeroalue
- Havainnontekijä

Lisäksi palvelussa on "meteorologi"-käyttäjiä, jotka voivat ladata json-muotoisen, ennusteen yllä mainituille sääparametreille postinumeroalueelle. Palvelussa meteorologi voi vertailla tekemänsä ennusteen ja käyttäjien kirjaamien havaintojen eroja jälkikäteen.

Tietokantaan lisätään jokaisesta ennusteesta:
- Ennustetut sääparametrit
- Ennustetunnit
- Ennusteen sijainti postinumeroalueena
- Analyysiaika (päivämäärä ja kellonaika jolloin ennuste on tuotettu)
- Ennusteen tehnyt meteorologi

Kuka tahansa voi luoda tunnuksen ja kirjautua palveluun tavallisena käyttäjänä. Meteorologi-taso vaatii erillisen hyväksynnän palvelun ylläpitäjältä.

### KÄYTTÄJÄTASOT

1. Palvelussa on ylläpitäjiä, jotka voivat lukita sekä tavallisia käyttäjiä, että meteorologeja pois palvelusta, mikäli nämä tuottavat selvästi virheellistä dataa tai muuten eivät käytä palvelua toivotulla tavalla. Ylläpitäjä voi muuttaa tavallisen käyttäjän meteorologi-tasolle perustellusta pyynnöstä. Ylläpitäjät voivat myös muuttaa ja poistaa havaintoja sekä ennusteita tietokannasta.

2. Tavalliset käyttäjät voivat tarkastella muiden havaintoja, mutta eivät voi poistaa antamiaan havaintoja. Kullekin tunnille ja postinumeroalueelle annettua havaintoa voi kuitenkin muokata kyseisen tunnin aikana (esim. kello 12 SA havaintoa voi päivittää 12:59 SA asti). Lisäksi käyttäjät voivat tarkastella menneitä meteorologien ennusteita ja verrata niitä annettuihin havaintoihin.

3. Meteorologit voivat käyttää palveua kuten tavalliset käyttäjät. Lisäksi he voivat listätä palveluun ennusteita. Meteorologit voivat tarkastella omia ja muiden tekemiä menneitä ennusteita, mutta eivät voi poistaa niitä. Meteorologit voivat myös tarkastella menneitä havaintoja ja verrata niitä saman ajanhetken ennusteisiin.

### TEKNISET LISÄTIEDOT

Sääparametrien lisäksi palvelu käyttää tietokantaa käyttäjätietojen säilömiseen.

Syötetyille sääparametreille (havainnot ja ennusteet) tehdään laaduntarkastusta niin, että selkeästi virheellisen datan pääsyä tietokantaan pyritään estämään.
- Lämpötilan osalta minimi- ja maksimiarvot
- Sateen olomuodon, -voimakkuuden ja pilvisyyden on oltava linjassa keskenään (ilman pilviä ei voi olla sadetta ja ilman sadetta ei voi olla olomuotoa jne.).

## VÄLIPALAUTUS 2
- Sovelluksen pohjatyöt on tehty kuten luotu eri sivujen html -tiedostoja joita hallinnoidaan wsgi.py ohjelmalla. Lisäksi on luotu styles.css -tyyli ja muotoilutiedosto
- Sovellukselle on luotu kirjautumistoiminnot, sekä käyttäjätilin luomisen toiminnot
  - Käyttäjien tiedot säilötään ja haetaan tietokannan tsoha_wos_db taulusta 'users'
  - Lisäksi käyttäjatasolle admin on lisätty oikeus muutta muiden käyttäjien tasoja (basic, meteorologist, admin ja locked).

- Varsinaiset havaintoihin liittyvät toiminnallisuudet ovat vasta suunnitteluasteella
  - Tietokantataulut hilapisteille, havainnoille sekä ennusteille ja erinäisille hiestoriatiedoille ja tilastoille

## VÄLIPALAUTUS 3
- Sovelluksen päätoiminnot ovat rakennettu. Eri käyttäjätasot voivat lisätä kantaan ennusteita ja havaintoja. Lisäksi sovelluksen toimintaa piti muuttaa pois hila-ruudukkomallista postinumeropohjaiseen toteutukseen. Hiladatan käsittely oli turhan raskasta ja monimutkaista tälle sovellukselle. Tämä poisti jotain aluksi suunniteltuja ominaisuuksia, mutta toisaalta alue laajeni koko Uudenmaan postinumeroalueiksi.
- Kehitettävää julkaisuversioon (lopullinen palautus):
    - Ulkoasun hiominen ja käytettävyyden parantaminen
    - Ohjeiden ja vinkkien lisääminen sovellukseen
    - Käyttäjille omien tietojen muokkaus ja salasanan vaihto -toiminnallisuus
    - Ennustedatan ja havaitnodatan vertailu -toiminnallisuus
    - Admin tasolle mahdollisuus poistaa ennusteita tietokannasta käyttäen sovellusta.
 
## LOPULLINEN PALAUTUS
- Sovelluksen toimintoja on hiottu
    - Ennusteita voi tarkastella palvelusta
    - Ennusteille lasketaan osuvuus havainnoista
    - Mahdollisuus muuttaa omia käyttäjätietoja
- Ulkoasua on paranneltu ja selkeyttä lisätty

## TESTAUS

1. Kloonaa repositorio:

    ```sh
    git clone https://github.com/Iikkater/tsoha-weather-observation-service.git
    cd tsoha-weather-observation-service
    ```

2. Luo sovelluksen käyttämä tietokantakäyttäjä ja tietokanta:
    - Avaa PostgreSQL-komentorivi:
    
        ```sh
        psql
        ```
    - Luo uusi käyttäjä `wos_app`:

        ```sql
        CREATE USER wos_app WITH PASSWORD 'salasana_tahan';
        ```
    - Luo uusi tietokanta `tsoha_wos_db` ja aseta sen omistajaksi `wos_app`:

        ```sql
        CREATE DATABASE tsoha_wos_db OWNER wos_app;
        ```
    - Poistu PostgreSQL-komentoriviltä:

        ```sql
        \q
        ```

3. Määritä ympäristömuuttujat .env -tiedostoon sovelluksen juuressa:

    ```env
    DB_NAME=tsoha_wos_db
    DB_USER=wos_app
    DB_PASSWORD=<salasana_tahan>
    DB_HOST=localhost
    DB_PORT=5432
    SECRET_KEY=<salainen_avain_tahan>
    ```

4. Alusta tietokanta skeemalla:

    ```sh
    psql -d tsoha_wos_db -f schema.sql
    ```

5. Luo itsellesi manuaalisesti admin-tason käyttäjä tietokantaan helpottamaan palvelun testaamista:
    - Luo ensin itsellesi kryptattu salasana:
        
        ```sh
        cd app/
        chmod +x crypt.py
        ./crypt.py 'salasana_tahan'
        ```

        Kopioi tämä kryptattu salasana ('pbkdf2:sha256:...').

    - Lisää admin-tason käyttäjä tietokantaan kryptatulla salasanalla (voit halutessasi muuttaa myös admin-käyttäjän muita tietoja sql-komennossa):
        
        Avaa PostgreSQL-komentorivi:

        ```sh
        psql -d tsoha_wos_db
        ```

        ```sql
        INSERT INTO user_credentials (id, username, password, tier) VALUES (10000000, 'admin', '<kryptattu_salasana>', 'admin');
        INSERT INTO user_details (user_id, firstname, surname, email) VALUES (10000000, 'Admin', 'User', 'admin@example.com');
        ```

        Varmista lisäys:
        
        ```sql
        SELECT * FROM user_credentials;
        SELECT * FROM user_details;
        ```

    - Poistu PostgreSQL-komentoriviltä:

        ```sql
        \q
        ```

5. Luo ja aktivoi virtuaaliympäristö:

    ```sh
    cd ..
    python3 -m venv venv
    source venv/bin/activate
    ```

6. Asenna riippuvuudet:

    ```sh
    pip install -r requirements.txt
    ```

7. Siirry hakemistoon /app ja käynnistä sovellus:

    ```sh
    cd app/
    flask run
    ```

8. Sovellus on nyt testattavissa osoitteessa: http://127.0.0.1:5000/

### Testidatan lisäys
Repositoriossa on valmiina testidataa sovelluksen testauksen helpottamiseksi

Voi käyttää valmista test_forecast_00180.json tiedostoa hakmistossa tsoha-weather-observation-service/app/data/forecasts/ ennusteen latauksen testaamiseen.

Lisäksi voit ajaa sovelluksen käynnistyksen jälkeen kantaan valmiita havaintoja käyttäen test_observations.sql tiedostoa repositorion juuresta:

    psql -d tsoha_wos_db -f test_observations.sql
    
