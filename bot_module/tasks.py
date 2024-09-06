import asyncio
from config.config import config
from bot_module.scheduler import check_and_send_update, notify_users

MINUTES_SCHEDULE_UPDATE = config['MINUTES_TO_CHECK_SCHEDULE_UPDATE']
MINUTES_TO_CHECK_SCHEDULE = config['MINUTES_TO_CHECK_SCHEDULE']

# Periodic task to check and send updates about the schedule
async def periodic_check():
    while True:
        await check_and_send_update()
        await asyncio.sleep(MINUTES_SCHEDULE_UPDATE * 60)

# Periodic task to check and send notifications to users
async def periodic_notify():
    while True:
        await notify_users()
        await asyncio.sleep(MINUTES_TO_CHECK_SCHEDULE * 60)