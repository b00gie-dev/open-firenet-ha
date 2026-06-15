# Open Firenet — Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)

Home Assistant integration for Rika pellet stoves controlled via the [open-firenet](https://github.com/openfirenet/open-firenet) WiFi bridge.

## Requirements

- An ESP32 flashed with the [open-firenet firmware](https://github.com/openfirenet/open-firenet), connected to your Rika stove and your WiFi network.
- Home Assistant 2024.1 or later.
- HACS (recommended) or manual installation.

## Installation

### Via HACS (recommended)

1. In HACS, go to **Integrations** → ⋮ → **Custom repositories**.
2. Add `https://github.com/openfirenet/open-firenet-ha` with category **Integration**.
3. Search for **Open Firenet** and install it.
4. Restart Home Assistant.

### Manual

Copy the `custom_components/open_firenet/` folder into your HA `config/custom_components/` directory and restart.

## Configuration

1. Go to **Settings** → **Devices & Services** → **Add Integration**.
2. Search for **Open Firenet**.
3. Enter the IP address of your open-firenet bridge and the desired poll interval (default: 30 s).

## Entities

| Entity | Type | Description |
|---|---|---|
| `climate.open_firenet` | Climate | Main thermostat — on/off, target temp, preset, fan speed |
| `binary_sensor.open_firenet_connected` | Binary sensor | Bridge ↔ stove link active |
| `sensor.open_firenet_*` | Sensor | All values reported by the stove |

### Climate presets

| Preset | Stove mode |
|---|---|
| `manual` | Manual (0) |
| `auto` | Auto / thermostat (1) |
| `comfort` | Comfort (2) |

### Fan modes

Maps to `heatingPower` (30 % – 100 %, steps of 10 %).

## License

MIT
