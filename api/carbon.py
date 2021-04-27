from .api_connection import ApiConnection
from datetime import datetime


class CarbonAPI:
    def __init__(self):
        self.api = ApiConnection("https://api.carbonintensity.org.uk/")

    @staticmethod
    def _get_api_time_format():
        time_now = datetime.utcnow()
        # reformat to yyyy-mm-ddThh:mm:ss+0000 to fit API call
        time_now = str(time_now).replace(" ", 'T')
        return time_now[:-7] + "+0000"

    """
    Returns a tuple of the combined average intensity for England, Scotland, and Wales
    along with a descriptor of intensity from very low -> very high
    """
    async def current_national_intensity(self):
        json = await self.api.get("intensity")
        intensity = json['data'][0]['intensity']
        return intensity['actual'], intensity['index']

    """
    region_id: https://carbon-intensity.github.io/api-definitions/?shell#region-list
    Returns a tuple of the estimated current carbon intensity for the region,
    along with a descriptor of intensity from very low -> very high
    """
    async def current_region_intensity(self, region_id):
        json = await self.api.get(f"regional/regionid/{region_id}")
        intensity = json['data'][0]['data'][0]['intensity']
        return intensity['forecast'], intensity['index']

    """
    Returns a dict of fuel types and percentages, which represent the current national fuel mix
    """
    async def current_national_mix(self):
        json = await self.api.get(f"generation")
        mix_list = json['data']['generationmix']
        return {mix['fuel']: mix['perc'] for mix in mix_list}

    """
    region_id: https://carbon-intensity.github.io/api-definitions/?shell#region-list
    Returns a dict of fuel types and percentages, which represent the current regional fuel mix
    """
    async def current_region_mix(self, region_id):
        json = await self.api.get(f"regional/regionid/{region_id}")
        mix_list = json['data'][0]['data'][0]['generationmix']
        return {mix['fuel']: mix['perc'] for mix in mix_list}

    """
    hours: int or float, should be less than 47.5
    Given a number of hours, returns the predicted national carbon intensity that many hours from now (rounded
    down to the nearest half hour)
    """
    async def national_forecast_single(self, hours):
        json = await self.api.get(f"intensity/{self._get_api_time_format()}/fw48h")
        # endpoint returns half hourly predictions from current half hour rounded
        # so index 2n gives n hours from now. Max time is therefore 47.5 hours
        index = int(hours*2) if hours < 48 else 95
        prediction = json['data'][index]['intensity']
        return prediction['forecast'], prediction['index']

    """
    hours: int or float, should be less than 47.5
    Given a number of hours, returns the predicted national carbon intensity at each half hour between now (rounded down
    to the nearest half hour) and that many hours from now 
    """
    async def national_forecast_range(self, hours):
        json = await self.api.get(f"intensity/{self._get_api_time_format()}/fw48h")
        # endpoint returns half hourly predictions from current half hour rounded
        index = int(hours*2) if hours < 48 else 95
        forecasts = json['data'][0: index]
        predictions = []
        for f in forecasts:
            predictions.append({"time": f['from'],
                                "forecast": f["intensity"]["forecast"],
                                "index": f["intensity"]["index"]})
        return predictions

    """
    region_id: https://carbon-intensity.github.io/api-definitions/?shell#region-list
    hours: int or float, should be less than 47.5
    Given a number of hours, returns the predicted regional carbon intensity that many hours from now (rounded
    down to the nearest half hour)
    """
    async def region_forecast_single(self, region_id, hours):
        json = await self.api.get(f"regional/intensity/{self._get_api_time_format()}/fw48h/regionid/{region_id}")
        index = int(hours*2) if hours < 48 else 95
        prediction = json['data']['data'][index]['intensity']
        return prediction['forecast'], prediction['index']

    """
    region_id: https://carbon-intensity.github.io/api-definitions/?shell#region-list
    hours: int or float, should be less than 47.5
    Given a number of hours, returns the predicted national carbon intensity at each half hour between now (rounded down
    to the nearest half hour) and that many hours from now
    """
    async def region_forecast_range(self, region_id, hours):
        json = await self.api.get(f"regional/intensity/{self._get_api_time_format()}/fw48h/regionid/{region_id}")
        index = int(hours*2) if hours < 48 else 95
        forecasts = json['data']['data'][0: index]
        predictions = []
        for f in forecasts:
            predictions.append({"time": f['from'],
                                "forecast": f["intensity"]["forecast"],
                                "index": f["intensity"]["index"]})
        return predictions
