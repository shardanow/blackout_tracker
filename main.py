import asyncio
from bot_module.bot import dp, bot
from bot_module.tasks import periodic_check, periodic_notify
from utils.debug_logger import print_debug_message

# Main entry point
async def main():
    print_debug_message("Bot started")
    
    # Start the periodic task to check and send updates about the schedule
    asyncio.create_task(periodic_check())

    # Start the periodic task to check and send notifications to users
    asyncio.create_task(periodic_notify())

    # Start bot polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
