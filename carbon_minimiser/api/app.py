from sanic import Sanic
from sanic.response import json
from carbon_minimiser.api.minimiser import Minimiser
from carbon_intensity_exporter.carbon_api_wrapper.carbon import REGIONS

app = Sanic("Carbon Minimiser")
min = Minimiser()
locations = ["LONDON", "NW_ENGLAND"]


def get_num_results(request):
    try:
        results = int(request.args['results'][0])
    except KeyError:
        results = 1
    return results


@app.get('/')
async def root(request):
    return json("Carbon Minimiser")


@app.get('/optimise')
async def optimal_time_and_location(request):
    result = await min.optimal_time_and_location(locations, num_options=get_num_results(request))
    return json(result)


@app.get('/optimise/location')
async def optimal_location(request):
    result = await min.optimal_location_now(locations)
    return json(result)


@app.get('/optimise/location/<location>')
async def optimal_time_for_location(request, location):
    location = location.upper()
    if location in REGIONS.keys():
        result = await min.optimal_time_for_location(location, num_options=get_num_results(request))
        return json(result)
    else:
        return json("Location not found", 404)


@app.get('/optimise/location/<location>/window/<window:int>')
async def optimal_time_window_for_location(request, location, window):
    location = location.upper()
    if location in REGIONS.keys():
        result = await min.optimal_time_window_for_location(location, window, num_options=get_num_results(request))
        return json(result)
    else:
        return json("Location not found", 404)


@app.get('/optimise/location/window/<window:int>')
async def optimal_time_window_and_location(request, window):
    result = await min.optimal_time_window_and_location(locations, window, num_options=get_num_results(request))
    return json(result)
