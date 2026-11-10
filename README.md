# actueelalarm P2000 voor Home Assistant

P2000-meldingen van brandweer, ambulance, traumahelikopter en KNRM rond je huis, in Home Assistant. De meldingen komen van [actueelalarm.nl](https://actueelalarm.nl/), dat ze met een eigen P2000-ontvanger opvangt en binnen seconden online zet.

*English below.*

## Wat je krijgt

- **Sensor "Laatste melding"**: de nieuwste melding binnen je straal. De attributen zijn dienst, prioriteit, plaats, straat, afstand, tijd en een link naar de melding. Met `latitude` en `longitude` staat de sensor op de kaart.
- **Event `actueelalarm_melding`** voor elke nieuwe melding, om automations op te starten.
- De integratie vraagt elke minuut de [open feed](https://actueelalarm.nl/api/meldingen.json?lat=52.37&lon=4.89&km=5) op. Een API-sleutel is niet nodig.

Huisnummers en namen staan nooit in de meldingen. De positie is het midden van de straat, of anders het midden van de plaats.

## Installeren

Je hebt Home Assistant nodig met **HACS** (de Home Assistant Community Store). Staat HACS nog niet in je zijbalk? Installeer het dan eerst met [de uitleg van HACS](https://hacs.xyz/docs/use/).

### Stap 1: download de integratie in HACS

[![Open in HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=phakkers&repository=ha-actueelalarm&category=integration)

Klik op de knop hierboven. Je Home Assistant opent HACS op deze integratie. Klik rechtsonder op **Downloaden** en in het venster dat volgt nog een keer op **Downloaden**.

Werkt de knop niet? Doe het dan met de hand:

1. Open **HACS** in de zijbalk.
2. Klik rechtsboven op de **drie puntjes (⋮)** en kies **Aangepaste repositories** (*Custom repositories*).
3. Vul bij *Repository* in: `https://github.com/phakkers/ha-actueelalarm`. Kies bij *Type* **Integratie** (*Integration*) en klik op **Toevoegen**. Sluit daarna het venster.
4. Zoek in HACS op **actueelalarm**, open **actueelalarm P2000** en klik rechtsonder op **Downloaden**.

### Stap 2: herstart Home Assistant

Ga naar **Instellingen → Systeem**, klik rechtsboven op het **aan/uit-icoon** en kies **Home Assistant opnieuw opstarten**. Pas na de herstart kent Home Assistant de integratie.

### Stap 3: kies je punt

[![Integratie toevoegen](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=actueelalarm)

Klik op de knop hierboven. Met de hand gaat het zo: **Instellingen → Apparaten en diensten**, rechtsonder **Integratie toevoegen**, en zoek op **actueelalarm P2000**.

Kies daarna:

- een punt op de kaart (standaard je thuislocatie);
- een straal van 1, 2, 5, 10 of 25 km;
- welke diensten je wilt volgen.

Klik op **Verzenden**. Je hebt nu een apparaat **P2000 binnen 5 km** (of de straal die je koos) met de sensor **Laatste melding**.

### Straal, punt of diensten later wijzigen

Ga naar **Instellingen → Apparaten en diensten** en open **actueelalarm P2000**. Klik bij je punt op **Configureren** (het tandwiel) en kies een andere straal, een ander punt of andere diensten. De meldingen starten meteen opnieuw met de nieuwe instellingen.

Wil je meerdere punten volgen, bijvoorbeeld thuis en je werk? Herhaal dan stap 3.

### Zonder HACS

Download het zip-bestand van de [laatste release](https://github.com/phakkers/ha-actueelalarm/releases/latest) en pak het uit. Kopieer de map `custom_components/actueelalarm` naar de map `custom_components` in je Home Assistant-configuratie (de map met `configuration.yaml`; maak `custom_components` aan als die er nog niet is). Herstart daarna en ga verder met stap 3.

## Voorbeeld: melding op je telefoon

```yaml
automation:
  - alias: P2000 in de buurt
    triggers:
      - trigger: event
        event_type: actueelalarm_melding
    actions:
      - action: notify.mobile_app_telefoon
        data:
          title: "{{ trigger.event.data.dienst_naam }} · {{ trigger.event.data.prio_naam }}"
          message: >-
            {{ trigger.event.data.titel }}, {{ trigger.event.data.straat or '' }}
            {{ trigger.event.data.plaats }} ({{ trigger.event.data.km }} km)
          data:
            url: "{{ trigger.event.data.url }}"
            clickAction: "{{ trigger.event.data.url }}"
```

Wil je alleen meldingen met grote spoed? Zet dan in `conditions` de voorwaarde `{{ trigger.event.data.prio is not none and trigger.event.data.prio <= 1 }}`.

## Velden van het event

| Veld | Voorbeeld |
|---|---|
| `id` | `ab12cd34` |
| `t` | `2026-11-10T12:06:08Z` (UTC) |
| `dienst`, `dienst_naam` | `brw`, `Brandweer` (ook `amb`, `mmt` en `knrm`) |
| `prio`, `prio_naam` | `1`, `Grote spoed` (van 0 = zeer grote spoed tot 3) |
| `titel` | `Woningbrand` |
| `plaats`, `straat` | `Hoofddorp`, `Kruisweg` |
| `lat`, `lon`, `km` | `52.3021`, `4.6889`, `0.2` |
| `url` | `https://actueelalarm.nl/melding/ab12cd34/` |

Dit is geen officieel alarmkanaal. Bij nood bel je **112**.

---

## English

Dutch P2000 emergency alerts (fire brigade, ambulance, trauma helicopter, KNRM lifeboats) around a point, from [actueelalarm.nl](https://actueelalarm.nl/), which receives them with its own P2000 receiver.

- **Sensor "Latest alert"**: its attributes are service, priority, place, street, distance, time, link and position (it shows on the map).
- **Event `actueelalarm_melding`** for every new alert, with the fields in the table above.
- **Install:**
  1. [Open this repository in HACS](https://my.home-assistant.io/redirect/hacs_repository/?owner=phakkers&repository=ha-actueelalarm&category=integration) and click **Download**. To do it by hand instead: HACS → ⋮ → *Custom repositories*, then add this repository's URL as type *Integration*.
  2. Restart Home Assistant (Settings → System → power icon).
  3. [Add the integration](https://my.home-assistant.io/redirect/config_flow_start/?domain=actueelalarm). Pick a point (your home by default), a radius from 1 to 25 km and the services. To change them later, click **Configure** on the entry.
- The integration polls the open feed `https://actueelalarm.nl/api/meldingen.json` once a minute. It needs no API key.

The data never includes house numbers or names. This is not an official alerting channel; in an emergency call 112.

## Licentie / License

MIT. Data © [actueelalarm.nl](https://actueelalarm.nl/); please link to it when you show it.
