from datetime import datetime
from bot_module.schedule import load_schedule_from_file, save_schedule_to_file, build_schedule_message, build_no_schedule_message, build_notify_users_message
from bot_module.bot import broadcast_message
from bot_module.api import fetch_data
from config.config import config
from utils.debug_logger import print_debug_message

SCHEDULES_FOLDER = config['SCHEDULES_FOLDER']

# Fetch and parse schedule data from the API
async def get_schedule_data():
    json_response = await fetch_data()
    if not json_response:
        print_debug_message("Failed to fetch data from the API.")
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
        print_debug_message(f"{day_label} schedule sent to Telegram.")
    elif message is None:
        print_debug_message(f"No changes in {day_label.lower()} schedule.")
    else:
        print_debug_message(f"{day_label} schedule not available.")

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

# Notify users about upcoming power outages
async def notify_users():
    minutes_label = config['MINUTES_BEFORE_TO_NOTIFY_USER_BLACKOUT']

    # Load today's schedule
    today_date_str = datetime.now().strftime("%Y-%m-%d")
    today_file = f"{SCHEDULES_FOLDER}/today_schedule_{today_date_str}.json"
    today_hours_list = load_schedule_from_file(today_file)

    # Skip processing if no data
    if today_hours_list is None:
        print_debug_message("No schedule data available to notify users.")
        return
    
    # Check if there are any power outages in the next {minutes_label}
    current_hour = datetime.now().hour
    current_minute = datetime.now().minute
    current_index = current_hour * 60 + current_minute

    # Find the power outages for today
    blackout_hours = [hour for hour in today_hours_list if hour.get('electricity') == 1]
    blackout_times = [hour['description'] for hour in blackout_hours]
    # Convert the time to an index
    blackout_indices = [int(time.split('-')[0].split(':')[0]) * 60 + int(time.split('-')[0].split(':')[1]) for time in blackout_times]

    # Find the next power outage
    next_blackout_index = None
    for index in blackout_indices:
        if index > current_index:
            next_blackout_index = index
            break

    # No upcoming power outages
    if next_blackout_index is None:
        print_debug_message("No upcoming power outages to notify users.")
        return
    
    # Check if the next power outage is within the {minutes_label} range
    if next_blackout_index - current_index > minutes_label:
        print_debug_message("No upcoming power outages within the notification range.")
        return

    # Send notification to users
    message = build_notify_users_message(minutes_label)
    await broadcast_message(message)
    print_debug_message("Notification about soon power outage was sent to users.")