import aiohttp
from config import API_URL, API_KEY

async def get_services():
    if not API_URL or not API_KEY:
        return []

    data = {
        "key": API_KEY,
        "action": "services"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data=data) as response:
            return await response.json()


async def create_order(service, link, quantity):
    if not API_URL or not API_KEY:
        return {"error": "API sozlanmagan"}

    data = {
        "key": API_KEY,
        "action": "add",
        "service": service,
        "link": link,
        "quantity": quantity
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data=data) as response:
            return await response.json()


async def order_status(order_id):
    if not API_URL or not API_KEY:
        return {"error": "API sozlanmagan"}

    data = {
        "key": API_KEY,
        "action": "status",
        "order": order_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, data=data) as response:
            return await response.json()
