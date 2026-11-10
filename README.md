# actueelalarm P2000 voor Home Assistant

P2000-meldingen van brandweer, ambulance, traumahelikopter en KNRM rond je huis, in Home Assistant. De meldingen komen van [actueelalarm.nl](https://actueelalarm.nl/), dat ze met een eigen P2000-ontvanger opvangt en binnen seconden online zet.

*English below.*

## Wat je krijgt

- **Sensor "Laatste melding"**: de nieuwste melding binnen je straal. De attributen zijn dienst, prioriteit, plaats, straat, afstand, tijd en een link naar de melding. Met `latitude` en `longitude` staat de sensor op de kaart.
- **Event `actueelalarm_melding`** voor elke nieuwe melding, om automations op te starten.
- De integratie vraagt elke minuut de [open feed](https://actueelalarm.nl/api/meldingen.json?lat=52.37&lon=4.89&km=5) op. Een API-sleutel is niet nodig.

Huisnummers en namen staan nooit in de meldingen. De positie is het midden van de straat, of anders het midden van de plaats.

## Installeren

1. Ga in HACS naar **Integraties**, open het menu en kies **Aangepaste repositories**. Voeg `https://github.com/phakkers/ha-actueelalarm` toe als *Integration*.
2. Installeer **actueelalarm P2000** en herstart Home Assistant.
3. Ga naar **Instellingen → Apparaten en diensten → Integratie toevoegen → actueelalarm P2000**. Kies een punt (standaard je thuislocatie), een straal van 1 tot 25 km en de diensten.

Wil je meerdere punten volgen, bijvoorbeeld thuis en je werk? Voeg de integratie dan nog een keer toe.

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
- Install as a HACS custom repository (*Integration*), then add **actueelalarm P2000** under Devices & services. You pick a point (your home by default), a radius from 1 to 25 km and the services.
- The integration polls the open feed `https://actueelalarm.nl/api/meldingen.json` once a minute. It needs no API key.

The data never includes house numbers or names. This is not an official alerting channel; in an emergency call 112.

## Licentie / License

MIT. Data © [actueelalarm.nl](https://actueelalarm.nl/); please link to it when you show it.
