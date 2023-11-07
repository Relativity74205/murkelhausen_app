import requests
import json

# Gebietscode von https://www.xrepository.de/api/xrepository/urn:de:bund:destatis:bevoelkerungsstatistik:schluessel:rs_2021-07-31/download/Regionalschl_ssel_2021-07-31.json
# ab Stelle 6 nur Nullen verwenden!
ninaBaseUrl = "https://warnung.bund.de/api31"
gebietscodeAugsburg = "051170000000"

# aktuelle Warnmeldungen abrufen nach Gebietscode
response = requests.get(
    ninaBaseUrl + "/dashboard/" + gebietscodeAugsburg + ".json"
)  # TODO: hier pruefen, ob Abruf erfolgreich war

# wenn Abruf erfolgreich war, erhalten wir ein JSON
warnungen = response.json()

# iteriere über alle Warnmeldungen
for warnung in warnungen:
    # Der Dashboard-Abruf enthält nur eine Kurzform der Warnmeldung
    # Deshalb rufen wir hier die Details ab:
    id = warnung["payload"]["id"]
    warningDetails = requests.get(
        ninaBaseUrl + "/warnings/" + id + ".json"
    ).json()  # TODO: Fehlerbehandlung ergaenzen
    # headline und description Felder aus dem JSON fuer die Ausgabe zusammensetzen
    meldungsText = (
        warningDetails["info"][0]["headline"]
        + ": "
        + warningDetails["info"][0]["description"]
    )
    print("- " + meldungsText)
