from .api_connection import ApiConnection


class CarbonAPI:
    def __init__(self):
        self.api = ApiConnection("https://api.carbonintensity.org.uk/")

    async def current_national_intensity(self):
        json = await self.api.get("intensity")
        intensity = json['data'][0]['intensity']
        return intensity['actual'], intensity['index']

    async def current_postcode_intensity(self):
        return False

    async def current_national_mix(self):
        return False

    async def current_postcode_mix(self):
        return False

    async def national_forecast(self):
        return False

    async def postcode_forecast(self):
        return False
