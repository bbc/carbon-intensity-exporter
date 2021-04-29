from api.carbon import CarbonAPI
from itertools import islice


class Minimiser:
    def __init__(self):
        self.api = CarbonAPI()

    def window(self, seq, n):
        """
        :return: Returns a sliding window (of width n) over data from the iterable
        s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
        from: https://stackoverflow.com/questions/6822725/rolling-or-sliding-window-iterator
        """
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

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
        return optimal_times[0] if len(optimal_times) == 1 else optimal_times

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
        return optimal_options[0] if len(optimal_options) == 1 else optimal_options

    async def optimal_time_window_for_location(self, location, window_len, num_options=1):
        times = await self.api.region_forecast_range(location, 48)
        costs = []
        for window in self.window(times, window_len):
            carbon_cost = sum([f['forecast'] for f in window])
            cost = {'time': window[0]['time'], 'cost': carbon_cost}
            costs.append(cost)
        sorted_times = sorted(costs, key=lambda x: x['cost'])
        optimal_times = [time['time'] for time in sorted_times[0:num_options]]
        return optimal_times[0] if len(optimal_times) == 1 else optimal_times
