from api.carbon import CarbonAPI


class Minimiser():
    def __init__(self):
        self.api = CarbonAPI()

    def optimal_location_now(self):
        return True

    def optimal_time_for_location(self, location, num_options=1):
        return True

    def optimal_time_and_location(self, locations):
        return True