from __future__ import annotations

DOMAIN = "open_firenet"

DEFAULT_SCAN_INTERVAL = 30  # seconds

API_STATE = "/api/state"
API_CONTROLS = "/api/controls"

OPERATING_MODES = {
    0: "manual",
    1: "auto",
    2: "comfort",
}
OPERATING_MODES_REVERSE = {v: k for k, v in OPERATING_MODES.items()}

TEMP_MIN = 14.0
TEMP_MAX = 28.0
TEMP_STEP = 1.0

HEATING_POWER_MIN = 30
HEATING_POWER_MAX = 100
HEATING_POWER_STEP = 5
