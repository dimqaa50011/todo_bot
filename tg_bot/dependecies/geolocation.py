import asyncio
from concurrent.futures import ProcessPoolExecutor

from geopy.adapters import AioHTTPAdapter
from geopy.geocoders import Nominatim
from geopy.location import Location
from timezonefinder import TimezoneFinder


class Geolocator:
    @classmethod
    async def get_timezone(cls, city_name: str):
        latitude, longitude = await cls._get_latitude_and_longitude(city_name)
        time_zone = await cls._process_timezone(latitude, longitude)

        return time_zone

    @classmethod
    async def _get_latitude_and_longitude(cls, city_name: str):
        async with Nominatim(user_agent="todo_bot", adapter_factory=AioHTTPAdapter) as geolocator:
            location: Location = await geolocator.geocode(city_name)

        return (location.latitude, location.longitude)

    @classmethod
    async def _process_timezone(cls, latitude: float, longitude: float):
        return await cls._run_blocked_function(cls._get_timezone_sync, latitude, longitude)

    @classmethod
    async def _run_blocked_function(cls, func, *args):
        loop = asyncio.get_running_loop()

        with ProcessPoolExecutor() as pool:
            return await loop.run_in_executor(pool, func, *args)

    @classmethod
    def _get_timezone_sync(cls, latitude: float, longitude: float):
        tz = TimezoneFinder()
        return tz.timezone_at_land(lat=latitude, lng=longitude)
