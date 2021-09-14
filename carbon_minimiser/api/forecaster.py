from carbon_intensity_exporter.carbon_api_wrapper.carbon import CarbonAPI


class Forecaster:
    def __init__(self):
        self.api = CarbonAPI()

    async def info_national_now(self):
        """
        Returns general nationwide information at the current time
        :return: current national intensity and current national mix of fuel types (dict: tuple, dict)
        """
        info = {}
        info['intensity'] = await self.api.current_national_intensity()
        info['mix'] = await self.api.current_national_mix()
        return info

    async def info_regional_now(self,location):
        """
        Returns general information at the current time for given region
        :param location: location string
        :return: current regional intensity and current regional mix of fuel types (dict: tuple, dict)
        """
        info = {}
        info['intensity'] = await self.api.current_region_intensity(location)
        info['mix'] = await self.api.current_region_mix(location)
        return info
        
    async def info_national_future(self,hours):
        """
        Returns nationwide half-hourly information on intensity over the next given number of hours 
        :param hours: float number of hours (must be <=47.5
        :return: list of dicts with national information on intensity
        """
        info = await self.api.national_forecast_range(hours)
        return info
        
    async def info_regional_future(self, location,hours):
        """
        Returns regional half-hourly information on intensity over the next given number of hours 
        :param location: location string
        :param hours: float number of hours (must be <=47.5)
        :return: list of dicts with regional information on intensity
        """
        info = await self.api.region_forecast_range(location,hours)
        return info 
