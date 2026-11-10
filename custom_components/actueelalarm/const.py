"""Constants for the actueelalarm P2000 integration."""

from datetime import timedelta

DOMAIN = "actueelalarm"
API = "https://actueelalarm.nl/api/meldingen.json"
SCAN_INTERVAL = timedelta(seconds=60)
EVENT = "actueelalarm_melding"
ATTRIBUTION = "Data: actueelalarm.nl"

CONF_RADIUS = "radius"
CONF_DIENSTEN = "diensten"
RADII = ["1", "2", "5", "10", "25"]
DIENSTEN = ["brw", "amb", "mmt", "knrm"]
