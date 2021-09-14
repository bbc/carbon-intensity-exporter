from sanic import Sanic
from sanic.response import json
from carbon_minimiser.api.minimiser import Minimiser
from carbon_intensity_exporter.carbon_api_wrapper.carbon import REGIONS
from carbon_minimiser.api.forecaster import Forecaster

app = Sanic("Carbon Minimiser")
min = Minimiser()
forecast = Forecaster()
locations = ["LONDON", "NW_ENGLAND"]


def get_num_results(request):
    try:
        results = int(request.args['results'][0])
    except KeyError:
        results = 1
    return results


def get_time_range(request):
    try:
        range_param = request.args['range'][0].split(",")
        range = [float(r) for r in range_param]
    except KeyError:
        range = [0,95]
    return range


@app.get('/')
async def root(request):
    return json("Carbon Minimiser")


@app.get('/optimise')
async def optimal_time_and_location(request):
    result = await min.optimal_time_and_location(locations, num_options=get_num_results(request), time_range=get_time_range(request))
    return json(result)


@app.get('/optimise/location')
async def optimal_location(request):
    result = await min.optimal_location_now(locations)
    return json(result)


@app.get('/optimise/location/<location>')
async def optimal_time_for_location(request, location):
    location = location.upper()
    if location in REGIONS.keys():
        result = await min.optimal_time_for_location(location, num_options=get_num_results(request), time_range=get_time_range(request))
        return json(result)
    else:
        return json("Location not found", 404)


@app.get('/optimise/location/<location>/window/<window:number>')
async def optimal_time_window_for_location(request, location, window):
    location = location.upper()
    if location in REGIONS.keys():
        result = await min.optimal_time_window_for_location(location, 
                                                            window, 
                                                            num_options=get_num_results(request),
                                                            time_range=get_time_range(request))
        return json(result)
    else:
        return json("Location not found", 404)


@app.get('/optimise/location/window/<window:number>')
async def optimal_time_window_and_location(request, window):
    result = await min.optimal_time_window_and_location(locations, window, num_options=get_num_results(request), time_range=get_time_range(request))
    return json(result)
    
#Grads 2021 additional routes
@app.get('/information')
async def info_national_now(request):
    result = await forecast.info_national_now()
    return json(result)
    
@app.get('/information/<location>')
async def info_regional_now(request, location):
    location = location.upper()
    if location in REGIONS.keys():
        result = await forecast.info_regional_now(location)
        return json(result)
    else:
        return json("Location not found", 404)
        
@app.get('/forecast/<hours>')
async def forecast_national(request, hours):
    result = await forecast.info_national_future(float(hours))
    return json(result)
    
@app.get('/forecast/<location>/<hours>')
async def forecast_regional(request, location, hours):
    location = location.upper()
    if location in REGIONS.keys():
        result = await forecast.info_regional_future(location, float(hours))
        return json(result)
    else:
        return json("Location not found", 404)
    

