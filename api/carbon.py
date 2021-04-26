from .api_connection import ApiConnection


class CarbonAPI:
    def __init__(self):
        self.api = ApiConnection("https://api.carbonintensity.org.uk/")

    async def current_national_intensity(self):
        json = await self.api.get("intensity")
        intensity = json['data'][0]['intensity']
        return intensity['actual'], intensity['index']

    """
    https://carbon-intensity.github.io/api-definitions/?shell#region-list
    """
    async def current_region_intensity(self, region_id):
        json = await self.api.get(f"regional/regionid/{region_id}")
        intensity = json['data'][0]['data'][0]['intensity']
        return intensity['forecast'], intensity['index']

    async def current_national_mix(self):
        return False

    async def current_region_mix(self):
        return False

    async def national_forecast(self):
        return False

    async def region_forecast(self):
        return False
