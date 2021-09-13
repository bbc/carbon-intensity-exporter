from asynctest import TestCase, mock
from carbon_minimiser.api.minimiser import Minimiser
from carbon_intensity_exporter.carbon_api_wrapper.carbon import CarbonAPI


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
        data = [{'forecast': 231, 'index': 'moderate', 'time': '2021-04-27T08:30Z'},
                {'forecast': 223, 'index': 'moderate', 'time': '2021-04-27T09:00Z'},
                {'forecast': 218, 'index': 'moderate', 'time': '2021-04-27T09:30Z'}]
        with mock.patch.object(CarbonAPI, "region_forecast_range", return_value=data):
            result = await self.min.optimal_time_for_location("")
            self.assertEqual(result, "2021-04-27T09:30Z")

    async def test_optimal_time_and_location(self):
        data = [[{'forecast': 231, 'index': 'moderate', 'time': '2021-04-27T08:30Z'},
                {'forecast': 23, 'index': 'moderate', 'time': '2021-04-27T09:00Z'}],
                [{'forecast': 261, 'index': 'moderate', 'time': '2021-04-27T08:30Z'},
                 {'forecast': 234, 'index': 'moderate', 'time': '2021-04-27T09:00Z'}],
                [{'forecast': 251, 'index': 'moderate', 'time': '2021-04-27T08:30Z'},
                 {'forecast': 253, 'index': 'moderate', 'time': '2021-04-27T09:00Z'}]]
        with mock.patch.object(CarbonAPI, "region_forecast_range", side_effect=data):
            result = await self.min.optimal_time_and_location(["a", "b", "c"])
            self.assertEqual(result, ("a", "2021-04-27T09:00Z"))

    async def test_optimal_time_window_for_location(self):
        data = [{'forecast': 100, 'index': 'moderate', 'time': '2021-04-27T08:30Z'},
                {'forecast': 200, 'index': 'moderate', 'time': '2021-04-27T09:00Z'},
                {'forecast': 50, 'index': 'moderate', 'time': '2021-04-27T09:30Z'},
                {'forecast': 300, 'index': 'low', 'time': '2021-04-27T10:00Z'},
                {'forecast': 200, 'index': 'moderate', 'time': '2021-04-27T10:30Z'},
                {'forecast': 150, 'index': 'moderate', 'time': '2021-04-27T11:00Z'}]
        with mock.patch.object(CarbonAPI, "region_forecast_range", return_value=data):
            result = await self.min.optimal_time_window_for_location("", 0.5)
            self.assertEqual(result, "2021-04-27T09:30Z")
            result = await self.min.optimal_time_window_for_location("", 1)
            self.assertEqual(result, "2021-04-27T09:00Z")
            result = await self.min.optimal_time_window_for_location("", 1.5)
            self.assertEqual(result, "2021-04-27T08:30Z")
            result = await self.min.optimal_time_window_for_location("", 2)
            self.assertEqual(result, "2021-04-27T08:30Z")
            result = await self.min.optimal_time_window_for_location("", 2.5)
            self.assertEqual(result, "2021-04-27T08:30Z")

    async def test_optimal_time_window_and_location(self):
        data = [[{'forecast': 201, 'index': 'moderate', 'time': '2021-04-27T08:30Z'},
                 {'forecast': 10, 'index': 'moderate', 'time': '2021-04-27T09:00Z'},
                 {'forecast': 200, 'index': 'moderate', 'time': '2021-04-27T09:30Z'}],
                [{'forecast': 200, 'index': 'moderate', 'time': '2021-04-27T08:30Z'},
                 {'forecast': 20, 'index': 'moderate', 'time': '2021-04-27T09:00Z'},
                 {'forecast': 100, 'index': 'moderate', 'time': '2021-04-27T09:30Z'}],
                [{'forecast': 200, 'index': 'moderate', 'time': '2021-04-27T08:30Z'},
                 {'forecast': 250, 'index': 'moderate', 'time': '2021-04-27T09:00Z'},
                 {'forecast': 200, 'index': 'moderate', 'time': '2021-04-27T09:30Z'}]]
        with mock.patch.object(CarbonAPI, "region_forecast_range", side_effect=data):
            result = await self.min.optimal_time_window_and_location(["a", "b", "c"], 0.5)
            self.assertEqual(result, ("a", "2021-04-27T09:00Z"))
        with mock.patch.object(CarbonAPI, "region_forecast_range", side_effect=data):
            result = await self.min.optimal_time_window_and_location(["a", "b", "c"], 1)
            self.assertEqual(result, ("b", "2021-04-27T09:00Z"))
        with mock.patch.object(CarbonAPI, "region_forecast_range", side_effect=data):
            result = await self.min.optimal_time_window_and_location(["a", "b", "c"], 1.5)
            self.assertEqual(result, ("b", "2021-04-27T08:30Z"))
