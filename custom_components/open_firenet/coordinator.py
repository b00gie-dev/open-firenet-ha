from __future__ import annotations

import asyncio
import logging
from datetime import timedelta

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import OpenFirenetClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class OpenFirenetCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, host: str, scan_interval: int) -> None:
        self.host = host
        self._client = OpenFirenetClient(host)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    async def _async_update_data(self) -> dict:
        try:
            async with asyncio.timeout(10):
                return await self._client.fetch_state()
        except asyncio.TimeoutError as err:
            raise UpdateFailed(f"Timeout connecting to {self.host}") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with {self.host}: {err}") from err

    async def async_set_controls(self, **kwargs) -> None:
        await self._client.set_controls(kwargs)
        if self.data and "controls" in self.data:
            current_controls = self.data["controls"].copy()
            current_controls.update(kwargs)
            self.async_set_updated_data({**self.data, "controls": current_controls})
        else:
            await self.async_request_refresh()
