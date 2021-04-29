from asynctest import TestCase, mock
from minimiser.carbon_minimise import Minimiser
from api.carbon import CarbonAPI


class TestCarbonMinimiser(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.min = Minimiser()

    async def test_optimal_location_now(self):
        data = [(231, 'moderate'), (131, 'moderate'), (331, 'moderate')]
        with mock.patch.object(CarbonAPI, "current_region_intensity", side_effect=data):
            result = await self.min.optimal_location_now(["a", "b", "c"])
            self.assertEqual(result, "b")

    async def test_optimal_time_for_location(self):
        data = [{'forecast': 231, 'index': 'moderate', 'time': '+00:30'},
                {'forecast': 223, 'index': 'moderate', 'time': '+01:00'},
                {'forecast': 218, 'index': 'moderate', 'time': '+01:30'}]
        with mock.patch.object(CarbonAPI, "region_forecast_range", return_value=data):
            result = await self.min.optimal_time_for_location("")
            self.assertEqual(result, "+01:30")

    async def test_optimal_time_and_location(self):
        pass

    async def test_optimal_time_window_for_location(self):
        data = [{'forecast': 231, 'index': 'moderate', 'time': '+00:30'},
                {'forecast': 223, 'index': 'moderate', 'time': '+01:00'},
                {'forecast': 218, 'index': 'moderate', 'time': '+01:30'},
                {'forecast': 100, 'index': 'low', 'time': '+02:00'},
                {'forecast': 200, 'index': 'moderate', 'time': '+02:30'},
                {'forecast': 218, 'index': 'moderate', 'time': '+03:00'}
                ]
        with mock.patch.object(CarbonAPI, "region_forecast_range", return_value=data):
            result = await self.min.optimal_time_window_for_location("", 2)
            self.assertEqual(result, "+02:00")

    async def test_optimal_time_window_and_location(self):
        pass
