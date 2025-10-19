# Her er et lite bidrag til streamen i form av et Python-script for å kunne trykke på en knapp for å øke shot-counteren.
# Etter streamen, eller før neste stream, trykker man på en annen knapp for å resette counteren.
# Scriptet bruker en tekstfil for å lagre et tall, og tar under 10kB i lagringsplass.
# Om det ikke fungerer selv om du har installert Python, sjekk sjekklisten nederst.
# Mest sannsynlig har du kanskje oversett en filsti (file path, file location), men dette regner jeg med du som content creator har sånn passe oversikt over.

# ---------------
# FINNE FRAM VERKTØY
# ---------------

# json er for å opprette tekstfil
import json
# sys og os er for å kunne lese fra (laste inn tall) og skrive til (oppdatere counter) til
# tekstfilen "counter.json".
import sys
import os
# Følgende skal allere være installert om du har OBS-versjon nyere enn 28.
from obsws_python import ReqClient


# ---------------
# OPPSETT
# ---------------
# La stå. Dette betyr bare at scriptet kjører på samme datamaskin som OBS. Ikke fjern anførselstegn.
OBS_HOST = "localhost"

# Standard port, dobbeltsjekk på Tools -> WebSocket Server Settings. Har du et annet tall, sett det til det tallet du har.
OBS_PORT = 4455

# Nei, jeg kan ikke se passordet ditt.
# Gå til Tools -> WebSocket Server Settings, huk av "Enable WebSocket server",
# klikk "Show connect info" og kopier passordet og lim det inn derfra.
# Er passordet "PASSORD123", limer du inn det. IKKE fjern anførselstegn.
OBS_PASSWORD = "PASSORD123"

# Gå i OBS, og opprett et nytt TOMT tekstelement. Bare opprett et tekstelement som du kaller f.eks ShotCounter, og trykk OK. Ikkenomer (inntil videre).
# Formater gjerne med stroke og gradient ETTER at du har sett det første tallet dukke opp.
# Hvis det heter ShotCounter i OBS-en din, heter det ShotCounter her også, det må hete det samme.
# IKKE endre på TEXT_SOURCE_NAME. Ikke fjern anførselstegn, men bytt ut det som står inni anførselstegnene, til det du kalte tekstelementet i OBS.
TEXT_SOURCE_NAME = "ShotCounter"

# La stå. Ikke fjern anførselstegn. counter.json er tekstfilen som lagrer tellingen.
COUNTER_FILE = "counter.json"

# ---------------
# FUNKSJONER
# ---------------

# Laste inn siste registrerte antall shot
def load_counter():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, 'r') as f:
            data = json.load(f)
            return data.get('counter', 0)
    return 0

# Lagre antall shots til variabelen som holder rede på det (count)
def save_counter(value):
    with open(COUNTER_FILE, 'w') as f:
        json.dump({'counter': value}, f)

# For å hente tallet fra filen, og oppdatere det på stream-elementet i OBS må vi gjøre dette:
def update_obs(counter_value):
    try:
        ws = ReqClient(host=OBS_HOST, port=OBS_PORT, password=OBS_PASSWORD)
        ws.set_input_settings(TEXT_SOURCE_NAME, {"text": f"Shots: {counter_value}"}, True)
        print(f"Counter updated to: {counter_value}")
    # Har du glemt å huke av for "Enable web socket", så ser du dette i terminalen:
    except Exception as e:
        print(f"Error connecting to OBS: {e}")

# Løkke for å kalle hovedmetoden, som gjør at du kan gjøre de andre def'ene
if __name__ == "__main__":
    # Om lengen på systemargumenter er mer enn 1 og det argumentet er "reset", så resettes telleren
    if len(sys.argv) > 1 and sys.argv[1].lower() == "reset":
        save_counter(0)
        update_obs(0)
        print("Counter reset to 0")
        # På norsk betyr det at hvis du åpner Terminal i mappen der denne filen ligger kan du skrive "ShotCounter.py reset" for å resette om du ikke får det inn på StreamDecken.
    else:
        # Hvis du åpner Terminal i mappen og skriver "ShotCounter.py" øker du counteren med 1.
        counter = load_counter()
        counter += 1
        save_counter(counter)
        update_obs(counter)

# ---------------
# Sjekkliste
# ---------------
# Installere Python
# Dobbeltsjekk at OBS-porten din er 4455. Er den noe annet, endre dette tallet.
# Kopier DITT OBS_PASSWORD inn i anførselstegnene. Ikke fjern anførselstegnene.
# I OBS-programmet, opprett et nytt tekst-element. La det stå tomt, trykk OK. IKKE klikk "Les fra fil" og velg counter.json, IKKE gjør det.
# Sørg for at denne filen, increment.bat, reset.bat og counter.json ligger i samme mappe.
#
# For å teste her og nå, høyreklikk i mappen denne filen ligger, åpne Terminal og skriv inn "ShotCounter-GrevenStream.py", og dobbeltsjekk at tallet øker i OBS.
# For å slippe å skrive det hver gang du får en shot, så kan du legge til snarveier i StreamDecken.
# Her er to måter å gjøre det på, tror den første er lettest for Streamdeck.
#
# METODE 1 (med StreamDeck)
#
# Knapp 1 (Øk counter (+1)
# Action: System -> Open
# App/File: C:\Python313\python.exe  (bruk "where python" i Terminal for å finne ut hvor din Python er)
# Arguments: C:\Users\BRUKERNAVN\DER\DU\HAR\LAGRET\ShotCounter-GrevenStream.py
#
# Knapp 2 (Reset counter), for å resette etter en stream eller før man begynner på neste
# Action: System -> Open
# App/File: C:\Python313\python.exe
# Arguments C:\Users\BRUKERNAVN\DER\DU\HAR\LAGRET\ShotCounter-GrevenStream.py reset
#
# METODE 2 (Uten streamdeck, men du kan også kjøre disse som program i StreamDeck)
#
# Øk counter
# Høyreklikk på filen increment.bat og endre filstien til der du har lagret ShotCounter-GrevenStream.py
# Dobbeltklikk på filen increment.bat
#
# Resette counter til 0
# Høyreklikk på filen reset.bat og endre filstien til der du har lagret ShotCounter-GrevenStream.py
# Dobbeltklikk på filen reset.bat
#
# Legg merke til at du må bruke "reset" som argument, i tillegg til filstien for å resette.
# Du må også bruke dine egne filstier, jeg vet ikke hvor du har lagret dine ting.
#
# Lykke til.
# Send gjerne en mail til Mister Fisteminister på hemmeligspion@protonmail.com om du står helt fast og AI heller ikke hjelper.
