from api.carbon import CarbonAPI


class Minimiser:
    def __init__(self):
        self.api = CarbonAPI()

    async def optimal_location_now(self, locations):
        options = {}
        for location in locations:
            intensity, _ = await self.api.current_region_intensity(location)
            options[location] = intensity
        sorted_options = sorted(options, key=options.get)
        return sorted_options[0]

    async def optimal_time_for_location(self, location, num_options=1):
        times = await self.api.region_forecast_range(location, 48)
        sorted_times = sorted(times, key=lambda x: x['forecast'])
        optimal_times = [time['time'] for time in sorted_times[0:num_options]]
        return optimal_times

    async def optimal_time_and_location(self, locations, num_options=1):
        options = []
        for location in locations:
            times = await self.api.region_forecast_range(location, 48)
            for time in times:
                # results don't come back with location attached
                time['location'] = location
            options = options + times
        sorted_options = sorted(options, key=lambda x: x['forecast'])
        optimal_options = [(opt['location'], opt['time']) for opt in sorted_options[0:num_options]]
        return optimal_options
