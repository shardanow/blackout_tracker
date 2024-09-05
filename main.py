import asyncio
from bot import dp, bot
from tasks import periodic_check

# Main entry point
async def main():
    print("Bot started")
    
    # Start the periodic task
    asyncio.create_task(periodic_check())

    # Start bot polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
