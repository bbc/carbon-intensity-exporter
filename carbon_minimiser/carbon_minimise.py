from carbon_intensity_exporter.api.carbon import CarbonAPI
from itertools import islice
from typing import List


class Minimiser:
    def __init__(self):
        self.api = CarbonAPI()

    @staticmethod
    def _window(seq: List, n: int):
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

    async def optimal_location_now(self, locations: List[str]):
        """
        Given a list of locations, returns the location with lowest carbon intensity right now
        :param locations: list of locations, see api.carbon.REGIONS
        :return: lowest carbon location (str)
        """
        options = {}
        for location in locations:
            intensity, _ = await self.api.current_region_intensity(location)
            options[location] = intensity
        sorted_options = sorted(options, key=options.get)
        return sorted_options[0]

    async def optimal_time_for_location(self, location: str, num_options: int = 1):
        """
        Given a location, returns the lowest carbon intensity half hour within the next 48 hours
        :param location: location string, see api.carbon.REGIONS
        :param num_options: define the number of top options returned
        :return: number of hours and mins till optimal time as +hh:mm string
        """
        times = await self.api.region_forecast_range(location, 48)
        sorted_times = sorted(times, key=lambda x: x['forecast'])
        optimal_times = [time['time'] for time in sorted_times[0:num_options]]
        return optimal_times[0] if len(optimal_times) == 1 else optimal_times

    async def optimal_time_and_location(self, locations: List[str], num_options: int = 1):
        """
        Given a list of locations, returns the time and location of the lowest carbon
        intensity half hour window over the next 48 hours
        :param locations: list of locations, see api.carbon.REGIONS
        :param num_options: define the number of top options returned
        :return: tuple of (location, time), where time is num hours until optimal start time in hh:mm
        """
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

    async def optimal_time_window_for_location(self, location: str, window_len: float, num_options: int = 1):
        """
        Given a location and time window, returns the start of the time window with lowest
        carbon intensity over the next 48 hours in that location
        :param location: location string, see api.carbon.REGIONS
        :param window_len: integer number of hours that you wish to optimise for
        :param num_options: define the number of top options returned
        :return: number of hours and mins from now as +hh:mm string
        """
        times = await self.api.region_forecast_range(location, 48)
        costs = []
        # convert hours into half hours
        half_hours = int(window_len * 2) if window_len < 48 else 95
        for window in self._window(times, half_hours):
            carbon_cost = sum([f['forecast'] for f in window])
            cost = {'time': window[0]['time'], 'cost': carbon_cost}
            costs.append(cost)
        sorted_times = sorted(costs, key=lambda x: x['cost'])
        optimal_times = [time['time'] for time in sorted_times[0:num_options]]
        return optimal_times[0] if len(optimal_times) == 1 else optimal_times

    async def optimal_time_window_and_location(self, locations: List[str], window_len: float, num_options: int = 1):
        """
        Given a list of locations and a time window, returns the location and start of the time window with lowest
        carbon intensity over the next 48 hours
        :param locations: list of locations, see api.carbon.REGIONS
        :param window_len: number of hours that you wish to optimise for
        :param num_options: define the number of top options returned
        :return: tuple of (location, time), where time is num hours until optimal start time in hh:mm
        """
        costs = []
        for location in locations:
            times = await self.api.region_forecast_range(location, 48)
            # convert hours into half hours
            half_hours = int(window_len * 2) if window_len < 48 else 95
            for window in self._window(times, half_hours):
                carbon_cost = sum([f['forecast'] for f in window])
                cost = {'location': location, 'time': window[0]['time'], 'cost': carbon_cost}
                costs.append(cost)
        sorted_options = sorted(costs, key=lambda x: x['cost'])
        optimal_options = [(opt['location'], opt['time']) for opt in sorted_options[0:num_options]]
        return optimal_options[0] if len(optimal_options) == 1 else optimal_options
