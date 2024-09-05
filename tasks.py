import asyncio
from config import config
from scheduler import check_and_send_update

MINUTES = config['MINUTES_TO_WAIT']

async def periodic_check():
    while True:
        await check_and_send_update()
        await asyncio.sleep(MINUTES * 60)