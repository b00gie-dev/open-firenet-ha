from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import API_CONTROLS, API_STATE, DOMAIN

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
                    async with session.get(f"{self._base}{API_STATE}") as resp:
                        resp.raise_for_status()
                        return await resp.json()
        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout connecting to {self.host}") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with {self.host}: {err}") from err

    async def async_set_controls(self, **kwargs) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self._base}{API_CONTROLS}",
                json=kwargs,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as resp:
                resp.raise_for_status()
        if self.data and "controls" in self.data:
            current_controls = self.data["controls"].copy()
            current_controls.update(kwargs)
            self.async_set_updated_data({**self.data, "controls": current_controls})
        else:
            await self.async_request_refresh()
