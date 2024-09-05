import aiohttp

url = 'https://svitlo.oe.if.ua/GAVTurnOff/GavGroupByAccountNumber'
form_data = {
    'accountNumber': '',
    'userSearchChoice': 'pob',
    'address': 'Івано-Франківськ,Національної Гвардії,14Т'
}

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form_data) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to retrieve data. Status code: {response.status}")
                return None
