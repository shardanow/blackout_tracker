from datetime import datetime
from schedule import load_schedule_from_file, save_schedule_to_file, build_schedule_message, build_no_schedule_message
from bot import broadcast_message
from api import fetch_data
from config import config

SCHEDULES_FOLDER = config['SCHEDULES_FOLDER']

# Fetch and parse schedule data from the API
async def get_schedule_data():
    json_response = await fetch_data()
    if not json_response:
        print("Failed to fetch data from the API.")
        return None, None, None, None

    today_data = json_response.get('graphs', {}).get('today', {})
    tomorrow_data = json_response.get('graphs', {}).get('tomorrow', {})

    today_hours_list = today_data.get('hoursList', [])
    tomorrow_hours_list = tomorrow_data.get('hoursList', [])

    return today_hours_list, tomorrow_hours_list, today_data, tomorrow_data

# Process schedule data, check for changes, and decide if an update is needed
def process_schedule_data(day_label, hours_list, previous_data, file_name, event_date):
    if not hours_list:
        return build_no_schedule_message(day_label), False

    # Check if previous data exists
    if previous_data is None:
        # First time sending schedule for the day
        message = build_schedule_message(hours_list, day_label, event_date)
        save_schedule_to_file(file_name, hours_list)
        return message, True

    # If there is a change in the schedule, append "обновленный"
    if hours_list != previous_data:
        updated_day_label = f"{day_label} обновленный"
        message = build_schedule_message(hours_list, updated_day_label, event_date)
        save_schedule_to_file(file_name, hours_list)
        return message, True

    # No changes detected
    return None, False

# Send the schedule updates to Telegram if changes are found
async def send_schedule_updates(day_label, hours_list, previous_data, file_name, event_date):
    message, should_send = process_schedule_data(day_label, hours_list, previous_data, file_name, event_date)
    if should_send and message:
        await broadcast_message(message)
        print(f"{day_label} schedule sent to Telegram.")
    elif message is None:
        print(f"No changes in {day_label.lower()} schedule.")
    else:
        print(f"{day_label} schedule not available.")

# Main function that checks and sends updates for today and tomorrow
async def check_and_send_update():
    today_date_str = datetime.now().strftime("%Y-%m-%d")

    today_hours_list, tomorrow_hours_list, today_data, tomorrow_data = await get_schedule_data()
    if today_hours_list is None and tomorrow_hours_list is None:
        return  # Skip processing if no data

    today_file = f"{SCHEDULES_FOLDER}/today_schedule_{today_date_str}.json"
    tomorrow_file = f"{SCHEDULES_FOLDER}/tomorrow_schedule_{today_date_str}.json"

    # Load previously saved schedules
    previous_today_data = load_schedule_from_file(today_file)
    previous_tomorrow_data = load_schedule_from_file(tomorrow_file)

    # Check and send updates for today's schedule
    await send_schedule_updates("Сегодняшний", today_hours_list, previous_today_data, today_file, today_data.get('eventDate'))

    # Check and send updates for tomorrow's schedule
    await send_schedule_updates("Завтрашний", tomorrow_hours_list, previous_tomorrow_data, tomorrow_file, tomorrow_data.get('eventDate'))
