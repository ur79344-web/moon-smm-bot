import aiohttp

API_URL = "https://nitrosms.uz/api/v2"
API_KEY = "143d4d1c23378d10ac70e7c458cc5346"


async def get_services():
    data = {
        "key": API_KEY,
        "action": "services"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data=data) as response:
            result = await response.json()

    return result