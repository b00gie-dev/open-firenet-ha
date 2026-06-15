from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_CONTROLS, API_SENSORS, API_STATUS, DOMAIN

_LOGGER = logging.getLogger(__name__)


class OpenFirenetCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, host: str, scan_interval: int) -> None:
        self.host = host
        self._base = f"http://{host}"
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        try:
            async with asyncio.timeout(10):
                async with aiohttp.ClientSession() as session:
                    status, sensors, controls = await asyncio.gather(
                        self._get(session, API_STATUS),
                        self._get(session, API_SENSORS),
                        self._get(session, API_CONTROLS),
                    )
            return {"status": status, "sensors": sensors, "controls": controls}
        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout connecting to {self.host}") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with {self.host}: {err}") from err

    async def _get(self, session: aiohttp.ClientSession, path: str) -> dict:
        async with session.get(f"{self._base}{path}") as resp:
            resp.raise_for_status()
            return await resp.json()

    async def async_set_controls(self, **kwargs) -> None:
        controls = self.data["controls"].copy()
        controls.update(kwargs)
        body = (
            f"onOff={controls['onOff']}; "
            f"operatingMode={controls['operatingMode']}; "
            f"heatingPower={controls['heatingPower']}; "
            f"tempRoomTarget={controls['tempRoomTarget']};"
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._base}{API_CONTROLS}",
                data=body,
                headers={"Content-Type": "text/plain"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                resp.raise_for_status()
        # Optimistic update: reflect the change immediately in the UI
        # without waiting for the next poll cycle.
        self.async_set_updated_data({**self.data, "controls": controls})
