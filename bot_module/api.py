import aiohttp
from utils.debug_logger import print_debug_message
from config.config import config

url = 'https://svitlo.oe.if.ua/GAVTurnOff/GavGroupByAccountNumber'
form_data = {
    'accountNumber': '',
    'userSearchChoice': 'pob',
    'address': {config['USER_ADRESS']}
}

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form_data) as response:
            if response.status == 200:
                return await response.json()
            else:
                print_debug_message(f"Failed to retrieve data. Status code: {response.status}")
                return None
