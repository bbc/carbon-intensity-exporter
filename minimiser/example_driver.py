from carbon_minimise import Minimiser
import asyncio


async def main():
    m = Minimiser()
    locations = ["LONDON", "NW_ENGLAND"]
    best_location = m.optimal_location_now(locations)
    best_london_time = m.optimal_time_for_location("LONDON")
    best_manchester_time = m.optimal_time_for_location("NW_ENGLAND")
    best_time_and_location = m.optimal_time_and_location(locations)
    result = await asyncio.gather(best_location, best_london_time, best_manchester_time, best_time_and_location)
    print(f"Best Location: {result[0]} \n"
          f"Best Time to Run in London: {result[1][0]} hours from now\n"
          f"Best Time to Run in Manchester: {result[2][0]} hours from now\n"
          f"Best Time and Location: {result[3][0][1]} hours from now in {result[3][0][0]}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
