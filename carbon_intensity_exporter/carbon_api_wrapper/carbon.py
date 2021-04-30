from .api_connection import ApiConnection
from datetime import datetime

REGIONS = {
    'N_SCOTLAND': 1, 'S_SCOTLAND': 2, 'NW_ENGLAND': 3, 'NE_ENGLAND': 4, 'YORKSHIRE': 5, 'N_WALES': 6, 'S_WALES': 7,
    'W_MIDLANDS': 8, 'E_MIDLANDS': 9, 'E_ENGLAND': 10, 'SW_ENGLAND': 11, 'S_ENGLAND': 12, 'LONDON': 13,
    'SE_ENGLAND': 14, 'ENGLAND': 15, 'SCOTLAND': 16, 'WALES': 17
}


class CarbonAPI:
    def __init__(self):
        self.api = ApiConnection("https://api.carbonintensity.org.uk/")

    @staticmethod
    def _get_api_time_delta(t1, t2):
        # convert yyyy-mm-ddThh:mmZ to yyyy-mm-dd:hh:mm for comparison
        t1 = datetime.strptime(t1, '%Y-%m-%dT%H:%MZ')
        t2 = datetime.strptime(t2, '%Y-%m-%dT%H:%MZ')
        diff = t2 - t1
        seconds = diff.total_seconds()
        hours = int(seconds // 3600)
        hours = "0" + str(hours) if hours < 10 else str(hours)  # format to hh
        minutes = int((seconds % 3600) // 60)
        minutes = "0" + str(minutes) if minutes < 10 else str(minutes)  # format to mm
        return f"+{hours}:{minutes}"

    """
    Returns 1 if 200 response received from API root, else 0
    """
    async def health_status(self):
        response = await self.api.status()
        return 1 if response == 200 else 0

    """
    Returns a tuple of the combined average intensity for England, Scotland, and Wales
    along with a descriptor of intensity from very low -> very high
    """
    async def current_national_intensity(self):
        json = await self.api.get("intensity")
        intensity = json['data'][0]['intensity']
        return intensity['actual'], intensity['index']

    """
    Returns a tuple of the estimated current carbon intensity for the region,
    along with a descriptor of intensity from very low -> very high
    """
    async def current_region_intensity(self, region):
        json = await self.api.get(f"regional/regionid/{REGIONS[region]}")
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
    Returns a dict of fuel types and percentages, which represent the current regional fuel mix
    """
    async def current_region_mix(self, region):
        json = await self.api.get(f"regional/regionid/{REGIONS[region]}")
        mix_list = json['data'][0]['data'][0]['generationmix']
        return {mix['fuel']: mix['perc'] for mix in mix_list}

    """
    hours: int or float, should be less than 47.5
    Given a number of hours, returns the predicted national carbon intensity that many hours from now (rounded
    down to the nearest half hour)
    """
    async def national_forecast_single(self, hours):
        json = await self.api.get(f"intensity/{datetime.utcnow().isoformat()}/fw48h")
        # endpoint returns half hourly predictions from current half hour rounded
        # so index 2n gives n hours from now. Max time is therefore 47.5 hours
        index = int(hours*2) if hours < 48 else 95
        prediction = json['data'][index]['intensity']
        return prediction['forecast'], prediction['index']

    """
    hours: int or float, max available is 47.5
    Given a number of hours, returns the predicted national carbon intensity at each half hour between now (rounded down
    to the nearest half hour) and that many hours from now 
    """
    async def national_forecast_range(self, hours):
        json = await self.api.get(f"intensity/{datetime.utcnow().isoformat()}/fw48h")
        # endpoint returns half hourly predictions from current half hour rounded
        index = int(hours*2) if hours < 48 else 95
        forecasts = json['data'][0: index + 1]
        predictions = []
        t0 = forecasts.pop(0)['from']
        for f in forecasts:
            time = self._get_api_time_delta(t0, f['from'])
            predictions.append({"time": time,
                                "forecast": f["intensity"]["forecast"],
                                "index": f["intensity"]["index"]})
        return predictions

    """
    hours: int or float, should be less than 47.5
    Given a number of hours, returns the predicted regional carbon intensity that many hours from now (rounded
    down to the nearest half hour)
    """
    async def region_forecast_single(self, region, hours):
        json = await self.api.get(f"regional/intensity/{datetime.utcnow().isoformat()}/fw48h/regionid/{REGIONS[region]}")
        index = int(hours*2) if hours < 48 else 95
        prediction = json['data']['data'][index]['intensity']
        return prediction['forecast'], prediction['index']

    """
    region_id: https://carbon-intensity.github.io/api-definitions/?shell#region-list
    hours: int or float, max available is 47.5
    Given a number of hours, returns the predicted national carbon intensity at each half hour between now (rounded down
    to the nearest half hour) and that many hours from now
    """
    async def region_forecast_range(self, region, hours):
        json = await self.api.get(f"regional/intensity/{datetime.utcnow().isoformat()}/fw48h/regionid/{REGIONS[region]}")
        index = int(hours*2) if hours < 48 else 95
        forecasts = json['data']['data'][0: index + 1]
        predictions = []
        t0 = forecasts.pop(0)['from']
        for f in forecasts:
            time = self._get_api_time_delta(t0, f['from'])
            predictions.append({"time": time,
                                "forecast": f["intensity"]["forecast"],
                                "index": f["intensity"]["index"]})
        return predictions