DOMAIN = "open_firenet"

DEFAULT_SCAN_INTERVAL = 30  # seconds

API_STATUS   = "/api/status"
API_SENSORS  = "/api/sensors"
API_CONTROLS = "/api/controls"

OPERATING_MODES = {
    0: "manual",
    1: "auto",
    2: "comfort",
}
OPERATING_MODES_REVERSE = {v: k for k, v in OPERATING_MODES.items()}

# Candidate sensor keys for current room temperature (×10 encoding, e.g. 195 = 19.5°C).
# The correct key depends on what the stove sends in POST_SENSORS.
ROOM_TEMP_KEYS = ["f0", "tRoom", "temperatureRoom", "room_temp", "T_room"]

TEMP_MIN = 14.0
TEMP_MAX = 28.0
TEMP_STEP = 1.0

HEATING_POWER_MIN = 30
HEATING_POWER_MAX = 100
