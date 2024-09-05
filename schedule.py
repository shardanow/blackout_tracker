import json
import os
from datetime import datetime
from config import config

# Ensure the schedules folder exists
if not os.path.exists(config['SCHEDULES_FOLDER']):
    os.makedirs(config['SCHEDULES_FOLDER'])

# Manual mapping of Russian days of the week and months
days_of_week = {
    'Monday': 'понедельник',
    'Tuesday': 'вторник',
    'Wednesday': 'среда',
    'Thursday': 'четверг',
    'Friday': 'пятница',
    'Saturday': 'суббота',
    'Sunday': 'воскресенье'
}

months = {
    'January': 'января',
    'February': 'февраля',
    'March': 'марта',
    'April': 'апреля',
    'May': 'мая',
    'June': 'июня',
    'July': 'июля',
    'August': 'августа',
    'September': 'сентября',
    'October': 'октября',
    'November': 'ноября',
    'December': 'декабря'
}

def generate_file_name(day_label, date_str):
    return os.path.join(config['SCHEDULES_FOLDER'], f"{day_label}_schedule_{date_str}.json")

def save_schedule_to_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_schedule_from_file(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def format_event_date(event_date_str):
    event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
    weekday = event_date.strftime("%A")
    day = event_date.strftime("%d").lstrip("0")
    month = event_date.strftime("%B")
    russian_weekday = days_of_week.get(weekday).capitalize()
    russian_month = months.get(month).capitalize()
    return f"{russian_weekday}, {day} {russian_month}"

def build_schedule_message(hours_list, day_label, event_date_str):
    grouped_hours = group_consecutive_hours(hours_list)
    formatted_date = format_event_date(event_date_str)
    message = f"🗒️ <b>{day_label} график отключений.\n📆 {formatted_date}.</b>\n\n"
    total_outage_duration = 0
    for group in grouped_hours:
        message += f"📍 <i>С <b>{group['start_time']}</b> до <b>{group['end_time']}</b></i> — без электричества на {group['total_hours']} час(ов).\n"
        total_outage_duration += group['total_hours']
    if total_outage_duration > 0:
        message += f"\n📊 <b>Итого без электричества: {total_outage_duration} час(ов)</b>\n"
    else:
        message += "⚡️ <b>Электричество будет доступно весь день!</b>\n"
    return message

def build_no_schedule_message(day_label):
    return f"⚡️ <b>На {day_label} день отключений не запланировано.</b>"

# Helper function to group consecutive hours
def group_consecutive_hours(hours_list):
    grouped_hours = []
    start_time = None
    end_time = None
    total_hours = 0

    for hour in hours_list:
        if hour.get('electricity') == 1:
            if start_time is None:
                # Start a new group
                start_time = hour['description'].split('-')[0]
            # Always update the end time
            end_time = hour['description'].split('-')[1]
            total_hours += 1
        else:
            # If we have an active group and the current hour is 0, close the group
            if start_time and end_time:
                grouped_hours.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'total_hours': total_hours
                })
            # Reset the group
            start_time = None
            end_time = None
            total_hours = 0

    # If the last hours were consecutive, close the group
    if start_time and end_time:
        grouped_hours.append({
            'start_time': start_time,
            'end_time': end_time,
            'total_hours': total_hours
        })

    return grouped_hours