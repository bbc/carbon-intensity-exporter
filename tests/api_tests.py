from asynctest import TestCase
from api.carbon import CarbonAPI


class TestCarbonAPI(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.carbon = CarbonAPI()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    async def test_current_national_intensity(self):
        result = await self.carbon.current_national_intensity()
        self.assertTrue(result)

    async def test_current_postcode_intensity(self):
        result = await self.carbon.current_postcode_intensity()
        self.assertTrue(result)

    async def test_current_national_mix(self):
        result = await self.carbon.current_national_mix()
        self.assertTrue(result)

    async def test_current_postcode_mix(self):
        result = await self.carbon.current_postcode_mix()
        self.assertTrue(result)

    async def test_national_forecast(self):
        result = await self.carbon.national_forecast()
        self.assertTrue(result)

    async def test_postcode_forecast(self):
        result = await self.carbon.postcode_forecast()
        self.assertTrue(result)
