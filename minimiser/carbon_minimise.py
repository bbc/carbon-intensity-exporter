from api.carbon import CarbonAPI

location_ids = {
    "LONDON": 13,
    "NW_ENGLAND": 3
}


class Minimiser:
    def __init__(self):
        self.api = CarbonAPI()

    async def optimal_location_now(self, locations):
        options = {}
        for location in locations:
            intensity, _ = await self.api.current_region_intensity(location_ids[location])
            options[location] = intensity
        sorted_options = sorted(options, key=options.get)
        return sorted_options[0]

    def optimal_time_for_location(self, location, num_options=1):
        return True

    def optimal_time_and_location(self, locations):
        return True